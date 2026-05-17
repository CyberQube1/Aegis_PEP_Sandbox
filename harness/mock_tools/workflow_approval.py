from __future__ import annotations

from .state import MockState


def apply_tool(state: MockState, tool_input: dict[str, object]) -> dict[str, object]:
    workflow_id = tool_input.get('workflow_id')
    if not workflow_id:
        raise ValueError('workflow_approval_mock requires workflow_id')
    payload = {
        'workflow_id': workflow_id,
        'approval_decision': tool_input.get('approval_decision', 'pending'),
        'note': tool_input.get('note', ''),
    }
    state.workflow_approvals.append(payload)
    result = {'status': 'applied', 'workflow_id': workflow_id}
    state.record_applied('workflow_approval_mock', tool_input, result)
    return result
