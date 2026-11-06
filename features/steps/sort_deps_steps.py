"""Step definitions for sort_deps feature."""

import difflib
from collections.abc import Sequence

from behave import then, when
from behave.runner import Context

from features.steps.common_steps import run_hook
from gtk_pre_commit.sort_deps import main


def _run_sort_deps(context: Context, argv: Sequence[str]) -> None:
    """Run gtk-sort-deps with captured I/O and store results on context.

    Args:
        context: The behave context object.
        argv: Command-line arguments to pass to main.

    """
    code, stdout, stderr = run_hook(main, argv)
    context.exit_code = code
    context.stdout = stdout
    context.stderr = stderr


@when("I run gtk-sort-deps on the file")
def step_when_run_on_file(context: Context) -> None:
    """Run gtk-sort-deps on the target file.

    Args:
        context: The behave context object.

    """
    _run_sort_deps(context, ["gtk-sort-deps", str(context.target_file)])


@when("I run gtk-sort-deps with no arguments")
def step_when_run_no_args(context: Context) -> None:
    """Run gtk-sort-deps with no arguments.

    Args:
        context: The behave context object.

    """
    _run_sort_deps(context, ["gtk-sort-deps"])


@when("I run gtk-sort-deps on a non-existent file")
def step_when_run_non_existent(context: Context) -> None:
    """Run gtk-sort-deps on a non-existent file.

    Args:
        context: The behave context object.

    """
    _run_sort_deps(context, ["gtk-sort-deps", "non_existent_pyproject.toml"])


@then("the file should be updated to:")
def step_then_file_updated(context: Context) -> None:
    """Verify that the target file content matches expected text.

    Args:
        context: The behave context object.

    """
    assert context.text is not None
    assert context.target_file is not None
    actual_content = context.target_file.read_text(encoding="utf-8")
    diff = "\n".join(
        difflib.unified_diff(
            context.text.splitlines(),
            actual_content.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm="",
        ),
    )
    assert actual_content == context.text, f"File content mismatch:\n{diff}"


@then("the file content should remain unchanged")
def step_then_file_unchanged(context: Context) -> None:
    """Verify that the target file content was not modified.

    Args:
        context: The behave context object.

    """
    assert context.target_file is not None
    actual_content = context.target_file.read_text(encoding="utf-8")
    original = str(context.original_content)
    diff = "\n".join(
        difflib.unified_diff(
            original.splitlines(),
            actual_content.splitlines(),
            fromfile="original",
            tofile="actual",
            lineterm="",
        ),
    )
    assert actual_content == context.original_content, (
        f"File was unexpectedly modified:\n{diff}"
    )
