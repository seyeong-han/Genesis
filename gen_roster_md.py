#!/usr/bin/env python3
"""Generate researcher.md from the real OpenAlex data cached in data/corpus/.

Reproducible: `python ingest.py` then `python gen_roster_md.py`. Nothing here is
hand-written about the researchers — every name, paper, year, and citation count is
read straight from the ingested OpenAlex records.
"""

from __future__ import annotations

import json
from pathlib import Path

from genesis.disciplines import slugify
from genesis.seeds import SEEDS

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "data" / "corpus"
OUT = ROOT / "researcher.md"


def load(discipline: str) -> dict | None:
    p = CORPUS / f"{slugify(discipline)}.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def doi_link(doi: str | None) -> str:
    if not doi:
        return "—"
    url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
    return f"[DOI]({url})"


def main() -> int:
    domains: list[str] = []
    for domain, *_ in SEEDS:
        if domain not in domains:
            domains.append(domain)

    records = {d: load(d) for *_, d, _, _ in [(x[0], x[1], x[2], x[3], x[4]) for x in SEEDS]}
    # map discipline -> (domain, lens) from SEEDS
    meta = {disc: (dom, lens) for dom, disc, _a, _t, lens in SEEDS}

    loaded = {disc: load(disc) for _dom, disc, *_ in SEEDS}
    n_total = sum(1 for v in loaded.values() if v)
    n_abstract = sum(1 for v in loaded.values() if v and v["papers"] and v["papers"][0].get("abstract"))

    lines: list[str] = []
    w = lines.append

    w("# Researcher Roster — Real OpenAlex Agents (Demo)")
    w("")
    w("> Generated from live OpenAlex data by `ingest.py` + `gen_roster_md.py`. Every")
    w("> researcher, paper, year, and citation count below is real and fetched from")
    w("> OpenAlex (no API key needed). Each becomes one Genesis Engine agent grounded")
    w("> in that paper's abstract (RAG). Demo scope: **one researcher + one paper per")
    w("> discipline**; scale up with `ingest.py --papers N` and a larger seed list.")
    w("")
    w("## How this roster was built")
    w("")
    w("1. **Seed** — one origin-relevant modern researcher per discipline (`genesis/seeds.py`).")
    w("   We seed by researcher (not by raw concept-citation) because OpenAlex's top-cited")
    w("   work *inside a concept* is usually a methods/tooling paper or a name collision")
    w("   (e.g. the \"Architecture\" concept's top paper is a neural-network paper).")
    w("2. **Verify + fetch** — resolve each name to a real OpenAlex author (name-matched,")
    w("   not just most-cited, to avoid collisions), then pull their top-cited paper that")
    w("   has an abstract, steered by a topic hint toward their origin-relevant work.")
    w("3. **Ground** — cache the paper's abstract to `data/corpus/<discipline>.json` for RAG.")
    w("")
    w(f"- Disciplines populated: **{n_total}/{len(SEEDS)}**")
    w(f"- Papers with abstract (RAG-ready): **{n_abstract}/{n_total}**")
    w(f"- Demo agents prepared: **{n_total}** (1 per discipline)")
    w("")
    w("---")
    w("")

    for dom in domains:
        w(f"## {dom}")
        w("")
        w("| Discipline | Researcher | Institution | Top paper (OpenAlex, cited-by) | Link | Origin lens |")
        w("|---|---|---|---|---|---|")
        for d2, disc, _a, _t, lens in SEEDS:
            if d2 != dom:
                continue
            rec = loaded.get(disc)
            if not rec or not rec["papers"]:
                w(f"| {disc} | _(unresolved)_ | — | — | — | {lens} |")
                continue
            p = rec["papers"][0]
            title = p["title"].replace("|", "/")
            yr = p.get("year") or "—"
            cites = f"{p.get('cited_by_count',0):,}"
            inst = (rec.get("institution") or "—").replace("|", "/")
            w(f"| {disc} | **{rec['author']}** | {inst} | {title} ({yr}) — {cites} cites | {doi_link(p.get('doi'))} | {lens} |")
        w("")

    w("---")
    w("")
    w("## From roster to agents")
    w("")
    w("- Each row -> a `Researcher` agent: persona seeded from the origin lens; corpus =")
    w("  the cached abstract(s); the model (sonnet-4.6) argues grounded in that text.")
    w("- Reproduce / refresh: `python ingest.py` (re-fetch from OpenAlex) then")
    w("  `python gen_roster_md.py` (regenerate this file).")
    w("- Scale: raise papers-per-author (`--papers N`) and extend `genesis/seeds.py` to")
    w("  5 researchers per discipline to reach the full ~215-agent population.")
    w("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}  ({n_total}/{len(SEEDS)} disciplines, {n_abstract} RAG-ready)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
