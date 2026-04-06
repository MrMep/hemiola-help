# Hemiola Help Content

[![Validate Help](https://github.com/MrMep/hemiola-help/actions/workflows/validate-help.yml/badge.svg)](https://github.com/MrMep/hemiola-help/actions/workflows/validate-help.yml)

Localized help content for the [Hemiola](https://hemiola.app) music app.

This repository contains the structured JSON files that power the in-app help system. Each file represents a complete translation of the help content.

## Supported languages

| File | Language |
|------|----------|
| `help/help_en.json` | English |
| `help/help_it.json` | Italiano |
| `help/help_de.json` | Deutsch |
| `help/help_es.json` | Español |
| `help/help_fr.json` | Français |
| `help/help_ja.json` | 日本語 |
| `help/help_zh.json` | 中文 |

## Repository layout

- `help/`: localized help JSON files
- `schema/`: JSON schema for validation and editor integration
- `tools/validate_help.py`: validates all help files against the schema

## JSON structure

Each help file follows this structure:

```json
{
  "version": 1,
  "language": "en",
  "sections": [
    {
      "id": "SectionName",
      "title": "Section Title",
      "icon": "material_icon_name",
      "entries": [
        { "type": "para", "text": "Paragraph text" },
        { "type": "item", "text": "Bullet point" },
        { "type": "subtitle", "text": "Sub-heading" },
        { "type": "note", "text": "Highlighted note" }
      ]
    }
  ]
}
```

### Entry types

| Type | Rendered as |
|------|-------------|
| `para` | Paragraph |
| `item` | Bullet point |
| `subtitle` | Sub-heading within a section |
| `note` | Highlighted note box |
| `table` | Table (pipe-separated columns, newline-separated rows) |

## Validation

Run the schema validator:

```bash
pip install jsonschema
python tools/validate_help.py
```

All files must pass validation before merge.

## Editor integration

For JSON autocompletion and inline validation, add to your VS Code `settings.json`:

```json
{
  "json.schemas": [
    {
      "fileMatch": ["help/help_*.json"],
      "url": "./schema/hemiola-help.schema.json"
    }
  ]
}
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to fix translations, improve existing text, or add a new language.

## License

[MIT](LICENSE)
