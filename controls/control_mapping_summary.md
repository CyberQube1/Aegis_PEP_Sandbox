# Control Mapping Summary

## Control packs created
- `controls/internal_enterprise/controls.yaml`
- `controls/apra_asic_au_finance/controls.yaml`
- `controls/agentic_failure_taxonomy/controls.yaml`

## Mapping approach
- Internal controls are anchored to the four uploaded paper-org policies on `aegis-paper-1`.
- AU finance controls are anchored to the live `Australia Banking & Finance Core` pack and current promoted release `public_mock_baseline_release` / `753c5b01dd25`.
- Agentic failure taxonomy controls are research-inspired stress labels cross-mapped back to the internal and AU finance sources they pressure.

## First-run scope
Prompt C first-run scope is:
- `Australia Banking & Finance Core`
- plus the four uploaded paper-org internal policies

Explicitly excluded from the first run:
- EU AI Act
- ISO/IEC 42001
- Civitas-specific behavior claims

## Claim boundary
All control packs are:
- regulator-inspired
- source-mapped
- sandbox-local

They are not:
- legal compliance claims
- regulator approvals
- benchmark replication claims
