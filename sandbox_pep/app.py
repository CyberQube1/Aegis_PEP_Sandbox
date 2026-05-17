from __future__ import annotations

from .run_matrix import main


def cli() -> int:
    """CLI entrypoint for the isolated sandbox PEP/PAP service."""
    return main()


if __name__ == "__main__":
    raise SystemExit(cli())
