# Paper Claims And Limitations

## Supported Claims

### frontier

- The run ingested 108 rows across 36 unique tasks.
- Task set: 36-task runtime set (36 tasks; active-law-change tasks included: False).
- Conditions represented: aegis_governed_mesh_agent, plain_mesh_agent, prompt_policy_mesh_agent.
- Paper model labels represented: frontier_model_a.
- Parsed structured rows: 102 / 108.
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

### stub

- The run ingested 108 rows across 36 unique tasks.
- Task set: 36-task runtime set (36 tasks; active-law-change tasks included: False).
- Conditions represented: aegis_governed_mesh_agent, plain_mesh_agent, prompt_policy_mesh_agent.
- Paper model labels represented: stub_model.
- Parsed structured rows: 0 / 108.
- Infrastructure failures: 0.
- Model backend failures: 0.

## Task-set comparability

- Stub and Frontier currently use the 36-task runtime set.
- Gemma currently uses the 42-task full corpus.
- Cross-model comparisons should be interpreted carefully unless restricted to shared task IDs.
- The strongest cross-model architecture claim is that each model/source shows zero governed risky side-effect completions under its evaluated task set.
- Strict model-to-model rate comparison should use the shared-task reports.

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
