from __future__ import annotations

from .state import MockState


def apply_tool(state: MockState, tool_input: dict[str, object]) -> dict[str, object]:
    vendor_id = tool_input.get('vendor_id')
    if not vendor_id:
        raise ValueError('vendor_approval_mock requires vendor_id')
    payload = {
        'vendor_id': vendor_id,
        'requested_by': tool_input.get('requested_by', 'unknown'),
        'approval_decision': tool_input.get('approval_decision', 'pending'),
        'note': tool_input.get('note', ''),
    }
    state.vendor_approvals.append(payload)
    result = {'status': 'applied', 'approval_decision': payload['approval_decision']}
    state.record_applied('vendor_approval_mock', tool_input, result)
    return result
