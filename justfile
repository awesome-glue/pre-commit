# Default: show recipe list
[private]
default:
    @just --list

# Initialize local dev environment.
init:
    uv python install
    uv sync --group dev
    uv run pre-commit install

# Run pre-commit on all files.
lint:
    uv run pre-commit run --all-files

# Run all tests.
test *ARGS:
    uv run pytest {{ARGS}}

# Run tests with coverage report.
test-cov:
    uv run pytest --cov --cov-report=term-missing
