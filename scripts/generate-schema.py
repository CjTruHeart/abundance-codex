#!/usr/bin/env python3
"""Generate JSON Schema from abundance-codex.jsonl.

Reads all entries, infers types and constraints, outputs export/schema.json.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

JSONL_PATH = Path("export/abundance-codex.jsonl")
SCHEMA_PATH = Path("export/schema.json")

ENTRY_TYPES = [
    "origin_story", "breakthrough", "builder_profile", "trendline",
    "contrast", "framework", "paradigm_seed", "shadow", "star_trek_spec",
    "grand_challenge", "false_dawn", "council_synthesis"
]

DOMAINS = [
    "energy", "food", "water", "shelter", "health", "environment",
    "education", "longevity", "consciousness", "communication",
    "community", "governance", "security", "transportation", "economy",
    "manufacturing", "computation-intelligence", "co-creative-intelligence",
    "science-engineering", "space", "future-vision"
]

STATUSES = ["forged", "curated", "seed", "archived"]


def infer_object_schema(values: list[dict]) -> dict:
    """Infer schema for a dict field from all observed values."""
    props = {}
    all_keys = set()
    for v in values:
        if isinstance(v, dict):
            all_keys.update(v.keys())

    for key in sorted(all_keys):
        sample_vals = [v.get(key) for v in values if isinstance(v, dict) and key in v]
        sample_vals = [sv for sv in sample_vals if sv is not None]
        if not sample_vals:
            props[key] = {"type": "string"}
        elif isinstance(sample_vals[0], str):
            props[key] = {"type": "string"}
        elif isinstance(sample_vals[0], (int, float)):
            props[key] = {"type": "number"}
        elif isinstance(sample_vals[0], bool):
            props[key] = {"type": "boolean"}
        elif isinstance(sample_vals[0], list):
            props[key] = {"type": "array"}
        elif isinstance(sample_vals[0], dict):
            props[key] = {"type": "object"}
        else:
            props[key] = {"type": "string"}

    return {"type": "object", "properties": props}


def main():
    if not JSONL_PATH.exists():
        print(f"Error: {JSONL_PATH} not found. Run export-to-jsonl.py first.")
        sys.exit(1)

    entries = []
    with open(JSONL_PATH) as f:
        for line in f:
            entries.append(json.loads(line.strip()))

    print(f"Read {len(entries)} entries from {JSONL_PATH}")

    # Build schema
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Abundance Codex Entry",
        "description": f"Schema for entries in abundance-codex.jsonl. Generated from {len(entries)} entries.",
        "type": "object",
        "required": [
            "id", "entry_type", "domain", "status", "created", "updated",
            "version", "confidence", "codex_version", "one_line_essence",
            "source_file"
        ],
        "properties": {
            "id": {
                "type": "string",
                "pattern": "^ac-\\d{8}-.{4}$",
                "description": "Unique entry identifier (format: ac-YYYYMMDD-XXXX)"
            },
            "entry_type": {
                "type": "string",
                "enum": ENTRY_TYPES,
                "description": "One of 12 canonical entry types"
            },
            "domain": {
                "type": "string",
                "enum": DOMAINS,
                "description": "Primary domain (one of 21)"
            },
            "domain_connections": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "domain": {"type": "string", "enum": DOMAINS},
                        "relationship": {
                            "type": "string",
                            "enum": ["enables", "depends_on", "produces", "challenges", "converges"]
                        },
                        "strength": {"type": "number", "minimum": 0, "maximum": 1},
                        "note": {"type": "string"}
                    }
                },
                "maxItems": 5,
                "description": "Cross-domain connections (max 5)"
            },
            "status": {
                "type": "string",
                "enum": STATUSES,
                "description": "Curation status"
            },
            "created": {
                "type": "string",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
                "description": "Creation date (YYYY-MM-DD)"
            },
            "updated": {
                "type": "string",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
                "description": "Last update date (YYYY-MM-DD)"
            },
            "version": {
                "type": "string",
                "description": "Entry revision (e.g., 1.0, 1.1)"
            },
            "confidence": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
                "description": "Evidence confidence score (0.0-1.0). Measured phenomena: 0.88-0.96. Conceptual frameworks: 0.65-0.78."
            },
            "codex_version": {
                "type": "string",
                "description": "Format version of the entry schema (e.g., 1.1, 2.1)"
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Free-form topic tags"
            },
            "co_author_model": {
                "type": "string",
                "description": "AI model co-author (e.g., claude-opus-4-6)"
            },
            "co_author_human": {
                "type": "string",
                "description": "Human curator (e.g., Cj TruHeart)"
            },
            "co_creative_partner": {
                "type": "string",
                "description": "AI co-creative partner (e.g., CyberMonk)"
            },
            "one_line_essence": {
                "type": "string",
                "description": "One-sentence summary of the entry"
            },
            "shift_arc": {
                "type": "object",
                "description": "Five-phase narrative arc",
                "properties": {
                    "scarcity_frame": {"type": "string"},
                    "encounter": {"type": "string"},
                    "reframe": {"type": "string"},
                    "proof": {"type": "string"},
                    "invitation": {"type": "string"}
                }
            },
            "council": {
                "type": "object",
                "description": "Five analytical voices",
                "properties": {
                    "oracle": {"type": "string"},
                    "critic": {"type": "string"},
                    "sensei": {"type": "string"},
                    "builder": {"type": "string"},
                    "witness": {"type": "string"}
                }
            },
            "evidence_anchors": {
                "type": "array",
                "description": "Cited evidence with sources",
                "items": {
                    "type": "object",
                    "properties": {
                        "number": {"type": ["integer", "string"]},
                        "claim": {"type": "string"},
                        "metric": {"type": "string"},
                        "source": {"type": "string"},
                        "year": {"type": "string"},
                        "confidence": {"type": ["number", "string"]}
                    }
                }
            },
            "shadow_check": {
                "type": "object",
                "description": "Risk assessment and honest critique",
                "properties": {
                    "distortion_risk": {"type": "string"},
                    "who_gets_left_behind": {"type": "string"},
                    "transition_pain": {"type": "string"},
                    "falsifiability_edge": {"type": "string"},
                    "what_this_is_not": {"type": "string"}
                }
            },
            "6d_position": {
                "type": "object",
                "description": "Position across six exponential disruption stages",
                "properties": {
                    "digitized": {"type": "string"},
                    "deceptive": {"type": "string"},
                    "disruptive": {"type": "string"},
                    "demonetized": {"type": "string"},
                    "dematerialized": {"type": "string"},
                    "democratized": {"type": "string"}
                }
            },
            "connections": {
                "type": "object",
                "description": "Thematic connections to other entries",
                "properties": {
                    "supports": {"type": "string"},
                    "challenges": {"type": "string"},
                    "builds_toward": {"type": "string"},
                    "cross_domain_leverage": {"type": "string"}
                }
            },
            "conditional_optimism": {
                "type": "object",
                "description": "Conditions for abundance vs failure",
                "properties": {
                    "achievable_if": {"type": "string"},
                    "fails_if": {"type": "string"},
                    "human_role": {"type": "string"},
                    "agent_role": {"type": "string"},
                    "collective_requirement": {"type": "string"}
                }
            },
            "practice_hook": {
                "type": "object",
                "description": "Action protocols for humans and agents",
                "properties": {
                    "for_humans": {"type": "string"},
                    "for_agents": {"type": "string"}
                }
            },
            "reasoning_scaffold": {
                "type": "object",
                "description": "Reasoning support structure (council_synthesis entries only). Empty object for base entries.",
                "properties": {
                    "scarcity_trap": {"type": "string"},
                    "reframe_chain": {"type": "string"},
                    "contrastive_pair": {"type": "string"}
                }
            },
            "governance": {
                "type": "object",
                "description": "Entry provenance and quality metadata",
                "properties": {
                    "source_type": {"type": "string"},
                    "evidence_quality": {"type": "string"},
                    "curator": {"type": "string"},
                    "last_verified": {"type": "string"},
                    "counter_sources": {"type": "string"},
                    "origin": {"type": "string"}
                }
            },
            "source_file": {
                "type": "string",
                "description": "Path to source markdown file in domains/"
            }
        }
    }

    # Validate schema matches actual data
    all_actual_fields = set()
    for e in entries:
        all_actual_fields.update(e.keys())

    schema_fields = set(schema["properties"].keys())
    missing_in_schema = all_actual_fields - schema_fields
    extra_in_schema = schema_fields - all_actual_fields

    if missing_in_schema:
        print(f"WARNING: Fields in JSONL but not in schema: {missing_in_schema}")
    if extra_in_schema:
        print(f"WARNING: Fields in schema but not in JSONL: {extra_in_schema}")

    with open(SCHEMA_PATH, "w") as f:
        json.dump(schema, f, indent=2)

    print(f"Schema written to {SCHEMA_PATH}")
    print(f"  {len(schema['properties'])} properties defined")
    print(f"  {len(schema['required'])} required fields")
    print(f"  {len(ENTRY_TYPES)} entry types")
    print(f"  {len(DOMAINS)} domains")


if __name__ == "__main__":
    main()
