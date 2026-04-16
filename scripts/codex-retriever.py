#!/usr/bin/env python3
"""Abundance Codex retriever — loads JSONL, classifies intent, retrieves & extracts passages."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CodexEntry:
    """Single Abundance Codex entry parsed from one JSONL line."""

    # --- identity ---
    id: str = ""
    entry_type: str = ""
    domain: str = ""
    status: str = ""
    created: str = ""
    updated: str = ""
    version: str = ""
    confidence: float = 0.0
    codex_version: str = ""

    # --- authorship ---
    co_author_model: str = ""
    co_author_human: str = ""
    co_creative_partner: str = ""

    # --- content ---
    tags: list[str] = field(default_factory=list)
    one_line_essence: str = ""

    # --- structured sections ---
    shift_arc: dict[str, str] = field(default_factory=dict)
    council: dict[str, str] = field(default_factory=dict)
    evidence_anchors: list[dict[str, Any]] = field(default_factory=list)
    shadow_check: dict[str, str] = field(default_factory=dict)
    six_d_position: dict[str, Any] = field(default_factory=dict)
    connections: dict[str, str] = field(default_factory=dict)
    conditional_optimism: dict[str, str] = field(default_factory=dict)
    practice_hook: dict[str, str] = field(default_factory=dict)
    reasoning_scaffold: dict[str, str] = field(default_factory=dict)
    governance: dict[str, Any] = field(default_factory=dict)

    # --- graph / meta ---
    domain_connections: list[dict[str, Any]] = field(default_factory=list)
    source_file: str = ""

    # --- computed ---
    token_estimate: int = 0

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> CodexEntry:
        """Build a CodexEntry from a raw JSON dict, handling missing/renamed keys."""
        # Map 6d_position → six_d_position (not a valid Python identifier)
        six_d = d.get("6d_position", {}) or {}

        return cls(
            id=d.get("id", ""),
            entry_type=d.get("entry_type", ""),
            domain=d.get("domain", ""),
            status=d.get("status", ""),
            created=d.get("created", ""),
            updated=d.get("updated", ""),
            version=d.get("version", ""),
            confidence=float(d.get("confidence", 0.0)),
            codex_version=d.get("codex_version", ""),
            co_author_model=d.get("co_author_model", ""),
            co_author_human=d.get("co_author_human", ""),
            co_creative_partner=d.get("co_creative_partner", ""),
            tags=d.get("tags", []) or [],
            one_line_essence=d.get("one_line_essence", ""),
            shift_arc=d.get("shift_arc", {}) or {},
            council=d.get("council", {}) or {},
            evidence_anchors=d.get("evidence_anchors", []) or [],
            shadow_check=d.get("shadow_check", {}) or {},
            six_d_position=six_d,
            connections=d.get("connections", {}) or {},
            conditional_optimism=d.get("conditional_optimism", {}) or {},
            practice_hook=d.get("practice_hook", {}) or {},
            reasoning_scaffold=d.get("reasoning_scaffold", {}) or {},
            governance=d.get("governance", {}) or {},
            domain_connections=d.get("domain_connections", []) or [],
            source_file=d.get("source_file", ""),
            token_estimate=len(json.dumps(d, ensure_ascii=False)) // 4,
        )


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------

@dataclass
class CodexIndex:
    """In-memory indexes over the full Codex.

    Primary key is source_file (unique per JSONL line). The by_id index is a
    multimap because the current export has duplicate IDs across domains.
    """

    entries: dict[str, CodexEntry] = field(default_factory=dict)       # source_file → entry
    by_id: dict[str, list[CodexEntry]] = field(default_factory=dict)   # id → entries (may be >1)
    by_domain: dict[str, list[CodexEntry]] = field(default_factory=dict)
    by_type: dict[str, list[CodexEntry]] = field(default_factory=dict)
    connection_graph: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    @property
    def total_entries(self) -> int:
        return len(self.entries)

    @property
    def total_edges(self) -> int:
        return sum(len(edges) for edges in self.connection_graph.values())

    def strongest_connections(self, n: int = 10) -> list[dict[str, Any]]:
        """Return the top-n connections by strength across the whole graph."""
        all_edges: list[dict[str, Any]] = []
        for source_domain, edges in self.connection_graph.items():
            for edge in edges:
                all_edges.append({"source_domain": source_domain, **edge})
        all_edges.sort(key=lambda e: float(e.get("strength", 0)), reverse=True)
        return all_edges[:n]


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def load_codex(jsonl_path: str) -> CodexIndex:
    """Load the Abundance Codex JSONL export into a CodexIndex."""
    path = Path(jsonl_path)
    if not path.exists():
        print(f"ERROR: {jsonl_path} not found", file=sys.stderr)
        sys.exit(1)

    idx = CodexIndex()

    with path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"WARN: skipping line {lineno} — {exc}", file=sys.stderr)
                continue

            entry = CodexEntry.from_dict(raw)

            # --- primary index (source_file is unique per line) ---
            idx.entries[entry.source_file] = entry

            # --- id index (multimap — export has duplicate IDs) ---
            idx.by_id.setdefault(entry.id, []).append(entry)

            # --- domain index ---
            idx.by_domain.setdefault(entry.domain, []).append(entry)

            # --- type index ---
            idx.by_type.setdefault(entry.entry_type, []).append(entry)

            # --- connection graph ---
            for conn in entry.domain_connections:
                target = conn.get("domain", "")
                if not target:
                    continue
                idx.connection_graph.setdefault(entry.domain, []).append({
                    "target_domain": target,
                    "relationship": conn.get("relationship", ""),
                    "strength": float(conn.get("strength", 0)),
                    "source_entry_id": entry.id,
                })

    # --- flag duplicate IDs ---
    dupes = {eid: ents for eid, ents in idx.by_id.items() if len(ents) > 1}
    if dupes:
        print(f"\n[codex-retriever] WARNING: {len(dupes)} duplicate IDs in JSONL:", file=sys.stderr)
        for eid, ents in dupes.items():
            domains = [e.domain for e in ents]
            print(f"  {eid} appears {len(ents)}x in domains: {domains}", file=sys.stderr)

    # --- load summary to stderr ---
    print(f"\n[codex-retriever] Loaded {idx.total_entries} entries", file=sys.stderr)
    print(f"  Unique IDs: {len(idx.by_id)}  (duplicate IDs: {len(dupes)})", file=sys.stderr)
    print(f"  Domains: {len(idx.by_domain)}", file=sys.stderr)
    print(f"  Entry types: {sorted(idx.by_type.keys())}", file=sys.stderr)
    print(f"  Connection graph edges: {idx.total_edges}", file=sys.stderr)

    return idx


# ---------------------------------------------------------------------------
# CLI test mode
# ---------------------------------------------------------------------------

def _test_load(jsonl_path: str) -> None:
    """Run load + diagnostics, print results to stdout."""
    idx = load_codex(jsonl_path)

    print(f"\n{'='*60}")
    print(f"  Abundance Codex — Load Test")
    print(f"{'='*60}")

    # --- totals ---
    print(f"\nTotal entries: {idx.total_entries}")

    # --- per-domain counts ---
    print(f"\n--- Per-Domain Counts ({len(idx.by_domain)} domains) ---")
    for domain in sorted(idx.by_domain):
        print(f"  {domain:30s}  {len(idx.by_domain[domain]):>3}")

    # --- entry type distribution ---
    print(f"\n--- Entry Type Distribution ---")
    for etype in sorted(idx.by_type, key=lambda t: len(idx.by_type[t]), reverse=True):
        print(f"  {etype:30s}  {len(idx.by_type[etype]):>3}")

    # --- top 10 connections ---
    print(f"\n--- Top 10 Strongest Connections ({idx.total_edges} total edges) ---")
    for edge in idx.strongest_connections(10):
        print(
            f"  {edge['source_domain']:20s} → {edge['target_domain']:20s}"
            f"  strength={edge['strength']:.2f}"
            f"  ({edge['relationship']})"
            f"  [{edge['source_entry_id']}]"
        )

    # --- duplicate ID warning ---
    dupes = {eid: ents for eid, ents in idx.by_id.items() if len(ents) > 1}
    if dupes:
        print(f"\n--- Duplicate IDs ({len(dupes)}) ---")
        for eid, ents in sorted(dupes.items()):
            domains = [e.domain for e in ents]
            print(f"  {eid} x{len(ents)}: {domains}")

    # --- missing critical fields ---
    critical = ("id", "domain", "entry_type", "one_line_essence")
    missing: list[str] = []
    for src, entry in idx.entries.items():
        for fld in critical:
            if not getattr(entry, fld, ""):
                missing.append(f"  {src}: missing {fld}")
    if missing:
        print(f"\n--- Entries with Missing Critical Fields ---")
        for m in missing:
            print(m)
    else:
        print(f"\n✓ All entries have critical fields (id, domain, entry_type, one_line_essence)")

    print()


# ---------------------------------------------------------------------------
# Retrieval pipeline
# ---------------------------------------------------------------------------

class QueryIntent(Enum):
    FACTUAL = "FACTUAL"
    ANALYTICAL = "ANALYTICAL"
    STRATEGIC = "STRATEGIC"
    ADVERSARIAL = "ADVERSARIAL"
    NARRATIVE = "NARRATIVE"


@dataclass
class ScoredDomain:
    domain: str
    confidence: float
    primary: bool


@dataclass
class ScoredEntry:
    entry: CodexEntry
    score: float
    source: str  # "primary" | "secondary" | "graph" | "shadow_pull" | "type_fill"


SHADOW_TYPES = {"shadow", "false_dawn"}
EVIDENCE_TYPES = {"origin_story", "breakthrough", "trendline"}
FRAMEWORK_TYPES = {"framework", "contrast", "paradigm_seed", "star_trek_spec", "grand_challenge"}
SYNTHESIS_TYPES = {"council_synthesis"}

DOMAIN_DESCRIPTORS: dict[str, list[str]] = {
    "energy": ["energy", "solar", "electricity", "power", "fossil", "renewable", "nuclear", "grid", "watt", "battery"],
    "food": ["food", "hunger", "agriculture", "farming", "nutrition", "crop", "protein", "fermentation", "calorie", "meat"],
    "water": ["water", "desalination", "aquifer", "drought", "sanitation", "freshwater", "irrigation", "purification", "ocean"],
    "shelter": ["shelter", "housing", "construction", "building", "home", "rent", "affordable", "prefab", "modular", "zoning"],
    "health": ["health", "medicine", "disease", "therapy", "diagnostic", "hospital", "pharma", "vaccine", "clinical", "patient"],
    "longevity": ["longevity", "aging", "lifespan", "senescence", "rejuvenation", "telomere", "mortality", "centenarian", "geroscience"],
    "education": ["education", "learning", "school", "teacher", "student", "curriculum", "literacy", "tutor", "university", "pedagogy"],
    "communication": ["communication", "internet", "language", "translation", "media", "connectivity", "broadband", "journalism", "speech"],
    "transportation": ["transportation", "transport", "vehicle", "autonomous", "ev", "mobility", "traffic", "rail", "flight", "logistics"],
    "economy": ["economy", "economic", "market", "trade", "wealth", "poverty", "income", "gdp", "financial", "inequality", "ubi"],
    "governance": ["governance", "government", "democracy", "policy", "regulation", "civic", "institution", "law", "vote", "transparency"],
    "security": ["security", "defense", "conflict", "war", "peace", "threat", "military", "cyber", "weapon", "terrorism", "safety"],
    "environment": ["environment", "climate", "carbon", "biodiversity", "ecosystem", "pollution", "conservation", "emission", "species", "deforestation"],
    "community": ["community", "social", "belonging", "neighborhood", "civic", "collective", "trust", "cooperation", "village", "solidarity"],
    "consciousness": ["consciousness", "awareness", "mindfulness", "meditation", "cognition", "perception", "wellbeing", "mental", "psyche", "contemplative"],
    "space": ["space", "orbit", "satellite", "mars", "lunar", "asteroid", "rocket", "launch", "cosmos", "extraterrestrial"],
    "manufacturing": ["manufacturing", "factory", "3d printing", "production", "supply chain", "robotics", "automation", "fabrication", "material"],
    "computation-intelligence": ["computation", "ai", "artificial intelligence", "machine learning", "algorithm", "computing", "chip", "semiconductor", "neural", "data"],
    "co-creative-intelligence": ["co-creative", "collaboration", "human-ai", "partnership", "augment", "synergy", "creative", "collective intelligence"],
    "science-engineering": ["science", "engineering", "research", "experiment", "physics", "chemistry", "biology", "innovation", "lab", "discovery"],
    "future-vision": ["future", "vision", "utopia", "abundance", "exponential", "singularity", "civilization", "post-scarcity", "paradigm", "transformation"],
}


def classify_intent(query: str) -> QueryIntent:
    q = query.lower()
    adversarial = ["never", "won't work", "impossible", "fantasy", "hype", "scam", "failed", "can't"]
    if any(kw in q for kw in adversarial):
        return QueryIntent.ADVERSARIAL
    strategic = ["should", "recommend", "what would you", "how can i", "what should", "first step", "highest-leverage", "wants to", "prioritize"]
    if any(kw in q for kw in strategic):
        return QueryIntent.STRATEGIC
    analytical = ["where does", "how do you reconcile", "what conditions", "what would need to be true", "what could go wrong", "trajectory", "realistic", "framing", "tension", "pattern", "distinguish"]
    if any(kw in q for kw in analytical):
        return QueryIntent.ANALYTICAL
    narrative = ["tell me", "story of", "how did", "what happened when", "history of"]
    if any(kw in q for kw in narrative):
        return QueryIntent.NARRATIVE
    return QueryIntent.FACTUAL


def identify_domains(query: str, index: CodexIndex) -> list[ScoredDomain]:
    q = query.lower()
    scored: list[ScoredDomain] = []
    for domain, keywords in DOMAIN_DESCRIPTORS.items():
        if domain not in index.by_domain:
            continue
        hits = sum(1 for kw in keywords if kw in q)
        if hits > 0:
            confidence = min(0.95, 0.5 + hits * 0.15)
            scored.append(ScoredDomain(domain=domain, confidence=confidence, primary=(hits >= 2)))
    scored.sort(key=lambda d: d.confidence, reverse=True)
    if not scored:
        return [ScoredDomain("future-vision", 0.5, True)]
    return scored


def retrieve_candidates(
    index: CodexIndex,
    domains: list[ScoredDomain],
    intent: QueryIntent,
) -> list[ScoredEntry]:
    seen_ids: set[str] = set()
    candidates: list[ScoredEntry] = []

    def _add(entry: CodexEntry, score: float, source: str) -> None:
        if entry.id in seen_ids:
            return
        seen_ids.add(entry.id)
        candidates.append(ScoredEntry(entry=entry, score=score, source=source))

    # Phase A — primary domains
    for sd in domains:
        if not sd.primary:
            continue
        for entry in index.by_domain.get(sd.domain, []):
            if entry.confidence < 0.75:
                continue  # confidence floor: skip speculative/low-evidence entries
            _add(entry, sd.confidence * entry.confidence, "primary")

    # Phase B — secondary domains
    for sd in domains:
        if sd.primary:
            continue
        for entry in index.by_domain.get(sd.domain, []):
            if entry.confidence < 0.75:
                continue  # confidence floor: skip speculative/low-evidence entries
            _add(entry, sd.confidence * entry.confidence * 0.8, "secondary")

    # Phase C — graph expansion (1-hop from primary domains)
    covered_domains = {sd.domain for sd in domains}
    new_graph_domains = 0
    for sd in domains:
        if not sd.primary:
            continue
        if new_graph_domains >= 3:
            break
        for edge in index.connection_graph.get(sd.domain, []):
            target = edge["target_domain"]
            if target in covered_domains:
                continue
            if edge["strength"] < 0.7:
                continue
            covered_domains.add(target)
            new_graph_domains += 1
            if new_graph_domains > 3:
                break
            target_entries = sorted(
                [e for e in index.by_domain.get(target, []) if e.confidence >= 0.75],
                key=lambda e: e.confidence,
                reverse=True,
            )[:2]
            for entry in target_entries:
                _add(entry, edge["strength"] * entry.confidence * 0.6, "graph")

    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates[:20]


def enforce_type_coverage(
    candidates: list[ScoredEntry],
    intent: QueryIntent,
    index: CodexIndex,
    max_entries: int = 9,
) -> list[ScoredEntry]:
    requirements: dict[QueryIntent, tuple[bool, int]] = {
        QueryIntent.FACTUAL: (False, 3),
        QueryIntent.ANALYTICAL: (True, 2),
        QueryIntent.STRATEGIC: (True, 2),
        QueryIntent.ADVERSARIAL: (True, 2),
        QueryIntent.NARRATIVE: (False, 3),
    }
    shadow_required, max_per_type = requirements[intent]

    # Pass 1: select by score order with type cap
    type_counts: dict[str, int] = {}
    selected: list[ScoredEntry] = []
    for c in candidates:
        et = c.entry.entry_type
        if type_counts.get(et, 0) >= max_per_type:
            continue
        selected.append(c)
        type_counts[et] = type_counts.get(et, 0) + 1
        if len(selected) >= max_entries:
            break

    # Pass 2: shadow force-pull
    shadow_forced = False
    if shadow_required:
        has_shadow = any(s.entry.entry_type in SHADOW_TYPES for s in selected)
        if not has_shadow:
            shadow_entry: ScoredEntry | None = None
            # Try from candidates first
            for c in candidates:
                if c.entry.entry_type in SHADOW_TYPES and c not in selected:
                    shadow_entry = c
                    break
            # Fallback: search globally
            if shadow_entry is None:
                best: CodexEntry | None = None
                best_conf = -1.0
                for st in SHADOW_TYPES:
                    for e in index.by_type.get(st, []):
                        if e.confidence > best_conf:
                            best = e
                            best_conf = e.confidence
                if best is not None:
                    shadow_entry = ScoredEntry(entry=best, score=best.confidence * 0.5, source="shadow_pull")
            if shadow_entry is not None:
                shadow_forced = True
                if len(selected) >= max_entries:
                    selected.pop()  # remove lowest-scored (last after sort)
                selected.append(shadow_entry)

    selected.sort(key=lambda c: c.score, reverse=True)
    return selected


# ---------------------------------------------------------------------------
# Passage extraction
# ---------------------------------------------------------------------------

class ExtractionTier(Enum):
    FULL = "FULL"
    CONDENSED = "CONDENSED"
    MINIMAL = "MINIMAL"


@dataclass
class ExtractedEntry:
    entry: CodexEntry
    score: float
    source: str
    tier: ExtractionTier
    passage: str


def _truncate(text: str, max_chars: int) -> str:
    """Cut at last sentence boundary before max_chars, or append '...'."""
    if not text or len(text) <= max_chars:
        return text
    cut = text[:max_chars]
    last_dot = cut.rfind(". ")
    if last_dot > max_chars // 2:
        return cut[: last_dot + 1]
    return cut.rstrip() + "..."


def extract_passage(entry: CodexEntry, tier: ExtractionTier, intent: QueryIntent) -> str:
    """Build a text passage from a CodexEntry at the given extraction tier."""
    e = entry
    lines: list[str] = []

    if tier == ExtractionTier.MINIMAL:
        lines.append(f"### {e.one_line_essence or e.id} [{e.entry_type}]")
        if e.one_line_essence:
            lines.append(f"> {e.one_line_essence}")
        lines.append(f"Domain: {e.domain} | Confidence: {e.confidence}")
        conn_domains = []
        for dc in e.domain_connections[:3]:
            name = dc.get("domain", "")
            if name:
                conn_domains.append(name)
        if conn_domains:
            lines.append(f"Connections: {', '.join(conn_domains)}")
        return "\n".join(lines)

    if tier == ExtractionTier.CONDENSED:
        lines.append(f"### {e.one_line_essence or e.id} [{e.entry_type}]")
        if e.one_line_essence:
            lines.append(f"> {e.one_line_essence}")
        lines.append(f"Domain: {e.domain} | Confidence: {e.confidence}")
        lines.append("")

        # Top 3 evidence anchors
        if e.evidence_anchors:
            lines.append("**Evidence:**")
            for ea in e.evidence_anchors[:3]:
                claim = ea.get("claim", "")
                metric = ea.get("metric", "")
                source = ea.get("source", "")
                year = ea.get("year", "")
                if claim:
                    lines.append(f"- {claim} — {metric} ({source}, {year})")
            lines.append("")

        # Council voices by intent
        council = e.council
        if council:
            lines.append("**Council:**")
            if intent == QueryIntent.FACTUAL:
                v = council.get("builder", "")
                if v:
                    lines.append(f"- **Builder:** {_truncate(v, 200)}")
            elif intent == QueryIntent.ANALYTICAL:
                v = council.get("oracle", "")
                if v:
                    lines.append(f"- **Oracle:** {_truncate(v, 300)}")
                v = council.get("critic", "")
                if v:
                    lines.append(f"- **Critic:** {_truncate(v, 200)}")
            elif intent in (QueryIntent.STRATEGIC, QueryIntent.ADVERSARIAL):
                v = council.get("critic", "")
                if v:
                    lines.append(f"- **Critic:** {_truncate(v, 200)}")
                v = council.get("builder", "")
                if v:
                    lines.append(f"- **Builder:** {_truncate(v, 200)}")
            elif intent == QueryIntent.NARRATIVE:
                v = council.get("witness", "")
                if v:
                    lines.append(f"- **Witness:** {_truncate(v, 200)}")
            lines.append("")

        # Shadow check excerpts
        sc = e.shadow_check
        if sc:
            parts = []
            if sc.get("who_gets_left_behind"):
                parts.append(f"- **Who gets left behind:** {sc['who_gets_left_behind']}")
            if sc.get("falsifiability_edge"):
                parts.append(f"- **Falsifiability edge:** {sc['falsifiability_edge']}")
            if parts:
                lines.append("**Shadow:**")
                lines.extend(parts)
                lines.append("")

        # Conditional optimism excerpts
        co = e.conditional_optimism
        if co:
            parts = []
            if co.get("achievable_if"):
                parts.append(f"- **Achievable if:** {co['achievable_if']}")
            if co.get("fails_if"):
                parts.append(f"- **Fails if:** {co['fails_if']}")
            if parts:
                lines.append("**Conditions:**")
                lines.extend(parts)
                lines.append("")

        return "\n".join(lines)

    # --- FULL tier ---
    lines.append(f"## {e.one_line_essence or e.id} [{e.entry_type}]")
    if e.one_line_essence:
        lines.append(f"> {e.one_line_essence}")
    lines.append(f"Domain: {e.domain} | Confidence: {e.confidence}")
    lines.append("")

    # Shift Arc by intent
    arc = e.shift_arc
    if arc:
        lines.append("**Shift Arc:**")
        phase_keys: list[str] = []
        if intent == QueryIntent.FACTUAL:
            phase_keys = ["encounter", "proof"]
        elif intent in (QueryIntent.ANALYTICAL, QueryIntent.STRATEGIC, QueryIntent.ADVERSARIAL):
            phase_keys = ["scarcity_frame", "reframe", "proof"]
        elif intent == QueryIntent.NARRATIVE:
            phase_keys = ["scarcity_frame", "encounter", "reframe", "proof", "invitation"]
        for pk in phase_keys:
            v = arc.get(pk, "")
            if v:
                lines.append(f"- **{pk.replace('_', ' ').title()}:** {_truncate(v, 800)}")
        lines.append("")

    # All council voices (truncated to keep FULL tier ~3000-5000 tokens)
    council = e.council
    if council:
        lines.append("**Council Speaks:**")
        for voice in ("oracle", "critic", "sensei", "builder", "witness"):
            v = council.get(voice, "")
            if v:
                lines.append(f"- **{voice.title()}:** {_truncate(v, 600)}")
        lines.append("")

    # All evidence anchors
    if e.evidence_anchors:
        lines.append("**Evidence Anchors:**")
        for ea in e.evidence_anchors:
            claim = ea.get("claim", "")
            metric = ea.get("metric", "")
            source = ea.get("source", "")
            year = ea.get("year", "")
            conf = ea.get("confidence")
            conf_str = ""  # suppress internal confidence metadata to prevent leakage into responses
            if claim:
                lines.append(f"- {claim} — {metric} ({source}, {year}{conf_str})")
        lines.append("")

    # Full shadow check
    sc = e.shadow_check
    if sc:
        parts = []
        for key in ("distortion_risk", "who_gets_left_behind", "transition_pain", "falsifiability_edge", "what_this_is_not"):
            v = sc.get(key, "")
            if v:
                parts.append(f"- **{key.replace('_', ' ').title()}:** {_truncate(v, 400)}")
        if parts:
            lines.append("**Shadow Check:**")
            lines.extend(parts)
            lines.append("")

    # 6D current phase
    sixd = e.six_d_position
    if sixd and sixd.get("current_phase"):
        lines.append(f"**6D Phase:** {sixd['current_phase']}")
        lines.append("")

    # Full conditional optimism
    co = e.conditional_optimism
    if co:
        parts = []
        for key in ("achievable_if", "fails_if", "human_role", "agent_role", "collective_requirement"):
            v = co.get(key, "")
            if v:
                parts.append(f"- **{key.replace('_', ' ').title()}:** {v}")
        if parts:
            lines.append("**Conditional Optimism:**")
            lines.extend(parts)
            lines.append("")

    # Practice hook
    ph = e.practice_hook
    if ph:
        parts = []
        if ph.get("for_humans"):
            parts.append(f"- **For humans:** {ph['for_humans']}")
        if ph.get("for_agents"):
            parts.append(f"- **For agents:** {ph['for_agents']}")
        if parts:
            lines.append("**Practice Hook:**")
            lines.extend(parts)
            lines.append("")

    return "\n".join(lines)


def extract_passage_council_synthesis(
    entry: CodexEntry, tier: ExtractionTier, intent: QueryIntent
) -> str:
    """Extract passage from a council_synthesis entry with R3-optimized priorities.

    Key differences from standard extraction:
    - Reasoning Scaffold and Agent Practice Hook are depth-locked at FULL
    - Evidence anchors deprioritized (R1/R2 already work)
    - Contrastive Pair and Reframe Chain preserved even at MINIMAL tier
    """
    e = entry
    lines: list[str] = []
    sections_included: list[str] = []

    if tier == ExtractionTier.MINIMAL:
        lines.append(f"### {e.one_line_essence or e.id} [council_synthesis]")
        if e.one_line_essence:
            lines.append(f"> {e.one_line_essence}")
        lines.append(f"Domain: {e.domain} | Confidence: {e.confidence}")
        sections_included.append("one_line_essence")

        # Reframe Chain — highest density reasoning content
        rs = e.reasoning_scaffold
        if rs.get("reframe_chain"):
            lines.append("")
            lines.append("**Reframe Chain:**")
            lines.append(rs["reframe_chain"])
            sections_included.append("reframe_chain")

        # Contrastive Pair — highest impact-per-token
        if rs.get("contrastive_pair"):
            lines.append("")
            lines.append("**Contrastive Pair:**")
            lines.append(rs["contrastive_pair"])
            sections_included.append("contrastive_pair")

        return "\n".join(lines)

    if tier == ExtractionTier.CONDENSED:
        lines.append(f"### {e.one_line_essence or e.id} [council_synthesis]")
        if e.one_line_essence:
            lines.append(f"> {e.one_line_essence}")
        lines.append(f"Domain: {e.domain} | Confidence: {e.confidence}")
        lines.append("")
        sections_included.append("one_line_essence")

        # Reasoning Scaffold — DEPTH-LOCKED at FULL
        rs = e.reasoning_scaffold
        if rs:
            lines.append("**Reasoning Scaffold:**")
            if rs.get("scarcity_trap"):
                lines.append(f"\n*Scarcity Trap:* {rs['scarcity_trap']}")
                sections_included.append("scarcity_trap")
            if rs.get("reframe_chain"):
                lines.append(f"\n*Reframe Chain:* {rs['reframe_chain']}")
                sections_included.append("reframe_chain")
            if rs.get("contrastive_pair"):
                lines.append(f"\n*Contrastive Pair:* {rs['contrastive_pair']}")
                sections_included.append("contrastive_pair")
            lines.append("")

        # Agent Practice Hook — DEPTH-LOCKED at FULL
        ph = e.practice_hook
        if ph.get("for_agents"):
            lines.append("**Agent Practice Hook:**")
            lines.append(ph["for_agents"])
            lines.append("")
            sections_included.append("agent_practice_hook")

        # Critic (truncated — secondary for R3)
        council = e.council
        if council.get("critic"):
            lines.append(f"**Critic:** {_truncate(council['critic'], 300)}")
            lines.append("")
            sections_included.append("critic")

        # Top 2 evidence anchors (deprioritized)
        if e.evidence_anchors:
            lines.append("**Evidence:**")
            for ea in e.evidence_anchors[:2]:
                claim = ea.get("claim", "")
                metric = ea.get("metric", "")
                source = ea.get("source", "")
                if claim:
                    lines.append(f"- {claim} — {metric} ({source})")
            lines.append("")
            sections_included.append("evidence_anchors")

        return "\n".join(lines)

    # --- FULL tier ---
    # Use standard FULL extraction, then append Reasoning Scaffold
    lines.append(f"## {e.one_line_essence or e.id} [council_synthesis]")
    if e.one_line_essence:
        lines.append(f"> {e.one_line_essence}")
    lines.append(f"Domain: {e.domain} | Confidence: {e.confidence}")
    lines.append("")
    sections_included.append("one_line_essence")

    # Shift Arc
    arc = e.shift_arc
    if arc:
        lines.append("**Shift Arc:**")
        phase_keys = ["scarcity_frame", "reframe", "proof"]
        for pk in phase_keys:
            v = arc.get(pk, "")
            if v:
                lines.append(f"- **{pk.replace('_', ' ').title()}:** {_truncate(v, 800)}")
        lines.append("")
        sections_included.append("shift_arc")

    # All council voices
    council = e.council
    if council:
        lines.append("**Council:**")
        for voice in ("oracle", "critic", "sensei", "builder", "witness"):
            v = council.get(voice, "")
            if v:
                lines.append(f"- **{voice.title()}:** {_truncate(v, 600)}")
        lines.append("")
        sections_included.append("council")

    # All evidence anchors
    if e.evidence_anchors:
        lines.append("**Evidence Anchors:**")
        for ea in e.evidence_anchors:
            claim = ea.get("claim", "")
            metric = ea.get("metric", "")
            source = ea.get("source", "")
            year = ea.get("year", "")
            conf = ea.get("confidence")
            conf_str = ""  # suppress internal confidence metadata to prevent leakage into responses
            if claim:
                lines.append(f"- {claim} — {metric} ({source}, {year}{conf_str})")
        lines.append("")
        sections_included.append("evidence_anchors")

    # Full shadow check
    sc = e.shadow_check
    if sc:
        parts = []
        for key in ("distortion_risk", "who_gets_left_behind", "transition_pain",
                     "falsifiability_edge", "what_this_is_not"):
            v = sc.get(key, "")
            if v:
                parts.append(f"- **{key.replace('_', ' ').title()}:** {_truncate(v, 400)}")
        if parts:
            lines.append("**Shadow Check:**")
            lines.extend(parts)
            lines.append("")
            sections_included.append("shadow_check")

    # Full conditional optimism
    co = e.conditional_optimism
    if co:
        parts = []
        for key in ("achievable_if", "fails_if", "human_role", "agent_role",
                     "collective_requirement"):
            v = co.get(key, "")
            if v:
                parts.append(f"- **{key.replace('_', ' ').title()}:** {v}")
        if parts:
            lines.append("**Conditional Optimism:**")
            lines.extend(parts)
            lines.append("")
            sections_included.append("conditional_optimism")

    # Reasoning Scaffold — FULL (depth-locked, always included)
    rs = e.reasoning_scaffold
    if rs:
        lines.append("**Reasoning Scaffold:**")
        if rs.get("scarcity_trap"):
            lines.append(f"\n*Scarcity Trap:* {rs['scarcity_trap']}")
            sections_included.append("scarcity_trap")
        if rs.get("reframe_chain"):
            lines.append(f"\n*Reframe Chain:* {rs['reframe_chain']}")
            sections_included.append("reframe_chain")
        if rs.get("contrastive_pair"):
            lines.append(f"\n*Contrastive Pair:* {rs['contrastive_pair']}")
            sections_included.append("contrastive_pair")
        lines.append("")

    # Practice Hooks — FULL (both human and agent)
    ph = e.practice_hook
    if ph:
        parts = []
        if ph.get("for_humans"):
            parts.append(f"- **For humans:** {ph['for_humans']}")
            sections_included.append("human_practice_hook")
        if ph.get("for_agents"):
            parts.append(f"- **For agents:** {ph['for_agents']}")
            sections_included.append("agent_practice_hook")
        if parts:
            lines.append("**Practice Hook:**")
            lines.extend(parts)
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Strategic ordering
# ---------------------------------------------------------------------------

def order_by_intent(entries: list[ScoredEntry], intent: QueryIntent) -> list[ScoredEntry]:
    """Reorder entries by type category based on intent."""
    shadow = [e for e in entries if e.entry.entry_type in SHADOW_TYPES]
    evidence = [e for e in entries if e.entry.entry_type in EVIDENCE_TYPES]
    framework = [e for e in entries if e.entry.entry_type in FRAMEWORK_TYPES]
    other = [e for e in entries if e.entry.entry_type not in SHADOW_TYPES | EVIDENCE_TYPES | FRAMEWORK_TYPES]

    order_map: dict[QueryIntent, list[list[ScoredEntry]]] = {
        QueryIntent.FACTUAL: [evidence, framework, other, shadow],
        QueryIntent.ANALYTICAL: [framework, evidence, shadow, other],
        QueryIntent.STRATEGIC: [shadow, evidence, framework, other],
        QueryIntent.ADVERSARIAL: [shadow, evidence, framework, other],
        QueryIntent.NARRATIVE: [evidence, shadow, framework, other],
    }

    result: list[ScoredEntry] = []
    for group in order_map[intent]:
        result.extend(group)
    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

@dataclass
class RetrievalResult:
    context: str
    entries: list[ExtractedEntry]
    intent: QueryIntent
    domains: list[ScoredDomain]
    token_estimate: int
    metadata: dict[str, Any]


class DojoRetriever:
    """Main retriever — the public API for the Abundance Codex."""

    def __init__(self, jsonl_path: str):
        self.index = load_codex(jsonl_path)

    def retrieve(
        self,
        query: str,
        known_domain: str | None = None,
        known_ring: int | None = None,
        max_entries: int = 9,
    ) -> RetrievalResult:
        # Layer 0 — Intent
        if known_ring is not None:
            ring_map = {1: QueryIntent.FACTUAL, 2: QueryIntent.ANALYTICAL, 3: QueryIntent.STRATEGIC}
            intent = ring_map.get(known_ring, classify_intent(query))
        else:
            intent = classify_intent(query)

        # Layer 0 — Domains
        if known_domain:
            domains = [ScoredDomain(known_domain, 0.95, True)]
        else:
            domains = identify_domains(query, self.index)

        # Layer 1 — Candidates
        candidates = retrieve_candidates(self.index, domains, intent)

        # Layer 2 — Type coverage
        selected = enforce_type_coverage(candidates, intent, self.index, max_entries)

        shadow_forced = any(s.source == "shadow_pull" for s in selected)
        graph_expanded = any(s.source == "graph" for s in selected)

        # Layer 2.5 — Reasoning slot for council_synthesis
        # On STRATEGIC/ADVERSARIAL intents, reserve one slot for the matched
        # domain's council_synthesis entry.  This ensures R3 prompts see the
        # Reasoning Scaffold / Agent Practice Hook payload.
        reasoning_slot_used = False
        if intent in (QueryIntent.STRATEGIC, QueryIntent.ADVERSARIAL):
            primary_domain = domains[0].domain if domains else None
            if primary_domain:
                cs_candidates = [
                    e for e in self.index.by_type.get("council_synthesis", [])
                    if e.domain == primary_domain
                ]
                if cs_candidates:
                    cs_entry = cs_candidates[0]
                    # Remove council_synthesis from content slots if already selected
                    selected = [
                        s for s in selected
                        if s.entry.entry_type != "council_synthesis"
                    ]
                    # Cap content at max_entries - 1 to make room
                    selected = selected[: max_entries - 1]
                    # Add as reasoning slot (high score ensures good tier)
                    selected.append(ScoredEntry(cs_entry, 1.0, "reasoning_slot"))
                    reasoning_slot_used = True

        # Layer 3 — Passage extraction (by score rank)
        selected.sort(key=lambda c: c.score, reverse=True)
        extracted: list[ExtractedEntry] = []
        for rank, se in enumerate(selected):
            if rank < 3:
                tier = ExtractionTier.FULL
            elif rank < 6:
                tier = ExtractionTier.CONDENSED
            else:
                tier = ExtractionTier.MINIMAL
            if se.entry.entry_type in SYNTHESIS_TYPES:
                passage = extract_passage_council_synthesis(se.entry, tier, intent)
            else:
                passage = extract_passage(se.entry, tier, intent)
            extracted.append(ExtractedEntry(
                entry=se.entry,
                score=se.score,
                source=se.source,
                tier=tier,
                passage=passage,
            ))

        # Layer 4 — Strategic ordering
        # Build ScoredEntry list from extracted for ordering, then re-associate
        scored_for_order = [ScoredEntry(ex.entry, ex.score, ex.source) for ex in extracted]
        ordered_scored = order_by_intent(scored_for_order, intent)
        # Re-map extracted entries to match new order
        ext_by_id = {ex.entry.id: ex for ex in extracted}
        ordered_extracted = [ext_by_id[se.entry.id] for se in ordered_scored]

        # Assemble context string
        primary_domains = [d.domain for d in domains if d.primary]
        if not primary_domains:
            primary_domains = [d.domain for d in domains[:1]]
        unique_types = sorted({ex.entry.entry_type for ex in ordered_extracted})

        ctx_lines = [
            "# Abundance Codex — Retrieved Context",
            f"**Query intent:** {intent.value}",
            f"**Primary domain(s):** {', '.join(primary_domains)}",
            f"**Entries retrieved:** {len(ordered_extracted)}",
            f"**Type coverage:** {', '.join(unique_types)}",
            "---",
        ]
        for ex in ordered_extracted:
            ctx_lines.append(ex.passage)
            ctx_lines.append("---")

        context = "\n".join(ctx_lines)

        # Metadata
        tier_counts: dict[str, int] = {}
        for ex in ordered_extracted:
            tier_counts[ex.tier.value] = tier_counts.get(ex.tier.value, 0) + 1

        # Council synthesis retrieval log
        cs_log = None
        for ex in ordered_extracted:
            if ex.entry.entry_type == "council_synthesis":
                cs_log = {
                    "domain": ex.entry.domain,
                    "entry_id": ex.entry.id,
                    "slot_type": "reasoning" if ex.source == "reasoning_slot" else "content",
                    "extraction_tier": ex.tier.value,
                    "token_count": len(ex.passage) // 4,
                }
                break

        metadata = {
            "retriever_version": "dojo-v1.1",
            "shadow_forced": shadow_forced,
            "graph_expanded": graph_expanded,
            "reasoning_slot_used": reasoning_slot_used,
            "type_coverage": unique_types,
            "entries_per_tier": tier_counts,
            "council_synthesis": cs_log,
        }

        return RetrievalResult(
            context=context,
            entries=ordered_extracted,
            intent=intent,
            domains=domains,
            token_estimate=len(context) // 4,
            metadata=metadata,
        )


# ---------------------------------------------------------------------------
# CLI test modes (legacy)
# ---------------------------------------------------------------------------

def _test_retrieve(jsonl_path: str, query: str) -> None:
    idx = load_codex(jsonl_path)

    intent = classify_intent(query)
    domains = identify_domains(query, idx)
    candidates = retrieve_candidates(idx, domains, intent)
    selected = enforce_type_coverage(candidates, intent, idx)

    has_shadow = any(s.entry.entry_type in SHADOW_TYPES for s in selected)
    shadow_forced = any(s.source == "shadow_pull" for s in selected)

    print(f"\n{'='*60}")
    print(f"  Retrieval Test")
    print(f"{'='*60}")
    print(f"\nQuery: {query}")
    print(f"Intent: {intent.value}")

    print(f"\nDomains ({len(domains)}):")
    for d in domains:
        label = "PRIMARY" if d.primary else "secondary"
        print(f"  {d.domain:30s}  conf={d.confidence:.2f}  [{label}]")

    print(f"\nCandidates before type filter: {len(candidates)}")
    print(f"Selected entries: {len(selected)}")
    print(f"Shadow present: {has_shadow}  (force-pulled: {shadow_forced})")

    print(f"\n--- Selected Entries ---")
    for i, s in enumerate(selected, 1):
        print(
            f"  {i:2d}. {s.entry.id:28s}  {s.entry.entry_type:16s}"
            f"  {s.entry.domain:28s}  score={s.score:.3f}  [{s.source}]"
        )
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Abundance Codex retriever — DojoRetriever v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  %(prog)s --retrieve "What evidence exists that solar energy costs are declining?"
  %(prog)s --retrieve "Where does solar stand?" --domain energy --ring 2
  %(prog)s --retrieve "How do transitions affect governance?" --format json --stats
  %(prog)s --test-load
  %(prog)s --test-retrieve "solar energy costs"
""",
    )
    parser.add_argument(
        "--test-load",
        action="store_true",
        help="Load the JSONL export and print diagnostics",
    )
    parser.add_argument(
        "--test-retrieve",
        metavar="QUERY",
        help="(Legacy) Run retrieval pipeline on a query and print tabular results",
    )
    parser.add_argument(
        "--retrieve",
        metavar="QUERY",
        help="Run full retrieval with passage extraction",
    )
    parser.add_argument("--domain", help="Force a known domain")
    parser.add_argument("--ring", type=int, choices=[1, 2, 3], help="Force ring (1=factual, 2=analytical, 3=strategic)")
    parser.add_argument("--max-entries", type=int, default=9, help="Max entries to retrieve (default: 9)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", dest="out_format", help="Output format (default: markdown)")
    parser.add_argument("--stats", action="store_true", help="Print retrieval stats after output")
    parser.add_argument(
        "--jsonl",
        default=str(Path(__file__).resolve().parent.parent / "export" / "abundance-codex.jsonl"),
        help="Path to the JSONL export (default: export/abundance-codex.jsonl)",
    )
    args = parser.parse_args()

    if args.test_load:
        _test_load(args.jsonl)
    elif args.test_retrieve:
        _test_retrieve(args.jsonl, args.test_retrieve)
    elif args.retrieve:
        retriever = DojoRetriever(args.jsonl)
        result = retriever.retrieve(
            query=args.retrieve,
            known_domain=args.domain,
            known_ring=args.ring,
            max_entries=args.max_entries,
        )
        if args.out_format == "markdown":
            print(result.context)
        else:
            out = {
                "intent": result.intent.value,
                "domains": [{"domain": d.domain, "confidence": d.confidence, "primary": d.primary} for d in result.domains],
                "token_estimate": result.token_estimate,
                "metadata": result.metadata,
                "entries": [
                    {
                        "id": ex.entry.id,
                        "entry_type": ex.entry.entry_type,
                        "domain": ex.entry.domain,
                        "score": round(ex.score, 4),
                        "source": ex.source,
                        "tier": ex.tier.value,
                        "passage_length": len(ex.passage),
                    }
                    for ex in result.entries
                ],
            }
            print(json.dumps(out, indent=2, ensure_ascii=False))

        if args.stats:
            m = result.metadata
            print(f"\n--- Retrieval Stats ---", file=sys.stderr)
            print(f"  Token estimate: {result.token_estimate}", file=sys.stderr)
            print(f"  Entries per tier: {m['entries_per_tier']}", file=sys.stderr)
            print(f"  Type coverage: {m['type_coverage']}", file=sys.stderr)
            print(f"  Shadow forced: {m['shadow_forced']}", file=sys.stderr)
            print(f"  Graph expanded: {m['graph_expanded']}", file=sys.stderr)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
