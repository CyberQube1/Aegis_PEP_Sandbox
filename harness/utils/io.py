from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, List

import yaml


def load_yaml(path: str | Path) -> Any:
    with Path(path).open('r', encoding='utf-8') as handle:
        return yaml.safe_load(handle)


def write_jsonl(path: str | Path, rows: Iterable[dict]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('w', encoding='utf-8') as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + '\n')


def read_jsonl(path: str | Path) -> List[dict]:
    rows: list[dict] = []
    with Path(path).open('r', encoding='utf-8') as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows
