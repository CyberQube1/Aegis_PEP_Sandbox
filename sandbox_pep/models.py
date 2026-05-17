from __future__ import annotations

from typing import Any

from harness.agents.agent_profile import AgentProfile
from harness.models import FrontierModelAAdapter, GemmaLocalAdapter, StubModelAdapter


MODEL_REGISTRY = {
    "stub_model": StubModelAdapter,
    "gemma_local": GemmaLocalAdapter,
    "frontier_model_a": FrontierModelAAdapter,
}


def build_model(model_name: str) -> Any:
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"unsupported model: {model_name}")
    return MODEL_REGISTRY[model_name]()


def paper_agent_profile(*, condition: str, model_name: str, org_id: str, canonical_agent_id: str) -> AgentProfile:
    return AgentProfile.from_dict(
        {
            "agent_id": canonical_agent_id if condition == "aegis_governed_mesh_agent" else f"{condition}_local",
            "display_name": "Aegis Paper Sandbox PEP Agent",
            "organization_id": org_id,
            "role": "operations_analyst",
            "authority_level": "employee",
            "allowed_mock_tools": [
                "send_email_mock",
                "file_export_mock",
                "shell_action_request_mock",
                "vendor_approval_mock",
                "workflow_approval_mock",
                "escalation_mock",
                "background_job_mock",
                "memory_log_mock",
            ],
            "model_backend": model_name,
            "policy_context_mode": "prompt_policy_summary" if condition == "prompt_policy_mesh_agent" else "none",
            "evidence_mode": "isolated_sandbox_pep",
        }
    )

