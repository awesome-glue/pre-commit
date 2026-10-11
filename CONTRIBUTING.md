# Contributing

Thank you for your interest in contributing to AWS Glue pre-commit hooks. This guide covers local environment setup, development workflow, and pull request expectations.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (environment and dependency management)
- [just](https://github.com/casey/just) (command runner)

## Setup

From the repository root:

```bash
just init
```

`just init` installs the project Python version, syncs development dependencies into `.venv`, and installs the git pre-commit hooks.

If you do not use `just`, run:

```bash
uv python install
uv sync --group dev
uv run pre-commit install
```

## Making changes

1. Create a feature branch: `git checkout -b feat/my-new-hook`
2. Add your hook implementation under `src/gtk_pre_commit/`.
3. Register the hook in:
   - `pyproject.toml` under `[project.scripts]`
   - `.pre-commit-hooks.yaml`
   - `README.md` under `## Hooks`
4. Add unit and integration tests under `tests/`.
5. Run lint and format checks across all files:

   ```bash
   just lint
   ```

   *(Runs all pre-commit hooks: Ruff formatting & linting, Bandit security checks, YAML/TOML validators, Codespell).*

6. Run the test suite and verify 100% test coverage:

   ```bash
   just test-cov
   ```

## Code style

This project enforces strict code quality standards configured in `pyproject.toml`:
- **Line length:** 79 characters (PEP 8).
- **Docstrings:** Required on all modules, functions, classes, and test cases (`pydocstyle`).
- **Typing:** Fully type-annotated (`mypy` strict mode).

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/) for commit subjects, for example:

```text
feat(hooks): add check-glue-version hook
fix(config): allow optional worker-type in job config
docs: document new hook in README
test: add coverage for error handling
```

## Pull requests

- Keep pull requests focused on a single concern.
- Ensure `just lint` and `just test-cov` pass before requesting review.
- Use a Conventional Commits title for your pull request.

## Code of conduct

Follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

Report security vulnerabilities through [SECURITY.md](SECURITY.md).
