"""Bridge detection + the in-loop Skeptic.

A *bridge* appears when traces from two or more different disciplines meet at the
same concept node — a confluence point. The Skeptic (distributed referee R2)
immediately attacks fresh bridges; if a bridge over-reaches, the Skeptic writes a
`contradicts` edge, which later expires the older belief (referee R1).
"""

from __future__ import annotations

from .brain_types import BridgeCandidate
from .graph import Edge, KnowledgeGraph
from .llm import Brain


def detect_bridges(graph: KnowledgeGraph, rnd: int) -> list[BridgeCandidate]:
    bridges: list[BridgeCandidate] = []
    for node_id in graph.nodes_touched_in_round(rnd):
        node = graph.nodes[node_id]
        if node.ntype != "Concept":
            continue
        incident = graph.edges_incident(node_id)
        disciplines = sorted(graph.disciplines_touching(node_id))
        if len(disciplines) >= 2:
            contributors = sorted(
                {e.author for e in incident if e.author and e.author != "Skeptic"}
            )
            bridges.append(
                BridgeCandidate(
                    node_id=node_id,
                    label=node.label,
                    disciplines=disciplines,
                    contributing=contributors,
                    round=rnd,
                )
            )
    return bridges


def skeptic_pass(
    graph: KnowledgeGraph, bridges: list[BridgeCandidate], brain: Brain, rnd: int
) -> list[dict]:
    """Run the Skeptic over fresh bridges. Returns critique records for the trace."""
    critiques: list[dict] = []
    for b in bridges:
        verdict = brain.critique(
            {"node": b.label, "disciplines": b.disciplines, "contributors": b.contributing},
            context=_bridge_context(graph, b),
        )
        if verdict.get("violates"):
            graph.add_edge(
                Edge(
                    src=f"skeptic::round{rnd}",
                    dst=b.node_id,
                    etype="contradicts",
                    author="Skeptic",
                    discipline="검증",
                    evidence=verdict.get("reason", ""),
                    claim=verdict.get("reason", ""),
                    created_round=rnd,
                )
            )
        critiques.append(
            {
                "node": b.node_id,
                "label": b.label,
                "disciplines": b.disciplines,
                "violates": bool(verdict.get("violates")),
                "reason": verdict.get("reason", ""),
            }
        )
    return critiques


def _bridge_context(graph: KnowledgeGraph, b: BridgeCandidate) -> str:
    lines = []
    for e in graph.edges_incident(b.node_id):
        if e.claim:
            lines.append(f"- ({e.discipline}) {e.author}: {e.claim}")
    return "\n".join(lines[:8])
