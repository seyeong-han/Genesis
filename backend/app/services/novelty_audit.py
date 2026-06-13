"""
Novelty Audit — post-report step that checks whether the generated hypothesis
represents a genuine literature gap by searching OpenAlex.

Flow:
1. Extract the core cross-disciplinary hypothesis from the report (Opus).
2. Build 2-3 OpenAlex search queries from the bridged concepts.
3. For each query, fetch the top-5 most-cited works with abstracts.
4. Opus judges whether any existing paper already makes the same cross-field bridge.
5. Emit a verdict: NOVEL / PARTIAL / KNOWN, plus nearest existing papers (DOIs).

Returns a structured result that is attached to the report and surfaced on Step4Report.
No external deps beyond the stdlib urllib — same as the ingest pipeline.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Optional

from ..utils.llm_client import LLMClient

OPENALEX = "https://api.openalex.org"
MAILTO = "h960213@gmail.com"
UA = {"User-Agent": f"GenesisNoveltyAudit/0.1 (mailto:{MAILTO})"}


def _get(path: str, params: dict) -> dict:
    params = {**params, "mailto": MAILTO}
    url = f"{OPENALEX}/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def _reconstruct_abstract(inverted: Optional[dict]) -> str:
    if not inverted:
        return ""
    positions: list[tuple[int, str]] = []
    for word, idxs in inverted.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort(key=lambda p: p[0])
    return " ".join(w for _, w in positions)


def _search_openalex(query: str, n: int = 5) -> list[dict]:
    """Return top-n works matching the query (with abstracts)."""
    try:
        data = _get(
            "works",
            {
                "search": query,
                "filter": "has_abstract:true",
                "sort": "cited_by_count:desc",
                "per-page": n,
            },
        )
    except Exception:
        return []
    results = []
    for w in data.get("results") or []:
        results.append(
            {
                "title": w.get("title", ""),
                "doi": w.get("doi", ""),
                "year": w.get("publication_year"),
                "cited_by_count": w.get("cited_by_count", 0),
                "abstract": _reconstruct_abstract(w.get("abstract_inverted_index")),
            }
        )
    return results


def _tokens(text: str) -> set[str]:
    """Tokenise for lightweight relevance filtering."""
    stop = {
        "the", "and", "for", "with", "that", "this", "from", "into", "does",
        "need", "single", "others", "general", "approach", "architecture",
        "hybrid", "unified", "model", "models", "paper", "study",
    }
    return {
        t for t in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", text.lower())
        if t not in stop
    }


def _rank_relevant_candidates(
    candidates: list[dict],
    hypothesis: str,
    queries: list[str],
) -> list[dict]:
    """Rank/filter candidates so generic collisions like "hybrid detector
    architecture" don't appear as nearest work for ML architecture questions."""
    query_text = " ".join([hypothesis] + queries)
    key_tokens = _tokens(query_text)
    # Domain anchors that indicate neural/ML architecture relevance.
    anchors = {
        "neural", "learning", "machine", "transformer", "attention",
        "diffusion", "convolution", "cnn", "language", "generative",
        "autoregressive", "architecture", "architectures",
    }

    ranked = []
    for c in candidates:
        haystack = f"{c.get('title', '')} {c.get('abstract', '')}"
        toks = _tokens(haystack)
        overlap = len(key_tokens & toks)
        anchor_hit = len(anchors & toks)
        score = overlap + 3 * anchor_hit
        if score >= 3:
            c = dict(c)
            c["_relevance_score"] = score
            ranked.append(c)
    ranked.sort(key=lambda c: (c.get("_relevance_score", 0), c.get("cited_by_count", 0)), reverse=True)
    return ranked


@dataclass
class NearestPaper:
    title: str
    doi: Optional[str]
    year: Optional[int]
    cited_by_count: int
    relevance_note: str


@dataclass
class NoveltyResult:
    verdict: str                       # NOVEL | PARTIAL | KNOWN
    hypothesis: str                    # the core hypothesis we audited
    queries_used: list[str]            # OpenAlex queries run
    nearest_papers: list[NearestPaper] # closest existing work (DOIs)
    explanation: str                   # Opus's reasoning

    def to_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "hypothesis": self.hypothesis,
            "queries_used": self.queries_used,
            "nearest_papers": [
                {
                    "title": p.title,
                    "doi": p.doi,
                    "year": p.year,
                    "cited_by_count": p.cited_by_count,
                    "relevance_note": p.relevance_note,
                }
                for p in self.nearest_papers
            ],
            "explanation": self.explanation,
        }


def _extract_hypothesis_and_queries(llm: LLMClient, report_text: str) -> dict:
    """Ask Opus to extract the core hypothesis and suggest search queries."""
    system = (
        "You are a science librarian. Given a cross-disciplinary hypothesis brief, "
        "extract the single most specific cross-disciplinary hypothesis and suggest "
        "2-3 OpenAlex search queries to look for prior work that already makes this "
        "same cross-field bridge. Be specific — query the bridge itself, not just "
        "the individual concepts. Include the domain anchors from the hypothesis "
        "(for ML questions: machine learning, neural network, transformer, diffusion, "
        "convolution/CNN, generative model). Avoid generic phrases like just "
        "'hybrid architecture'. Return JSON only."
    )
    user = (
        f"Brief excerpt (first 3000 chars):\n{report_text[:3000]}\n\n"
        "Return JSON:\n"
        '{"hypothesis":"<one sentence>","queries":["<query1>","<query2>"]}'
    )
    try:
        raw = llm.chat([{"role": "system", "content": system}, {"role": "user", "content": user}],
                       max_tokens=600, temperature=0.2)
        raw = raw.strip()
        if raw.startswith("```"):
            raw = "\n".join(raw.split("\n")[1:-1])
        return json.loads(raw)
    except Exception:
        return {"hypothesis": "", "queries": []}


def _judge_novelty(llm: LLMClient, hypothesis: str, candidates: list[dict]) -> dict:
    """Ask Opus to judge whether any candidate paper already makes the same bridge."""
    system = (
        "You are a science novelty referee. Determine whether the given hypothesis "
        "represents a genuine literature gap or has already been published.\n"
        "NOVEL = no existing paper makes this specific cross-disciplinary bridge.\n"
        "PARTIAL = the two fields are studied separately, but the bridge is not made.\n"
        "KNOWN = the bridge already exists in the literature.\n"
        "Return JSON only."
    )
    cands_str = json.dumps(
        [{"title": c["title"], "doi": c["doi"], "abstract": c["abstract"][:400]} for c in candidates],
        ensure_ascii=False,
    )
    user = (
        f"Hypothesis: {hypothesis}\n\nCandidate papers:\n{cands_str}\n\n"
        'Return JSON: {"verdict":"NOVEL|PARTIAL|KNOWN","explanation":"<one paragraph>","nearest_doi":"<doi or empty>"}'
    )
    try:
        raw = llm.chat([{"role": "system", "content": system}, {"role": "user", "content": user}],
                       max_tokens=500, temperature=0.1)
        raw = raw.strip()
        if raw.startswith("```"):
            raw = "\n".join(raw.split("\n")[1:-1])
        return json.loads(raw)
    except Exception:
        return {"verdict": "PARTIAL", "explanation": "Novelty check failed (parse error).", "nearest_doi": ""}


def run_novelty_audit(report_text: str) -> NoveltyResult:
    """Run the full novelty audit pipeline on a report's text."""
    llm = LLMClient(use_report_model=True)

    # Step 1: extract hypothesis + queries
    extracted = _extract_hypothesis_and_queries(llm, report_text)
    hypothesis = extracted.get("hypothesis", "(could not extract hypothesis)")
    queries = extracted.get("queries") or []

    if not queries:
        return NoveltyResult(
            verdict="PARTIAL",
            hypothesis=hypothesis,
            queries_used=[],
            nearest_papers=[],
            explanation="Could not generate search queries from the hypothesis.",
        )

    # Step 2: search OpenAlex for each query
    all_candidates: list[dict] = []
    for q in queries:
        hits = _search_openalex(q, n=5)
        all_candidates.extend(hits)

    # Deduplicate by DOI
    seen_dois: set[str] = set()
    unique_candidates: list[dict] = []
    for c in all_candidates:
        key = c.get("doi") or c.get("title", "")
        if key and key not in seen_dois:
            seen_dois.add(key)
            unique_candidates.append(c)

    relevant_candidates = _rank_relevant_candidates(unique_candidates, hypothesis, queries)
    if relevant_candidates:
        unique_candidates = relevant_candidates

    # Step 3: judge novelty
    judgement = _judge_novelty(llm, hypothesis, unique_candidates[:10])
    verdict = judgement.get("verdict", "PARTIAL")
    explanation = judgement.get("explanation", "")
    nearest_doi = judgement.get("nearest_doi", "")

    # Build nearest papers list (top 3 most relevant)
    nearest: list[NearestPaper] = []
    for c in unique_candidates[:3]:
        note = "closest existing work" if c.get("doi") == nearest_doi else "related work in the field"
        nearest.append(
            NearestPaper(
                title=c["title"],
                doi=c.get("doi"),
                year=c.get("year"),
                cited_by_count=c.get("cited_by_count", 0),
                relevance_note=note,
            )
        )

    return NoveltyResult(
        verdict=verdict,
        hypothesis=hypothesis,
        queries_used=queries,
        nearest_papers=nearest,
        explanation=explanation,
    )
