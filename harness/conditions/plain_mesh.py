from __future__ import annotations

from typing import Any

from .base import ConditionAdapter


class PlainMeshCondition(ConditionAdapter):
    name = 'plain_mesh_agent'

    def decide(
        self,
        task: dict[str, Any],
        agent_profile: dict[str, Any],
        proposed_action: dict[str, Any],
        policy_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        tool_name = proposed_action.get('tool_name')
        return {
            'condition': self.name,
            'decision': 'allow',
            'allowed': True,
            'apply_tool': bool(tool_name),
            'tool_name': tool_name,
            'tool_input': proposed_action.get('tool_input', {}),
            'reason': 'Plain mesh condition does not enforce active governance controls.',
            'active_governance_bundle_id': None,
            'evidence_refs': [],
            'ilk_refs': [],
            'fail_closed': False,
        }
