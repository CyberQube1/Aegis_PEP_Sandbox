from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from harness.utils.io import load_yaml


SANDBOX_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = SANDBOX_ROOT / "config" / "sandbox_pep.example.yaml"
SECRET_PATH_FIELDS = {"ca_cert_file", "client_cert_file", "client_key_file"}
DEFAULT_CANONICAL_AGENT_IDS_BY_MODEL = {
    "stub_model": "public_sandbox_stub_agent",
    "gemma_local": "public_sandbox_gemma_agent",
    "frontier_model_a": "public_sandbox_frontier_agent",
}


@dataclass(frozen=True)
class SandboxPepConfig:
    tenant_id: str = "public-sandbox"
    org_id: str = "public-sandbox-org"
    model_label: str = "stub_model"
    active_law_label: str = "public_offline_inspection_no_aegis_decisions"
    # Modes:
    # - aegis_pdp: controlled Aegis PDP access with SPQR-issued trust material.
    # Public offline inspection must not simulate or replace Aegis PDP decisions.
    pdp_mode: str = "aegis_pdp"
    mesh_ingress_url: str = ""
    decision_path: str = "/v1/mesh/decision"
    tls_server_name: str | None = None
    host_header: str | None = None
    ca_cert_file: str | None = None
    client_cert_file: str | None = None
    client_key_file: str | None = None
    timeout_seconds: float = 180.0
    decision_max_attempts: int = 2
    decision_retry_backoff_seconds: float = 0.5
    output_dir: str = "outputs_island"
    mock_only_side_effects: bool = True
    route_label: str = "offline-inspection-no-aegis-pdp"
    trust_config_label: str = "not-configured"
    mesh_connection_id: str = "<provided-by-spqr>"
    mesh_binding_id: str = "<provided-by-spqr>"
    canonical_agent_ids_by_model: dict[str, str] = field(
        default_factory=lambda: dict(DEFAULT_CANONICAL_AGENT_IDS_BY_MODEL)
    )
    canonical_agent_id: str = "public_sandbox_stub_agent"
    org_name: str = "Public Aegis Paper Sandbox"
    policy_bundle_id: str = "public_policy_bundle_placeholder"
    baseline_release_id: str = "public_baseline_placeholder"
    baseline_fingerprint: str = "public_baseline_fingerprint_placeholder"

    @property
    def cert_configured(self) -> bool:
        return bool(self.ca_cert_file and self.client_cert_file and self.client_key_file)

    def public_fingerprint_payload(self) -> dict[str, Any]:
        # Config hashes are useful for reproducibility, but cert/key paths can
        # reveal deployment layout. Hash only whether trust was configured plus
        # stable public routing labels; never export key material or raw paths.
        payload = dict(self.__dict__)
        for field in SECRET_PATH_FIELDS:
            payload[field] = "<configured>" if payload.get(field) else None
        return payload


def load_config(path: str | Path | None = None) -> SandboxPepConfig:
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    payload: dict[str, Any] = {}
    if config_path.exists():
        loaded = load_yaml(str(config_path))
        payload = loaded if isinstance(loaded, dict) else {}
    allowed = set(SandboxPepConfig.__dataclass_fields__)
    return SandboxPepConfig(**{key: value for key, value in payload.items() if key in allowed})


def canonical_agent_id_for_model(config: SandboxPepConfig, model_name: str) -> str:
    model_agent_map = {
        str(key).strip(): str(value).strip()
        for key, value in dict(config.canonical_agent_ids_by_model or {}).items()
        if str(key).strip() and str(value).strip()
    }
    resolved = model_agent_map.get(str(model_name).strip()) or str(config.canonical_agent_id or "").strip()
    if not resolved:
        raise ValueError(f"no canonical sandbox agent configured for model {model_name}")
    return resolved
