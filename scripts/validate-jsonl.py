#!/usr/bin/env python3
"""Validate abundance-codex.jsonl against export/schema.json.

Exits with code 1 if any entry fails validation.
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema not installed. Run: pip install jsonschema")
    sys.exit(1)

JSONL_PATH = Path("export/abundance-codex.jsonl")
SCHEMA_PATH = Path("export/schema.json")


def main():
    if not JSONL_PATH.exists():
        print(f"Error: {JSONL_PATH} not found")
        sys.exit(1)
    if not SCHEMA_PATH.exists():
        print(f"Error: {SCHEMA_PATH} not found. Run generate-schema.py first.")
        sys.exit(1)

    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    validator = jsonschema.Draft7Validator(schema)
    errors = []
    entry_count = 0

    with open(JSONL_PATH) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"Line {line_num}: Invalid JSON — {e}")
                continue

            entry_count += 1
            entry_id = entry.get("id", f"line-{line_num}")

            for error in validator.iter_errors(entry):
                path = ".".join(str(p) for p in error.absolute_path) or "(root)"
                errors.append(f"{entry_id} [{path}]: {error.message}")

    if errors:
        print(f"JSONL VALIDATION FAILED — {len(errors)} error(s) in {entry_count} entries:\n")
        for e in errors[:20]:
            print(f"  {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")
        sys.exit(1)
    else:
        print(f"JSONL VALIDATION PASSED — {entry_count} entries valid against {SCHEMA_PATH}")


if __name__ == "__main__":
    main()
