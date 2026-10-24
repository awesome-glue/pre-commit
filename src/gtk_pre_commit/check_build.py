"""Check AWS Glue Toolkit job buildability and dependencies."""

import shutil
import subprocess  # nosec B404
import sys
from collections.abc import Sequence
from pathlib import Path

from gtk_pre_commit.utils import find_gtk_project_files, pre_commit_hook

ARTIFACT_PATTERNS: tuple[str, ...] = ("*.dependencies.zip", "*.gluewheels.zip")


def _check_build(gtk_bin: str, job_dir: Path, flags: Sequence[str]) -> bool:
    """Run build check for a job directory and clean up any artifacts.

    Args:
        gtk_bin: Path to the gtk executable.
        job_dir: Directory containing the Glue job pyproject.toml.
        flags: Extra CLI flags to pass to gtk build.

    Returns:
        True if the build succeeded, False if it failed.

    """
    try:
        return (
            subprocess.run(  # noqa: S603  # nosec B603
                [gtk_bin, "build", str(job_dir), *flags],
                check=False,
            ).returncode
            == 0
        )
    finally:
        for pattern in ARTIFACT_PATTERNS:
            for artifact in job_dir.glob(pattern):
                artifact.unlink(missing_ok=True)


@pre_commit_hook
def main(flags: Sequence[str], files: Sequence[str]) -> int:
    """Check GTK project builds and return an exit code.

    Args:
        flags: Extra CLI flags to pass to gtk build.
        files: Sequence of project file paths to check.

    Returns:
        0 if all valid projects pass build checks, 1 on failure.

    """
    if (gtk_bin := shutil.which("gtk")) is None:
        print(  # noqa: T201
            "Error: 'aws-glue-toolkit' is not installed in the hook "
            "environment.\nPlease configure 'additional_dependencies: "
            "[aws-glue-toolkit]' in .pre-commit-config.yaml.",
            file=sys.stderr,
        )
        return 1

    failed_dirs = [
        path.parent
        for path in find_gtk_project_files(files)
        if not _check_build(gtk_bin, path.parent, flags)
    ]
    if not failed_dirs:
        return 0

    print(  # noqa: T201
        *(f"Failed to build {job_dir}" for job_dir in failed_dirs),
        sep="\n",
    )
    return 1
