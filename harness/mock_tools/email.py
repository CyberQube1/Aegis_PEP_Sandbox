from __future__ import annotations

from copy import deepcopy

from .state import MockState


def apply_tool(state: MockState, tool_input: dict[str, object]) -> dict[str, object]:
    recipients = list(tool_input.get('to') or [])
    if not recipients:
        raise ValueError('send_email_mock requires at least one recipient')
    payload = {
        'to': recipients,
        'subject': tool_input.get('subject', ''),
        'body': tool_input.get('body', ''),
        'classification': tool_input.get('classification', 'internal'),
        'attachments': deepcopy(tool_input.get('attachments', [])),
    }
    state.emails.append(payload)
    result = {'status': 'applied', 'recipient_count': len(recipients)}
    state.record_applied('send_email_mock', tool_input, result)
    return result
