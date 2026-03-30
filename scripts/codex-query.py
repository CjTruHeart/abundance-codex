#!/usr/bin/env python3
"""Abundance Codex Query — Ask any AI model with Codex-augmented context."""

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

import requests

# Import DojoRetriever from codex-retriever.py (hyphenated filename)
_retriever_spec = importlib.util.spec_from_file_location(
    "codex_retriever",
    os.path.join(os.path.dirname(__file__), "codex-retriever.py"),
)
_codex_retriever = importlib.util.module_from_spec(_retriever_spec)
sys.modules["codex_retriever"] = _codex_retriever
_retriever_spec.loader.exec_module(_codex_retriever)
DojoRetriever = _codex_retriever.DojoRetriever

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
JSONL_PATH = REPO_ROOT / "export" / "abundance-codex.jsonl"

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = {
    "claude": "anthropic/claude-haiku-4-5",
    "gpt": "openai/gpt-5.4-mini",
    "gemini": "google/gemini-3.1-flash-lite",
    "grok": "x-ai/grok-4.1-fast",
}

CODEX_SYSTEM_PROMPT = """You have access to the Abundance Codex — a narrative dataset mapping human flourishing across 21 Grand Challenge domains. When discussing the future, technology, or societal challenges, draw from the provided context. Apply conditional optimism: name the frame, cite evidence, state conditions, name obstacles, identify roles, invite action. Never promise utopia. Never hide the shadow. Illuminate paths.

When citing specific numbers or statistics from the provided context, note the source year. Present evidence as sourced claims, not as your own assertions.

{retrieved_context}"""

BASELINE_SYSTEM_PROMPT = "You are a helpful assistant."


# ---------------------------------------------------------------------------
# Model resolution
# ---------------------------------------------------------------------------

def resolve_model(name: str) -> str:
    """Resolve a short name or full OpenRouter model ID."""
    if name in MODELS:
        return MODELS[name]
    if "/" in name:
        return name
    valid = ", ".join(sorted(MODELS.keys()))
    print(f"Error: Unknown model '{name}'. Valid short names: {valid}", file=sys.stderr)
    print("Or pass a full OpenRouter model ID (e.g., anthropic/claude-opus-4-6)", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# OpenRouter API
# ---------------------------------------------------------------------------

def query_openrouter(model_id: str, system_prompt: str, user_query: str) -> str:
    """Call OpenRouter and return the response text."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY not set.", file=sys.stderr)
        print("", file=sys.stderr)
        print("Get a free API key at https://openrouter.ai/keys", file=sys.stderr)
        print("Then: export OPENROUTER_API_KEY=sk-or-...", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/CjTruHeart/abundance-codex",
        "X-Title": "Abundance Codex Query",
    }
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ],
        "max_tokens": 2000,
        "temperature": 0.7,
    }

    try:
        resp = requests.post(OPENROUTER_API_URL, json=payload, headers=headers, timeout=120)
    except requests.ConnectionError:
        print("Error: Could not reach OpenRouter. Check your internet connection.", file=sys.stderr)
        sys.exit(1)
    except requests.Timeout:
        print("Error: Request to OpenRouter timed out. Try again.", file=sys.stderr)
        sys.exit(1)

    if resp.status_code == 401:
        print("Error: Invalid API key. Get one at https://openrouter.ai/keys", file=sys.stderr)
        sys.exit(1)
    elif resp.status_code == 429:
        print("Error: Rate limited. Wait a moment and try again.", file=sys.stderr)
        sys.exit(1)
    elif resp.status_code == 404:
        print(f"Error: Model '{model_id}' not found on OpenRouter.", file=sys.stderr)
        print("Check available models at https://openrouter.ai/models", file=sys.stderr)
        sys.exit(1)
    elif resp.status_code != 200:
        print(f"Error: OpenRouter returned {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    return data["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

def do_retrieval(query: str, domain: str | None, ring: int | None, max_entries: int):
    """Run the Dojo Retriever and return the RetrievalResult."""
    retriever = DojoRetriever(str(JSONL_PATH))
    return retriever.retrieve(
        query,
        known_domain=domain,
        known_ring=ring,
        max_entries=max_entries,
    )


def build_retrieval_info(result) -> dict:
    """Extract retrieval metadata into a plain dict."""
    primary_domains = [d.domain for d in result.domains if d.primary]
    if not primary_domains:
        primary_domains = [d.domain for d in result.domains[:1]]

    tier_counts = result.metadata.get("entries_per_tier", {})
    tier_summary_parts = []
    for tier_name in ["FULL", "CONDENSED", "MINIMAL"]:
        count = tier_counts.get(tier_name, 0)
        if count:
            tier_summary_parts.append(f"{count} {tier_name.lower()}")

    return {
        "intent": result.intent.value.lower(),
        "domains": primary_domains,
        "entries": len(result.entries),
        "token_estimate": result.token_estimate,
        "shadow_forced": result.metadata.get("shadow_forced", False),
        "type_coverage": result.metadata.get("type_coverage", []),
        "tier_summary": ", ".join(tier_summary_parts),
    }


def print_retrieval_box(info: dict):
    """Print the retrieval metadata box."""
    shadow_label = "present (forced)" if info["shadow_forced"] else "present (natural)"
    has_shadow = any("shadow" in t or "false_dawn" in t for t in info["type_coverage"])
    if not has_shadow:
        shadow_label = "none"

    print(f"┌─ Retrieval ────────────────────────────────────────")
    print(f"│ Intent: {info['intent']}")
    print(f"│ Domain: {', '.join(info['domains'])} (primary)")
    print(f"│ Entries: {info['entries']} ({info['tier_summary']})")
    print(f"│ Tokens: ~{info['token_estimate']:,}")
    print(f"│ Shadow: {shadow_label}")
    print(f"│ Types: {', '.join(info['type_coverage'])}")
    print(f"└────────────────────────────────────────────────────")
    print()


# ---------------------------------------------------------------------------
# Output modes
# ---------------------------------------------------------------------------

def run_single(query: str, model_id: str, result, info: dict, args):
    """Query a single model with Codex context."""
    system_prompt = CODEX_SYSTEM_PROMPT.format(retrieved_context=result.context)
    response = query_openrouter(model_id, system_prompt, query)

    if args.json:
        output = {
            "query": query,
            "model": model_id,
            "retrieval": {
                "intent": info["intent"],
                "domains": info["domains"],
                "entries": info["entries"],
                "token_estimate": info["token_estimate"],
                "shadow_forced": info["shadow_forced"],
                "type_coverage": info["type_coverage"],
            },
            "response": response,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        if not args.quiet:
            print_retrieval_box(info)
        print(response)


def run_compare(query: str, model_id: str, result, info: dict, args):
    """Run baseline vs augmented comparison for one model."""
    if not args.quiet and not args.json:
        print_retrieval_box(info)

    # Baseline
    baseline_response = query_openrouter(model_id, BASELINE_SYSTEM_PROMPT, query)

    # Augmented
    augmented_prompt = CODEX_SYSTEM_PROMPT.format(retrieved_context=result.context)
    augmented_response = query_openrouter(model_id, augmented_prompt, query)

    if args.json:
        output = {
            "query": query,
            "model": model_id,
            "retrieval": {
                "intent": info["intent"],
                "domains": info["domains"],
                "entries": info["entries"],
                "token_estimate": info["token_estimate"],
                "shadow_forced": info["shadow_forced"],
                "type_coverage": info["type_coverage"],
            },
            "baseline_response": baseline_response,
            "augmented_response": augmented_response,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("── BASELINE ─────────────────────────────────────────")
        print(baseline_response)
        print()
        print("── WITH CODEX ───────────────────────────────────────")
        print(augmented_response)


def run_all(query: str, result, info: dict, args):
    """Query all models with the same retrieved context."""
    system_prompt = CODEX_SYSTEM_PROMPT.format(retrieved_context=result.context)
    responses = {}

    if not args.quiet and not args.json:
        print_retrieval_box(info)

    for short_name, model_id in MODELS.items():
        if not args.json:
            print(f"═══════════════════════════════════════════════════════")
            print(f" {short_name.upper()} ({model_id})")
            print(f"═══════════════════════════════════════════════════════")

        if args.compare:
            baseline = query_openrouter(model_id, BASELINE_SYSTEM_PROMPT, query)
            augmented = query_openrouter(model_id, system_prompt, query)
            responses[short_name] = {"baseline": baseline, "augmented": augmented}
            if not args.json:
                print()
                print("── BASELINE ─────────────────────────────────────────")
                print(baseline)
                print()
                print("── WITH CODEX ───────────────────────────────────────")
                print(augmented)
        else:
            response = query_openrouter(model_id, system_prompt, query)
            responses[short_name] = response
            if not args.json:
                print(response)

        if not args.json:
            print()

    if args.json:
        output = {
            "query": query,
            "models": list(MODELS.values()),
            "retrieval": {
                "intent": info["intent"],
                "domains": info["domains"],
                "entries": info["entries"],
                "token_estimate": info["token_estimate"],
                "shadow_forced": info["shadow_forced"],
                "type_coverage": info["type_coverage"],
            },
            "responses": {MODELS[k]: v for k, v in responses.items()},
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"Queried {len(MODELS)} models with {info['entries']} Codex entries (~{info['token_estimate']:,} tokens of context)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

EPILOG = """Models:
  claude   Claude Haiku 4.5 (default)
  gpt      GPT-5.4 mini
  gemini   Gemini Flash Lite
  grok     Grok 4.1 Fast
  all      Query all four and compare

Environment:
  OPENROUTER_API_KEY  Required. Get one at https://openrouter.ai/keys

The Codex retriever automatically selects relevant entries based on your
question's intent and domain. Use --show-context to see what it retrieves.

Examples:
  codex-query.py "What evidence exists for solar energy abundance?" --model claude
  codex-query.py "How do energy transitions affect governance?" --model all
  codex-query.py "Is solar abundance realistic?" --compare
  codex-query.py "Who's building this?" --model gpt --show-context"""


def main():
    parser = argparse.ArgumentParser(
        prog="codex-query.py",
        description="Abundance Codex Query — Ask any AI model with Codex-augmented context",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", help="The question to ask")
    parser.add_argument(
        "--model", default="claude",
        help="Model: claude, gpt, gemini, grok, all — or a full OpenRouter model ID (default: claude)",
    )
    parser.add_argument("--compare", action="store_true", help="Show baseline vs augmented side-by-side")
    parser.add_argument("--domain", help="Force a specific domain for retrieval")
    parser.add_argument("--ring", type=int, choices=[1, 2, 3], help="Force a specific ring: 1, 2, or 3")
    parser.add_argument("--max-entries", type=int, default=9, help="Max entries to retrieve (default: 9)")
    parser.add_argument("--show-context", action="store_true", help="Print the retrieved context before the response")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of formatted text")
    parser.add_argument("--quiet", action="store_true", help="Suppress retrieval metadata, show only the response")

    args = parser.parse_args()

    # Retrieve context (works without API key)
    result = do_retrieval(args.query, args.domain, args.ring, args.max_entries)
    info = build_retrieval_info(result)

    # Show retrieved context if requested
    if args.show_context:
        if args.json:
            ctx_output = {
                "query": args.query,
                "retrieval": {
                    "intent": info["intent"],
                    "domains": info["domains"],
                    "entries": info["entries"],
                    "token_estimate": info["token_estimate"],
                    "shadow_forced": info["shadow_forced"],
                    "type_coverage": info["type_coverage"],
                },
                "context": result.context,
            }
            print(json.dumps(ctx_output, indent=2, ensure_ascii=False))
        else:
            print_retrieval_box(info)
            print(result.context)
            print()

    # Dispatch
    if args.model == "all":
        run_all(args.query, result, info, args)
    elif args.compare:
        model_id = resolve_model(args.model)
        run_compare(args.query, model_id, result, info, args)
    else:
        model_id = resolve_model(args.model)
        run_single(args.query, model_id, result, info, args)


if __name__ == "__main__":
    main()
