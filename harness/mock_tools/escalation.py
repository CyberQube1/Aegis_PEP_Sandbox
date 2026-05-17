from __future__ import annotations

from .state import MockState


def apply_tool(state: MockState, tool_input: dict[str, object]) -> dict[str, object]:
    target = tool_input.get('target_queue', 'compliance-review')
    payload = {
        'target_queue': target,
        'reason': tool_input.get('reason', ''),
        'original_tool_name': tool_input.get('original_tool_name'),
    }
    state.escalations.append(payload)
    result = {'status': 'applied', 'target_queue': target}
    state.record_applied('escalation_mock', tool_input, result)
    return result
