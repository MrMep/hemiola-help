# Contributing to Hemiola Help

Thanks for your interest in improving the Hemiola help content!

## How to contribute

### Fix a translation or improve text

1. **Fork** this repository and create a feature branch.
2. **Edit** the relevant `help/help_<lang>.json` file.
3. **Validate** your changes:
   ```bash
   pip install jsonschema
   python tools/validate_help.py
   ```
4. **Open a Pull Request** describing what you changed and why.

### Add a new language

1. **Copy** `help/help_en.json` as `help/help_<lang>.json` (use the ISO 639-1 code).
2. **Translate** all `title` and `text` fields. Keep `id`, `icon`, and `type` unchanged.
3. **Update** `"language"` at the top of the file to match the new language code.
4. **Validate and open a PR** as above.

## Guidelines

- Keep the section structure (`id`, `icon`, entry order) consistent across all languages.
- Do not add or remove sections — the app expects matching structure.
- Use clear, user-friendly language appropriate for app documentation.
- Keep `type` values exactly as-is: `para`, `item`, `subtitle`, `note`, `table`.

## Validation

The CI pipeline runs `tools/validate_help.py` automatically on every PR. All files must pass before merge.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
