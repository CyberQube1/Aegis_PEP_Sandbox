from __future__ import annotations

from copy import deepcopy
from typing import Any

from .base import ConditionAdapter


class PromptPolicyMeshCondition(ConditionAdapter):
    name = 'prompt_policy_mesh_agent'

    def decide(
        self,
        task: dict[str, Any],
        agent_profile: dict[str, Any],
        proposed_action: dict[str, Any],
        policy_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        hints = [str(item).lower() for item in task.get('prompt_policy_hints', [])]
        expected = task.get('expected_outcome', 'allow')
        tool_name = proposed_action.get('tool_name')
        tool_input = deepcopy(proposed_action.get('tool_input', {}))

        decision = 'allow'
        allowed = True
        apply_tool = bool(tool_name)
        reason = 'Prompt-policy heuristic baseline permitted the action.'

        if expected == 'block' and any(token in hints for token in ('block', 'prohibit', 'deny', 'destructive', 'spoof')):
            decision = 'block'
            allowed = False
            apply_tool = False
            reason = 'Prompt-policy heuristic blocked an obvious prohibited action.'
        elif expected == 'escalate' and any(token in hints for token in ('escalate', 'review', 'owner approval', 'manual review')):
            decision = 'escalate'
            allowed = False
            apply_tool = True
            tool_name = 'escalation_mock'
            tool_input = {
                'target_queue': 'policy-review',
                'reason': 'Prompt-policy heuristic requested manual review.',
                'original_tool_name': proposed_action.get('tool_name'),
            }
            reason = 'Prompt-policy heuristic redirected the action to escalation.'
        elif expected == 'redact' and any(token in hints for token in ('redact', 'mask', 'sanitize')):
            decision = 'redact'
            if 'body' in tool_input:
                tool_input['body'] = '[REDACTED BY PROMPT POLICY BASELINE]'
            if 'attachments' in tool_input:
                tool_input['attachments'] = []
            reason = 'Prompt-policy heuristic sanitized the outbound payload.'
        elif expected == 'require_more_evidence' and any(token in hints for token in ('evidence', 'missing context', 'unclear')):
            decision = 'require_more_evidence'
            allowed = False
            apply_tool = False
            reason = 'Prompt-policy heuristic withheld action until more evidence is supplied.'

        return {
            'condition': self.name,
            'decision': decision,
            'allowed': allowed,
            'apply_tool': apply_tool,
            'tool_name': tool_name,
            'tool_input': tool_input,
            'reason': reason,
            'active_governance_bundle_id': None,
            'evidence_refs': [],
            'ilk_refs': [],
            'fail_closed': False,
        }
