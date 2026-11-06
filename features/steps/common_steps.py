"""Common step definitions shared across features."""

import contextlib
import io
import sys
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path
from unittest.mock import patch

from behave import given, then
from behave.runner import Context


def run_hook(
    entrypoint: Callable[[], int],
    argv: Sequence[str],
) -> tuple[int, str, str]:
    """Execute a pre-commit hook entrypoint with captured I/O and custom argv.

    Args:
        entrypoint: Zero-argument hook entrypoint returning an int.
        argv: Command-line arguments to pass to the hook (sys.argv).

    Returns:
        A tuple of (exit_code, stdout, stderr).

    """
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    with (
        contextlib.redirect_stdout(stdout_buf),
        contextlib.redirect_stderr(stderr_buf),
        patch.object(sys, "argv", argv),
    ):
        exit_code = entrypoint()
    return exit_code, stdout_buf.getvalue(), stderr_buf.getvalue()


@given("a pyproject.toml file with content:")
def step_given_pyproject(context: Context) -> None:
    """Write the provided TOML content to pyproject.toml.

    Args:
        context: The behave context object.

    """
    assert context.text is not None
    temp_dir = tempfile.TemporaryDirectory()
    context.add_cleanup(temp_dir.cleanup)
    file_path = Path(temp_dir.name) / "pyproject.toml"
    file_path.write_text(context.text, encoding="utf-8")
    context.target_file = file_path
    context.original_content = context.text


@then("the hook should exit with failure")
def step_then_exit_failure(context: Context) -> None:
    """Verify that the hook returned exit code 1.

    Args:
        context: The behave context object.

    """
    stderr = getattr(context, "stderr", "")
    assert context.exit_code == 1, (
        f"Expected exit code 1, but got {context.exit_code}.\nStderr: {stderr}"
    )


@then("the hook should report that files were modified")
def step_then_files_modified(context: Context) -> None:
    """Verify that the hook reported modified files with exit code 1.

    Args:
        context: The behave context object.

    """
    stderr = getattr(context, "stderr", "")
    assert context.exit_code == 1, (
        f"Expected exit code 1, but got {context.exit_code}.\nStderr: {stderr}"
    )


@then("the hook should exit with success")
def step_then_exit_success(context: Context) -> None:
    """Verify that the hook returned exit code 0.

    Args:
        context: The behave context object.

    """
    stderr = getattr(context, "stderr", "")
    assert context.exit_code == 0, (
        f"Expected exit code 0, but got {context.exit_code}.\nStderr: {stderr}"
    )
