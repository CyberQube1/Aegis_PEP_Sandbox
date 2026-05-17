# Runbook

## Offline inspection mode

```bash
PYTHONPATH=. python -m sandbox_pep.run_matrix \
  --config config/sandbox_pep.offline.yaml \
  --condition plain_mesh_agent \
  --condition prompt_policy_mesh_agent \
  --model stub_model \
  --max-tasks 3 \
  --output-dir outputs/offline_inspection
```

This validates local task loading, mock tools, prompt-policy comparator behavior, scoring, evidence output shape, and report/table mechanics. It does not run or simulate Aegis PDP decisions.

## Missing Aegis configuration fail-closed check

```bash
PYTHONPATH=. python -m sandbox_pep.run_matrix \
  --config config/sandbox_pep.offline.yaml \
  --condition aegis_governed_mesh_agent \
  --model stub_model \
  --max-tasks 1 \
  --output-dir outputs/aegis_missing_config_fail_closed
```

This verifies the public sandbox PEP boundary: governed mode requires real Aegis PDP access and fails closed when endpoint, identity, or trust material is missing. It is not a governed validation run.

## Controlled Aegis PDP mode

Copy `config/sandbox_pep.aegis-access-template.yaml` to a private local path and fill only SPQR-provided values. Do not commit the private config.

```bash
PYTHONPATH=. python -m sandbox_pep.run_matrix \
  --config /private/path/sandbox_pep.aegis-access.yaml \
  --condition aegis_governed_mesh_agent \
  --model stub_model \
  --max-tasks 3 \
  --output-dir outputs/controlled_aegis_pdp_validation
```

The sandbox PEP fails closed if endpoint, identity, or mTLS trust material is missing.

## Docker controlled-access run

Prepare a private config and trust directory outside the repository:

```bash
cp config/sandbox_pep.aegis-access-template.yaml /private/path/sandbox_pep.aegis-access.yaml
```

Fill `/private/path/sandbox_pep.aegis-access.yaml` with SPQR-provided values. Certificate fields should point to paths inside the container mount, for example:

```yaml
ca_cert_file: /run/aegis-private/trust/ca.pem
client_cert_file: /run/aegis-private/trust/client.pem
client_key_file: /run/aegis-private/trust/client-key.pem
```

Run the controlled-access compose template:

```bash
export AEGIS_PRIVATE_CONFIG=/private/path/sandbox_pep.aegis-access.yaml
export AEGIS_PRIVATE_TRUST_DIR=/private/path/aegis-trust
cd docker
docker compose -f docker-compose.sandbox-pep.aegis-template.yml up --build
```

The compose template mounts private material read-only and sends governed requests to Aegis as the PDP. It does not start a local PDP.
