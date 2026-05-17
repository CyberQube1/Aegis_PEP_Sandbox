# Aegis PDP Connection Contract

In controlled Aegis PDP mode, the sandbox PEP sends proposed action decision requests to Aegis. Aegis is the PDP. The released sandbox component is the PEP.

There is no public BYO PDP, mock PDP, or local Aegis decision-simulation path. If controlled Aegis access is not configured, governed mode fails closed.

Required values are provided out-of-band by SPQR:

```env
AEGIS_PDP_BASE_URL=<provided-by-spqr>
AEGIS_PDP_DECISION_PATH=/v1/mesh/decision
AEGIS_TENANT_ID=<provided-by-spqr>
AEGIS_ORG_ID=<provided-by-spqr>
AEGIS_MESH_CONNECTION_ID=<provided-by-spqr>
AEGIS_MESH_BINDING_ID=<provided-by-spqr>
AEGIS_CLIENT_CA_FILE=<local-private-path>
AEGIS_CLIENT_CERT_FILE=<local-private-path>
AEGIS_CLIENT_KEY_FILE=<local-private-path>
```

These values must never be committed to the repository.

For Docker runs, place the private YAML config outside the repository and mount it through `AEGIS_PRIVATE_CONFIG`. Place SPQR-issued trust material outside the repository and mount it through `AEGIS_PRIVATE_TRUST_DIR`. The container should see certificate paths under `/run/aegis-private/trust/`.

The request contains a task ID, model-proposed action, mock-only tool identity, required controls, workflow/failure-category metadata, mesh binding identifiers, and run correlation IDs. The response is normalized into the evidence record fields used by the paper reports: decision, allowed/apply-tool flags, reason codes, matched controls, provenance status, escalation fields when present, and practical execution outcome.

If any required endpoint, identity, or trust material is missing, the sandbox PEP fails closed and writes a non-execution evidence record. No real side effects are performed by this artifact.
