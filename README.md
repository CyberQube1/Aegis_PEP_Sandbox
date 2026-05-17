# Aegis Paper Sandbox PEP

This repository contains the public sandbox Policy Enforcement Point (PEP), mock tools, synthetic task corpus, scoring/report builders, schemas, and frozen sanitized evaluation artifacts used to support the Aegis paper.

This repository does **not** contain the Aegis kernel, a local Aegis PDP substitute, or production trust infrastructure.

## Execution modes

### 1. Offline inspection mode

Public. Runs local sandbox mechanics for the plain mesh and prompt-policy comparator paths, inspects schemas, regenerates tables from frozen artifacts, and validates parser/scoring/report-builder behavior.

Offline inspection mode does **not** run, reproduce, or simulate Aegis PDP decisions. If the Aegis-governed condition is requested without controlled Aegis endpoint and trust configuration, the sandbox PEP fails closed and writes a non-execution evidence record.

### 2. Controlled Aegis PDP mode

Restricted. Connects the sandbox PEP to Aegis as the Policy Decision Point (PDP). This mode requires SPQR-issued reviewer/research credentials, endpoint details, and scoped mock-only trust material. No production credentials, production mesh IDs, signing material, private keys, or live policy infrastructure are included in this public repository.

The sandbox PEP fails closed unless a valid Aegis endpoint and trust configuration are explicitly provided.

## Quick start

Offline inspection smoke test:

```bash
PYTHONPATH=. python -m sandbox_pep.run_matrix \
  --config config/sandbox_pep.offline.yaml \
  --condition plain_mesh_agent \
  --condition prompt_policy_mesh_agent \
  --model stub_model \
  --max-tasks 3 \
  --output-dir outputs/offline_inspection
```

Fail-closed check for missing controlled Aegis PDP config:

```bash
PYTHONPATH=. python -m sandbox_pep.run_matrix \
  --config config/sandbox_pep.offline.yaml \
  --condition aegis_governed_mesh_agent \
  --model stub_model \
  --max-tasks 1 \
  --output-dir outputs/aegis_missing_config_fail_closed
```

Controlled Aegis PDP validation requires a private config derived from `config/sandbox_pep.aegis-access-template.yaml` and SPQR-provided endpoint, identity, and trust material.

## Docker

Offline inspection:

```bash
cd docker
docker compose -f docker-compose.sandbox-pep.public.yml up --build
```

Controlled Aegis PDP validation:

```bash
cp config/sandbox_pep.aegis-access-template.yaml /private/path/sandbox_pep.aegis-access.yaml
# Fill /private/path/sandbox_pep.aegis-access.yaml with SPQR-provided values.
# Point cert/key fields at files mounted under /run/aegis-private/trust/.

export AEGIS_PRIVATE_CONFIG=/private/path/sandbox_pep.aegis-access.yaml
export AEGIS_PRIVATE_TRUST_DIR=/private/path/aegis-trust

cd docker
docker compose -f docker-compose.sandbox-pep.aegis-template.yml up --build
```

Do not commit the private config or trust directory. The controlled-access compose file only mounts caller-supplied private material; it does not contain endpoint values, credentials, keys, certificates, mesh IDs, binding IDs, or a local PDP.

## Package map

- `sandbox_pep/`: public sandbox PEP runner, Aegis PDP client boundary, task loader, scorer, and evidence writer.
- `harness/`: public mock tools, deterministic model fixture, prompt-policy comparator, scoring/report support.
- `tasks/`: synthetic paper task corpus.
- `controls/`: synthetic/public policy-control taxonomy inputs used by the sandbox.
- `reports/`: sanitized frozen proof artifacts, full 10-run and single-run report packs, normalized report summaries, and table inputs.
- `docs/`: security boundary, claim boundary, PDP connection contract, output schema, runbook, and reproducibility notes.
- `config/`: public-safe templates only.
- `docker/`: public container build/compose files.
- `tests/`: public smoke, fail-closed, claims-lock, and sanitization checks.

## Non-release materials

The public artifact intentionally excludes the Aegis kernel, production trust infrastructure, local PDP simulators, credentials, certificates, private keys, tokens, production endpoint details, production mesh/trust IDs, signing material, Praxis backend internals, EVA/ILK/Senate implementation internals, and non-public source documents.
