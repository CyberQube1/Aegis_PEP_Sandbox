from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def build_run_manifest(
    *,
    condition: str,
    model_backend: str,
    paper_safe_model_label: str,
    agent_id: str,
    task_source: str,
    output_path: str,
    run_count: int,
    org_id: str | None = None,
    baseline_release_id: str | None = None,
    baseline_fingerprint: str | None = None,
    policy_bundle_id: str | None = None,
    workflow_families: list[str] | None = None,
    model_adapter_status: dict[str, Any] | None = None,
    allow_real_model_calls: bool = False,
    selected_task_ids: list[str] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'condition': condition,
        'model_backend': model_backend,
        'paper_safe_model_label': paper_safe_model_label,
        'agent_id': agent_id,
        'task_source': task_source,
        'output_path': output_path,
        'run_count': run_count,
        'org_id': org_id,
        'baseline_release_id': baseline_release_id,
        'baseline_fingerprint': baseline_fingerprint,
        'policy_bundle_id': policy_bundle_id,
        'workflow_families': workflow_families or [],
        'model_adapter_status': model_adapter_status or {},
        'allow_real_model_calls': bool(allow_real_model_calls),
        'selected_task_ids': selected_task_ids or [],
    }
    if extra:
        manifest.update(extra)
    return manifest
