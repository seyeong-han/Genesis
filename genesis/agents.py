"""Researcher agents — they never talk to each other directly. Each round an agent
reads its local neighborhood of the shared graph (plus the freshest traces) and
lays one new grounded trace. Coordination is purely stigmergic, via the graph.
"""

from __future__ import annotations

from dataclasses import dataclass

from .brain_types import MoveResult
from .corpus import CONCEPTS, Researcher
from .graph import Edge, KnowledgeGraph, Node
from .llm import Brain


@dataclass
class ResearcherAgent:
    researcher: Researcher
    brain: Brain
    _cursor: int = 0  # index into scripted moves

    @property
    def name(self) -> str:
        return self.researcher.name

    @property
    def discipline(self) -> str:
        return self.researcher.discipline

    def seed_into(self, graph: KnowledgeGraph) -> None:
        """Plant the researcher node so the roster is visible on the graph."""
        graph.add_node(
            Node(
                id=f"researcher::{self.researcher.name}",
                label=self.researcher.name,
                ntype="Researcher",
                discipline=self.researcher.discipline,
            )
        )

    def _next_scripted(self):
        moves = self.researcher.moves
        if self._cursor >= len(moves):
            return None
        m = moves[self._cursor]
        self._cursor += 1
        return m

    def act(self, graph: KnowledgeGraph, recent_context: str, rnd: int) -> MoveResult | None:
        scripted = self._next_scripted()
        move = self.brain.propose_move(self.researcher, scripted, recent_context, rnd)
        if not move:
            return None

        concept_id = move["concept"]
        concept_label = move.get("concept_label") or CONCEPTS.get(concept_id, concept_id)

        # Ensure the central concept node exists.
        graph.add_node(
            Node(id=concept_id, label=concept_label, ntype="Concept", created_round=rnd)
        )

        etype = move.get("etype", "supports")
        evidence = move.get("evidence", "")
        claim = move.get("claim", "")

        written: list[Edge] = []
        # The researcher's trace onto the central concept.
        written.append(
            graph.add_edge(
                Edge(
                    src=f"researcher::{self.researcher.name}",
                    dst=concept_id,
                    etype=etype,
                    author=self.researcher.name,
                    discipline=self.researcher.discipline,
                    evidence=evidence,
                    claim=claim,
                    created_round=rnd,
                )
            )
        )

        # Links from this concept to the other concepts it connects to.
        for other in move.get("connects_to", []):
            if not other:
                continue
            graph.add_node(
                Node(
                    id=other,
                    label=CONCEPTS.get(other, other),
                    ntype="Concept",
                    created_round=rnd,
                )
            )
            link_type = "bridges" if etype == "bridges" else "builds_on"
            written.append(
                graph.add_edge(
                    Edge(
                        src=concept_id,
                        dst=other,
                        etype=link_type,
                        author=self.researcher.name,
                        discipline=self.researcher.discipline,
                        evidence=evidence,
                        claim=claim,
                        created_round=rnd,
                    )
                )
            )

        return MoveResult(
            author=self.researcher.name,
            discipline=self.researcher.discipline,
            concept=concept_id,
            concept_label=concept_label,
            claim=claim,
            etype=etype,
            connects_to=list(move.get("connects_to", [])),
            edges=written,
        )


def build_agents(researchers: list[Researcher], brain: Brain) -> list[ResearcherAgent]:
    return [ResearcherAgent(researcher=r, brain=brain) for r in researchers]
