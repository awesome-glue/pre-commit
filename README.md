# pre-commit hooks

Pre-commit hooks for [AWS Glue Toolkit](https://github.com/awesome-glue/aws-glue-toolkit).

## Hooks

- `gtk-sort-deps`: Sort dependencies under `[project]` and `[tool.aws-glue-toolkit]` in `pyproject.toml`.
- `gtk-check-build`: Verify AWS Glue job configuration, runtime version, and dependency resolution by checking that the job builds successfully. Requires `aws-glue-toolkit` in `additional_dependencies`.

> [!NOTE]
> Malformed or syntactically invalid TOML files and non-GTK projects are
> ignored without error. It is recommended to configure a dedicated TOML
> syntax validator (such as `check-toml` from `pre-commit-hooks`) in your
> `.pre-commit-config.yaml` to catch syntax issues.

## Usage

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/awesome-glue/pre-commit
    rev: v0.0.0
    hooks:
      - id: gtk-sort-deps
      - id: gtk-check-build
        additional_dependencies:
          - aws-glue-toolkit>=0.5.0
```

## License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/awesome-glue/pre-commit/blob/main/LICENSE) file for details.
