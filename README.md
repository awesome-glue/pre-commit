# pre-commit hooks

Pre-commit hooks for [AWS Glue Toolkit](https://github.com/awesome-glue/aws-glue-toolkit).

## Hooks

- `gtk-noop`: No-op hook that always passes.

## Usage

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/awesome-glue/pre-commit
    rev: v0.1.0
    hooks:
      - id: gtk-noop
```

## License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/awesome-glue/pre-commit/blob/main/LICENSE) file for details.
