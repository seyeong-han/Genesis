#!/usr/bin/env python3
"""Fetch the demo researchers for the ML-architecture question into an isolated
corpus dir (data/demo_corpus/). Self-contained, keyless OpenAlex (stdlib urllib).
See demo_researchers.md.

Usage (from anywhere):
    python backend/scripts/openalex/demo_ingest.py
"""

from __future__ import annotations

import json
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

OPENALEX = "https://api.openalex.org"
MAILTO = "h960213@gmail.com"
UA = {"User-Agent": f"GenesisEngine/0.1 (mailto:{MAILTO})"}

# (domain, discipline, author_name, topic_hint, lens)
DEMO_SEEDS = [
    ("Cognitive & Interdisciplinary", "Transformers", "Ashish Vaswani",
     "attention is all you need transformer",
     "attention as a general-purpose architecture that may subsume others"),
    ("Cognitive & Interdisciplinary", "Convolutional / Energy-Based Models", "Yann LeCun",
     "convolutional networks gradient-based learning",
     "inductive biases matter; pure autoregressive LLMs are insufficient"),
    ("Cognitive & Interdisciplinary", "Diffusion Models", "Jonathan Ho",
     "denoising diffusion probabilistic models",
     "diffusion as a distinct generative pillar, increasingly hybridized"),
]

# __file__ = backend/scripts/openalex/demo_ingest.py → parents[3] = repo root (Genesis/)
REPO_ROOT = Path(__file__).resolve().parents[3]
DEMO_CORPUS = REPO_ROOT / "data" / "demo_corpus"


def _get(path: str, params: dict) -> dict:
    params = {**params, "mailto": MAILTO}
    url = f"{OPENALEX}/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def reconstruct_abstract(inverted: Optional[dict]) -> str:
    if not inverted:
        return ""
    positions = []
    for word, idxs in inverted.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort(key=lambda p: p[0])
    return " ".join(w for _, w in positions)


def _norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(c for c in s.lower() if c.isalnum() or c == " ").strip()


def _name_match(query: str, candidate: str) -> bool:
    q, c = _norm_name(query).split(), _norm_name(candidate).split()
    if not q or not c:
        return False
    if q[-1] != c[-1]:
        return False
    return q[0][0] == c[0][0]


def resolve_author(name: str) -> Optional[dict]:
    try:
        data = _get("authors", {"search": name, "per-page": 10})
    except Exception as e:
        print(f"    [author resolve error] {name}: {e}")
        return None
    results = data.get("results") or []
    if not results:
        return None
    matches = [a for a in results if _name_match(name, a.get("display_name", ""))]
    pool = matches or results
    best = max(pool, key=lambda a: a.get("cited_by_count", 0))
    if not matches:
        print(f"    ~ no exact match for '{name}', using closest: {best['display_name']}")
    insts = best.get("last_known_institutions") or []
    return {
        "id": best["id"].rsplit("/", 1)[-1],
        "name": best["display_name"],
        "cited_by_count": best.get("cited_by_count", 0),
        "institution": insts[0].get("display_name") if insts else None,
    }


def fetch_author_top_work(author_id: str, topic: str) -> list[dict]:
    base = {"filter": f"author.id:{author_id},has_abstract:true",
            "sort": "cited_by_count:desc", "per-page": 1}
    try:
        data = _get("works", {**base, "search": topic})
        if data.get("results"):
            return data["results"]
    except Exception:
        pass
    for filt in (f"author.id:{author_id},has_abstract:true", f"author.id:{author_id}"):
        try:
            data = _get("works", {"filter": filt, "sort": "cited_by_count:desc", "per-page": 1})
            if data.get("results"):
                return data["results"]
        except Exception:
            continue
    return []


def _to_paper(work: dict) -> dict:
    loc = work.get("best_oa_location") or {}
    return {
        "openalex_id": (work.get("id") or "").rsplit("/", 1)[-1],
        "title": work.get("title") or "(untitled)",
        "year": work.get("publication_year"),
        "cited_by_count": work.get("cited_by_count", 0),
        "doi": work.get("doi"),
        "oa_pdf_url": loc.get("pdf_url"),
        "abstract": reconstruct_abstract(work.get("abstract_inverted_index")),
    }


def slugify(name: str) -> str:
    keep = []
    for ch in name.lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in (" ", "-", "&", "/"):
            keep.append("_")
    slug = "".join(keep)
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug.strip("_")


def main() -> int:
    DEMO_CORPUS.mkdir(parents=True, exist_ok=True)
    roster = []
    for i, (domain, discipline, name, topic, lens) in enumerate(DEMO_SEEDS, 1):
        print(f"[{i}/{len(DEMO_SEEDS)}] {discipline}: {name}")
        author = resolve_author(name)
        time.sleep(0.25)
        if not author:
            print(f"    ! not found: {name}")
            continue
        works = fetch_author_top_work(author["id"], topic)
        time.sleep(0.25)
        if not works:
            print(f"    ! no works with abstract for {author['name']}")
            continue
        rec = {
            "domain": domain,
            "discipline": discipline,
            "concept": topic,
            "concept_id": author["id"],
            "author": author["name"],
            "author_openalex_id": author["id"],
            "institution": author.get("institution"),
            "papers": [_to_paper(works[0])],
            "origin_lens": lens,
            "author_total_citations": author.get("cited_by_count", 0),
        }
        roster.append(rec)
        (DEMO_CORPUS / f"{slugify(name)}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        top = rec["papers"][0]
        print(f"    -> {rec['author']} | {top['cited_by_count']:,} cites | {top['title'][:64]}")

    (DEMO_CORPUS / "roster.json").write_text(
        json.dumps(roster, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nWrote {len(roster)} demo researchers to {DEMO_CORPUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
