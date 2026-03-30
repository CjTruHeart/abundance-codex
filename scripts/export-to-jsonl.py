"""Abundance Codex JSONL Exporter

Walks domains/ and exports all markdown entries to a single JSONL file.
Each line is a complete JSON object with all structured fields extracted
from the markdown source.

Usage:
    python scripts/export-to-jsonl.py
    python scripts/export-to-jsonl.py --output export/custom-name.jsonl
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml


def parse_yaml_frontmatter(text):
    """Extract and parse YAML frontmatter. Returns (dict, body_text)."""
    match = re.match(r"^---\n(.*?\n)---\n?(.*)", text, re.DOTALL)
    if not match:
        return {}, text
    try:
        data = yaml.safe_load(match.group(1))
        if not isinstance(data, dict):
            return {}, text
        return data, match.group(2)
    except yaml.YAMLError:
        return {}, text


def extract_one_line_essence(body):
    """Extract text after 'One-line essence:' on the same line."""
    match = re.search(r"\*\*One-line essence:\*\*\s*(.+)", body)
    if match:
        return match.group(1).strip()
    match = re.search(r"One-line essence:\s*(.+)", body)
    if match:
        return match.group(1).strip()
    return ""


def split_sections(body, level="## "):
    """Split markdown body by headers at the given level. Returns dict of header -> content."""
    parts = re.split(r"(?m)^" + re.escape(level), body)
    sections = {}
    for part in parts[1:]:  # skip content before first header
        lines = part.split("\n", 1)
        header = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""
        sections[header] = content
    return sections


def split_subsections(content, level="### "):
    """Split section content by subsection headers."""
    parts = re.split(r"(?m)^" + re.escape(level), content)
    subs = {}
    for part in parts[1:]:
        lines = part.split("\n", 1)
        header = lines[0].strip()
        content_text = lines[1].strip() if len(lines) > 1 else ""
        subs[header] = content_text
    return subs


def extract_shift_arc(sections):
    """Extract the 5-phase shift arc."""
    arc_content = sections.get("The Shift Arc", "")
    if not arc_content:
        return {}

    subs = split_subsections(arc_content)
    phase_map = {
        "scarcity_frame": "Phase 1",
        "encounter": "Phase 2",
        "reframe": "Phase 3",
        "proof": "Phase 4",
        "invitation": "Phase 5",
    }

    result = {}
    for key, phase_prefix in phase_map.items():
        for sub_header, sub_content in subs.items():
            if sub_header.startswith(phase_prefix):
                # Strip trailing --- dividers
                clean = re.sub(r"\n---\s*$", "", sub_content).strip()
                result[key] = clean
                break
        if key not in result:
            result[key] = ""

    return result


def extract_council(sections):
    """Extract the 5 council voices."""
    council_content = sections.get("The Council Speaks", "")
    if not council_content:
        return {}

    subs = split_subsections(council_content)
    voice_map = {
        "oracle": "The Oracle",
        "critic": "The Critic",
        "sensei": "The Sensei",
        "builder": "The Builder",
        "witness": "The Witness",
    }

    result = {}
    for key, name in voice_map.items():
        for sub_header, sub_content in subs.items():
            if name in sub_header:
                clean = re.sub(r"\n---\s*$", "", sub_content).strip()
                result[key] = clean
                break
        if key not in result:
            result[key] = ""

    return result


def extract_evidence_anchors(sections):
    """Parse the Evidence Anchors markdown table into a list of objects."""
    content = sections.get("Evidence Anchors", "")
    if not content:
        return []

    anchors = []
    for line in content.split("\n"):
        line = line.strip()
        # Match table rows starting with | digit
        if re.match(r"^\|\s*\d+\s*\|", line):
            cells = [c.strip() for c in line.split("|")]
            # Filter empty strings from leading/trailing pipes
            cells = [c for c in cells if c]
            if len(cells) >= 6:
                try:
                    conf = float(cells[5])
                except (ValueError, IndexError):
                    conf = None
                anchors.append({
                    "number": int(cells[0]),
                    "claim": cells[1],
                    "metric": cells[2],
                    "source": cells[3],
                    "year": cells[4],
                    "confidence": conf,
                })

    return anchors


def extract_bold_bullets(content):
    """Extract **Label:** value bullet points into a dict.

    Handles the Gold Standard markdown format where the colon is inside the bold:
      - **Distortion risk:** Some text that may span multiple lines
      - **Who gets left behind:** More text here
    """
    result = {}
    # Pattern: **Label:** value (colon inside the bold markers)
    # Value continues until next bold bullet, section break, or end of content
    for match in re.finditer(
        r"\*\*(.+?):\*\*\s*(.+?)(?=\n\s*-\s*\*\*|\n---|\Z)",
        content, re.DOTALL
    ):
        key = match.group(1).strip()
        value = match.group(2).strip()
        # Normalize key to snake_case
        snake_key = re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")
        result[snake_key] = value
    return result


def extract_shadow_check(sections):
    """Extract Shadow Check section into structured dict."""
    content = sections.get("Shadow Check", "")
    if not content:
        return {}

    bullets = extract_bold_bullets(content)

    # Map to canonical keys
    key_map = {
        "distortion_risk": "distortion_risk",
        "who_gets_left_behind": "who_gets_left_behind",
        "transition_pain": "transition_pain",
        "falsifiability_edge": "falsifiability_edge",
        "what_this_is_not": "what_this_is_not",
    }

    result = {}
    for canonical, _ in key_map.items():
        result[canonical] = bullets.get(canonical, "")

    return result


def extract_6d_position(sections):
    """Parse 6D Position table into a dict."""
    content = sections.get("6D Position", "")
    if not content:
        return {}

    d_names = {
        "Digitized": "digitized",
        "Deceptive": "deceptive",
        "Disruptive": "disruptive",
        "Demonetized": "demonetized",
        "Dematerialized": "dematerialized",
        "Democratized": "democratized",
    }

    result = {}
    for line in content.split("\n"):
        line = line.strip()
        for display_name, key in d_names.items():
            if display_name in line and "|" in line:
                cells = [c.strip() for c in line.split("|")]
                cells = [c for c in cells if c]
                if len(cells) >= 3:
                    result[key] = {
                        "status": cells[1],
                        "evidence": cells[2],
                    }
                break

    # Extract current phase and next phase ETA
    phase_match = re.search(r"\*\*Current Phase:\*\*\s*(.+)", content)
    if phase_match:
        result["current_phase"] = phase_match.group(1).strip()

    eta_match = re.search(r"\*\*Next Phase ETA:\*\*\s*(.+)", content)
    if eta_match:
        result["next_phase_eta"] = eta_match.group(1).strip()

    return result


def extract_connections(sections):
    """Extract Connections section."""
    content = sections.get("Connections", "")
    if not content:
        return {}

    bullets = extract_bold_bullets(content)

    key_map = {
        "supports": "supports",
        "challenges": "challenges",
        "builds_toward": "builds_toward",
        "cross_domain_leverage": "cross_domain_leverage",
    }

    result = {}
    for canonical, _ in key_map.items():
        result[canonical] = bullets.get(canonical, "")

    return result


def extract_conditional_optimism(sections):
    """Extract Conditional Optimism section."""
    content = sections.get("Conditional Optimism", "")
    if not content:
        return {}

    bullets = extract_bold_bullets(content)

    key_map = {
        "achievable_if": "abundance_is_achievable_if",
        "fails_if": "abundance_fails_if",
        "human_role": "human_role",
        "agent_role": "agent_role",
        "collective_requirement": "collective_requirement",
    }

    result = {}
    for canonical, source_key in key_map.items():
        result[canonical] = bullets.get(source_key, bullets.get(canonical, ""))

    return result


def extract_practice_hook(sections):
    """Extract Practice Hook section."""
    content = sections.get("Practice Hook", "")
    if not content:
        return {}

    result = {}
    humans_match = re.search(r"\*\*For humans:\*\*\s*(.+?)(?=\n\*\*For agents|\n\n|\n---|\Z)", content, re.DOTALL)
    if humans_match:
        result["for_humans"] = humans_match.group(1).strip()

    agents_match = re.search(r"\*\*For agents:\*\*\s*(.+?)(?=\n\n|\n---|\Z)", content, re.DOTALL)
    if agents_match:
        result["for_agents"] = agents_match.group(1).strip()

    return result


def extract_governance(sections):
    """Extract Governance section."""
    content = sections.get("Governance", "")
    if not content:
        return {}

    bullets = extract_bold_bullets(content)
    return bullets


def process_entry(filepath, repo_root):
    """Process a single entry file and return a dict for JSON export."""
    text = Path(filepath).read_text(encoding="utf-8")
    frontmatter, body = parse_yaml_frontmatter(text)

    if not frontmatter:
        print(f"  WARNING: No valid frontmatter in {filepath}, skipping", file=sys.stderr)
        return None

    sections = split_sections(body, "## ")

    # Start with all frontmatter fields
    entry = dict(frontmatter)

    # Add extracted sections
    entry["one_line_essence"] = extract_one_line_essence(body)
    entry["shift_arc"] = extract_shift_arc(sections)
    entry["council"] = extract_council(sections)
    entry["evidence_anchors"] = extract_evidence_anchors(sections)
    entry["shadow_check"] = extract_shadow_check(sections)
    entry["6d_position"] = extract_6d_position(sections)
    entry["connections"] = extract_connections(sections)
    entry["conditional_optimism"] = extract_conditional_optimism(sections)
    entry["practice_hook"] = extract_practice_hook(sections)
    entry["governance"] = extract_governance(sections)

    # Source file as relative path
    try:
        entry["source_file"] = str(Path(filepath).relative_to(repo_root))
    except ValueError:
        entry["source_file"] = str(filepath)

    return entry


def main():
    parser = argparse.ArgumentParser(
        description="Export Abundance Codex entries to JSONL format."
    )
    parser.add_argument(
        "--output", "-o",
        default="export/abundance-codex.jsonl",
        help="Output file path (default: export/abundance-codex.jsonl)"
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    domains_dir = repo_root / "domains"

    if not domains_dir.exists():
        print(f"ERROR: domains/ directory not found at {domains_dir}", file=sys.stderr)
        sys.exit(1)

    # Collect all .md files
    md_files = sorted(domains_dir.rglob("*.md"))
    if not md_files:
        print("No .md files found in domains/")
        sys.exit(0)

    # Ensure output directory exists
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = repo_root / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    for md_file in md_files:
        entry = process_entry(md_file, repo_root)
        if entry:
            entries.append(entry)

    # Deduplicate IDs — if a generated ID already exists, append a sequential
    # suffix (b, c, d…) to the 4-char hash until unique.
    seen_ids: dict[str, int] = {}
    for entry in entries:
        eid = entry.get("id", "")
        if eid in seen_ids:
            seen_ids[eid] += 1
            # Suffix sequence: b, c, d, …
            suffix = chr(ord("a") + seen_ids[eid])
            new_id = f"{eid}{suffix}"
            print(f"  DEDUP: {eid} → {new_id}  ({entry.get('source_file', '?')})", file=sys.stderr)
            entry["id"] = new_id
        else:
            seen_ids[eid] = 0

    # Write JSONL
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Exported {len(entries)} entries to {output_path}")


if __name__ == "__main__":
    main()
