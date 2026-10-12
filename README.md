# pre-commit hooks

Pre-commit hooks for [AWS Glue Toolkit](https://github.com/awesome-glue/aws-glue-toolkit).

## Hooks

- `gtk-sort-deps`: Sort dependencies under `[project]` and `[tool.aws-glue-toolkit]` in `pyproject.toml`.

## Usage

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/awesome-glue/pre-commit
    rev: v0.0.0
    hooks:
      - id: gtk-sort-deps
```

## License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/awesome-glue/pre-commit/blob/main/LICENSE) file for details.
