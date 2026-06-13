"""OpenAlex ingestion pipeline.

Resolves each discipline to an OpenAlex concept, pulls the highest-cited works
(real papers, real authors, real citation counts), reconstructs abstracts, and
caches everything to `data/corpus/<discipline>.json`. A roster summary is written
to `data/roster.json`.

Everything here uses only the Python stdlib (urllib). OpenAlex needs no API key;
we use the polite pool via a `mailto`.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from .disciplines import DISCIPLINES, slugify
from .seeds import SEEDS

OPENALEX = "https://api.openalex.org"
MAILTO = "h960213@gmail.com"
UA = {"User-Agent": f"GenesisEngine/0.1 (mailto:{MAILTO})"}

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CORPUS_DIR = DATA_DIR / "corpus"


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
def _get(path: str, params: dict) -> dict:
    params = {**params, "mailto": MAILTO}
    url = f"{OPENALEX}/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def reconstruct_abstract(inverted_index: Optional[dict]) -> str:
    if not inverted_index:
        return ""
    positions: list[tuple[int, str]] = []
    for word, idxs in inverted_index.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort(key=lambda p: p[0])
    return " ".join(w for _, w in positions)


def resolve_concept(term: str) -> Optional[dict]:
    try:
        data = _get("concepts", {"search": term, "per-page": 1})
    except Exception as e:  # noqa: BLE001
        print(f"    [concept resolve error] {term}: {e}")
        return None
    results = data.get("results") or []
    if not results:
        return None
    c = results[0]
    return {"id": c["id"].rsplit("/", 1)[-1], "name": c["display_name"], "level": c.get("level")}


def fetch_top_works(concept_id: str, n: int, require_abstract: bool = True) -> list[dict]:
    filt = f"concepts.id:{concept_id}"
    if require_abstract:
        filt += ",has_abstract:true"
    try:
        data = _get(
            "works",
            {"filter": filt, "sort": "cited_by_count:desc", "per-page": max(n, 1)},
        )
    except Exception as e:  # noqa: BLE001
        print(f"    [works fetch error] {concept_id}: {e}")
        return []
    return data.get("results") or []


@dataclass
class Paper:
    openalex_id: str
    title: str
    year: Optional[int]
    cited_by_count: int
    doi: Optional[str]
    oa_pdf_url: Optional[str]
    abstract: str


@dataclass
class ResearcherRecord:
    domain: str
    discipline: str
    concept: str
    concept_id: str
    author: str
    author_openalex_id: Optional[str]
    institution: Optional[str]
    papers: list[dict]


def _lead_author(work: dict) -> tuple[str, Optional[str], Optional[str]]:
    auths = work.get("authorships") or []
    if not auths:
        return ("Unknown", None, None)
    a = auths[0]
    name = a["author"]["display_name"]
    aid = (a["author"].get("id") or "").rsplit("/", 1)[-1] or None
    insts = a.get("institutions") or []
    inst = insts[0]["display_name"] if insts else None
    return (name, aid, inst)


def _to_paper(work: dict) -> Paper:
    loc = work.get("best_oa_location") or {}
    return Paper(
        openalex_id=(work.get("id") or "").rsplit("/", 1)[-1],
        title=work.get("title") or "(untitled)",
        year=work.get("publication_year"),
        cited_by_count=work.get("cited_by_count", 0),
        doi=work.get("doi"),
        oa_pdf_url=loc.get("pdf_url"),
        abstract=reconstruct_abstract(work.get("abstract_inverted_index")),
    )


def _norm_name(s: str) -> str:
    import unicodedata

    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(c for c in s.lower() if c.isalnum() or c == " ").strip()


def _name_match(query: str, candidate: str) -> bool:
    """True if surname matches and the first initial is consistent — guards against
    name-collisions where a far more cited stranger would otherwise win."""
    q, c = _norm_name(query).split(), _norm_name(candidate).split()
    if not q or not c:
        return False
    if q[-1] != c[-1]:  # surname must match
        return False
    return q[0][0] == c[0][0]  # first initial consistent


def resolve_author(name: str) -> Optional[dict]:
    """Find the best-matching real OpenAlex author. Prefer a genuine name match;
    only then break ties by citation count (so collisions can't hijack the seed)."""
    try:
        data = _get("authors", {"search": name, "per-page": 10})
    except Exception as e:  # noqa: BLE001
        print(f"    [author resolve error] {name}: {e}")
        return None
    results = data.get("results") or []
    if not results:
        return None
    matches = [a for a in results if _name_match(name, a.get("display_name", ""))]
    pool = matches or results
    best = max(pool, key=lambda a: a.get("cited_by_count", 0))
    if not matches:
        print(f"    ~ no exact name match for '{name}', using closest: {best['display_name']}")
    return {
        "id": best["id"].rsplit("/", 1)[-1],
        "name": best["display_name"],
        "cited_by_count": best.get("cited_by_count", 0),
        "works_count": best.get("works_count", 0),
        "institution": ((best.get("last_known_institutions") or [{}])[0].get("display_name")
                        if best.get("last_known_institutions") else None),
    }


def fetch_author_top_work(author_id: str, topic: str, papers: int) -> list[dict]:
    """Top-cited works by an author, steered toward a topic if possible."""
    base = {"filter": f"author.id:{author_id},has_abstract:true",
            "sort": "cited_by_count:desc", "per-page": max(papers, 1)}
    # First try with topic search to bias toward the origin-relevant paper.
    try:
        data = _get("works", {**base, "search": topic})
        results = data.get("results") or []
        if results:
            return results
    except Exception:  # noqa: BLE001
        pass
    # Fall back to plain top-cited (with then without abstract requirement).
    for filt in (f"author.id:{author_id},has_abstract:true", f"author.id:{author_id}"):
        try:
            data = _get("works", {"filter": filt, "sort": "cited_by_count:desc", "per-page": max(papers, 1)})
            results = data.get("results") or []
            if results:
                return results
        except Exception:  # noqa: BLE001
            continue
    return []


def ingest_by_seeds(papers_per_author: int = 1, sleep: float = 0.25) -> list[ResearcherRecord]:
    """Demo ingestion: one curated origin-relevant researcher per discipline,
    verified and fetched from OpenAlex (real author + their real top paper)."""
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    roster: list[ResearcherRecord] = []

    for i, (domain, discipline, author_name, topic, lens) in enumerate(SEEDS, 1):
        print(f"[{i:>2}/{len(SEEDS)}] {discipline}: {author_name}")
        author = resolve_author(author_name)
        time.sleep(sleep)
        if not author:
            print(f"    ! author '{author_name}' not found on OpenAlex; skipping")
            continue

        works = fetch_author_top_work(author["id"], topic, papers_per_author)
        time.sleep(sleep)
        if not works:
            print(f"    ! no works with abstract for {author['name']}; skipping")
            continue

        rec = ResearcherRecord(
            domain=domain,
            discipline=discipline,
            concept=topic,
            concept_id=author["id"],
            author=author["name"],
            author_openalex_id=author["id"],
            institution=author.get("institution"),
            papers=[asdict(_to_paper(w)) for w in works[:papers_per_author]],
        )
        # carry the origin lens for downstream persona generation
        rec_dict = asdict(rec)
        rec_dict["origin_lens"] = lens
        rec_dict["author_total_citations"] = author.get("cited_by_count", 0)
        roster.append(rec)

        out = CORPUS_DIR / f"{slugify(discipline)}.json"
        out.write_text(json.dumps(rec_dict, ensure_ascii=False, indent=2), encoding="utf-8")
        top = rec.papers[0]
        print(f"    -> {rec.author} ({author.get('cited_by_count',0):,} total cites) "
              f"| paper {top['cited_by_count']:,} cites | {top['title'][:64]}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "roster.json").write_text(
        json.dumps([asdict(r) for r in roster], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nWrote {len(roster)}/{len(SEEDS)} researcher records to {CORPUS_DIR}")
    return roster


def ingest(per_discipline: int = 1, papers_per_author: int = 1, sleep: float = 0.25) -> list[ResearcherRecord]:
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    roster: list[ResearcherRecord] = []

    for i, (domain, discipline, term) in enumerate(DISCIPLINES, 1):
        print(f"[{i:>2}/{len(DISCIPLINES)}] {discipline}  (search: '{term}')")
        concept = resolve_concept(term)
        time.sleep(sleep)
        if not concept:
            print("    ! concept not resolved; skipping")
            continue

        works = fetch_top_works(concept["id"], per_discipline, require_abstract=True)
        if not works:
            works = fetch_top_works(concept["id"], per_discipline, require_abstract=False)
        time.sleep(sleep)
        if not works:
            print("    ! no works found; skipping")
            continue

        # One researcher per discipline in demo mode: take the lead author of the
        # single top-cited work, and that one paper.
        seen_authors: dict[str, ResearcherRecord] = {}
        for work in works[:per_discipline]:
            name, aid, inst = _lead_author(work)
            paper = _to_paper(work)
            rec = seen_authors.get(name)
            if rec is None:
                rec = ResearcherRecord(
                    domain=domain,
                    discipline=discipline,
                    concept=concept["name"],
                    concept_id=concept["id"],
                    author=name,
                    author_openalex_id=aid,
                    institution=inst,
                    papers=[],
                )
                seen_authors[name] = rec
            if len(rec.papers) < papers_per_author:
                rec.papers.append(asdict(paper))

        for rec in seen_authors.values():
            roster.append(rec)
            out = CORPUS_DIR / f"{slugify(discipline)}.json"
            out.write_text(json.dumps(asdict(rec), ensure_ascii=False, indent=2), encoding="utf-8")
            top = rec.papers[0]
            print(f"    -> {rec.author} | {top['cited_by_count']:,} cites | {top['title'][:70]}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "roster.json").write_text(
        json.dumps([asdict(r) for r in roster], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nWrote {len(roster)} researcher records to {CORPUS_DIR}")
    print(f"Roster summary: {DATA_DIR / 'roster.json'}")
    return roster
