"""No-op pre-commit hook that always succeeds."""

from collections.abc import Sequence


def main(_argv: Sequence[str] | None = None) -> int:
    """Run no-op hook and return exit code 0.

    Args:
        _argv: Optional command-line arguments (unused).

    Returns:
        Always 0.

    """
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
