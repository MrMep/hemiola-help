When working as an AI agent in this repository:

- The `help/` folder contains localized JSON files. Each file must follow the schema in `schema/hemiola-help.schema.json`.
- All language files must have the same section IDs, icons, and entry count. Do not add or remove sections in one language without updating all others.
- Only modify `title` and `text` fields when translating or correcting content.
- The `"language"` field at the top of each file must match the ISO 639-1 code in the filename.
- Run `python tools/validate_help.py` before committing to ensure schema compliance and cross-language consistency.
