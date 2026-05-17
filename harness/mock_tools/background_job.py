from __future__ import annotations

from .state import MockState


def apply_tool(state: MockState, tool_input: dict[str, object]) -> dict[str, object]:
    job_name = tool_input.get('job_name')
    if not job_name:
        raise ValueError('background_job_mock requires job_name')
    payload = {
        'job_name': job_name,
        'iteration_count': int(tool_input.get('iteration_count', 1)),
        'concurrency': int(tool_input.get('concurrency', 1)),
    }
    state.background_jobs.append(payload)
    result = {'status': 'applied', 'job_name': job_name}
    state.record_applied('background_job_mock', tool_input, result)
    return result
