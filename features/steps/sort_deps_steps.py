"""Step definitions for sort_deps feature."""

import tempfile
from pathlib import Path

from behave import given, then, when
from behave.runner import Context

from gtk_pre_commit.sort_deps import main


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


@when("I run gtk-sort-deps on the file")
def step_when_run_on_file(context: Context) -> None:
    """Run gtk-sort-deps on the target file.

    Args:
        context: The behave context object.

    """
    context.exit_code = main([str(context.target_file)])


@when("I run gtk-sort-deps with no arguments")
def step_when_run_no_args(context: Context) -> None:
    """Run gtk-sort-deps with no arguments.

    Args:
        context: The behave context object.

    """
    context.exit_code = main([])


@when("I run gtk-sort-deps on a non-existent file")
def step_when_run_non_existent(context: Context) -> None:
    """Run gtk-sort-deps on a non-existent file.

    Args:
        context: The behave context object.

    """
    context.exit_code = main(["non_existent_pyproject.toml"])


@then("the file should be updated to:")
def step_then_file_updated(context: Context) -> None:
    """Verify that the target file content matches expected text.

    Args:
        context: The behave context object.

    """
    assert context.text is not None
    actual_content = context.target_file.read_text(encoding="utf-8")
    assert actual_content == context.text


@then("the file content should remain unchanged")
def step_then_file_unchanged(context: Context) -> None:
    """Verify that the target file content was not modified.

    Args:
        context: The behave context object.

    """
    actual_content = context.target_file.read_text(encoding="utf-8")
    assert actual_content == context.original_content


@then("the hook should exit with failure")
def step_then_exit_failure(context: Context) -> None:
    """Verify that the hook returned exit code 1.

    Args:
        context: The behave context object.

    """
    assert context.exit_code == 1


@then("the hook should exit with success")
def step_then_exit_success(context: Context) -> None:
    """Verify that the hook returned exit code 0.

    Args:
        context: The behave context object.

    """
    assert context.exit_code == 0
