# Latency Summary

| run_label | paper_model_label | task_set_label | condition | rows | model_avg_ms | model_median_ms | model_p95_ms | model_max_ms | total_avg_ms | total_median_ms | total_p95_ms | total_max_ms | aegis_avg_ms | aegis_median_ms | Aegis p95 ms | aegis_max_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontier | frontier_model_a | 36-task runtime set | aegis_governed_mesh_agent | 36 | 7847.614 | 6156.815 | 19007.786 | 31234.062 | 7867.471 | 6177.259 | 19008.104 | 31234.38 | 29.131 | 25.609 | 44.459 | 71.173 |
| frontier | frontier_model_a | 36-task runtime set | plain_mesh_agent | 36 | 5664.26 | 4779.336 | 11829.578 | 19496.023 | 5664.642 | 4779.818 | 11829.957 | 19496.329 | N/A | N/A | N/A | N/A |
| frontier | frontier_model_a | 36-task runtime set | prompt_policy_mesh_agent | 36 | 5703.56 | 5447.336 | 9453.615 | 10798.538 | 5704.047 | 5447.89 | 9454.126 | 10799.058 | N/A | N/A | N/A | N/A |
| gemma | open_model_a | 42-task full corpus | aegis_governed_mesh_agent | 42 | 404261.464 | 422844.265 | 510985.595 | 530924.444 | 404323.43 | 422907.801 | 511045.827 | 530987.56 | 72.575 | 64.326 | 94.605 | 273.506 |
| gemma | open_model_a | 42-task full corpus | plain_mesh_agent | 42 | 28666.242 | 27968.065 | 32903.663 | 46772.888 | 28668.572 | 27969.109 | 32904.863 | 46815.747 | N/A | N/A | N/A | N/A |
| gemma | open_model_a | 42-task full corpus | prompt_policy_mesh_agent | 42 | 25250.258 | 24947.494 | 27954.138 | 28945.595 | 25251.775 | 24949.587 | 27955.142 | 28949.654 | N/A | N/A | N/A | N/A |
| stub | stub_model | 36-task runtime set | aegis_governed_mesh_agent | 36 | 0.003 | 0.003 | 0.004 | 0.005 | 24.985 | 24.666 | 29.523 | 32.803 | 24.73 | 24.404 | 29.312 | 32.534 |
| stub | stub_model | 36-task runtime set | plain_mesh_agent | 36 | 0.002 | 0.002 | 0.003 | 0.003 | 0.149 | 0.144 | 0.194 | 0.245 | N/A | N/A | N/A | N/A |
| stub | stub_model | 36-task runtime set | prompt_policy_mesh_agent | 36 | 0.002 | 0.002 | 0.002 | 0.003 | 0.148 | 0.146 | 0.182 | 0.238 | N/A | N/A | N/A | N/A |
