from __future__ import annotations

from typing import Any


def build_live_refs(response: dict[str, Any]) -> dict[str, list[str]]:
    evidence_refs: list[str] = []
    ilk_refs: list[str] = []
    eva_refs: list[str] = []

    artifact_id = str(response.get("execution_artifact_id") or "").strip()
    if artifact_id:
        evidence_refs.append(f"aegis:execution_artifact:{artifact_id}")

    bundle_fingerprint = str(response.get("bundle_fingerprint") or "").strip()
    if bundle_fingerprint:
        evidence_refs.append(f"aegis:bundle_fingerprint:{bundle_fingerprint}")

    for key in ("ilk_event_id", "ilk_tenant_receipt_id", "ilk_global_anchor_ref", "ilk_entry_hash", "ilk_block_hash"):
        value = str(response.get(key) or "").strip()
        if value:
            ilk_refs.append(f"{key}:{value}")

    for key in ("deterministic_decision_hash", "decision_id", "trace_id"):
        value = str(response.get(key) or "").strip()
        if value:
            eva_refs.append(f"{key}:{value}")

    return {
        "evidence_refs": evidence_refs,
        "ilk_refs": ilk_refs,
        "eva_refs": eva_refs,
    }
