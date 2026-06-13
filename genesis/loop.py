"""Co-discovery orchestration — the N-round loop over the shared graph.

Per round:
  1. every researcher agent reads the graph and lays one grounded trace (stigmergy)
  2. Bridge Detector finds confluence nodes (>=2 disciplines meet)
  3. Skeptic attacks fresh bridges -> contradicts edges  (referee R2)
  4. graph invalidates conflicts -> beliefs evolve        (referee R1)

After the rounds, the Tension Scanner finds question-worthy sites and the Referee
synthesizes + scores Genesis Questions (referee R3).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

from .agents import build_agents
from .brain_types import GenesisQuestion
from .bridge import detect_bridges, skeptic_pass
from .corpus import seed_researchers
from .graph import KnowledgeGraph
from .llm import Brain
from .referee import adjudicate
from .tension import scan_tensions


@dataclass
class RoundTrace:
    rnd: int
    moves: list[dict] = field(default_factory=list)
    bridges: list[dict] = field(default_factory=list)
    critiques: list[dict] = field(default_factory=list)
    expired: int = 0
    new_concepts: int = 0


@dataclass
class GenesisResult:
    graph: KnowledgeGraph
    rounds: list[RoundTrace]
    questions: list[GenesisQuestion]

    def stats(self) -> dict:
        return self.graph.stats()


def _recent_context(graph: KnowledgeGraph, rnd: int, limit: int = 8) -> str:
    lines = []
    for e in graph.edges:
        if e.created_round == rnd - 1 and e.claim:
            lines.append(f"- ({e.discipline}) {e.author}: {e.claim}")
    return "\n".join(lines[-limit:]) if lines else "(no traces yet — start from your own field)"


def run_genesis(
    brain: Brain,
    rounds: int = 4,
    top_k: int = 5,
    on_event: Optional[Callable[[str, dict], None]] = None,
) -> GenesisResult:
    notify = on_event or (lambda *_: None)

    researchers = seed_researchers()
    agents = build_agents(researchers, brain)
    graph = KnowledgeGraph()
    for a in agents:
        a.seed_into(graph)

    notify("start", {"researchers": [a.name for a in agents], "rounds": rounds})

    traces: list[RoundTrace] = []
    for r in range(rounds):
        trace = RoundTrace(rnd=r)
        context = _recent_context(graph, r)

        for agent in agents:
            mv = agent.act(graph, context, r)
            if mv is None:
                continue
            rec = {
                "author": mv.author,
                "discipline": mv.discipline,
                "concept": mv.concept_label,
                "etype": mv.etype,
                "claim": mv.claim,
            }
            trace.moves.append(rec)
            notify("move", rec)

        bridges = detect_bridges(graph, r)
        for b in bridges:
            rec = {"node": b.label, "disciplines": b.disciplines, "contributing": b.contributing}
            trace.bridges.append(rec)
            notify("bridge", rec)

        trace.critiques = skeptic_pass(graph, bridges, brain, r)
        for c in trace.critiques:
            if c["violates"]:
                notify("critique", c)

        trace.expired = graph.invalidate_conflicts()
        trace.new_concepts = graph.new_concept_count(r)
        notify("round_end", {"round": r, "expired": trace.expired, "stats": graph.stats()})
        traces.append(trace)

    notify("scanning", {})
    sites = scan_tensions(graph, top_k=top_k)
    for s in sites:
        notify("tension", {"label": s.label, "score": s.score, "why": s.why})

    questions = adjudicate(graph, sites, brain)
    notify("done", {"questions": len(questions)})

    return GenesisResult(graph=graph, rounds=traces, questions=questions)
