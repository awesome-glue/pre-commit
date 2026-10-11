"""Pre-commit hooks for AWS Glue Toolkit."""

from importlib.metadata import version

__all__ = ["__version__"]

__version__ = version("gtk-pre-commit")
