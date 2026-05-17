# Reproducibility Notes

The public package supports three reproducibility layers:

1. Inspect frozen sanitized 10-run and single-run proof artifacts in `reports/frozen_10_run_folder/` and `reports/frozen_one_run_folder/`, or inspect the curated summaries in `reports/10_run/` and `reports/single_run/`.
2. Run offline sandbox mechanics for the plain and prompt-policy paths with a deterministic model.
3. Run controlled Aegis PDP validation only with SPQR-issued reviewer/research credentials and scoped mock-only trust material.

Offline public execution does not run, reproduce, or simulate Aegis PDP decisions. Governed validation requires connecting the sandbox PEP to real Aegis as the PDP.

The public package includes the sandbox PEP, synthetic task corpus, mock tools, prompt-policy comparator, scoring logic, report builders, output schemas, frozen sanitized result artifacts, and documentation required to inspect the reported tables.

The public package excludes the Aegis kernel, production trust infrastructure, private credentials, production policy bundles, signing material, live endpoint details, and non-public source documents.
