# Security Boundary

The public artifact intentionally excludes:

- Aegis kernel source code
- production trust infrastructure
- credentials, certificates, private keys, tokens, and secrets
- production endpoint details
- production mesh/trust IDs
- signing material
- production policy bundles
- local PDP simulators or Aegis decision substitutes
- Praxis backend internals
- EVA/ILK/Senate implementation internals
- non-public source documents

Any credential, certificate, key, endpoint, mesh ID, binding ID, connection ID, or organization identifier found in an internal sandbox checkout must be treated as non-public and removed from the public export. If a real credential was ever present in a working tree intended for export, rotate it before release.

Public configs use placeholders only. Controlled Aegis PDP validation requires SPQR-issued reviewer/research credentials and scoped mock-only trust material delivered out of band.

The public package must not include code that represents, simulates, or replaces Aegis PDP decisions.

The frozen proof-artifact folders under `reports/frozen_10_run_folder/` and `reports/frozen_one_run_folder/` may contain synthetic evidence identifiers used by the paper evaluation, including paper policy-bundle IDs, baseline-release IDs, decision IDs, trace IDs, escalation IDs, and Senate tally IDs. These are retained as part of the report chain. They are not credentials, keys, certificates, tokens, endpoints, production mesh IDs, or production trust material.
