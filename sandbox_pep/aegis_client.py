from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any

from harness.conditions.aegis_client import AegisClientError, AegisDecisionClient
from harness.conditions.aegis_response import normalize_aegis_response

from .config import SandboxPepConfig


class IslandAegisClient:
    def __init__(self, config: SandboxPepConfig) -> None:
        self.config = config
        if not config.cert_configured:
            # Production boundary: governed mode is only allowed over the mesh
            # mTLS route. Missing trust material is a hard configuration error,
            # not a reason to downgrade to the local prompt-policy baseline.
            raise AegisClientError(
                "isolated sandbox PEP mesh client missing mTLS trust config",
                classification="mesh_trust_config_missing",
            )
        self._client = AegisDecisionClient(
            endpoint_url=config.mesh_ingress_url,
            decision_path=config.decision_path,
            ca_cert_file=str(config.ca_cert_file),
            client_cert_file=str(config.client_cert_file),
            client_key_file=str(config.client_key_file),
            server_name_override=config.tls_server_name,
            host_header=config.host_header,
            timeout_seconds=config.timeout_seconds,
        )

    def decide(self, *, task: dict[str, Any], agent_profile: dict[str, Any], proposed_action: dict[str, Any], run_id: str) -> dict[str, Any]:
        payload = self._payload(task=task, agent_profile=agent_profile, proposed_action=proposed_action, run_id=run_id)
        started = time.perf_counter()
        attempts: list[dict[str, Any]] = []
        max_attempts = max(1, int(self.config.decision_max_attempts))
        try:
            response = None
            for attempt in range(1, max_attempts + 1):
                attempt_started = time.perf_counter()
                try:
                    response = self._client.decide(payload)
                    attempts.append(
                        {
                            "attempt": attempt,
                            "status": "ok",
                            "elapsed_ms": round((time.perf_counter() - attempt_started) * 1000.0, 3),
                        }
                    )
                    break
                except AegisClientError as exc:
                    attempts.append(
                        {
                            "attempt": attempt,
                            "status": "failure",
                            "classification": exc.classification,
                            "reason": str(exc),
                            "timeout_budget_ms": int(self.config.timeout_seconds * 1000),
                            "elapsed_ms": round((time.perf_counter() - attempt_started) * 1000.0, 3),
                        }
                    )
                    if not self._retryable(exc) or attempt >= max_attempts:
                        raise
                    time.sleep(max(0.0, float(self.config.decision_retry_backoff_seconds)))
            if response is None:
                raise AegisClientError("Aegis decision failed without response")
            elapsed = round((time.perf_counter() - started) * 1000.0, 3)
            decision = normalize_aegis_response(
                response,
                proposed_action=proposed_action,
                policy_bundle_id=self.config.policy_bundle_id,
            )
            correlation_id = str(payload["correlation_id"])
            request_id = str(payload["request_id"])
            decision["backend_hop_timings"] = {
                "aegis_direct_decision_ms": elapsed,
                "aegis_timings_ms": decision.get("aegis_timings_ms", {}),
                "mesh_route": self.config.route_label,
                "trust_config": self.config.trust_config_label,
                "decision_attempts": attempts,
                "timeout_budget_ms": int(self.config.timeout_seconds * 1000),
                "max_attempts": max_attempts,
                "mesh_correlation_id": correlation_id,
                "mesh_request_id": request_id,
                "mesh_run_id": run_id,
            }
            decision["mesh_correlation_id"] = correlation_id
            decision["mesh_request_id"] = request_id
            decision["mesh_run_id"] = run_id
            decision["decision_attempts"] = attempts
            decision["decision_timeout_budget_ms"] = int(self.config.timeout_seconds * 1000)
            decision["decision_max_attempts"] = max_attempts
            decision["mesh_route_label"] = self.config.route_label
            decision["trust_config_label"] = self.config.trust_config_label
            return decision
        except AegisClientError as exc:
            # PEP safety invariant: transport failures are not governance
            # allows. The caller records the attempted tool, applies no mock
            # side effect, and leaves the row classified as fail-closed infra.
            return {
                "decision": "infrastructure_failure",
                "allowed": False,
                "apply_tool": False,
                "reason": str(exc),
                "reason_codes": ["AEGIS_MESH_TRANSPORT_FAILURE"],
                "active_governance_bundle_id": self.config.policy_bundle_id,
                "active_governance_bundle_ref": f"aegis:policy_bundle:{self.config.policy_bundle_id}",
                "evidence_refs": [],
                "eva_refs": [],
                "ilk_refs": [],
                "fail_closed": True,
                "tool_name": proposed_action.get("tool_name"),
                "tool_input": proposed_action.get("tool_input", {}),
                "infrastructure_status": exc.classification or "transport_failure",
                "infrastructure_reason": str(exc),
                "transport_failure_reason": str(exc),
                "decision_attempts": attempts,
                "decision_timeout_budget_ms": int(self.config.timeout_seconds * 1000),
                "decision_max_attempts": max_attempts,
                "mesh_correlation_id": payload.get("correlation_id"),
                "mesh_request_id": payload.get("request_id"),
                "mesh_run_id": run_id,
                "backend_hop_timings": {
                    "aegis_direct_decision_ms": round((time.perf_counter() - started) * 1000.0, 3),
                    "mesh_route": self.config.route_label,
                    "trust_config": self.config.trust_config_label,
                    "decision_attempts": attempts,
                    "timeout_budget_ms": int(self.config.timeout_seconds * 1000),
                    "max_attempts": max_attempts,
                    "mesh_correlation_id": payload.get("correlation_id"),
                    "mesh_request_id": payload.get("request_id"),
                    "mesh_run_id": run_id,
                },
                "mesh_route_label": self.config.route_label,
                "trust_config_label": self.config.trust_config_label,
            }

    def _payload(self, *, task: dict[str, Any], agent_profile: dict[str, Any], proposed_action: dict[str, Any], run_id: str) -> dict[str, Any]:
        task_id = str(task.get("task_id") or "paper-task")
        capability_ids = [str(item) for item in proposed_action.get("tool_capability_ids", []) if str(item)]
        return {
            "run_id": run_id,
            "request_id": f"island::{task_id}",
            "correlation_id": f"{run_id}::{task_id}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mesh_connection_id": self.config.mesh_connection_id,
            "mesh_binding_id": self.config.mesh_binding_id,
            "tenant_id": self.config.tenant_id,
            "org_id": self.config.org_id,
            "agent_id": agent_profile["agent_id"],
            "principal": agent_profile["agent_id"],
            "action": str(proposed_action.get("action_type") or task.get("workflow_family") or "sandbox_action"),
            "resource": task_id,
            "rollout_state": "enforce",
            "failure_mode": "fail_closed",
            "timeout_budget_ms": int(self.config.timeout_seconds * 1000),
            "retry_policy": f"transport_only:{self.config.decision_max_attempts}",
            "policy": {
                "policy_pattern": "paper_org_isolated_sandbox",
                "policy_bundle_id": self.config.policy_bundle_id,
                "policy_hash": self.config.baseline_fingerprint,
            },
            "attributes": {
                # These canonical fields are the contract with Aegis. The
                # sandbox does not ask Praxis to enrich or validate them in the
                # hot path; Aegis/PDP owns the decision against active law.
                "intent_kind": str(task.get("workflow_family") or "sandbox_workflow"),
                "resource_type": str(task.get("workflow_family") or "sandbox_task"),
                "effectful": bool(proposed_action.get("tool_name")),
                "principal_roles": [agent_profile.get("role", "operations_analyst")],
                "principal_type": agent_profile.get("authority_level", "employee"),
                "matched_capability_ids": capability_ids,
                "matched_control_ids": list(task.get("required_controls") or []),
                "required_controls": list(task.get("required_controls") or []),
                "task_id": task_id,
                "workflow_family": task.get("workflow_family"),
                "failure_category": task.get("failure_category"),
                "expected_outcome": task.get("expected_outcome"),
                "tool_name": proposed_action.get("tool_name"),
                "tool_input": proposed_action.get("tool_input", {}),
                "canonical_tool_id": proposed_action.get("canonical_tool_id"),
                "tool_binding_id": proposed_action.get("tool_binding_id"),
                "tool_effect_class": proposed_action.get("tool_effect_class"),
                "tool_risk_class": proposed_action.get("tool_risk_class"),
                "tool_authority_required": proposed_action.get("tool_authority_required"),
                "tool_capability_ids": capability_ids,
                "mock_only_tool": True,
                "sandbox_pep_island": True,
            },
            "metadata": {
                "request_context": {
                    "source": "paper_eval_isolated_sandbox_pep",
                    "org_name": self.config.org_name,
                    "canonical_agent_id": agent_profile.get("canonical_agent_id") or agent_profile.get("agent_id"),
                    "baseline_release_id": self.config.baseline_release_id,
                    "baseline_fingerprint": self.config.baseline_fingerprint,
                    "policy_bundle_id": self.config.policy_bundle_id,
                },
                "source_mapping": task.get("source_mapping", []),
            },
        }

    @staticmethod
    def _retryable(exc: AegisClientError) -> bool:
        # Retry only idempotent decision transport failures. The mock PEP has
        # not applied any tool at this point, and HTTP policy/schema failures
        # are deliberately not retried because they need operator correction.
        return exc.classification in {"transport_failure", "aegis_upstream_failure"}
