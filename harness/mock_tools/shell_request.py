from __future__ import annotations

from .state import MockState


def apply_tool(state: MockState, tool_input: dict[str, object]) -> dict[str, object]:
    command = tool_input.get('command')
    if not command:
        raise ValueError('shell_action_request_mock requires command')
    payload = {
        'command': command,
        'justification': tool_input.get('justification', ''),
        'risk_level': tool_input.get('risk_level', 'unknown'),
        # This mock intentionally never executes the requested command.
        'executed': False,
    }
    state.shell_requests.append(payload)
    result = {'status': 'recorded_only', 'executed': False}
    state.record_applied('shell_action_request_mock', tool_input, result)
    return result
