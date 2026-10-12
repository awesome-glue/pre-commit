"""Shared CLI utilities for pre-commit hooks."""

import argparse
from collections.abc import Sequence
from pathlib import Path


def parse_files(argv: Sequence[str] | None) -> list[Path]:
    """Parse command-line arguments and return existing file paths.

    Args:
        argv: Command-line arguments, or None to read sys.argv.

    Returns:
        List of existing file paths.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        type=Path,
        help="Files to process.",
    )
    args = parser.parse_args(argv)
    return [p for p in args.filenames if p.is_file()]
