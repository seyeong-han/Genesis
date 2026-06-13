"""Tension scanner — the heart of Genesis Engine.

Good questions are not given; they show up as *structural tension* in the fused
graph. We score every concept node on three signatures and surface the highest as
Genesis Question candidates:

  1. orphan_bridge       — many disciplines touch this node, but no edge actually
                           connects their claims (a meeting with no bridge yet).
  2. contradiction       — many `contradicts` edges meet here (fields disagree).
  3. cross_centrality    — high degree AND high discipline diversity (everyone
                           keeps returning to it, nobody owns it).

The weighted sum is the tension score. High score = a question only fusion can ask.
"""

from __future__ import annotations

from .brain_types import TensionSite
from .graph import KnowledgeGraph

W_ORPHAN = 3.0
W_CONTRADICTION = 2.0
W_CENTRALITY = 1.0


def _orphan_bridge_score(graph: KnowledgeGraph, node_id: str, disciplines: set[str]) -> float:
    """Disciplines meet here, but few `bridges` edges actually link them."""
    if len(disciplines) < 2:
        return 0.0
    bridges = sum(
        1 for e in graph.edges_incident(node_id) if e.etype == "bridges"
    )
    # The more disciplines with the fewer explicit bridges, the more "orphaned".
    return max(0.0, len(disciplines) - bridges)


def scan_tensions(graph: KnowledgeGraph, top_k: int = 5) -> list[TensionSite]:
    sites: list[TensionSite] = []
    for node_id, node in graph.nodes.items():
        if node.ntype != "Concept":
            continue
        disciplines = graph.disciplines_touching(node_id)
        if len(disciplines) < 2:
            continue  # a question worth asking must cross fields

        orphan = _orphan_bridge_score(graph, node_id, disciplines)
        contradiction = len(graph.contradiction_edges_for(node_id))
        degree = graph.degree(node_id)
        centrality = degree * len(disciplines) / 10.0

        score = (
            W_ORPHAN * orphan
            + W_CONTRADICTION * contradiction
            + W_CENTRALITY * centrality
        )

        why_bits = []
        if orphan > 0:
            why_bits.append(f"{len(disciplines)} fields meet but few connecting bridges (orphan {orphan:.0f})")
        if contradiction > 0:
            why_bits.append(f"{contradiction} cross-field contradictions")
        why_bits.append(f"centrality {centrality:.1f} (degree {degree})")

        sites.append(
            TensionSite(
                node_id=node_id,
                label=node.label,
                disciplines=sorted(disciplines),
                signatures={
                    "orphan_bridge": orphan,
                    "contradiction": contradiction,
                    "centrality": round(centrality, 2),
                    "degree": degree,
                    "disciplines": len(disciplines),
                },
                score=round(score, 2),
                why="; ".join(why_bits),
            )
        )

    sites.sort(key=lambda s: s.score, reverse=True)
    return sites[:top_k]
