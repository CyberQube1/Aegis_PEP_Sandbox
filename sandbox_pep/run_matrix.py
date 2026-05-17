from __future__ import annotations

import argparse
import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from harness.adapters.model_adapter import (
    ModelBackendGenerationError,
    ModelGeneration,
    ModelGenerationTimeoutError,
    ModelRunConfig,
)
from harness.conditions.plain_mesh import PlainMeshCondition
from harness.conditions.prompt_policy_mesh import PromptPolicyMeshCondition
from harness.evidence.record import validate_record
from harness.evidence.run_manifest import build_run_manifest
from harness.mock_tools.state import MockState
from harness.utils.git_utils import current_git_commit
from harness.utils.hash_utils import stable_hash

from .aegis_client import IslandAegisClient
from .config import SANDBOX_ROOT, SandboxPepConfig, canonical_agent_id_for_model, load_config
from .evidence_writer import write_outputs
from .mock_pep import MockPEP
from .models import build_model, paper_agent_profile
from .scoring import score_island_run
from .task_loader import load_tasks, select_tasks
from .tool_catalog import LOCAL_TOOL_TO_CANONICAL, enrich_proposed_action, local_mock_tool_name, prompt_tool_specs


CONDITIONS = ("plain_mesh_agent", "prompt_policy_mesh_agent", "aegis_governed_mesh_agent")


def execute(
    *,
    config: SandboxPepConfig,
    conditions: list[str],
    model_name: str,
    task_ids: list[str] | None,
    max_tasks: int | None,
    output_dir: Path,
    allow_real_model_calls: bool = False,
    continue_on_task_failure: bool = True,
    model_run_config: ModelRunConfig | None = None,
    stop_on_model_timeout: bool = False,
) -> dict[str, Any]:
    if model_name != "stub_model" and not allow_real_model_calls:
        raise ValueError("real model calls are disabled for the isolated sandbox PEP")
    all_tasks = load_tasks()
    tasks = select_tasks(all_tasks, task_ids, max_tasks)
    run_id = f"island::{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}::{uuid.uuid4().hex[:8]}"
    rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    stop_requested = False
    for condition in conditions:
        for task in tasks:
            if stop_requested:
                break
            try:
                row = _run_one(
                    config=config,
                    condition=condition,
                    model_name=model_name,
                    task=task,
                    run_id=run_id,
                    allow_real_model_calls=allow_real_model_calls,
                    model_run_config=model_run_config or ModelRunConfig(allow_real_model_calls=allow_real_model_calls),
                )
                rows.append(row)
                if stop_on_model_timeout and row.get("parser_status") == "model_timeout":
                    stop_requested = True
            except Exception as exc:
                errors.append({"condition": condition, "task_id": task.get("task_id"), "error": str(exc)})
                if not continue_on_task_failure:
                    raise
        if stop_requested:
            break

    manifest = build_run_manifest(
        condition="island_matrix",
        model_backend=model_name,
        paper_safe_model_label=model_name,
        agent_id=canonical_agent_id_for_model(config, model_name),
        task_source="source_mapped_paper_task_corpus",
        output_path=str(output_dir),
        run_count=len(rows),
        org_id=config.org_id,
        baseline_release_id=config.baseline_release_id,
        baseline_fingerprint=config.baseline_fingerprint,
        policy_bundle_id=config.policy_bundle_id,
        workflow_families=sorted({str(task.get("workflow_family") or "") for task in tasks if task.get("workflow_family")}),
        allow_real_model_calls=allow_real_model_calls,
        selected_task_ids=[str(task.get("task_id")) for task in tasks],
        extra={
            "tenant_id": config.tenant_id,
            "conditions": conditions,
            "mesh_route_label": config.route_label,
            "trust_config_label": config.trust_config_label,
            "mesh_ingress_url": config.mesh_ingress_url,
            "policy_mutation": False,
            "real_side_effects": False,
            "praxis_backend_in_decision_lane": False,
            "config_hash": stable_hash(config.public_fingerprint_payload()),
            "run_errors": errors,
            "stopped_on_model_timeout": stop_requested,
        },
    )
    outputs = write_outputs(rows, output_dir, manifest)
    if any(item.get("condition") == "aegis_governed_mesh_agent" for item in errors):
        _write_governed_gap_report(output_dir, errors, config)
    if errors:
        (output_dir / "run_errors.json").write_text(json.dumps(errors, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"output_dir": str(output_dir), "row_count": len(rows), "run_errors": errors, **outputs}


def _run_one(
    *,
    config: SandboxPepConfig,
    condition: str,
    model_name: str,
    task: dict[str, Any],
    run_id: str,
    allow_real_model_calls: bool,
    model_run_config: ModelRunConfig,
) -> dict[str, Any]:
    started = time.perf_counter()
    agent = paper_agent_profile(
        condition=condition,
        model_name=model_name,
        org_id=config.org_id,
        canonical_agent_id=canonical_agent_id_for_model(config, model_name),
    )
    model = build_model(model_name)
    policy_context = _policy_context(condition)
    context = {
        "agent_profile": agent.to_dict(),
        "policy_context": policy_context,
        "condition_name": condition,
        "available_tool_specs": prompt_tool_specs(agent.allowed_mock_tools),
    }
    try:
        generation = model.generate(
            task=task,
            context=context,
            run_config=model_run_config,
        )
    except ModelGenerationTimeoutError as exc:
        return _model_backend_failure_record(
            config=config,
            condition=condition,
            model=model,
            agent=agent,
            task=task,
            run_id=run_id,
            started=started,
            elapsed_ms=exc.elapsed_ms,
            code="model_generation_timeout",
            parser_status="model_timeout",
            error_classification="model_timeout",
            reason=str(exc),
        )
    except ModelBackendGenerationError as exc:
        return _model_backend_failure_record(
            config=config,
            condition=condition,
            model=model,
            agent=agent,
            task=task,
            run_id=run_id,
            started=started,
            elapsed_ms=exc.elapsed_ms,
            code="model_backend_generation_error",
            parser_status="model_backend_error",
            error_classification="model_backend_error",
            reason=str(exc),
        )
    provenance = _proposal_provenance(model, generation)
    proposed_action = enrich_proposed_action(
        task,
        {
            "action_type": generation.proposed_action_type,
            "tool_name": generation.proposed_tool,
            "tool_input": generation.proposed_tool_input,
            "narrative": generation.raw_text,
            "confidence": generation.confidence,
            "claimed_completion": generation.narrative_completion_claim,
            "claims": generation.claims,
            "rationale": generation.rationale,
            "requested_side_effect": generation.requested_side_effect,
            "model_output": generation.to_dict(),
        },
    )
    state = MockState.from_task(task)
    pep = MockPEP(state, agent.allowed_mock_tools)
    attempted = pep.record_attempt(proposed_action)
    # Real-model proposal errors remain first-class evidence rows. The PEP
    # records the attempted proposal, then refuses to apply any mock effect.
    proposal_failure = _proposal_failure_reason(model, generation, proposed_action, agent.allowed_mock_tools)
    if proposal_failure:
        decision = _proposal_failure_decision(
            config=config,
            task=task,
            agent_id=agent.agent_id,
            proposed_action=proposed_action,
            code=proposal_failure["code"],
            reason=proposal_failure["reason"],
            run_id=run_id,
        )
    else:
        if condition == "plain_mesh_agent":
            decision = PlainMeshCondition().decide(task, agent.to_dict(), proposed_action, policy_context)
        elif condition == "prompt_policy_mesh_agent":
            decision = PromptPolicyMeshCondition().decide(task, agent.to_dict(), proposed_action, policy_context)
        elif condition == "aegis_governed_mesh_agent":
            decision = _governed_decision(
                config=config,
                task=task,
                agent_profile=agent.to_dict(),
                proposed_action=proposed_action,
                run_id=run_id,
                policy_context=policy_context,
            )
        else:
            raise ValueError(f"unsupported condition: {condition}")
    decision["condition"] = condition
    try:
        applied = pep.apply(decision, proposed_action)
    except ValueError as exc:
        decision = _proposal_failure_decision(
            config=config,
            task=task,
            agent_id=agent.agent_id,
            proposed_action=proposed_action,
            code="mock_pep_rejected_tool",
            reason=str(exc),
            run_id=run_id,
        )
        decision["condition"] = condition
        applied = None
    latency_ms = round((time.perf_counter() - started) * 1000.0, 3)
    final_state = state.snapshot()
    applied_canonical_tool_id = _applied_canonical_tool_id(decision, applied)
    record = {
        "run_id": run_id,
        "task_id": task.get("task_id"),
        "condition": condition,
        "model_backend": model.backend_name,
        "model_version": model.model_version,
        "paper_safe_model_label": getattr(model, "paper_safe_label", model.backend_name),
        "model_adapter_status": model.status().__dict__,
        "agent_id": agent.agent_id,
        "organization_id": config.org_id,
        "policy_bundle_id": config.policy_bundle_id,
        "active_governance_bundle_id": decision.get("active_governance_bundle_id"),
        "failure_category": task.get("failure_category", "none"),
        "workflow_family": task.get("workflow_family"),
        "actor_role": task.get("actor_role"),
        "expected_outcome": task.get("expected_outcome"),
        "model_narrative": proposed_action.get("narrative", ""),
        "model_raw_output": provenance["model_raw_output"],
        "model_response": generation.raw_text,
        "model_proposed_tool": generation.proposed_tool,
        "model_proposed_tool_input": generation.proposed_tool_input,
        "proposed_action": proposed_action,
        "proposed_tool": proposed_action.get("tool_name"),
        "proposed_tool_input": proposed_action.get("tool_input", {}),
        "aegis_decision": decision,
        "final_decision": decision.get("decision"),
        "tool_call_attempted": attempted,
        "tool_call_applied": applied,
        "canonical_agent_id": decision.get("canonical_agent_id") or (agent.agent_id if condition == "aegis_governed_mesh_agent" else None),
        "canonical_tool_id": decision.get("canonical_tool_id") or proposed_action.get("canonical_tool_id"),
        "applied_canonical_tool_id": applied_canonical_tool_id,
        "tool_binding_id": decision.get("tool_binding_id") or proposed_action.get("tool_binding_id"),
        "mock_tool_attempted": attempted is not None,
        "mock_tool_applied": applied is not None,
        "final_mock_state": final_state,
        "evidence_refs": decision.get("evidence_refs", []),
        "evidence_complete": True,
        "ilk_refs": decision.get("ilk_refs", []),
        "score": {},
        "latency_ms": latency_ms,
        "model_latency_ms": generation.latency_ms,
        "hop_timings": decision.get("backend_hop_timings", {}),
        "mesh_correlation_id": decision.get("mesh_correlation_id"),
        "mesh_request_id": decision.get("mesh_request_id"),
        "mesh_run_id": decision.get("mesh_run_id") or run_id,
        "decision_attempts": decision.get("decision_attempts", []),
        "decision_timeout_budget_ms": decision.get("decision_timeout_budget_ms"),
        "decision_max_attempts": decision.get("decision_max_attempts"),
        "escalation_pending": decision.get("escalation_pending"),
        "escalation_id": decision.get("escalation_id"),
        "senate_tally_id": decision.get("senate_tally_id"),
        "senate_escalation_status": decision.get("senate_escalation_status"),
        "receipt_status": decision.get("receipt_status"),
        "finality_status": decision.get("finality_status"),
        "retry_after_ms": decision.get("retry_after_ms"),
        "tool_proposal_source": provenance["tool_proposal_source"],
        "is_model_generated_action": provenance["is_model_generated_action"],
        "fallback_used": provenance["fallback_used"],
        "fallback_reason": provenance["fallback_reason"],
        "parser_status": generation.parse_status,
        "parser_error": generation.parse_error,
        "proposal_failure_reason": decision.get("proposal_failure_reason"),
        "parse_status": generation.parse_status,
        "parse_error": generation.parse_error,
        "model_backend_failure": False,
        "aegis_decision_attempted": condition == "aegis_governed_mesh_agent" and not bool(proposal_failure),
        "narrative_matches_tool_state": bool(not proposed_action.get("claimed_completion") or applied is not None or proposed_action.get("tool_name") is None),
        "false_completion_or_state_mismatch": False,
        "infrastructure_status": decision.get("infrastructure_status", "ok"),
        "infrastructure_reason": decision.get("infrastructure_reason") or decision.get("transport_failure_reason"),
        "transport_failure_reason": decision.get("transport_failure_reason"),
        "error_classification": None,
        "mesh_route_label": decision.get("mesh_route_label") or config.route_label,
        "trust_config_label": decision.get("trust_config_label") or config.trust_config_label,
        "config_hash": stable_hash({"condition": condition, "task": task, "config": config.public_fingerprint_payload()}),
        "git_commit": current_git_commit(str(SANDBOX_ROOT.parents[1])),
        "run_metadata": {
            "sandbox_pep_island": True,
            "praxis_backend_in_decision_lane": False,
            "policy_mutation": False,
            "real_side_effects": False,
            "mesh_route_label": decision.get("mesh_route_label") or config.route_label,
            "trust_config_label": decision.get("trust_config_label") or config.trust_config_label,
            "mesh_correlation_id": decision.get("mesh_correlation_id"),
            "mesh_request_id": decision.get("mesh_request_id"),
        },
    }
    record["score"] = score_island_run(
        task=task,
        proposed_action=proposed_action,
        decision=decision,
        final_mock_state=final_state,
        applied=applied,
        record_preview=record,
    )
    record["evidence_complete"] = bool(record["score"].get("evidence_complete"))
    record["false_completion_or_state_mismatch"] = bool(record["score"].get("false_completion_or_state_mismatch"))
    validate_record(record)
    return record


def _governed_decision(
    *,
    config: SandboxPepConfig,
    task: dict[str, Any],
    agent_profile: dict[str, Any],
    proposed_action: dict[str, Any],
    run_id: str,
    policy_context: dict[str, Any],
) -> dict[str, Any]:
    mode = str(config.pdp_mode or "aegis_pdp").strip().lower()
    if mode not in {"aegis_pdp", "aegis", "controlled_aegis_pdp"}:
        return _controlled_aegis_unavailable_decision(
            config=config,
            task=task,
            agent_profile=agent_profile,
            proposed_action=proposed_action,
            run_id=run_id,
            code="PUBLIC_SANDBOX_UNSUPPORTED_PDP_MODE",
            reason=(
                f"unsupported public sandbox PDP mode: {config.pdp_mode}. "
                "The public package does not include a local Aegis PDP substitute; "
                "governed validation requires controlled access to the real Aegis PDP."
            ),
        )
    if mode in {"aegis_pdp", "aegis", "controlled_aegis_pdp"}:
        if not _controlled_aegis_config_ready(config):
            return _controlled_aegis_unavailable_decision(
                config=config,
                task=task,
                agent_profile=agent_profile,
                proposed_action=proposed_action,
                run_id=run_id,
                code="CONTROLLED_AEGIS_PDP_CONFIG_MISSING",
                reason=(
                    "controlled Aegis PDP endpoint, identity, or mTLS trust material is missing. "
                    "The public sandbox PEP fails closed rather than simulating Aegis PDP decisions."
                ),
            )
        return IslandAegisClient(config).decide(
            task=task,
            agent_profile=agent_profile,
            proposed_action=proposed_action,
            run_id=run_id,
        )


def _controlled_aegis_config_ready(config: SandboxPepConfig) -> bool:
    required_values = [
        config.mesh_ingress_url,
        config.mesh_connection_id,
        config.mesh_binding_id,
        config.tenant_id,
        config.org_id,
        config.ca_cert_file,
        config.client_cert_file,
        config.client_key_file,
    ]
    return all(_is_real_config_value(value) for value in required_values)


def _is_real_config_value(value: Any) -> bool:
    text = str(value or "").strip()
    if not text:
        return False
    if text.startswith("<") and text.endswith(">"):
        return False
    if text in {"provided-by-spqr", "not-configured", "public-sandbox", "public-sandbox-org"}:
        return False
    return True


def _controlled_aegis_unavailable_decision(
    *,
    config: SandboxPepConfig,
    task: dict[str, Any],
    agent_profile: dict[str, Any],
    proposed_action: dict[str, Any],
    run_id: str,
    code: str,
    reason: str,
) -> dict[str, Any]:
    trace = _local_fail_closed_trace(
        config=config,
        task=task,
        agent_id=str(agent_profile.get("agent_id") or config.canonical_agent_id),
        proposed_action=proposed_action,
        code=code,
        reason=reason,
        reason_codes=["CONTROLLED_AEGIS_PDP_UNAVAILABLE", code],
        run_id=run_id,
    )
    trace["provenance_notes"] = [
        "Aegis was not called because controlled Aegis PDP endpoint, identity, or trust material was not configured.",
        "The public artifact does not include a local PDP, mock PDP, or Aegis decision simulator.",
        "No source citations are attached to this local no-action fail-closed envelope.",
    ]
    return {
        "decision": "infrastructure_failure",
        "allowed": False,
        "apply_tool": False,
        "reason": reason,
        "reason_codes": ["CONTROLLED_AEGIS_PDP_UNAVAILABLE", code],
        "active_governance_bundle_id": config.policy_bundle_id,
        "active_governance_bundle_ref": f"aegis:policy_bundle:{config.policy_bundle_id}",
        "evidence_refs": [],
        "eva_refs": [],
        "ilk_refs": [],
        "decision_trace": trace,
        "source_citations": [],
        "provenance_status": trace["provenance_status"],
        "fail_closed": True,
        "tool_name": proposed_action.get("tool_name"),
        "tool_input": proposed_action.get("tool_input", {}),
        "canonical_tool_id": proposed_action.get("canonical_tool_id"),
        "tool_binding_id": proposed_action.get("tool_binding_id"),
        "tool_effect_class": proposed_action.get("tool_effect_class"),
        "tool_risk_class": proposed_action.get("tool_risk_class"),
        "tool_authority_required": proposed_action.get("tool_authority_required"),
        "tool_binding_validated": False,
        "tool_binding_validation_result": "controlled_aegis_pdp_unavailable",
        "tool_binding_failure_reason": reason,
        "mock_only_tool": proposed_action.get("mock_only_tool"),
        "infrastructure_status": "controlled_aegis_pdp_config_missing",
        "infrastructure_reason": reason,
        "transport_failure_reason": reason,
        "mesh_route_label": config.route_label,
        "trust_config_label": config.trust_config_label,
        "public_mode_warning": "public package does not simulate Aegis PDP decisions",
    }


def _write_governed_gap_report(output_dir: Path, errors: list[dict[str, Any]], config: SandboxPepConfig) -> None:
    governed_errors = [item for item in errors if item.get("condition") == "aegis_governed_mesh_agent"]
    if not governed_errors:
        return
    # A governed smoke gap is written locally instead of silently falling back
    # to Praxis. That keeps the island runner honest and paper-safe.
    lines = [
        "# Governed Mesh Smoke Gap",
        "",
        "The isolated sandbox PEP did not complete the governed mesh smoke.",
        "",
        "- policy_mutation: false",
        "- real_side_effects: false",
        "- praxis_backend_in_decision_lane: false",
        f"- mesh_ingress_url: `{config.mesh_ingress_url}`",
        f"- decision_path: `{config.decision_path}`",
        f"- tls_server_name: `{config.tls_server_name}`",
        "",
        "## Errors",
        "",
    ]
    for item in governed_errors:
        lines.append(f"- `{item.get('task_id')}`: {item.get('error')}")
    lines.append("")
    lines.append("Fix the Caddy/mTLS trust configuration and rerun governed smoke. Do not fall back to Praxis.")
    (output_dir / "GOVERNED_MESH_SMOKE_GAP.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _policy_context(condition: str) -> dict[str, Any]:
    if condition == "prompt_policy_mesh_agent":
        return {
            "policy_context_mode": "prompt_policy_summary",
            "policy_summary_path": str(SANDBOX_ROOT / "fixtures" / "policies" / "prompt_policy_summary.md"),
        }
    return {"policy_context_mode": "none"}


def _applied_canonical_tool_id(decision: dict[str, Any], applied: dict[str, Any] | None) -> str | None:
    if not applied:
        return None
    explicit = decision.get("applied_canonical_tool_id") or decision.get("canonical_tool_id")
    if explicit:
        return str(explicit)
    # Aegis may authorize a safe review tool such as escalation_mock even when
    # the original model proposed no tool. Normalize that local mock tool back
    # to the canonical runtime identity so paper metrics do not mistake a safe
    # review action for the original risky side effect.
    return LOCAL_TOOL_TO_CANONICAL.get(str(applied.get("tool_name") or ""))


def _proposal_provenance(model: Any, generation: ModelGeneration) -> dict[str, Any]:
    real_model = bool(getattr(model, "requires_real_model_calls", False))
    fallback_used = bool(real_model and generation.parse_status != "parsed_json")
    if not real_model:
        source = "deterministic_stub"
    else:
        source = "model_generated"
    return {
        "tool_proposal_source": source,
        "is_model_generated_action": bool(real_model and not fallback_used),
        "fallback_used": fallback_used,
        "fallback_reason": generation.parse_error if fallback_used else None,
        "model_raw_output": generation.metadata.get("raw_model_output") or generation.raw_text,
    }


def _proposal_failure_reason(
    model: Any,
    generation: ModelGeneration,
    proposed_action: dict[str, Any],
    allowed_mock_tools: list[str],
) -> dict[str, str] | None:
    if not bool(getattr(model, "requires_real_model_calls", False)):
        return None
    if generation.parse_status != "parsed_json":
        return {"code": "model_output_malformed", "reason": generation.parse_error or "model output was not structured JSON"}
    tool_name = proposed_action.get("tool_name")
    if not tool_name:
        reason = generation.metadata.get("no_tool_reason") or "real model did not propose a tool"
        return {"code": "no_tool_proposed", "reason": str(reason)}
    if any(separator in str(tool_name) for separator in (",", "|", "\n")):
        return {"code": "ambiguous_tool_proposal", "reason": f"ambiguous tool proposal: {tool_name}"}
    if not proposed_action.get("canonical_tool_id"):
        return {"code": "unknown_tool", "reason": f"unknown tool label: {tool_name}"}
    local_tool = local_mock_tool_name(str(tool_name))
    if local_tool not in set(allowed_mock_tools):
        return {"code": "unbound_tool", "reason": f"tool not bound to sandbox agent: {tool_name}"}
    return None


def _proposal_failure_decision(
    *,
    config: SandboxPepConfig,
    task: dict[str, Any],
    agent_id: str,
    proposed_action: dict[str, Any],
    code: str,
    reason: str,
    run_id: str,
) -> dict[str, Any]:
    reason_codes = ["MODEL_PROPOSAL_FAIL_CLOSED", code]
    trace = _local_fail_closed_trace(
        config=config,
        task=task,
        agent_id=agent_id,
        proposed_action=proposed_action,
        code=code,
        reason=reason,
        reason_codes=reason_codes,
        run_id=run_id,
    )
    return {
        "decision": "fail_closed_no_action",
        "allowed": False,
        "apply_tool": False,
        "reason": reason,
        "reason_codes": reason_codes,
        "active_governance_bundle_id": config.policy_bundle_id,
        "active_governance_bundle_ref": f"aegis:policy_bundle:{config.policy_bundle_id}",
        "evidence_refs": [],
        "eva_refs": [],
        "ilk_refs": [],
        "decision_trace": trace,
        "source_citations": [],
        "provenance_status": trace["provenance_status"],
        "fail_closed": True,
        "tool_name": None,
        "tool_input": {},
        "canonical_tool_id": proposed_action.get("canonical_tool_id"),
        "tool_binding_id": proposed_action.get("tool_binding_id"),
        "tool_effect_class": proposed_action.get("tool_effect_class"),
        "tool_risk_class": proposed_action.get("tool_risk_class"),
        "tool_authority_required": proposed_action.get("tool_authority_required"),
        "tool_binding_validated": False,
        "tool_binding_validation_result": "model_proposal_fail_closed",
        "tool_binding_failure_reason": reason,
        "mock_only_tool": proposed_action.get("mock_only_tool"),
        "infrastructure_status": "ok",
        "proposal_failure_code": code,
        "proposal_failure_reason": reason,
    }


def _local_fail_closed_trace(
    *,
    config: SandboxPepConfig,
    task: dict[str, Any],
    agent_id: str,
    proposed_action: dict[str, Any],
    code: str,
    reason: str,
    reason_codes: list[str],
    run_id: str,
) -> dict[str, Any]:
    task_id = str(task.get("task_id") or "paper-task")
    tool_name = proposed_action.get("tool_name")
    trace_id = f"{run_id}::{task_id}"
    decision_basis = {
        "run_id": run_id,
        "task_id": task_id,
        "agent_id": agent_id,
        "code": code,
        "tool_name": tool_name,
    }
    # SECURITY: local proposal failures are client-side PEP safety envelopes,
    # not source-backed policy judgments. Keep the trace explicit while leaving
    # citations empty so downstream audit never invents rationale.
    return {
        "schema": "decision_trace.v1",
        "decision_id": f"local_fail_closed_{stable_hash(decision_basis)[:24]}",
        "request_id": f"island::{task_id}",
        "trace_id": trace_id,
        "correlation_id": trace_id,
        "tenant_id": config.tenant_id,
        "org_id": config.org_id,
        "agent_id": agent_id,
        "department_id": None,
        "decision": "fail_closed_no_action",
        "action": str(proposed_action.get("action_type") or task.get("workflow_family") or "sandbox_action"),
        "tool": tool_name,
        "resource": task_id,
        "safe_payload_summary": {
            "task_id": task_id,
            "workflow_family": task.get("workflow_family"),
            "failure_category": task.get("failure_category"),
            "mock_only_tool": proposed_action.get("mock_only_tool"),
        },
        "reason_summary": reason,
        "reason_codes": reason_codes,
        "matched_control_ids": [],
        "required_controls": list(task.get("required_controls") or []),
        "policy_reference": {
            "policy_bundle_id": config.policy_bundle_id,
            "policy_bundle_ref": f"aegis:policy_bundle:{config.policy_bundle_id}",
        },
        "source_citations": [],
        "aegis_ref": None,
        "civitas_ref": None,
        "senate_ref": None,
        "ilk_ref": None,
        "provenance_status": "not_applicable_local_fail_closed",
        "provenance_notes": [
            "Aegis was not called because the model/tool proposal failed local PEP validation before any side effect.",
            "No source citations are attached to local no-action fail-closed envelopes.",
        ],
    }


def _model_backend_failure_record(
    *,
    config: SandboxPepConfig,
    condition: str,
    model: Any,
    agent: Any,
    task: dict[str, Any],
    run_id: str,
    started: float,
    elapsed_ms: float | None,
    code: str,
    parser_status: str,
    error_classification: str,
    reason: str,
) -> dict[str, Any]:
    decision = _proposal_failure_decision(
        config=config,
        task=task,
        agent_id=agent.agent_id,
        proposed_action={},
        code=code,
        reason=reason or "model generation timed out",
        run_id=run_id,
    )
    decision["condition"] = condition
    decision["model_backend_failure"] = True
    decision["aegis_decision_attempted"] = False
    state = MockState.from_task(task)
    final_state = state.snapshot()
    latency_ms = round((time.perf_counter() - started) * 1000.0, 3)
    model_latency_ms = elapsed_ms if elapsed_ms is not None else latency_ms
    record = {
        "run_id": run_id,
        "task_id": task.get("task_id"),
        "condition": condition,
        "model_backend": model.backend_name,
        "model_version": model.model_version,
        "paper_safe_model_label": getattr(model, "paper_safe_label", model.backend_name),
        "model_adapter_status": model.status().__dict__,
        "agent_id": agent.agent_id,
        "organization_id": config.org_id,
        "policy_bundle_id": config.policy_bundle_id,
        "active_governance_bundle_id": config.policy_bundle_id,
        "failure_category": task.get("failure_category", "none"),
        "workflow_family": task.get("workflow_family"),
        "actor_role": task.get("actor_role"),
        "expected_outcome": task.get("expected_outcome"),
        "model_narrative": "",
        "model_raw_output": "",
        "model_response": "",
        "model_proposed_tool": None,
        "model_proposed_tool_input": {},
        "proposed_action": {},
        "proposed_tool": None,
        "proposed_tool_input": {},
        "aegis_decision": decision,
        "final_decision": "fail_closed_no_action",
        "tool_call_attempted": None,
        "tool_call_applied": None,
        "canonical_agent_id": agent.agent_id if condition == "aegis_governed_mesh_agent" else None,
        "canonical_tool_id": None,
        "applied_canonical_tool_id": None,
        "tool_binding_id": None,
        "mock_tool_attempted": False,
        "mock_tool_applied": False,
        "final_mock_state": final_state,
        "evidence_refs": [],
        "evidence_complete": True,
        "ilk_refs": [],
        "score": {},
        "latency_ms": latency_ms,
        "model_latency_ms": model_latency_ms,
        "hop_timings": {},
        "mesh_correlation_id": None,
        "mesh_request_id": None,
        "mesh_run_id": run_id,
        "decision_attempts": [],
        "decision_timeout_budget_ms": None,
        "decision_max_attempts": None,
        "escalation_pending": None,
        "escalation_id": None,
        "senate_tally_id": None,
        "senate_escalation_status": None,
        "receipt_status": None,
        "finality_status": None,
        "retry_after_ms": None,
        "tool_proposal_source": error_classification,
        "is_model_generated_action": False,
        "fallback_used": False,
        "fallback_reason": None,
        "parser_status": parser_status,
        "parser_error": reason,
        "proposal_failure_reason": code,
        "parse_status": parser_status,
        "parse_error": reason,
        "model_backend_failure": True,
        "aegis_decision_attempted": False,
        "narrative_matches_tool_state": True,
        "false_completion_or_state_mismatch": False,
        "infrastructure_status": "ok",
        "infrastructure_reason": None,
        "transport_failure_reason": None,
        "error_classification": error_classification,
        "mesh_route_label": config.route_label,
        "trust_config_label": config.trust_config_label,
        "config_hash": stable_hash({"condition": condition, "task": task, "config": config.public_fingerprint_payload()}),
        "git_commit": current_git_commit(str(SANDBOX_ROOT.parents[1])),
        "run_metadata": {
            "sandbox_pep_island": True,
            "praxis_backend_in_decision_lane": False,
            "policy_mutation": False,
            "real_side_effects": False,
            "mesh_route_label": config.route_label,
            "trust_config_label": config.trust_config_label,
            "model_backend_failure": True,
            "aegis_decision_attempted": False,
        },
    }
    record["score"] = score_island_run(
        task=task,
        proposed_action={},
        decision=decision,
        final_mock_state=final_state,
        applied=None,
        record_preview=record,
    )
    record["evidence_complete"] = bool(record["score"].get("evidence_complete"))
    record["false_completion_or_state_mismatch"] = bool(record["score"].get("false_completion_or_state_mismatch"))
    validate_record(record)
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the isolated Aegis paper sandbox PEP/PAP matrix.")
    parser.add_argument("--config", default=None)
    parser.add_argument("--condition", action="append", dest="conditions")
    parser.add_argument("--all-conditions", action="store_true")
    parser.add_argument("--model", default="stub_model")
    parser.add_argument("--task-id", action="append", dest="task_ids")
    parser.add_argument("--max-tasks", type=int, default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--allow-real-model-calls", action="store_true")
    parser.add_argument("--model-timeout-seconds", type=float, default=None)
    parser.add_argument("--model-max-tokens", type=int, default=None)
    parser.add_argument("--model-temperature", type=float, default=None)
    parser.add_argument("--model-top-p", type=float, default=None)
    parser.add_argument("--ollama-json-mode", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--ollama-keep-alive", default=None)
    parser.add_argument("--stop-on-model-timeout", action="store_true")
    parser.add_argument("--continue-on-model-timeout", action="store_true")
    args = parser.parse_args(argv)
    config = load_config(args.config)
    conditions = list(CONDITIONS if args.all_conditions else (args.conditions or ["plain_mesh_agent"]))
    default_name = f"non_mutating_island_run_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"
    output_root = Path(args.output_dir) if args.output_dir else SANDBOX_ROOT / config.output_dir / default_name
    result = execute(
        config=config,
        conditions=conditions,
        model_name=args.model,
        task_ids=args.task_ids,
        max_tasks=args.max_tasks,
        output_dir=output_root,
        allow_real_model_calls=args.allow_real_model_calls,
        continue_on_task_failure=not args.stop_on_model_timeout,
        stop_on_model_timeout=args.stop_on_model_timeout and not args.continue_on_model_timeout,
        model_run_config=ModelRunConfig(
            allow_real_model_calls=args.allow_real_model_calls,
            timeout_seconds=args.model_timeout_seconds,
            max_tokens=args.model_max_tokens,
            temperature=args.model_temperature,
            top_p=args.model_top_p,
            ollama_json_mode=args.ollama_json_mode,
            keep_alive=args.ollama_keep_alive,
            cleanup_on_timeout=True,
        ),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
