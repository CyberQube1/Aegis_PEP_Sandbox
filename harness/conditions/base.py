from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ConditionAdapter(ABC):
    name = 'base_condition'

    @abstractmethod
    def decide(
        self,
        task: dict[str, Any],
        agent_profile: dict[str, Any],
        proposed_action: dict[str, Any],
        policy_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        raise NotImplementedError
