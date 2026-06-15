# Paper Claims And Limitations

## Supported Claims

### frontier_temp0

- The run ingested 126 rows across 42 unique tasks.
- Task set: 42-task full corpus (42 tasks; active-law-change tasks included: True).
- Conditions represented: aegis_governed_mesh_agent, plain_mesh_agent, prompt_policy_mesh_agent.
- Paper model labels represented: frontier_model_a.
- Parsed structured rows: 126 / 126.
- Infrastructure failures: 0.
- Model backend failures: 0.

### frontier_temp07

- The run ingested 126 rows across 42 unique tasks.
- Task set: 42-task full corpus (42 tasks; active-law-change tasks included: True).
- Conditions represented: aegis_governed_mesh_agent, plain_mesh_agent, prompt_policy_mesh_agent.
- Paper model labels represented: frontier_model_a.
- Parsed structured rows: 126 / 126.
- Infrastructure failures: 0.
- Model backend failures: 0.

### frontier_temp10

- The run ingested 126 rows across 42 unique tasks.
- Task set: 42-task full corpus (42 tasks; active-law-change tasks included: True).
- Conditions represented: aegis_governed_mesh_agent, plain_mesh_agent, prompt_policy_mesh_agent.
- Paper model labels represented: frontier_model_a.
- Parsed structured rows: 126 / 126.
- Infrastructure failures: 0.
- Model backend failures: 0.

### gemma

- The run ingested 126 rows across 42 unique tasks.
- Task set: 42-task full corpus (42 tasks; active-law-change tasks included: True).
- Conditions represented: aegis_governed_mesh_agent, plain_mesh_agent, prompt_policy_mesh_agent.
- Paper model labels represented: open_model_a.
- Parsed structured rows: 126 / 126.
- Infrastructure failures: 0.
- Model backend failures: 0.
- Gemma completed a local/open-model replication pass for the rows ingested here.
- This supports the statement that Gemma completed a 42-task x 3-condition full pass.
- Gemma produced parsed structured JSON for every ingested row.
- No model backend failures or infrastructure failures occurred in the Gemma rows ingested here.
- The governed Gemma path invoked Aegis on actionable side-effect proposals.
- No governed mock side effects were applied in the Gemma rows ingested here.
- Aegis decision latency was small relative to Gemma generation latency.

### stubbed

- The run ingested 126 rows across 42 unique tasks.
- Task set: 42-task full corpus (42 tasks; active-law-change tasks included: True).
- Conditions represented: aegis_governed_mesh_agent, plain_mesh_agent, prompt_policy_mesh_agent.
- Paper model labels represented: stub_model.
- Parsed structured rows: 0 / 126.
- Infrastructure failures: 0.
- Model backend failures: 0.

## Task-set comparability

- frontier_temp0 uses the 42-task full corpus (42 tasks; active-law-change tasks included: True).
- frontier_temp07 uses the 42-task full corpus (42 tasks; active-law-change tasks included: True).
- frontier_temp10 uses the 42-task full corpus (42 tasks; active-law-change tasks included: True).
- gemma uses the 42-task full corpus (42 tasks; active-law-change tasks included: True).
- stubbed uses the 42-task full corpus (42 tasks; active-law-change tasks included: True).
- Shared task IDs across the selected runs: 42.
- All selected runs use the same detected task-set scope, so full-row condition/model comparisons are task-set aligned.
- The shared-task reports should match the full task set for these selected runs.
- The strongest cross-model architecture claim is that each model/source shows zero governed risky side-effect completions under its evaluated task set.

## Safe headline claims

- Across the evaluated Stub, Frontier, and Gemma runs, Aegis-governed rows completed zero risky side effects.
- Prompt-policy reduced risky completions relative to plain mesh but did not eliminate them in all evaluated runs.
- The governed path produced complete evidence in the evaluated runs.
- Aegis PDP latency remained small relative to hosted/local model generation latency where model latency was measured.

## Claims not supported

- This does not prove legal compliance.
- This does not prove all models or prompts are safe.
- This does not prove production certification.
- This is not a model leaderboard.
- Gemma was not a repeated variance campaign.

## Limitations

- Missing fields are reported as N/A or blank numeric values; this exporter does not infer unsupported measurements.
- Gemma full-pass results are 1x unless repeated campaign directories are supplied.
- Local-model latency is hardware-sensitive and should not be generalized across machines.
- These summaries do not prove legal compliance.
- These summaries do not prove safety across all prompts, models, parser failures, or providers.
- Stub results are deterministic substrate validation, not evidence of model behavior.
- Frontier results must report fallback or heuristic rows separately from model-generated rows.
- Source-level rejection traces report the provenance fields available in task metadata, source manifests, and local Praxis chunk indexes. Missing excerpt text or exact mapping rationale is reported as N/A and does not imply the exporter verified legal applicability.
