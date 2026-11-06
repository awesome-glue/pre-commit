"""Shared utilities for pre-commit hooks."""

import sys
import tomllib
from collections.abc import Callable, Iterable, Iterator, Sequence
from functools import wraps
from pathlib import Path


def find_gtk_project_files(files: Iterable[str]) -> Iterator[Path]:
    """Filter and yield Path objects for valid AWS Glue Toolkit projects.

    Args:
        files: Sequence or iterable of file path strings.

    Yields:
        Path objects for valid GTK pyproject.toml files.

    Note:
        Non-existent files and malformed TOML files are ignored without error.
        It is recommended to pair this with a dedicated TOML syntax validator
        (such as 'check-toml') to detect syntax errors.

    """
    for file_path in files:
        path = Path(file_path)
        try:
            toml_data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (tomllib.TOMLDecodeError, OSError):
            continue

        tool = toml_data.get("tool")
        if isinstance(tool, dict) and "aws-glue-toolkit" in tool:
            yield path


def split_flags_and_files(
    argv: Sequence[str],
) -> tuple[Sequence[str], Sequence[str]]:
    """Split hook arguments into forwarded CLI flags and trailing files.

    Examines command-line arguments from pre-commit and separates them
    into flags and target file path strings using a two-tier strategy:
    1. Delimiter: If the explicit POSIX delimiter '--' is present,
       arguments preceding '--' are treated as flags, and arguments
       following '--' are treated as file operands.
    2. Tail-Parsing: Otherwise, inspects argv from right to left.
       Contiguous arguments at the tail that end with 'pyproject.toml'
       and do not start with '-' are collected as target files. The
       scan stops at the first option (e.g. '--mode') or option value
       (e.g. 'host'), treating all preceding tokens as forwarded flags.

    Args:
        argv: Command-line argument strings (typically sys.argv[1:]).

    Returns:
        A tuple of (flags, files):
        - flags: Sequence of forwarded CLI flag strings and option values.
        - files: Sequence of trailing target file path strings.

    """
    if "--" in argv:
        idx = argv.index("--")
        return argv[:idx], argv[idx + 1 :]

    idx = len(argv)
    for arg in reversed(argv):
        if arg.startswith("-") or not arg.endswith("pyproject.toml"):
            break
        idx -= 1

    return argv[:idx], argv[idx:]


def pre_commit_hook(
    func: Callable[[Sequence[str], Sequence[str]], int],
) -> Callable[[], int]:
    """Decorate a pre-commit hook function to receive split flags and files.

    Args:
        func: Hook entrypoint taking (flags, files) sequences returning int.

    Returns:
        Wrapped zero-argument entrypoint returning int.

    """

    @wraps(func)
    def wrapper() -> int:
        flags, files = split_flags_and_files(sys.argv[1:])
        return func(flags, files)

    return wrapper
