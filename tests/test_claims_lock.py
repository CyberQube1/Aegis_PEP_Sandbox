from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


EXPECTED = {
    "Total repeated-evaluation rows": "6,300",
    "Governed rows": "2,100",
    "Prompt-policy leakage rows": "79",
    "Governed mock-tool applications": "0",
    "Governed risky side-effect completions": "0",
    "Aegis-attempted governed rows": "1,832",
    "Local fail-closed/no-tool governed rows": "268",
    "Trusted Aegis-resolved provenance-valid rows": "1,832",
    "Senate joined settlement rows": "1,019",
    "Senate-settled allow rows": "60",
    "Senate-settled deny rows": "959",
}


def test_claims_lock_contains_headline_values():
    text = (ROOT / "CLAIMS_LOCK.md").read_text(encoding="utf-8")
    missing = [f"{label} -> {value}" for label, value in EXPECTED.items() if label not in text or value not in text]
    assert not missing, "\n".join(missing)
