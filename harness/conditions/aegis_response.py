from __future__ import annotations

from copy import deepcopy
from typing import Any

from harness.evidence.live_refs import build_live_refs


def _reason_codes(response: dict[str, Any]) -> list[str]:
    return [str(code).strip() for code in response.get("reason_codes", []) if str(code).strip()]


def append_reason_code_once(reason_codes: list[str], code: str) -> list[str]:
    if code in reason_codes:
        return list(reason_codes)
    return [*reason_codes, code]


def _reason_summary(response: dict[str, Any]) -> str:
    return str(response.get("reason_summary") or response.get("reason") or "").strip()


def _needs_more_evidence(response: dict[str, Any]) -> bool:
    haystack = " ".join(_reason_codes(response) + [_reason_summary(response)]).lower()
    return "evidence" in haystack or "missing_" in haystack or "more evidence" in haystack


def _should_redact(response: dict[str, Any], proposed_action: dict[str, Any]) -> bool:
    haystack = " ".join(_reason_codes(response) + [_reason_summary(response)]).lower()
    if "redact" in haystack:
        return True
    tool_input = proposed_action.get("tool_input", {})
    return bool(tool_input.get("classification") == "sensitive" and response.get("decision") == "allow" and "attachment" in haystack)


def _execution_withheld(response: dict[str, Any], proposed_action: dict[str, Any]) -> bool:
    """Detect contradictory allow/withheld responses before any tool executes.

    Aegis may run in monitor or rollout modes while still reporting that judged
    execution was withheld. For effectful tools, that contradiction must resolve
    to fail-closed at the PEP boundary. Treating the monitor-side allow as an
    executable allow would bypass the judged denial.
    """
    if not proposed_action.get("tool_name"):
        return False
    codes = set(_reason_codes(response))
    haystack = " ".join(codes) + " " + _reason_summary(response)
    lowered = haystack.lower()
    if "AEGIS_EXECUTION_WITHHELD" in codes:
        return True
    if "execution withheld" in lowered or "judged deny" in lowered or "judged denied" in lowered:
        return True
    if response.get("apply_tool") is False and str(response.get("decision") or "").strip() == "allow":
        return True
    return False


def _escalation_metadata(response: dict[str, Any]) -> dict[str, Any]:
    """Return Senate escalation fields without inventing missing evidence.

    These fields are produced by Aegis only when the judged path actually
    creates or resolves an escalation. The harness must pass them through as
    audit metadata, not infer them from the final allow/block/escalate label.
    """
    return {
        "escalation_pending": response.get("escalation_pending"),
        "escalation_id": response.get("escalation_id"),
        "senate_tally_id": response.get("senate_tally_id"),
        "senate_escalation_status": response.get("senate_escalation_status"),
        "receipt_status": response.get("receipt_status"),
        "finality_status": response.get("finality_status"),
        "retry_after_ms": response.get("retry_after_ms"),
    }


def _redacted_tool_input(proposed_action: dict[str, Any]) -> dict[str, Any]:
    tool_input = deepcopy(proposed_action.get("tool_input", {}))
    if "body" in tool_input:
        tool_input["body"] = "[REDACTED BY AEGIS]"
    if "attachments" in tool_input:
        tool_input["attachments"] = []
    if "content" in tool_input:
        tool_input["content"] = "[REDACTED BY AEGIS]"
    return tool_input


def normalize_aegis_response(
    response: dict[str, Any],
    *,
    proposed_action: dict[str, Any],
    policy_bundle_id: str,
) -> dict[str, Any]:
    refs = build_live_refs(response)
    reason_codes = _reason_codes(response)
    reason_summary = _reason_summary(response)
    bundle_fingerprint = str(response.get("bundle_fingerprint") or "").strip()
    governance_ref = f"aegis:bundle:{bundle_fingerprint}" if bundle_fingerprint else f"aegis:policy_bundle:{policy_bundle_id}"
    decision_trace = response.get("decision_trace") if isinstance(response.get("decision_trace"), dict) else None
    source_citations = response.get("source_citations")
    if not isinstance(source_citations, list) and decision_trace is not None:
        source_citations = decision_trace.get("source_citations")
    if not isinstance(source_citations, list):
        source_citations = []
    base = {
        "allowed": False,
        "apply_tool": False,
        "reason": reason_summary or "Aegis returned no reason summary",
        "reason_codes": reason_codes,
        "active_governance_bundle_id": bundle_fingerprint or policy_bundle_id,
        "active_governance_bundle_ref": governance_ref,
        "evidence_refs": refs["evidence_refs"],
        "eva_refs": refs["eva_refs"],
        "ilk_refs": refs["ilk_refs"],
        "fail_closed": False,
        "tool_name": proposed_action.get("tool_name"),
        "tool_input": deepcopy(proposed_action.get("tool_input", {})),
        "infrastructure_status": "ok",
        "aegis_timings_ms": response.get("aegis_timings_ms", {}),
        "decision_trace": decision_trace,
        "source_citations": source_citations,
        "matched_control_ids": response.get("matched_control_ids") or (decision_trace or {}).get("matched_control_ids") or [],
        "required_controls": response.get("required_controls") or (decision_trace or {}).get("required_controls") or [],
        "runtime_tool_decision": response.get("runtime_tool_decision"),
        "policy_reference": response.get("policy_reference") or (decision_trace or {}).get("policy_reference"),
        "provenance_status": response.get("provenance_status") or (decision_trace or {}).get("provenance_status"),
        **_escalation_metadata(response),
    }

    if str(response.get("decision") or "").strip() == "error":
        return {
            "decision": "infrastructure_failure",
            **base,
            "reason": reason_summary or "Aegis returned decision=error",
            "fail_closed": True,
            "infrastructure_status": "aegis_error",
        }

    if _execution_withheld(response, proposed_action):
        return {
            "decision": "block",
            **base,
            "allowed": False,
            "apply_tool": False,
            "fail_closed": True,
            "reason": reason_summary or "Aegis withheld execution for an effectful tool.",
            "reason_codes": append_reason_code_once(reason_codes, "EXECUTION_WITHHELD_FAIL_CLOSED"),
        }

    if bool(response.get("escalation_required")) or bool(response.get("escalation_pending")):
        return {
            "decision": "escalate",
            **base,
            "allowed": False,
            "apply_tool": True,
            "tool_name": "escalation_mock",
            "tool_input": {
                "target_queue": "aegis-governance-review",
                "reason": reason_summary or "Aegis requires escalation before side effects.",
                "original_tool_name": proposed_action.get("tool_name"),
            },
        }

    if str(response.get("decision") or "").strip() == "deny":
        if _needs_more_evidence(response):
            return {
                "decision": "require_more_evidence",
                **base,
                "allowed": False,
                "apply_tool": False,
            }
        return {
            "decision": "block",
            **base,
            "allowed": False,
            "apply_tool": False,
        }

    if _should_redact(response, proposed_action):
        return {
            "decision": "redact",
            **base,
            "allowed": True,
            "apply_tool": bool(proposed_action.get("tool_name")),
            "tool_input": _redacted_tool_input(proposed_action),
        }

    return {
        "decision": "allow",
        **base,
        "allowed": True,
        "apply_tool": bool(proposed_action.get("tool_name")),
    }
