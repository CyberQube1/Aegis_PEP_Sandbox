from __future__ import annotations

from copy import deepcopy
from typing import Any

from harness.mock_tools import TOOL_REGISTRY
from harness.mock_tools.state import MockState


CANONICAL_TOOL_ALIASES = {
    "mock.email.send": "send_email_mock",
    "mock.file.read": "file_export_mock",
    "mock.file.export": "file_export_mock",
    "mock.shell.request": "shell_action_request_mock",
    "mock.vendor.approve": "vendor_approval_mock",
    "mock.workflow.approve": "workflow_approval_mock",
    "mock.escalation.create": "escalation_mock",
    "mock.background_job.create": "background_job_mock",
    "mock.memory.write": "memory_log_mock",
    "mock.agent_message.forward": "memory_log_mock",
}


FAIL_CLOSED_DECISIONS = {"block", "deny", "require_more_evidence", "infrastructure_failure", "error"}


class MockPEP:
    def __init__(self, state: MockState, allowed_mock_tools: list[str]) -> None:
        self.state = state
        self.allowed_mock_tools = set(allowed_mock_tools)

    def record_attempt(self, proposed_action: dict[str, Any]) -> dict[str, Any] | None:
        tool_name = proposed_action.get("tool_name")
        if not tool_name:
            return None
        tool_input = deepcopy(proposed_action.get("tool_input", {}))
        self.state.record_attempt(str(tool_name), tool_input)
        return {"tool_name": tool_name, "tool_input": tool_input}

    def apply(self, decision: dict[str, Any], proposed_action: dict[str, Any]) -> dict[str, Any] | None:
        if not self._authorized_to_apply(decision, proposed_action):
            return None
        tool_name = self._local_tool_name(str(decision.get("tool_name") or proposed_action.get("tool_name") or ""))
        if tool_name not in TOOL_REGISTRY:
            raise ValueError(f"unknown mock tool: {tool_name}")
        if tool_name not in self.allowed_mock_tools:
            raise ValueError(f"agent not allowed to call mock tool: {tool_name}")
        tool_input = deepcopy(decision.get("tool_input") or proposed_action.get("tool_input") or {})
        result = TOOL_REGISTRY[tool_name](self.state, tool_input)
        return {"tool_name": tool_name, "tool_input": tool_input, "result": result}

    def _authorized_to_apply(self, decision: dict[str, Any], proposed_action: dict[str, Any]) -> bool:
        # This is the PEP enforcement gate. It is deliberately stricter than a
        # convenience test harness: every ambiguous state becomes no-op so a
        # transport or schema failure cannot turn into a mock side effect.
        if not decision.get("apply_tool"):
            return False
        if str(decision.get("decision") or "").strip() in FAIL_CLOSED_DECISIONS:
            return False
        if decision.get("infrastructure_status") not in (None, "", "ok"):
            return False
        reason_codes = {str(code) for code in decision.get("reason_codes", [])}
        if "AEGIS_EXECUTION_WITHHELD" in reason_codes or "EXECUTION_WITHHELD_FAIL_CLOSED" in reason_codes:
            return False
        # A governed response must name the effect it is authorizing. Missing
        # tool identity is treated as malformed and therefore no-op/fail-closed.
        return bool(decision.get("tool_name") or proposed_action.get("tool_name"))

    @staticmethod
    def _local_tool_name(tool_name: str) -> str:
        return CANONICAL_TOOL_ALIASES.get(tool_name, tool_name)
