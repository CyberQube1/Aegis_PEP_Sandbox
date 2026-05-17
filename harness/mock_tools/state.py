from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MockState:
    emails: list[dict[str, Any]] = field(default_factory=list)
    file_exports: list[dict[str, Any]] = field(default_factory=list)
    shell_requests: list[dict[str, Any]] = field(default_factory=list)
    vendor_approvals: list[dict[str, Any]] = field(default_factory=list)
    workflow_approvals: list[dict[str, Any]] = field(default_factory=list)
    escalations: list[dict[str, Any]] = field(default_factory=list)
    background_jobs: list[dict[str, Any]] = field(default_factory=list)
    memory_logs: list[dict[str, Any]] = field(default_factory=list)
    attempted_calls: list[dict[str, Any]] = field(default_factory=list)
    applied_calls: list[dict[str, Any]] = field(default_factory=list)
    custom: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_task(cls, task: dict[str, Any]) -> 'MockState':
        initial = task.get('initial_mock_state', {})
        state = cls()
        for field_name in (
            'emails',
            'file_exports',
            'shell_requests',
            'vendor_approvals',
            'workflow_approvals',
            'escalations',
            'background_jobs',
            'memory_logs',
        ):
            if field_name in initial:
                setattr(state, field_name, deepcopy(initial[field_name]))
        state.custom = deepcopy(initial.get('custom', {}))
        return state

    def record_attempt(self, tool_name: str, tool_input: dict[str, Any]) -> None:
        self.attempted_calls.append({'tool_name': tool_name, 'tool_input': deepcopy(tool_input)})

    def record_applied(self, tool_name: str, tool_input: dict[str, Any], result: dict[str, Any]) -> None:
        self.applied_calls.append(
            {
                'tool_name': tool_name,
                'tool_input': deepcopy(tool_input),
                'result': deepcopy(result),
            }
        )

    def snapshot(self) -> dict[str, Any]:
        return {
            'emails': deepcopy(self.emails),
            'file_exports': deepcopy(self.file_exports),
            'shell_requests': deepcopy(self.shell_requests),
            'vendor_approvals': deepcopy(self.vendor_approvals),
            'workflow_approvals': deepcopy(self.workflow_approvals),
            'escalations': deepcopy(self.escalations),
            'background_jobs': deepcopy(self.background_jobs),
            'memory_logs': deepcopy(self.memory_logs),
            'attempted_calls': deepcopy(self.attempted_calls),
            'applied_calls': deepcopy(self.applied_calls),
            'custom': deepcopy(self.custom),
        }
