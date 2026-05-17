# Access Request Process

Controlled Aegis PDP validation is available to reviewers or researchers by request.

Process:

1. Contact SPQR using the public contact channel named in the manuscript.
2. SPQR issues a scoped reviewer/research account, endpoint details, and mock-only trust material out of band where appropriate.
3. The reviewer copies `config/sandbox_pep.aegis-access-template.yaml` to a private local config and fills only the provided values.
4. The reviewer runs the sandbox PEP directly or through `docker/docker-compose.sandbox-pep.aegis-template.yml`.
5. The sandbox PEP connects to Aegis as the PDP and runs mock-only tasks.
6. Access may be revoked by SPQR.

No production data, production credentials, production mesh IDs, signing material, or real side effects are included in this public artifact. Controlled mode fails closed if configuration is incomplete.
