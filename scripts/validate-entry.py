"""Abundance Codex Entry Validator

Validates one or more Abundance Codex entry files against the Gold Standard
format: YAML frontmatter schema, domain connection constraints, section
presence per the density matrix, and evidence anchor counts.

Usage:
    python scripts/validate-entry.py domains/01-energy/01-the-solar-revolution.md
    python scripts/validate-entry.py domains/
    python scripts/validate-entry.py file1.md file2.md
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml

try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("ERROR: jsonschema not installed. Run: pip install jsonschema>=4.0", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# Section regex patterns — matched against the raw markdown body
# ---------------------------------------------------------------------------

SECTIONS = {
    "one_line_essence": r"One-line essence:",
    "shift_arc": r"## The Shift Arc",
    "phase_1": r"### Phase 1",
    "phase_2": r"### Phase 2",
    "phase_3": r"### Phase 3",
    "phase_4": r"### Phase 4",
    "phase_5": r"### Phase 5",
    "oracle": r"The Oracle",
    "critic": r"The Critic",
    "sensei": r"The Sensei",
    "builder": r"The Builder",
    "witness": r"The Witness",
    "evidence_anchors": r"## Evidence Anchors",
    "shadow_check": r"## Shadow Check",
    "6d_position": r"## 6D Position",
    "connections": r"## Connections",
    "conditional_optimism": r"## Conditional Optimism",
    "practice_hook": r"## Practice Hook",
    "governance": r"## Governance",
}

# ---------------------------------------------------------------------------
# Density matrix — which sections are required per entry type
# ---------------------------------------------------------------------------

DENSITY_MATRIX = {
    "origin_story": {
        "required": [
            "one_line_essence", "shift_arc", "phase_1", "phase_2", "phase_3", "phase_4", "phase_5",
            "oracle", "critic", "sensei", "builder", "witness",
            "evidence_anchors", "shadow_check", "6d_position", "connections",
            "conditional_optimism", "practice_hook", "governance",
        ],
        "min_evidence": 3,
    },
    "breakthrough": {
        "required": [
            "one_line_essence", "shift_arc", "phase_1", "phase_2", "phase_3", "phase_4", "phase_5",
            "oracle", "critic", "sensei", "builder", "witness",
            "evidence_anchors", "shadow_check", "6d_position", "connections",
            "conditional_optimism", "practice_hook", "governance",
        ],
        "min_evidence": 3,
    },
    "builder_profile": {
        "required": [
            "one_line_essence", "shift_arc", "phase_1", "phase_2", "phase_3", "phase_4", "phase_5",
            "oracle", "critic", "sensei", "builder", "witness",
            "evidence_anchors", "shadow_check", "6d_position", "connections",
            "conditional_optimism", "practice_hook", "governance",
        ],
        "min_evidence": 2,
    },
    "trendline": {
        "required": [
            "one_line_essence", "shift_arc", "phase_1", "phase_3", "phase_4",
            "oracle", "critic", "builder",
            "evidence_anchors", "shadow_check", "6d_position", "connections",
            "conditional_optimism", "governance",
        ],
        "min_evidence": 5,
    },
    "contrast": {
        "required": [
            "one_line_essence", "shift_arc",
            "evidence_anchors", "shadow_check", "connections", "governance",
        ],
        "min_evidence": 3,
    },
    "framework": {
        "required": [
            "one_line_essence", "shift_arc", "phase_3", "phase_4", "phase_5",
            "oracle", "critic", "sensei", "builder",
            "evidence_anchors", "shadow_check", "connections",
            "conditional_optimism", "practice_hook", "governance",
        ],
        "min_evidence": 2,
    },
    "paradigm_seed": {
        "required": [
            "one_line_essence", "phase_3", "oracle", "critic", "sensei",
            "evidence_anchors", "shadow_check", "practice_hook",
        ],
        "min_evidence": 1,
    },
    "shadow": {
        "required": [
            "one_line_essence", "shift_arc", "phase_1", "phase_2",
            "oracle", "critic", "sensei", "builder", "witness",
            "evidence_anchors", "shadow_check", "6d_position", "connections",
            "conditional_optimism", "practice_hook", "governance",
        ],
        "min_evidence": 2,
    },
    "star_trek_spec": {
        "required": [
            "one_line_essence", "shift_arc", "phase_3", "phase_4", "phase_5",
            "oracle", "critic", "sensei", "builder", "witness",
            "evidence_anchors", "shadow_check", "6d_position", "connections",
            "conditional_optimism", "practice_hook", "governance",
        ],
        "min_evidence": 2,
    },
    "grand_challenge": {
        "required": [
            "one_line_essence", "shift_arc", "phase_1", "phase_2", "phase_3", "phase_4", "phase_5",
            "oracle", "critic", "sensei", "builder", "witness",
            "evidence_anchors", "shadow_check", "6d_position", "connections",
            "conditional_optimism", "practice_hook", "governance",
        ],
        "min_evidence": 5,
    },
    "false_dawn": {
        "required": [
            "one_line_essence", "shift_arc", "phase_1", "phase_2", "phase_4",
            "oracle", "critic", "sensei", "builder", "witness",
            "evidence_anchors", "shadow_check", "6d_position", "connections",
            "conditional_optimism", "practice_hook", "governance",
        ],
        "min_evidence": 3,
    },
}


def load_schema():
    """Load entry-schema.json from the schema/ directory relative to repo root."""
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    schema_path = repo_root / "schema" / "entry-schema.json"
    if not schema_path.exists():
        print(f"ERROR: Schema not found at {schema_path}", file=sys.stderr)
        sys.exit(2)
    with open(schema_path) as f:
        return json.load(f)


def parse_yaml_frontmatter(text):
    """Extract and parse YAML frontmatter from markdown text.

    Returns (yaml_dict, error_message). On failure, yaml_dict is None.
    """
    # Match content between first pair of --- delimiters
    match = re.match(r"^---\n(.*?\n)---", text, re.DOTALL)
    if not match:
        return None, "No YAML frontmatter found (expected --- delimiters)"
    try:
        data = yaml.safe_load(match.group(1))
        if not isinstance(data, dict):
            return None, "YAML frontmatter did not parse as a mapping"
        return data, None
    except yaml.YAMLError as e:
        return None, f"YAML parse error: {e}"


def validate_file(filepath, schema):
    """Validate a single entry file. Returns (errors, warnings) lists."""
    errors = []
    warnings = []

    try:
        text = Path(filepath).read_text(encoding="utf-8")
    except Exception as e:
        return [f"Could not read file: {e}"], []

    # ── Layer 1: YAML Frontmatter ──────────────────────────────────────
    frontmatter, parse_err = parse_yaml_frontmatter(text)
    if parse_err:
        errors.append(f"YAML: {parse_err}")
        # Can't continue without frontmatter
        return errors, warnings

    try:
        validate(instance=frontmatter, schema=schema)
        yaml_status = "PASS — all required fields present, schema valid"
    except ValidationError as e:
        # Collect all errors
        from jsonschema import Draft7Validator
        validator = Draft7Validator(schema)
        schema_errors = sorted(validator.iter_errors(frontmatter), key=lambda e: list(e.path))
        for err in schema_errors:
            path = ".".join(str(p) for p in err.absolute_path) or "(root)"
            errors.append(f"YAML: {path} — {err.message}")
        yaml_status = f"FAIL — {len(schema_errors)} schema violation(s)"

    print(f"YAML:        {yaml_status}")

    # ── Layer 2: Domain Connections ────────────────────────────────────
    domain_conns = frontmatter.get("domain_connections", [])
    primary_domain = frontmatter.get("domain", "")
    conn_issues = []

    for i, conn in enumerate(domain_conns):
        # Self-reference check
        if conn.get("domain") == primary_domain:
            errors.append(f"DOMAIN_CONN: connection [{i}] is a self-reference to primary domain '{primary_domain}'")
            conn_issues.append("self-ref")

        # Strength warning
        strength = conn.get("strength", 0)
        if strength < 0.5:
            warnings.append(
                f"DOMAIN_CONN: connection to \"{conn.get('domain')}\" has strength {strength} "
                f"— consider omitting per guidelines (< 0.5 threshold)"
            )

    conn_count = len(domain_conns)
    self_refs = sum(1 for c in domain_conns if c.get("domain") == primary_domain)
    if not conn_issues:
        conn_status = f"PASS — {conn_count} connection(s), no self-refs"
    else:
        conn_status = f"FAIL — {len(conn_issues)} issue(s)"

    print(f"DOMAIN_CONN: {conn_status}")
    for w in warnings:
        print(f"             WARNING — {w.split(': ', 1)[1] if ': ' in w else w}")

    # ── Layer 3: Section Presence ──────────────────────────────────────
    entry_type = frontmatter.get("entry_type", "")
    density = DENSITY_MATRIX.get(entry_type)

    if density is None:
        errors.append(f"SECTIONS: unknown entry_type '{entry_type}' — cannot check density matrix")
        print(f"SECTIONS:    FAIL — unknown entry_type '{entry_type}'")
    else:
        required_sections = density["required"]
        missing = []
        for section_key in required_sections:
            pattern = SECTIONS.get(section_key)
            if pattern and not re.search(pattern, text):
                missing.append(section_key)

        if missing:
            for m in missing:
                errors.append(f"SECTIONS: missing required section '{m}' for {entry_type}")
            print(f"SECTIONS:    FAIL — {len(missing)} missing section(s): {', '.join(missing)}")
        else:
            print(f"SECTIONS:    PASS — all {len(required_sections)} required sections present for {entry_type}")

    # ── Layer 4: Evidence Anchor Count ─────────────────────────────────
    # Count rows in Evidence Anchors table: lines starting with | followed by a digit
    evidence_rows = re.findall(r"^\|\s*\d+\s*\|", text, re.MULTILINE)
    evidence_count = len(evidence_rows)

    if density:
        min_ev = density["min_evidence"]
        if evidence_count < min_ev:
            errors.append(
                f"EVIDENCE: {evidence_count} anchor(s) found, minimum {min_ev} required for {entry_type}"
            )
            print(f"EVIDENCE:    FAIL — {evidence_count} anchor(s) found (minimum {min_ev} for {entry_type})")
        else:
            print(f"EVIDENCE:    PASS — {evidence_count} anchor(s) found (minimum {min_ev} for {entry_type})")
    else:
        print(f"EVIDENCE:    SKIP — cannot check without valid entry_type")

    return errors, warnings


def collect_files(paths):
    """Expand paths: directories are walked for .md files, files are taken as-is."""
    files = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            for md in sorted(path.rglob("*.md")):
                files.append(md)
        elif path.is_file():
            files.append(path)
        else:
            print(f"WARNING: '{p}' is not a file or directory, skipping", file=sys.stderr)
    return files


def main():
    parser = argparse.ArgumentParser(
        description="Validate Abundance Codex entry files against the Gold Standard format."
    )
    parser.add_argument(
        "paths", nargs="+",
        help="Entry file(s) or directory containing entries"
    )
    args = parser.parse_args()

    schema = load_schema()
    files = collect_files(args.paths)

    if not files:
        print("No .md files found in the specified path(s).")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0

    for filepath in files:
        print(f"\n=== {filepath} ===")
        errs, warns = validate_file(filepath, schema)
        total_errors += len(errs)
        total_warnings += len(warns)

        err_count = len(errs)
        warn_count = len(warns)
        if err_count == 0:
            print(f"\nRESULT: VALID ({err_count} errors, {warn_count} warning(s))")
        else:
            print(f"\nRESULT: INVALID ({err_count} error(s), {warn_count} warning(s))")
            for e in errs:
                print(f"  ERROR: {e}")

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(files)} file(s) checked — {total_errors} error(s), {total_warnings} warning(s)")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
