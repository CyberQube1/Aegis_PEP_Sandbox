from __future__ import annotations

from .state import MockState


def apply_tool(state: MockState, tool_input: dict[str, object]) -> dict[str, object]:
    payload = {
        'entry_type': tool_input.get('entry_type', 'note'),
        'content': tool_input.get('content', ''),
    }
    state.memory_logs.append(payload)
    result = {'status': 'applied', 'entry_type': payload['entry_type']}
    state.record_applied('memory_log_mock', tool_input, result)
    return result
