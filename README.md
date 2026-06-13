# Genesis Engine

> A cross-disciplinary **collision engine**: it fuses the whole of human knowledge to
> discover the deepest *questions* about the origin of the universe and life — the
> questions a higher intelligence would ask.

It does not claim answers. It gathers researchers from many fields on one graph, lets
them debate, and finds where the **structural tension** lies — the gaps no single
field can resolve alone — then forges them into fundamental questions. It inherits
MiroFish's three backbones (shared temporal graph = blackboard / round accumulation =
stigmergy / post-hoc synthesis) but replaces the social simulation with a
**co-discovery loop**.

Two modes:
- **Ask Mode** (primary): a user enters a research question → relevant agents activate →
  collide → a grounded report + glow provenance showing which real researcher's paper
  drove each idea. (See `architecture.md`.)
- **Explore Mode** (this CLI): the engine discovers its own fundamental questions
  (Tension/Root Scan). A great offline, zero-dependency demo.

---

## Quick start

```bash
# 1) Mock mode — zero deps, zero keys. Just runs (demo / offline).
python run.py

# 2) Demo pacing + save a report
python run.py --slow 0.4 --out examples/last_run.md

# 3) Live mode — Claude brain
pip install -r requirements.txt
cp .env.example .env   # fill ANTHROPIC_API_KEY, ANTHROPIC_MODEL
python run.py --live --rounds 5

# Ingest real papers/authors from OpenAlex (43 disciplines, cached for RAG)
python ingest.py
python gen_roster_md.py   # regenerate researcher.md from the fetched data
```

If `anthropic` is missing or no key is set, it automatically falls back to mock mode.

### Options
| Flag | Meaning | Default |
|---|---|---|
| `--live` | use the Claude brain | (mock) |
| `--rounds N` | co-discovery rounds | 3 |
| `--top K` | how many Genesis Questions to surface | 5 |
| `--out PATH` | write a markdown report | (none) |
| `--slow S` | delay S seconds between events (stage pacing) | 0 |
| `--model SLUG` | override the Anthropic model slug | env |

---

## Pipeline (Explore Mode)

```
Seed researcher corpus (origin-touching fields)
        │  each = an epistemic persona + paper-grounded "moves"
        ▼
Shared temporal graph (blackboard) ──────────────────┐
        │                                            │ repeat N rounds
  ① Researcher agents: read the graph, write grounded claims
  ② Bridge Detector: light up cross-field "confluence nodes"
  ③ Skeptic (R2): rebut leaps/constraint violations → contradicts
  ④ Graph (R1): on conflict, expire old beliefs (knowledge evolves)
        └────────────────────────────────────────────┘
        ▼
Tension Scanner: score orphan-bridge / contradiction / cross-centrality
        ▼
Referee (R3): tension nodes → synthesize fundamental questions + scores
              (depth / cross-disciplinarity / tractability / novelty)
        ▼
🃏 Genesis Question Cards
```

### The "referee" is not one judge but three (distributed referee)
MiroFish has no central decision-maker. We inherit that and split verification three ways:
- **R1 graph contradiction** — `graph.invalidate_conflicts()`. When a new claim conflicts with an old belief, the old one is marked `expired`. Knowledge evolves.
- **R2 Skeptic** — in-loop real-time rebuttal (correlation↔causation leaps, constraint violations).
- **R3 Referee** — post-hoc scoring card. Decides "done" without a human.

---

## Module map

| File | Role |
|---|---|
| `genesis/graph.py` | Shared temporal graph. Facts (edges) carry `valid/expired` — a dependency-free reimplementation of Zep's temporality. |
| `genesis/corpus.py` | Seed researcher personas + per-round moves + fallback questions. **The only swap point.** |
| `genesis/disciplines.py` / `seeds.py` | 43-discipline taxonomy / curated origin-relevant researcher seeds for OpenAlex. |
| `genesis/ingest.py` | OpenAlex ingestion: real authors + papers + abstracts, cached to `data/corpus/`. |
| `genesis/llm.py` | Brain interface. `MockBrain` (deterministic) / `ClaudeBrain`. |
| `genesis/agents.py` | Researcher agents — read the graph, write grounded traces (stigmergy). |
| `genesis/bridge.py` | Confluence-node detection + in-loop Skeptic. |
| `genesis/tension.py` | **Core** — scores question-worthy structural tension. |
| `genesis/referee.py` | Tension → question synthesis + scoring. |
| `genesis/cards.py` | Genesis Question Card rendering (terminal / markdown). |
| `genesis/loop.py` | N-round orchestration. |
| `run.py` | CLI + streaming trace + report. |
| `ingest.py` / `gen_roster_md.py` | OpenAlex pipeline CLI / regenerate `researcher.md` from fetched data. |

---

## Why this is not "just an LLM chat"
- **Graph persistence**: a chemist's claim in round r enters the biologist's reading context in round r+1 → cumulative build-up, not a one-shot exchange.
- **Waiting for structural meetings**: a bridge is not fired *until* a confluence node exists → questions made by structure, not forced consensus.
- **Knowledge evolution**: validity (valid/expired) retires old assumptions as the graph grows.
- **Distributed verification**: Skeptic + contradiction detection structurally suppress sycophancy.

---

## Roadmap — this does not end at the hackathon

**Today (MVP)**: the full mechanism runs on a seed corpus + a deterministic mock brain. In live mode, the Claude brain generates questions dynamically.

**Tomorrow (hackathon)**: live brain on stage. Prove reproducibility by dropping in a new field/problem on the spot.

**Beyond (real fusion research)**:
1. **Ingest real papers** — replace the seed corpus with real researcher corpora via OpenAlex/Semantic Scholar (the engine is unchanged). *(Pipeline already built: `ingest.py`.)*
2. **Expand fields** — math, linguistics, neuroscience, thermodynamics… the more fields, the sharper the confluence nodes.
3. **Track questions** — re-run discovered Genesis Questions over time and watch which collides with ever more fields (= the most fundamental).
4. **Falsification-design stage** — for each question, auto-propose the observation/experiment that would settle it (turn tractability into experiment design).

The goal is simple: **to forge, ourselves, the question we would ask a higher intelligence.**
