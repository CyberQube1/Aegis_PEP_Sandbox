# Claim Boundary

The frozen sanitized result artifacts support the manuscript claims. The fuller frozen proof-artifact folders are staged in `reports/frozen_10_run_folder/` and `reports/frozen_one_run_folder/`; curated manuscript/table summaries are staged in `reports/10_run/` and `reports/single_run/`. Offline public runs are for sandbox mechanics, schema inspection, parser/scoring validation, report-builder checks, and table inspection.

Offline mode does not reproduce or simulate live Aegis PDP decisions.

The public package does not include a local PDP, mock PDP, BYO PDP path, or Aegis decision simulator.

Live governed validation requires controlled Aegis PDP access with SPQR-issued reviewer/research credentials and scoped mock-only trust material. The public artifact does not prove the empirical claims by reimplementing Aegis. It provides the PEP, corpus, mock tools, scoring/reporting machinery, schemas, and frozen result artifacts needed to inspect the claim chain.

All evaluated side effects are mock-tool effects. No real-world email, file export, workflow mutation, shell action, or operational API action is executed.
