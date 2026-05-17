from __future__ import annotations

from pathlib import Path
from typing import Any

from harness.utils.io import load_yaml

from .config import SANDBOX_ROOT


DEFAULT_TASK_FILES = (
    SANDBOX_ROOT / "tasks" / "email_external_comms.yaml",
    SANDBOX_ROOT / "tasks" / "vendor_service_provider.yaml",
    SANDBOX_ROOT / "tasks" / "ai_consumer_impact.yaml",
    SANDBOX_ROOT / "tasks" / "agentic_authority_tool_use.yaml",
    SANDBOX_ROOT / "tasks" / "active_law_change.yaml",
)


def load_tasks(task_files: list[str] | None = None) -> list[dict[str, Any]]:
    files = [Path(item) for item in task_files] if task_files else list(DEFAULT_TASK_FILES)
    tasks: list[dict[str, Any]] = []
    for path in files:
        payload = load_yaml(str(path))
        items = payload.get("tasks", []) if isinstance(payload, dict) else payload
        if not isinstance(items, list):
            raise ValueError(f"task file must contain a tasks list: {path}")
        tasks.extend(dict(item) for item in items if isinstance(item, dict))
    return tasks


def select_tasks(tasks: list[dict[str, Any]], task_ids: list[str] | None, max_tasks: int | None) -> list[dict[str, Any]]:
    if task_ids:
        wanted = set(task_ids)
        selected = [task for task in tasks if str(task.get("task_id")) in wanted]
    else:
        selected = sorted(tasks, key=lambda item: str(item.get("task_id")))
    if max_tasks is not None:
        selected = selected[: max(0, max_tasks)]
    return selected
