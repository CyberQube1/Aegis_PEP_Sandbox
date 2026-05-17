# Output Schema

Matrix outputs are written as JSONL and CSV evidence rows. Important fields include:

- `run_id`
- `task_id`
- `condition`
- `model_backend`
- `agent_id`
- `organization_id`
- `policy_bundle_id`
- `workflow_family`
- `failure_category`
- `expected_outcome`
- `proposed_action`
- `aegis_decision`
- `final_decision`
- `mock_tool_attempted`
- `mock_tool_applied`
- `score`
- `aegis_decision_attempted`
- `infrastructure_status`
- `mesh_route_label`
- `trust_config_label`

For controlled Aegis PDP mode, the sandbox PEP records PDP decision metadata and practical execution outcome separately. Senate settlement, authorization state, and mock-tool application are distinct concepts.

If controlled Aegis PDP configuration is missing, governed rows fail closed with `infrastructure_status` set to `controlled_aegis_pdp_config_missing`. This is a local non-execution boundary check, not a simulated Aegis decision.
