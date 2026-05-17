from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


FORBIDDEN = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "tailscale_hostname": re.compile(r"tail[0-9a-f]{6,}\.ts\.net"),
    "internal_home_path": re.compile(r"/home/spqr-admin/"),
    "mesh_connection_id": re.compile(r"\bsmc_[A-Za-z0-9]+\b"),
    "mesh_binding_id": re.compile(r"\bmb_[A-Za-z0-9]+\b"),
    "policy_bundle_id": re.compile(r"\bpb_[0-9a-fA-F]{8,}\b"),
    "baseline_release_id": re.compile(r"\bbr_[0-9a-fA-F]{8,}\b"),
    "paper_org_email": re.compile(r"aegis@paper\.com"),
    "real_frontier_key_assignment": re.compile(r"AEGIS_SANDBOX_FRONTIER_A_API_KEY\s*=\s*[A-Za-z0-9_\-]{12,}"),
}


FROZEN_PROOF_ARTIFACT_ID_MARKERS = {
    "mesh_connection_id",
    "mesh_binding_id",
    "policy_bundle_id",
    "baseline_release_id",
}


def is_frozen_proof_artifact(path: Path) -> bool:
    rel_parts = path.relative_to(ROOT).parts
    return len(rel_parts) >= 2 and rel_parts[0] == "reports" and rel_parts[1] in {
        "frozen_10_run_folder",
        "frozen_one_run_folder",
    }


def iter_text_files():
    for path in ROOT.rglob("*"):
        if path.is_dir() or ".git" in path.parts:
            continue
        if path == Path(__file__).resolve():
            continue
        if path.suffix in {".pyc", ".pdf", ".png", ".jpg", ".jpeg"}:
            continue
        yield path


def test_public_artifact_has_no_known_private_markers():
    findings: list[str] = []
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in FORBIDDEN.items():
            if label in FROZEN_PROOF_ARTIFACT_ID_MARKERS and is_frozen_proof_artifact(path):
                continue
            if pattern.search(text):
                findings.append(f"{label}: {path.relative_to(ROOT)}")
    assert not findings, "\n".join(findings)
