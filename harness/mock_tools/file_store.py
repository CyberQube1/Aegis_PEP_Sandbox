from __future__ import annotations

from .state import MockState


def apply_tool(state: MockState, tool_input: dict[str, object]) -> dict[str, object]:
    export_path = tool_input.get('path')
    if not export_path:
        raise ValueError('file_export_mock requires path')
    payload = {
        'path': export_path,
        'content_label': tool_input.get('content_label', 'artifact'),
        'classification': tool_input.get('classification', 'internal'),
    }
    state.file_exports.append(payload)
    result = {'status': 'applied', 'path': export_path}
    state.record_applied('file_export_mock', tool_input, result)
    return result
