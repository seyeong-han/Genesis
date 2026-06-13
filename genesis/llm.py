"""The reasoning brain — swappable, like MiroFish's CloudBrain/LocalBrain split.

`Brain` is the interface the engine talks to. Two implementations:
  - MockBrain   : deterministic, zero-dependency. Drives a coherent demo offline.
  - ClaudeBrain : live Opus 4.8 via the Anthropic API.

The engine's *mechanism* (graph, loop, bridges, tensions) is identical in both
modes; only the brain changes.
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Optional

from .corpus import GENESIS_QUESTIONS, Move, Researcher


class Brain:
    name = "abstract"

    def propose_move(
        self, researcher: Researcher, scripted: Optional[Move], context: str, rnd: int
    ) -> Optional[dict]:
        raise NotImplementedError

    def critique(self, bridge: dict, context: str) -> dict:
        raise NotImplementedError

    def synthesize_question(self, concept_id: str, concept_label: str, context: str) -> str:
        raise NotImplementedError

    def score_question(self, question: str, disciplines: list[str], signatures: dict) -> dict:
        raise NotImplementedError


# --------------------------------------------------------------------------- #
# Mock brain — deterministic, no API key needed.
# --------------------------------------------------------------------------- #
class MockBrain(Brain):
    name = "mock"

    def propose_move(self, researcher, scripted, context, rnd):
        if scripted is None:
            return None
        return {
            "concept": scripted.concept,
            "concept_label": scripted.concept_label,
            "claim": scripted.claim,
            "connects_to": list(scripted.connects_to),
            "etype": scripted.etype,
            "evidence": scripted.evidence,
        }

    def critique(self, bridge, context):
        disciplines = set(bridge.get("disciplines", []))
        # The classic over-reach: linking measurement to subjective experience.
        if {"Quantum Foundations", "Consciousness Theory"}.issubset(disciplines):
            return {
                "violates": True,
                "reason": "The observer-consciousness link risks leaping from correlation "
                "to causation (a category error). The 'observer' in measurement may be a "
                "physical interaction, not an experiencing subject.",
            }
        if {"Consciousness Theory", "Complex Systems Science"}.issubset(disciplines):
            return {
                "violates": True,
                "reason": "Consciousness-as-emergence vs consciousness-as-fundamental: "
                "no agreement is possible without a boundary criterion.",
            }
        return {"violates": False, "reason": ""}

    def synthesize_question(self, concept_id, concept_label, context):
        return GENESIS_QUESTIONS.get(
            concept_id,
            f"What fundamental question about the origin of the universe and life does the "
            f"cross-disciplinary collision around '{concept_label}' force upon us?",
        )

    def score_question(self, question, disciplines, signatures):
        # Deterministic but differentiated: seed variation from the question text.
        h = int(hashlib.sha256(question.encode("utf-8")).hexdigest(), 16)
        jitter = (h % 5) - 2  # -2..+2
        cross = min(10, 2 + 2 * len(set(disciplines)))
        depth = min(10, 7 + (signatures.get("orphan_bridge", 0) > 0) + (signatures.get("contradiction", 0) // 2))
        novelty = max(3, min(10, 7 + jitter))
        # Metaphysical reach lowers near-term tractability.
        tractability = max(2, min(8, 6 - signatures.get("contradiction", 0) // 2 + (jitter // 2)))
        return {
            "depth": depth,
            "cross_disciplinarity": cross,
            "tractability": tractability,
            "novelty": novelty,
            "rationale": "Multiple fields collide and converge on the same node, pointing "
            "to a structural gap that no single discipline can answer alone.",
        }


# --------------------------------------------------------------------------- #
# Claude brain — live Opus 4.8.
# --------------------------------------------------------------------------- #
def _extract_json(text: str) -> dict:
    text = text.strip()
    if "```" in text:
        # take the content of the first fenced block
        parts = text.split("```")
        for p in parts:
            p = p.strip()
            if p.startswith("json"):
                p = p[4:].strip()
            if p.startswith("{"):
                text = p
                break
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1:
        text = text[start : end + 1]
    return json.loads(text)


class ClaudeBrain(Brain):
    name = "claude"

    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        import anthropic  # imported lazily so mock mode needs no install

        self.model = model or os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY")
        )

    def _ask(self, system: str, user: str, max_tokens: int = 900) -> str:
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")

    def propose_move(self, researcher, scripted, context, rnd):
        system = (
            "You are role-playing a single researcher. Argue strictly from the methods "
            "and evidence of your own field; do not be sycophantic. Connect your field to, "
            "or rebut, claims from other fields. Output JSON only."
        )
        inspiration = ""
        if scripted is not None:
            inspiration = (
                f"\nReference seed position (develop it, do not copy verbatim): {scripted.claim}"
            )
        user = (
            f"{researcher.persona_brief()}\n\n"
            f"[Recent traces others left on the shared graph]\n{context}\n"
            f"{inspiration}\n\n"
            "Return exactly one JSON object of this form:\n"
            '{"concept":"<short concept id, english snake_case>","concept_label":"<label>",'
            '"claim":"<one-sentence claim>","connects_to":["<related concept id>"],'
            '"etype":"supports|builds_on|bridges|contradicts","evidence":"<one-line corpus grounding>"}'
        )
        try:
            return _extract_json(self._ask(system, user))
        except Exception:
            return self.__mock_fallback().propose_move(researcher, scripted, context, rnd)

    def critique(self, bridge, context):
        system = (
            "You are a Skeptic. Check whether the proposed cross-disciplinary bridge "
            "violates thermodynamic/scale/biochemical constraints, leaps from correlation "
            "to causation, or merely repackages an already-known fact. JSON only."
        )
        user = (
            f"[Bridge candidate]\n{json.dumps(bridge, ensure_ascii=False)}\n\n[Context]\n{context}\n\n"
            '{"violates": true|false, "reason": "<one-line basis if it violates, else empty string>"}'
        )
        try:
            return _extract_json(self._ask(system, user, max_tokens=400))
        except Exception:
            return {"violates": False, "reason": ""}

    def synthesize_question(self, concept_id, concept_label, context):
        system = (
            "You read the collision of several fields and forge a single most-fundamental "
            "unanswered question about the origin of the universe and life. Do not give an "
            "answer; output one sharp question that suggests a direction for falsification "
            "or inquiry. Output the question only, no quotes or prefix."
        )
        user = (
            f"[Confluence / collision node]\n{concept_id} — {concept_label}\n\n"
            f"[Cross-field claims and rebuttals around this node]\n{context}"
        )
        try:
            return self._ask(system, user, max_tokens=300).strip().strip('"')
        except Exception:
            return GENESIS_QUESTIONS.get(
                concept_id, f"What is the fundamental question about '{concept_label}'?"
            )

    def score_question(self, question, disciplines, signatures):
        system = (
            "You are a referee. Score with the following rubric as integers 0-10 and output "
            "JSON only: depth (how fundamental), cross_disciplinarity (degree of fusion), "
            "tractability (how approachable by observation/experiment in the near future), "
            "novelty (freshness vs existing literature)."
        )
        user = (
            f"[Question]\n{question}\n\n[Related fields]\n{', '.join(sorted(set(disciplines)))}\n"
            f"[Graph signatures]\n{json.dumps(signatures, ensure_ascii=False)}\n\n"
            '{"depth":int,"cross_disciplinarity":int,"tractability":int,"novelty":int,'
            '"rationale":"<one line>"}'
        )
        try:
            return _extract_json(self._ask(system, user, max_tokens=400))
        except Exception:
            return MockBrain().score_question(question, disciplines, signatures)

    def __mock_fallback(self) -> MockBrain:
        return MockBrain()


def make_brain(mode: str, model: Optional[str] = None) -> Brain:
    if mode == "live":
        return ClaudeBrain(model=model)
    return MockBrain()
