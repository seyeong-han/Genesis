"""Shared knowledge graph — the blackboard every researcher reads from and writes to.

This is the MiroFish "Zep temporal graph" idea, reimplemented with zero deps:
facts (edges) carry validity so the graph can *evolve* (contradictions expire old
beliefs). No agent talks to another directly; they coordinate by leaving traces here
(stigmergy).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional


NODE_TYPES = ("Concept", "Claim", "Researcher", "Question")
EDGE_TYPES = ("studies", "builds_on", "supports", "bridges", "contradicts")


@dataclass
class Node:
    id: str
    label: str
    ntype: str = "Concept"
    discipline: str = ""
    created_round: int = 0


@dataclass
class Edge:
    src: str
    dst: str
    etype: str
    author: str = ""          # researcher name who left this trace
    discipline: str = ""      # author's field — this is what makes a node "cross-disciplinary"
    evidence: str = ""        # one-line grounding from the author's corpus
    claim: str = ""           # natural-language statement of the trace
    created_round: int = 0
    valid: bool = True        # temporal validity (Zep-style)
    expired_by: Optional[str] = None  # edge key that invalidated this one


class KnowledgeGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []

    # ---- writes -------------------------------------------------------------
    def add_node(self, node: Node) -> Node:
        existing = self.nodes.get(node.id)
        if existing is None:
            self.nodes[node.id] = node
            return node
        # Concept nodes are shared; keep the earliest, but let a discipline-less
        # node inherit a discipline if one shows up.
        if not existing.discipline and node.discipline:
            existing.discipline = node.discipline
        return existing

    def add_edge(self, edge: Edge) -> Edge:
        self.edges.append(edge)
        return edge

    # ---- reads --------------------------------------------------------------
    def has_node(self, node_id: str) -> bool:
        return node_id in self.nodes

    def valid_edges(self) -> list[Edge]:
        return [e for e in self.edges if e.valid]

    def edges_incident(self, node_id: str, valid_only: bool = True) -> list[Edge]:
        out = []
        for e in self.edges:
            if valid_only and not e.valid:
                continue
            if e.src == node_id or e.dst == node_id:
                out.append(e)
        return out

    def disciplines_touching(self, node_id: str) -> set[str]:
        # "검증" is the Skeptic/referee, not a research field — it never counts
        # as one of the disciplines that *meet* at a node.
        return {
            e.discipline
            for e in self.edges_incident(node_id)
            if e.discipline and e.discipline != "검증"
        }

    def degree(self, node_id: str) -> int:
        return len(self.edges_incident(node_id))

    def nodes_touched_in_round(self, r: int) -> list[str]:
        touched: set[str] = set()
        for e in self.edges:
            if e.created_round == r:
                touched.add(e.src)
                touched.add(e.dst)
        return [n for n in touched if n in self.nodes]

    def new_concept_count(self, r: int) -> int:
        return sum(
            1
            for n in self.nodes.values()
            if n.created_round == r and n.ntype in ("Concept", "Claim")
        )

    def neighborhood(self, node_ids: Iterable[str], hops: int = 2) -> dict[str, list[Edge]]:
        """Edges reachable within `hops` of any seed node. Keeps each agent's read
        local so context does not explode."""
        frontier = set(node_ids)
        seen = set(frontier)
        collected: list[Edge] = []
        for _ in range(hops):
            nxt: set[str] = set()
            for e in self.valid_edges():
                if e.src in frontier or e.dst in frontier:
                    collected.append(e)
                    nxt.add(e.src)
                    nxt.add(e.dst)
            frontier = nxt - seen
            seen |= nxt
        # de-dup while preserving order
        uniq: dict[tuple, Edge] = {}
        for e in collected:
            uniq[(e.src, e.dst, e.etype, e.author, e.created_round)] = e
        return {"edges": list(uniq.values()), "nodes": sorted(seen)}

    def contradiction_edges_for(self, node_id: str) -> list[Edge]:
        return [
            e
            for e in self.edges_incident(node_id)
            if e.etype == "contradicts"
        ]

    # ---- evolution (distributed referee R1) ---------------------------------
    def invalidate_conflicts(self) -> int:
        """Zep-style temporal invalidation. When a `contradicts` edge targets a
        claim, expire the *older* supporting trace on the same node so the graph
        reflects the current best belief, not the original one. Returns count."""
        expired = 0
        for c in self.edges:
            if not c.valid or c.etype != "contradicts":
                continue
            target = c.dst
            rivals = [
                e
                for e in self.edges_incident(target)
                if e.valid
                and e.etype in ("supports", "builds_on", "studies")
                and e.created_round < c.created_round
            ]
            for e in rivals:
                e.valid = False
                e.expired_by = f"{c.src}->{c.dst}:contradicts@{c.created_round}"
                expired += 1
        return expired

    # ---- summaries ----------------------------------------------------------
    def stats(self) -> dict:
        return {
            "nodes": len(self.nodes),
            "concepts": sum(1 for n in self.nodes.values() if n.ntype == "Concept"),
            "edges_total": len(self.edges),
            "edges_valid": len(self.valid_edges()),
            "edges_expired": sum(1 for e in self.edges if not e.valid),
            "contradictions": sum(1 for e in self.edges if e.etype == "contradicts"),
        }
