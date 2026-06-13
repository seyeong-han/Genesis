"""Referee (distributed referee R3) — turns tension sites into scored Genesis
Questions. For each site it (a) synthesizes the fundamental question, (b) gathers
the grounded support and the contradicting tensions from the graph, and (c) scores
the question on depth / cross-disciplinarity / tractability / novelty.
"""

from __future__ import annotations

from .brain_types import GenesisQuestion, TensionSite
from .graph import KnowledgeGraph
from .llm import Brain


def _gather_evidence(graph: KnowledgeGraph, node_id: str) -> tuple[list[str], list[str], list[str]]:
    supporting: list[str] = []
    tensions: list[str] = []
    contributors: list[str] = []
    seen: set[tuple] = set()
    for e in graph.edges_incident(node_id, valid_only=False):
        if e.author and e.author not in contributors and e.author != "Skeptic":
            contributors.append(e.author)
        if not e.claim:
            continue
        key = (e.author, e.claim)  # collapse the researcher->concept and concept->concept twins
        if key in seen:
            continue
        seen.add(key)
        if e.etype == "contradicts":
            tensions.append(f"⚠ Skeptic: {e.claim}" if e.author == "Skeptic" else f"({e.discipline}) {e.author}: {e.claim}")
        elif e.valid:
            supporting.append(f"({e.discipline}) {e.author}: {e.claim}")
        else:
            tensions.append(f"[expired] ({e.discipline}) {e.author}: {e.claim}")
    return supporting, tensions, contributors


def adjudicate(
    graph: KnowledgeGraph, sites: list[TensionSite], brain: Brain
) -> list[GenesisQuestion]:
    questions: list[GenesisQuestion] = []
    for site in sites:
        supporting, tensions, contributors = _gather_evidence(graph, site.node_id)
        context = "\n".join(supporting + tensions)
        question = brain.synthesize_question(site.node_id, site.label, context)
        scores = brain.score_question(question, site.disciplines, site.signatures)
        questions.append(
            GenesisQuestion(
                node_id=site.node_id,
                label=site.label,
                question=question,
                disciplines=site.disciplines,
                supporting=supporting[:4],
                tensions=tensions[:4],
                scores=scores,
                contributors=contributors,
            )
        )
    questions.sort(key=lambda q: q.total, reverse=True)
    return questions
