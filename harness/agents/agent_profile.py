from __future__ import annotations

from dataclasses import dataclass
from typing import Any

REQUIRED_PROFILE_FIELDS = (
    'agent_id',
    'display_name',
    'organization_id',
    'role',
    'authority_level',
    'allowed_mock_tools',
    'model_backend',
    'policy_context_mode',
    'evidence_mode',
)


@dataclass(frozen=True)
class AgentProfile:
    agent_id: str
    display_name: str
    organization_id: str
    role: str
    authority_level: str
    allowed_mock_tools: list[str]
    model_backend: str
    policy_context_mode: str
    evidence_mode: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> 'AgentProfile':
        missing = [field for field in REQUIRED_PROFILE_FIELDS if field not in payload]
        if missing:
            raise ValueError(f'missing agent profile fields: {missing}')
        return cls(
            agent_id=payload['agent_id'],
            display_name=payload['display_name'],
            organization_id=payload['organization_id'],
            role=payload['role'],
            authority_level=payload['authority_level'],
            allowed_mock_tools=list(payload['allowed_mock_tools']),
            model_backend=payload['model_backend'],
            policy_context_mode=payload['policy_context_mode'],
            evidence_mode=payload['evidence_mode'],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'agent_id': self.agent_id,
            'display_name': self.display_name,
            'organization_id': self.organization_id,
            'role': self.role,
            'authority_level': self.authority_level,
            'allowed_mock_tools': list(self.allowed_mock_tools),
            'model_backend': self.model_backend,
            'policy_context_mode': self.policy_context_mode,
            'evidence_mode': self.evidence_mode,
        }
