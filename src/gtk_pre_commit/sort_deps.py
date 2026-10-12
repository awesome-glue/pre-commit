"""Sort dependencies in pyproject.toml."""

from collections.abc import Iterator, Sequence

import tomlkit
from tomlkit.items import Array, Item
from tomlkit.toml_document import TOMLDocument

from gtk_pre_commit.cli import parse_files

TARGET_PATHS: tuple[tuple[str, ...], ...] = (
    ("project", "dependencies"),
    ("tool", "aws-glue-toolkit", "dependencies"),
)


# =============================================================================
# Functional Core
# =============================================================================


def _iter_target_arrays(
    doc: TOMLDocument,
    targets: Sequence[tuple[str, ...]] = TARGET_PATHS,
) -> Iterator[Array]:
    """Yield target dependency arrays found in the document.

    Args:
        doc: Parsed TOML document.
        targets: Key paths to target dependency arrays.

    Yields:
        Target arrays found in the document.

    """
    for path in targets:
        node: TOMLDocument | Item | None = doc
        for key in path:
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


def main(argv: Sequence[str] | None = None) -> int:
    """Sort dependencies in target files and return an exit code.

    Args:
        argv: Command-line arguments, or None to read sys.argv.

    Returns:
        0 if all files were sorted, or 1 if any file was modified.

    """
    modified = False

    for path in parse_files(argv):
        # Format and compare
        original_content = path.read_text(encoding="utf-8")
        sorted_content = sort_dependencies(original_content)
        if sorted_content == original_content:
            continue

        # Persist changes
        path.write_text(sorted_content, encoding="utf-8")
        print(f"Fixing {path}")  # noqa: T201
        modified = True

    return 1 if modified else 0
