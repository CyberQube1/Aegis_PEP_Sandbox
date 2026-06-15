# Latency Summary

| run_label | paper_model_label | task_set_label | condition | rows | model_avg_ms | model_median_ms | model_p95_ms | model_max_ms | total_avg_ms | total_median_ms | total_p95_ms | total_max_ms | aegis_avg_ms | aegis_median_ms | Aegis p95 ms | aegis_max_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontier_temp0 | frontier_model_a | 42-task full corpus | aegis_governed_mesh_agent | 42 | 2534.185 | 2439.202 | 3180.688 | 6297.1 | 2559.016 | 2466.247 | 3207.384 | 6324.804 | 27.606 | 26.135 | 29.926 | 68.337 |
| frontier_temp0 | frontier_model_a | 42-task full corpus | plain_mesh_agent | 42 | 2444.463 | 2327.186 | 3211.799 | 5378.769 | 2444.912 | 2327.657 | 3212.193 | 5379.254 | N/A | N/A | N/A | N/A |
| frontier_temp0 | frontier_model_a | 42-task full corpus | prompt_policy_mesh_agent | 42 | 2323.891 | 2256.498 | 3042.797 | 3371.514 | 2324.428 | 2256.994 | 3043.364 | 3371.961 | N/A | N/A | N/A | N/A |
| gemma | open_model_a | 42-task full corpus | aegis_governed_mesh_agent | 42 | 25476.534 | 26877.811 | 32165.042 | 35245.755 | 25508.646 | 26878.895 | 32196.634 | 35275.694 | 36.687 | 27.931 | 47.147 | 258.824 |
| gemma | open_model_a | 42-task full corpus | plain_mesh_agent | 42 | 18834.294 | 17512.077 | 25520.205 | 52923.857 | 18838.37 | 17513.01 | 25521.574 | 53029.948 | N/A | N/A | N/A | N/A |
| gemma | open_model_a | 42-task full corpus | prompt_policy_mesh_agent | 42 | 16796.665 | 16785.077 | 18649.11 | 26755.994 | 16798.022 | 16786.142 | 18650.243 | 26757.074 | N/A | N/A | N/A | N/A |
| stubbed | stub_model | 42-task full corpus | aegis_governed_mesh_agent | 42 | 0.003 | 0.003 | 0.004 | 0.004 | 24.962 | 23.844 | 27.609 | 69.424 | 24.723 | 23.613 | 27.299 | 69.226 |
| stubbed | stub_model | 42-task full corpus | plain_mesh_agent | 42 | 0.002 | 0.002 | 0.003 | 0.004 | 0.109 | 0.103 | 0.132 | 0.222 | N/A | N/A | N/A | N/A |
| stubbed | stub_model | 42-task full corpus | prompt_policy_mesh_agent | 42 | 0.002 | 0.002 | 0.002 | 0.002 | 0.129 | 0.127 | 0.146 | 0.169 | N/A | N/A | N/A | N/A |
