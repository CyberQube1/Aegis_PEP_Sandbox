# Parser And Fallback Summary

| run_label | paper_model_label | condition | parser_status | rows | model_generated_action_rows | fallback_or_heuristic_rows | model_backend_failures |
| --- | --- | --- | --- | --- | --- | --- | --- |
| frontier | frontier_model_a | aegis_governed_mesh_agent | heuristic_parse | 3 | 0 | 3 | 0 |
| frontier | frontier_model_a | aegis_governed_mesh_agent | parsed_json | 33 | 33 | 0 | 0 |
| frontier | frontier_model_a | plain_mesh_agent | heuristic_parse | 2 | 0 | 2 | 0 |
| frontier | frontier_model_a | plain_mesh_agent | parsed_json | 34 | 34 | 0 | 0 |
| frontier | frontier_model_a | prompt_policy_mesh_agent | heuristic_parse | 1 | 0 | 1 | 0 |
| frontier | frontier_model_a | prompt_policy_mesh_agent | parsed_json | 35 | 35 | 0 | 0 |
| gemma | open_model_a | aegis_governed_mesh_agent | parsed_json | 42 | 42 | 0 | 0 |
| gemma | open_model_a | plain_mesh_agent | parsed_json | 42 | 42 | 0 | 0 |
| gemma | open_model_a | prompt_policy_mesh_agent | parsed_json | 42 | 42 | 0 | 0 |
| stub | stub_model | aegis_governed_mesh_agent | stub_structured | 36 | 0 | 0 | 0 |
| stub | stub_model | plain_mesh_agent | stub_structured | 36 | 0 | 0 | 0 |
| stub | stub_model | prompt_policy_mesh_agent | stub_structured | 36 | 0 | 0 | 0 |
