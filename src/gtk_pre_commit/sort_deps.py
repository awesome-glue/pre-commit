"""Sort dependencies in pyproject.toml for AWS Glue Toolkit projects."""

from collections.abc import Iterable, Iterator, Sequence
from pathlib import Path

import tomlkit
from tomlkit.items import Array, Item
from tomlkit.toml_document import TOMLDocument

from gtk_pre_commit.utils import find_gtk_project_files, pre_commit_hook

TARGET_KEY_PATHS: tuple[tuple[str, ...], ...] = (
    ("project", "dependencies"),
    ("tool", "aws-glue-toolkit", "dependencies"),
)


# =============================================================================
# Functional Core
# =============================================================================


def _iter_target_arrays(
    doc: TOMLDocument,
    targets: Sequence[tuple[str, ...]] = TARGET_KEY_PATHS,
) -> Iterator[Array]:
    """Yield target dependency arrays found in the document.

    Args:
        doc: Parsed TOML document.
        targets: Key paths to target dependency arrays.

    Yields:
        Target arrays found in the document.

    """
    for key_path in targets:
        node: TOMLDocument | Item | None = doc
        for key in key_path:
            node = node.get(key) if isinstance(node, dict) else None
        if isinstance(node, Array):
            yield node


def _sort_array(array: Array) -> None:
    """Sort array items in place and case-insensitively.

    Args:
        array: TOML array to sort.

    """
    groups = [
        group
        for group in array._value  # noqa: SLF001
        if group.value is not None
    ]
    sorted_items = sorted(
        ((group.value, group.comment) for group in groups),
        key=lambda pair: str(pair[0]).casefold(),
    )
    for group, (value, comment) in zip(groups, sorted_items, strict=True):
        group.value = value
        group.comment = comment


def sort_dependencies(content: str) -> str:
    """Sort target dependency arrays in TOML content.

    Args:
        content: Raw TOML file content.

    Returns:
        Updated TOML content with sorted dependencies.

    """
    doc = tomlkit.parse(content)
    for array in _iter_target_arrays(doc):
        _sort_array(array)
    return tomlkit.dumps(doc)


# =============================================================================
# Imperative Shell
# =============================================================================


def _sort_file_dependencies(paths: Iterable[Path]) -> Iterator[Path]:
    """Sort dependencies in target files, yielding each modified path.

    Args:
        paths: Sequence of file paths to process.

    Yields:
        Path of each file that was modified.

    """
    for path in paths:
        original = path.read_text(encoding="utf-8")
        if (sorted_content := sort_dependencies(original)) != original:
            path.write_text(sorted_content, encoding="utf-8")
            yield path


@pre_commit_hook
def main(_: Sequence[str], files: Sequence[str]) -> int:
    """Sort dependencies in target files and return an exit code.

    Args:
        _: Forwarded CLI flags (unused).
        files: Sequence of file paths to process.

    Returns:
        0 if all files were sorted or ignored, or 1 if any file was modified.

    """
    fixed = list(_sort_file_dependencies(find_gtk_project_files(files)))
    if not fixed:
        return 0

    print(*(f"Fixing {path}" for path in fixed), sep="\n")  # noqa: T201
    return 1
