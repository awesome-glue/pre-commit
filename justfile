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
lint *ARGS:
    uv run pre-commit run {{ARGS}}

# Run all tests.
test *ARGS:
    uv run behave {{ARGS}}

# Run tests with coverage report.
coverage *ARGS:
    uv run coverage run -m behave {{ARGS}}
    uv run coverage report --show-missing
