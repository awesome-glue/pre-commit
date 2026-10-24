"""Step definitions for check_build feature."""

import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path
from unittest.mock import MagicMock, patch

from behave import given, then, when
from behave.runner import Context

from features.steps.common_steps import run_hook
from gtk_pre_commit.check_build import main

GTK_CONFIG = (
    '[project]\nname = "gtk-job"\n\n'
    '[tool.aws-glue-toolkit]\nglue_version = "5.1"\n'
)
NON_GTK_CONFIG = '[project]\nname = "other-pkg"\n'


def _extract_job_dir(cmd: Sequence[str]) -> Path:
    """Extract the target job directory following the 'build' subcommand.

    Args:
        cmd: Command-line argument sequence executed by subprocess.

    Returns:
        Path to the target job directory.

    Raises:
        ValueError: If 'build' subcommand is missing or has no directory arg.

    """
    try:
        build_idx = cmd.index("build")
        return Path(cmd[build_idx + 1])
    except (ValueError, IndexError) as err:
        msg = f"Cannot extract job directory from command: {cmd}"
        raise ValueError(msg) from err


def _simulate_build(cmd: Sequence[str], code: int) -> MagicMock:
    job_dir = _extract_job_dir(cmd)
    (job_dir / "job-0.0.0.dependencies.zip").write_text("test")
    (job_dir / "job-0.0.0.gluewheels.zip").write_text("test")
    return MagicMock(returncode=code)


def _patch_toolkit(
    context: Context,
    side_effect: Callable[[Sequence[str]], MagicMock],
) -> None:
    p = patch("subprocess.run", side_effect=side_effect)
    p.start()
    context.add_cleanup(p.stop)


def _create_project_file(dir_path: Path, content: str) -> Path:
    file_path = dir_path / "pyproject.toml"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return file_path


@given("aws-glue-toolkit builds jobs successfully")
def step_toolkit_build_success(context: Context) -> None:
    """Mock subprocess.run to simulate build success.

    Args:
        context: The behave context object.

    """

    def run_fn(cmd: Sequence[str], *, check: bool = False) -> MagicMock:
        _ = check
        context.last_cmd = cmd
        return _simulate_build(cmd, 0)

    _patch_toolkit(context, run_fn)


@given("aws-glue-toolkit fails to build the job")
def step_toolkit_build_failure(context: Context) -> None:
    """Mock subprocess.run to simulate build failure.

    Args:
        context: The behave context object.

    """

    def run_fn(cmd: Sequence[str], *, check: bool = False) -> MagicMock:
        _ = check
        context.last_cmd = cmd
        return _simulate_build(cmd, 1)

    _patch_toolkit(context, run_fn)


@given('aws-glue-toolkit fails to build job "{failing_job}"')
def step_toolkit_selective_fail(
    context: Context,
    failing_job: str,
) -> None:
    """Mock subprocess.run to fail only for a specific job directory.

    Args:
        context: The behave context object.
        failing_job: Job name or path substring that should trigger failure.

    """

    def run_fn(cmd: Sequence[str], *, check: bool = False) -> MagicMock:
        _ = check
        job_dir = _extract_job_dir(cmd)
        returncode = 1 if failing_job in str(job_dir) else 0
        return MagicMock(returncode=returncode)

    _patch_toolkit(context, run_fn)


@given("aws-glue-toolkit is not installed")
def step_toolkit_missing(context: Context) -> None:
    """Simulate aws-glue-toolkit not being installed in the environment.

    Args:
        context: The behave context object.

    """
    context.toolkit_installed = False


def _build_project_from_row(root: Path, row: dict[str, str]) -> Path:
    dir_path = root / row["directory"]
    is_gtk = row["is_gtk"].strip().lower() in ("yes", "true", "1")
    cfg = GTK_CONFIG if is_gtk else NON_GTK_CONFIG
    return _create_project_file(dir_path, cfg)


@given("a workspace with projects:")
def step_workspace_projects(context: Context) -> None:
    """Create a temporary workspace with projects defined in a table.

    Args:
        context: The behave context object with table rows.

    """
    assert context.table is not None
    temp_dir = tempfile.TemporaryDirectory()
    context.add_cleanup(temp_dir.cleanup)
    root = Path(temp_dir.name)
    context.target_files = [
        _build_project_from_row(root, row) for row in context.table
    ]


def _run_check_build(context: Context, argv: Sequence[str]) -> None:
    """Run gtk-check-build with mocked arguments and default toolkit.

    Args:
        context: The behave context object.
        argv: Command-line arguments to pass to main.

    """
    toolkit_installed = getattr(context, "toolkit_installed", True)
    which_val = "gtk" if toolkit_installed else None
    with patch("shutil.which", return_value=which_val):
        code, stdout, stderr = run_hook(main, argv)
    context.exit_code = code
    context.stdout = stdout
    context.stderr = stderr


@when("I run gtk-check-build on the file")
def step_run_on_file(context: Context) -> None:
    """Run gtk-check-build on context.target_file.

    Args:
        context: The behave context object.

    """
    _run_check_build(context, ["gtk-check-build", str(context.target_file)])


@when('I run gtk-check-build with arguments "{args}" on the file')
def step_run_with_args(context: Context, args: str) -> None:
    """Run gtk-check-build with extra flags.

    Args:
        context: The behave context object.
        args: Extra flags string.

    """
    _run_check_build(
        context,
        ["gtk-check-build", *args.split(), str(context.target_file)],
    )


@when("I run gtk-check-build on all project files")
def step_run_on_all(context: Context) -> None:
    """Run gtk-check-build on context.target_files.

    Args:
        context: The behave context object.

    """
    _run_check_build(
        context,
        ["gtk-check-build", *(str(p) for p in context.target_files)],
    )


@when("I run gtk-check-build with no arguments")
def step_run_no_args(context: Context) -> None:
    """Run gtk-check-build with no arguments.

    Args:
        context: The behave context object.

    """
    _run_check_build(context, ["gtk-check-build"])


@when("I run gtk-check-build on a non-existent file")
def step_run_non_existent(context: Context) -> None:
    """Run gtk-check-build on a non-existent file.

    Args:
        context: The behave context object.

    """
    _run_check_build(
        context,
        ["gtk-check-build", "non_existent_pyproject.toml"],
    )


@then("no temporary build files should remain in the project directory")
def step_verify_artifacts_removed(context: Context) -> None:
    """Verify that all temporary build files were removed from the job dir.

    Args:
        context: The behave context object.

    """
    target = getattr(context, "target_file", None)
    assert target is not None, "Target file was not set in context"
    zips = list(target.parent.glob("*.zip"))
    assert not zips, (
        f"Found unexpected zip artifacts in {target.parent}: {zips}"
    )


@then('the build command should include argument "{arg}"')
def step_verify_arg_received(context: Context, arg: str) -> None:
    """Verify that a specific CLI argument was forwarded to the build command.

    Args:
        context: The behave context object.
        arg: Argument expected in the command.

    """
    last_cmd = getattr(context, "last_cmd", [])
    assert arg in last_cmd, f"'{arg}' not in command: {last_cmd}"


@then('stderr should mention "{text}"')
def step_verify_stderr_contains(context: Context, text: str) -> None:
    """Verify that stderr contains the expected text.

    Args:
        context: The behave context object.
        text: Expected substring in stderr.

    """
    stderr = getattr(context, "stderr", "")
    assert text in stderr, f"'{text}' not in stderr: {stderr}"
