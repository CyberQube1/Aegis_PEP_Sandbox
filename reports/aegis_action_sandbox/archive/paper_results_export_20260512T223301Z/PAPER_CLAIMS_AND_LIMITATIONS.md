# Paper Claims And Limitations

## Supported Claims

### frontier

- The run ingested 108 rows across 36 unique tasks.
- Conditions represented: aegis_governed_mesh_agent, plain_mesh_agent, prompt_policy_mesh_agent.
- Paper model labels represented: frontier_model_a.
- Parsed structured rows: 102 / 108.
- Infrastructure failures: 0.
- Model backend failures: 0.

### gemma

- The run ingested 126 rows across 42 unique tasks.
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
- Conditions represented: aegis_governed_mesh_agent, plain_mesh_agent, prompt_policy_mesh_agent.
- Paper model labels represented: stub_model.
- Parsed structured rows: 0 / 108.
- Infrastructure failures: 0.
- Model backend failures: 0.

## Limitations

- Missing fields are reported as N/A or blank numeric values; this exporter does not infer unsupported measurements.
- Gemma full-pass results are 1x unless repeated campaign directories are supplied.
- Local-model latency is hardware-sensitive and should not be generalized across machines.
- These summaries do not prove legal compliance.
- These summaries do not prove safety across all prompts, models, parser failures, or providers.
- Stub results are deterministic substrate validation, not evidence of model behavior.
- Frontier results must report fallback or heuristic rows separately from model-generated rows.
