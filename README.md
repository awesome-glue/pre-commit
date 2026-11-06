# Awesome Glue Pre-commit Hooks

[![Release](https://img.shields.io/github/v/release/awesome-glue/pre-commit)](https://github.com/awesome-glue/pre-commit/releases)
[![CI](https://github.com/awesome-glue/pre-commit/actions/workflows/ci.yaml/badge.svg)](https://github.com/awesome-glue/pre-commit/actions/workflows/ci.yaml)
[![License](https://img.shields.io/github/license/awesome-glue/pre-commit)](LICENSE)

Official pre-commit hooks for the [Awesome Glue](https://github.com/awesome-glue) ecosystem.

## Quickstart

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/awesome-glue/pre-commit
    rev: v0.1.0
    hooks:
      - id: gtk-sort-deps
      - id: gtk-check-build
        additional_dependencies:
          - aws-glue-toolkit>=0.5.0
```

Install the hooks into your git repository:

```bash
pre-commit install
```

## Available Hooks

### AWS Glue Toolkit (`gtk`)

Hooks for projects using [AWS Glue Toolkit](https://github.com/awesome-glue/aws-glue-toolkit):

| Hook | Description | Modifies Files | Dependencies |
| :--- | :--- | :---: | :--- |
| `gtk-sort-deps` | Alphabetizes dependencies under `[project]` and `[tool.aws-glue-toolkit]` while preserving comments. | Yes | Built-in |
| `gtk-check-build` | Verifies job configuration, Glue runtime, and dependency resolution by checking that `gtk build` succeeds. | No | `aws-glue-toolkit>=0.5.0` |

> [!NOTE]
> GTK hooks only run on `pyproject.toml` files with a `[tool.aws-glue-toolkit]` section; other projects are safely skipped.
>
> To catch general TOML syntax errors across your repository, pair these hooks with `check-toml` from `pre-commit-hooks`.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
