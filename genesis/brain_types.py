"""Shared value objects passed between pipeline stages.

Kept dependency-free (no imports from other genesis modules) to avoid cycles.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MoveResult:
    author: str
    discipline: str
    concept: str
    concept_label: str
    claim: str
    etype: str
    connects_to: list[str]
    edges: list[Any] = field(default_factory=list)


@dataclass
class BridgeCandidate:
    node_id: str
    label: str
    disciplines: list[str]
    contributing: list[str]   # author names whose traces meet here
    round: int


@dataclass
class TensionSite:
    node_id: str
    label: str
    disciplines: list[str]
    signatures: dict          # orphan_bridge / contradiction / centrality scores
    score: float
    why: str


@dataclass
class GenesisQuestion:
    node_id: str
    label: str
    question: str
    disciplines: list[str]
    supporting: list[str]     # evidence lines (grounded claims)
    tensions: list[str]       # contradicting claims / constraints
    scores: dict              # depth / cross_disciplinarity / tractability / novelty
    contributors: list[str]

    @property
    def total(self) -> float:
        s = self.scores
        return (
            s.get("depth", 0)
            + s.get("cross_disciplinarity", 0)
            + s.get("tractability", 0)
            + s.get("novelty", 0)
        )
