# SPDX-License-Identifier: MIT
"""Validate all help JSON files against the Hemiola help schema.

Usage:
    python tools/validate_help.py

Validates every help/help_*.json file against schema/hemiola-help.schema.json.
Also performs cross-language consistency checks:
  - All files must have the same section IDs in the same order.
  - All files must have the same number of entries per section.
  - All files must use the same icon per section.

Exit code 0 on success, 1 on any validation failure.
"""

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERROR: jsonschema is required.  pip install jsonschema", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "hemiola-help.schema.json"
HELP_DIR = REPO_ROOT / "help"


def load_json(path: Path) -> dict:
    """Load and parse a JSON file.

    Args:
        path: Path to the JSON file.

    Returns:
        Parsed JSON as a dict.
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate_schema(data: dict, validator: Draft202012Validator, path: Path) -> list[str]:
    """Validate a help file against the JSON schema.

    Args:
        data: Parsed help JSON.
        validator: JSON schema validator instance.
        path: File path for error messages.

    Returns:
        List of error strings (empty if valid).
    """
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        location = " → ".join(str(p) for p in error.absolute_path) or "(root)"
        errors.append(f"  {location}: {error.message}")
    return errors


def check_consistency(files: dict[str, dict]) -> list[str]:
    """Check cross-language structural consistency.

    All help files must have the same section IDs (in order),
    the same icons, and the same number of entries per section.

    Args:
        files: Dict mapping filename to parsed help JSON.

    Returns:
        List of error strings (empty if consistent).
    """
    errors = []
    if not files:
        return errors

    ref_name, ref_data = next(iter(files.items()))
    ref_sections = [(s["id"], s["icon"], len(s["entries"])) for s in ref_data["sections"]]

    for name, data in files.items():
        if name == ref_name:
            continue
        sections = [(s["id"], s["icon"], len(s["entries"])) for s in data["sections"]]

        if len(sections) != len(ref_sections):
            errors.append(
                f"  {name}: has {len(sections)} sections, "
                f"expected {len(ref_sections)} (reference: {ref_name})"
            )
            continue

        for i, (ref, cur) in enumerate(zip(ref_sections, sections)):
            ref_id, ref_icon, ref_count = ref
            cur_id, cur_icon, cur_count = cur
            if cur_id != ref_id:
                errors.append(
                    f"  {name}: section {i} id is '{cur_id}', "
                    f"expected '{ref_id}' (reference: {ref_name})"
                )
            if cur_icon != ref_icon:
                errors.append(
                    f"  {name}: section '{cur_id}' icon is '{cur_icon}', "
                    f"expected '{ref_icon}' (reference: {ref_name})"
                )
            if cur_count != ref_count:
                errors.append(
                    f"  {name}: section '{cur_id}' has {cur_count} entries, "
                    f"expected {ref_count} (reference: {ref_name})"
                )

    return errors


def main() -> int:
    """Run validation on all help files.

    Returns:
        Exit code: 0 if all pass, 1 if any fail.
    """
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)

    help_files = sorted(HELP_DIR.glob("help_*.json"))
    if not help_files:
        print("ERROR: no help files found in help/", file=sys.stderr)
        return 1

    all_ok = True
    loaded: dict[str, dict] = {}

    for path in help_files:
        data = load_json(path)
        errors = validate_schema(data, validator, path)
        if errors:
            print(f"FAIL {path.relative_to(REPO_ROOT)}")
            for e in errors:
                print(e)
            all_ok = False
        else:
            print(f"  OK {path.relative_to(REPO_ROOT)}")
            loaded[path.name] = data

    # Cross-language consistency (warnings only — does not fail CI)
    consistency_errors = check_consistency(loaded)
    if consistency_errors:
        print("\nCross-language consistency warnings:")
        for e in consistency_errors:
            print(f"  WARN {e}")
    elif loaded:
        print(f"\nCross-language consistency: OK ({len(loaded)} files)")

    print(f"\nValidated {len(help_files)} help file(s)")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
