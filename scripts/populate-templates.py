#!/usr/bin/env python3
"""
Populate Abundance Codex entry templates
"""
import os
from pathlib import Path

domains = {
    "03-water": "WATER",
    "04-health": "HEALTH",
    "05-education": "EDUCATION",
    "06-shelter": "SHELTER",
    "07-environment": "ENVIRONMENT",
    "08-security": "SECURITY",
    "09-governance": "GOVERNANCE",
    "10-economy": "ECONOMY",
    "11-resources": "RESOURCES",
    "12-space": "SPACE",
    "13-consciousness": "CONSCIOUSNESS",
    "14-longevity": "LONGEVITY",
    "15-transportation": "TRANSPORTATION",
    "16-communication": "COMMUNICATION",
    "17-computation-intelligence": "COMPUTATION-INTELLIGENCE",
    "18-co-evolutionary-intelligence": "CO-EVOLUTIONARY-INTELLIGENCE",
    "19-community": "COMMUNITY",
    "20-human-capability": "HUMAN-CAPABILITY",
    "21-future-vision": "FUTURE-VISION"
}

entry_types = [
    ("01-origin-story.md", "origin_story", "Origin Story"),
    ("02-breakthrough.md", "breakthrough", "Breakthrough"),
    ("03-builder-profile.md", "builder_profile", "Builder Profile"),
    ("04-trendline.md", "trendline", "Trendline"),
    ("05-star-trek-spec.md", "star_trek_spec", "Star Trek Spec"),
    ("06-false-dawn.md", "shadow", "False Dawn")
]

template = """---
id: "ac-[TIMESTAMP]-[HASH]"
entry_type: "{entry_type}"
domain: "{domain}"
status: "template"
created: "2026-03-24"
---

# {domain_pretty}: {entry_pretty}
**Domain:** {domain_pretty} | **Type:** {entry_pretty} | **Status:** Template

---

## One-Line Essence
> [Awaiting curation]

---

## The Council Speaks

### 🔮 The Oracle

### 🗡️ The Critic

### 🧘 The Sensei

### 🔧 The Builder

### 👁️ The Witness

---

*Template | Awaiting Curation*
"""

base_path = Path.home() / ".openclaw/workspace/projects/abundance-codex/domains"

for domain_dir, domain_name in domains.items():
    for filename, entry_type, entry_pretty in entry_types:
        filepath = base_path / domain_dir / filename
        domain_pretty = domain_name.replace("-", " ").title()
        content = template.format(
            entry_type=entry_type,
            domain=domain_name,
            domain_pretty=domain_pretty,
            entry_pretty=entry_pretty
        )
        with open(filepath, 'w') as f:
            f.write(content)

print(f"Populated {len(domains) * len(entry_types)} entry templates")
