# Genesis — Cross-Disciplinary Research Debate Engine

> Convene a live panel of real researchers over their *actual* papers. Watch them
> debate your question, discover novel cross-disciplinary hypotheses, and see exactly
> whose paper sparked each idea — with DOIs you can verify.

Genesis does not assert answers. It surfaces **grounded, novel, testable leads**:
- **Grounded**: every claim cites a real paper (DOI)
- **Novel**: an OpenAlex Novelty Audit checks whether the bridge is already published
- **Testable**: the brief ends with a falsifiable next experiment

> Genesis is an AGPL-3.0 fork of [MiroFish](https://github.com/666ghj/MiroFish).
> MiroFish's three core ideas are inherited (shared temporal graph / stigmergic
> round accumulation / post-hoc synthesis) and the social-simulation semantics are
> replaced with a researcher-debate pipeline.

---

## Quick start

```bash
# 1) Copy and fill env variables
cp .env.example .env
#    Fill ANTHROPIC_API_KEY and ZEP_API_KEY

# 2) Import real researcher papers (one per discipline, 43 disciplines)
python backend/scripts/import_openalex_corpus.py --auto
# Note the project_id printed

# 3) Start backend + frontend
docker-compose up       # OR:
cd backend && python run.py   # backend :5001
cd frontend && npm run dev    # frontend :3000

# 4) Open http://localhost:3000
#    Use the project_id from step 2 to build the graph
```

## How it works (5-step pipeline)

1. **Graph Build** — OpenAlex papers ingested → Zep temporal knowledge graph (real researcher + concept + claim nodes)
2. **Environment** — your research question routes to relevant researcher agents + RAG load
3. **Simulation** — agents debate: each claim is a graph edge; bridges light up as confluence nodes
4. **Report** — Opus 4.8 synthesizes a hypothesis brief (grounded, cited, contribution-tracked)
5. **Interact** — click a glowing node → live interview with the real researcher (grounded in their papers)

After the report: **Novelty Audit** searches OpenAlex for prior work making the same cross-field bridge → emits NOVEL / PARTIAL / KNOWN with nearest DOIs.

## What's different from the original MiroFish

| Layer | MiroFish original | Genesis |
|---|---|---|
| Agents | social-media user personas | real researchers + paper RAG |
| Graph edges | posts, likes, follows | claims, rebuttals, bridges |
| Report framing | future-prediction, opinion sim | cross-disciplinary hypothesis brief |
| Post-report | — | OpenAlex Novelty Audit |
| Viz | standard graph | glow by contribution (influence) |
| Models | gpt-4o-mini (all) | sonnet-4.5 (agents) + Opus 4.5 (synthesis) |

## Env variables

See `.env.example`. Minimum required:
- `ANTHROPIC_API_KEY` — Claude (sonnet for agents, Opus for synthesis)
- `ZEP_API_KEY` — Zep cloud temporal graph

## License

GNU Affero General Public License v3.0 (AGPL-3.0).

Genesis is a fork of [MiroFish](https://github.com/666ghj/MiroFish), originally
licensed under AGPL-3.0. This derivative work is also released under AGPL-3.0.
The full license text is in `LICENSE`.

Copyright (C) 2024 original MiroFish contributors
Copyright (C) 2026 Seyeong Han — Genesis fork
