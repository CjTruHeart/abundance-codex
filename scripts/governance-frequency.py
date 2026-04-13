#!/usr/bin/env python3
"""Governance keyword frequency analysis across conditional_optimism fields.

Validates the claim in META-PATTERNS.md that governance appears in 90%+ of
conditional optimism statements across the Abundance Codex.

Usage:
    python scripts/governance-frequency.py
    python scripts/governance-frequency.py --output council-synthesis/governance-frequency-report.md
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


GOVERNANCE_KEYWORDS = [
    # Direct governance terms
    "regulation", "regulatory", "policy", "policies", "governance",
    "legislation", "legal", "law", "laws", "treaty", "treaties",
    "standards", "oversight", "enforcement", "compliance",
    # Institutional terms
    "institution", "institutional", "government", "agency", "agencies",
    "ministry", "department", "commission", "authority",
    # Governance actions
    "reform", "mandate", "ban", "prohibition",
    "licensing", "certification", "accreditation",
    "international cooperation", "multilateral", "bilateral",
    # Democratic/participation terms
    "democratic", "democracy", "voting", "election",
    "transparency", "accountability", "participation",
    "public trust", "social contract",
]

PILLAR_MAP = {
    "energy": "I Material Foundation",
    "food": "I Material Foundation",
    "water": "I Material Foundation",
    "shelter": "I Material Foundation",
    "health": "I Material Foundation",
    "environment": "I Material Foundation",
    "education": "II Human Capability",
    "longevity": "II Human Capability",
    "consciousness": "II Human Capability",
    "communication": "III Collective Coordination",
    "community": "III Collective Coordination",
    "governance": "III Collective Coordination",
    "security": "III Collective Coordination",
    "transportation": "III Collective Coordination",
    "economy": "III Collective Coordination",
    "manufacturing": "IV Production & Discovery",
    "computation-intelligence": "IV Production & Discovery",
    "co-creative-intelligence": "IV Production & Discovery",
    "science-engineering": "IV Production & Discovery",
    "space": "V Transcendent Frontier",
    "future-vision": "V Transcendent Frontier",
}


def get_co_text(entry: dict) -> str:
    """Extract full conditional_optimism text from an entry."""
    co = entry.get("conditional_optimism", {})
    if not co:
        return ""
    if isinstance(co, str):
        return co
    parts = []
    for key in ("achievable_if", "fails_if", "human_role", "agent_role", "collective_requirement"):
        v = co.get(key, "")
        if v:
            parts.append(v)
    return " ".join(parts)


def find_keywords(text: str) -> list[str]:
    """Return list of governance keywords found in text (case-insensitive)."""
    text_lower = text.lower()
    found = []
    for kw in GOVERNANCE_KEYWORDS:
        if re.search(r"\b" + re.escape(kw) + r"\b", text_lower):
            found.append(kw)
    return found


def main():
    parser = argparse.ArgumentParser(description="Governance keyword frequency analysis.")
    parser.add_argument(
        "--input", "-i",
        default="export/abundance-codex.jsonl",
        help="Input JSONL file",
    )
    parser.add_argument(
        "--output", "-o",
        default="council-synthesis/governance-frequency-report.md",
        help="Output report file",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    jsonl_path = repo_root / args.input
    output_path = repo_root / args.output

    # Load entries
    entries = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

    total = len(entries)
    keyword_counter = Counter()
    entries_with_co = 0
    entries_with_gov = 0
    zero_gov_entries = []
    pillar_stats: dict[str, dict[str, int]] = {}
    type_stats: dict[str, dict[str, int]] = {}

    for entry in entries:
        co_text = get_co_text(entry)
        domain = entry.get("domain", "unknown")
        entry_type = entry.get("entry_type", "unknown")
        pillar = PILLAR_MAP.get(domain, "Unknown")

        if not co_text.strip():
            continue

        entries_with_co += 1
        found = find_keywords(co_text)

        for kw in found:
            keyword_counter[kw] += 1

        if found:
            entries_with_gov += 1
        else:
            zero_gov_entries.append({
                "domain": domain,
                "entry_type": entry_type,
                "id": entry.get("id", "?"),
            })

        # Pillar stats
        if pillar not in pillar_stats:
            pillar_stats[pillar] = {"total": 0, "with_gov": 0}
        pillar_stats[pillar]["total"] += 1
        if found:
            pillar_stats[pillar]["with_gov"] += 1

        # Type stats
        if entry_type not in type_stats:
            type_stats[entry_type] = {"total": 0, "with_gov": 0}
        type_stats[entry_type]["total"] += 1
        if found:
            type_stats[entry_type]["with_gov"] += 1

    pct = (100 * entries_with_gov / entries_with_co) if entries_with_co else 0

    # Build report
    lines = [
        "# Governance Keyword Frequency Report",
        "",
        f"Generated from `{args.input}` ({total} entries).",
        "",
        "## Summary",
        "",
        f"- **Total entries:** {total}",
        f"- **Entries with conditional_optimism content:** {entries_with_co}/{total}",
        f"- **Entries with 1+ governance keyword:** {entries_with_gov}/{entries_with_co} ({pct:.1f}%)",
        f"- **Entries with zero governance keywords:** {len(zero_gov_entries)}",
        "",
    ]

    # Verdict
    if pct >= 90:
        lines.append(f"**Verdict:** The 90%+ claim is **validated** ({pct:.1f}%).")
    elif pct >= 60:
        lines.append(f"**Verdict:** The 90%+ claim needs softening — actual rate is {pct:.1f}%.")
    else:
        lines.append(f"**Verdict:** The 90%+ claim should be dropped — actual rate is {pct:.1f}%.")
    lines.append("")

    # Top 10 keywords
    lines.append("## Top 10 Governance Keywords")
    lines.append("")
    lines.append("| Rank | Keyword | Occurrences |")
    lines.append("|------|---------|-------------|")
    for rank, (kw, count) in enumerate(keyword_counter.most_common(10), 1):
        lines.append(f"| {rank} | {kw} | {count} |")
    lines.append("")

    # Pillar breakdown
    lines.append("## Breakdown by Pillar")
    lines.append("")
    lines.append("| Pillar | Entries w/ CO | w/ Gov Keywords | % |")
    lines.append("|--------|-------------|-----------------|---|")
    for pillar in sorted(pillar_stats.keys()):
        s = pillar_stats[pillar]
        p = (100 * s["with_gov"] / s["total"]) if s["total"] else 0
        lines.append(f"| {pillar} | {s['total']} | {s['with_gov']} | {p:.0f}% |")
    lines.append("")

    # Type breakdown
    lines.append("## Breakdown by Entry Type")
    lines.append("")
    lines.append("| Entry Type | Entries w/ CO | w/ Gov Keywords | % |")
    lines.append("|-----------|-------------|-----------------|---|")
    for et in sorted(type_stats.keys()):
        s = type_stats[et]
        p = (100 * s["with_gov"] / s["total"]) if s["total"] else 0
        lines.append(f"| {et} | {s['total']} | {s['with_gov']} | {p:.0f}% |")
    lines.append("")

    # Zero-governance entries
    if zero_gov_entries:
        lines.append("## Entries with Zero Governance Keywords")
        lines.append("")
        lines.append("These entries have conditional_optimism content but no governance-related keywords:")
        lines.append("")
        lines.append("| Domain | Entry Type | ID |")
        lines.append("|--------|-----------|-----|")
        for e in sorted(zero_gov_entries, key=lambda x: x["domain"]):
            lines.append(f"| {e['domain']} | {e['entry_type']} | {e['id']} |")
        lines.append("")

    report = "\n".join(lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(report)
    print(f"\nReport saved to {output_path}")


if __name__ == "__main__":
    main()
