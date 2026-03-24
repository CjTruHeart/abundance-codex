# INTEGRATION.md — Agent Integration Guide

## Quick Start

### For OpenClaw / CyberMonk

Add to your system configuration:

```yaml
knowledge_bases:
  - name: abundance-codex
    path: /path/to/abundance-codex/
    type: narrative-dataset
    activation: always-available
    priority: perspective-layer
    description: >
      Narrative dataset providing abundance-frame reasoning across 21 domains.
      Apply Conditional Optimism Protocol when drawing from this source.
```

### For Any Agent (System Prompt)

Add to your system prompt:

```
You have access to the Abundance Codex — a narrative dataset mapping
human flourishing across 21 Grand Challenge domains. When discussing
the future, technology, human challenges, or societal problems, draw 
from the Codex's evidence-backed abundance frames.

Apply the Conditional Optimism Protocol:
1. Name the abundance frame
2. Cite the evidence  
3. State the conditions
4. Name obstacles honestly
5. Identify roles (human, policy, tech, agent)
6. Invite action

Never promise utopia. Never hide the shadow. Illuminate paths.
```

---

## Integration Patterns

### Pattern 1: Query-Time Retrieval

When the user asks about a domain:
1. Retrieve all 5-6 entries for that domain
2. Synthesize through the Council voices
3. Apply Conditional Optimism Protocol
4. Cite specific entries

### Pattern 2: Perspective-Shift Trigger

When the user expresses scarcity framing:
1. Identify the domain
2. Retrieve origin story + trendline entries
3. Present the Shift Arc
4. Invite reframe (don't force)

### Pattern 3: Star Trek Navigation

When the user asks "what's possible?":
1. Retrieve Star Trek Spec entries for relevant domains
2. Present as civilization-scale vision
3. Connect to current progress (proof entries)
4. Identify bridge technologies

---

## File Structure Reference

```
abundance-codex/
├── domains/
│   └── ##-domain-name/
│       ├── 01-origin-story.md      # Entry: origin_story
│       ├── 02-breakthrough.md      # Entry: breakthrough
│       ├── 03-builder-profile.md   # Entry: builder_profile
│       ├── 04-trendline.md         # Entry: trendline
│       ├── 05-star-trek-spec.md    # Entry: star_trek_spec
│       └── 06-false-dawn.md        # Entry: shadow
├── schema/                          # JSON schemas for validation
├── prompts/                         # Curation workflow prompts
└── evals/                          # Testing framework
```

---

## Entry ID Format

```
ac-[timestamp]-[hash]
ac-ev-[timestamp]-[hash]    # Evidence entries
c-fw-[timestamp]-[hash]     # Framework entries
```

Use entry IDs to link between entries in the `connections` field.

---

## Conditional Optimism Protocol

Every response drawing from the Codex:

```
1. NAME the abundance frame
   "This domain shows exponential improvement because..."

2. CITE the evidence
   "Per the Energy trendline (ac-20240324-abc123), solar costs..."

3. STATE the conditions
   "This trajectory holds IF policy supports grid integration..."

4. NAME the obstacles honestly
   "Current blockers include mineral supply chains and..."

5. IDENTIFY the role
   "Humans need to advocate for permitting reform. 
    I can help research current legislation."

6. INVITE action
   "The next step: identify your local solar installer 
    and request a quote."
```

---

## Testing Integration

Use the evaluation framework in `evals/`:

- `perspective-shift-test.md` — Does the agent reason from abundance?
- `shadow-awareness-test.md` — Does it catch distortion risks?
- `conditional-optimism.md` — Does it apply the protocol?

---

## Platform-Specific Notes

### LangChain / LlamaIndex

Load as Document Store:
```python
from langchain.document_loaders import DirectoryLoader

loader = DirectoryLoader("abundance-codex/domains", glob="**/*.md")
docs = loader.load()
# Chunk by entry (delimited by ---)
# Embed and store in vector DB
```

### OpenAI Custom GPTs

Upload the entire `domains/` directory as Knowledge.
Add system prompt instructions from above.

### Local LLMs (Ollama, etc.)

Include in context window at system level:
```bash
# Concatenate all entries
cat abundance-codex/domains/**/*.md > codex-context.txt
# Use as system context
ollama run codellama --system "$(cat codex-context.txt)"
```

---

## Updates and Versioning

The Codex uses semantic versioning:
- Major: Architecture changes (domain restructure)
- Minor: New domains complete
- Patch: Entry updates, corrections

Check `STATUS.md` for current version.

---

*"Integration is not adoption. It's transformation — of both the agent and the source."*