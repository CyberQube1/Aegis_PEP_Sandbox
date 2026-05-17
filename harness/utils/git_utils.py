from __future__ import annotations

import subprocess
from pathlib import Path


def current_git_commit(repo_root: str | Path) -> str:
    try:
        result = subprocess.run(
            ['git', '-C', str(repo_root), 'rev-parse', 'HEAD'],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return 'unknown'
    return result.stdout.strip() or 'unknown'
