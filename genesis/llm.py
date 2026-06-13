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
        if {"양자기초론", "의식 이론"}.issubset(disciplines):
            return {
                "violates": True,
                "reason": "관찰자-의식 연결은 상관을 인과로 비약할 위험 (범주오류). "
                "측정의 '관찰자'는 물리적 상호작용이지 경험 주체가 아닐 수 있다.",
            }
        if {"의식 이론", "복잡계 과학"}.issubset(disciplines):
            return {
                "violates": True,
                "reason": "창발로서의 의식 vs 근본 성질로서의 의식 — 경계 기준 없이 합의 불가.",
            }
        return {"violates": False, "reason": ""}

    def synthesize_question(self, concept_id, concept_label, context):
        return GENESIS_QUESTIONS.get(
            concept_id,
            f"'{concept_label}'를 둘러싼 분야 간 충돌은 우주·생명의 기원에 대해 "
            f"어떤 근본 질문을 강제하는가?",
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
            "rationale": "여러 분야가 같은 노드에서 충돌·합류하며, 어느 단일 분야도 "
            "단독으로 답할 수 없는 구조적 공백을 가리킨다.",
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
            "너는 한 명의 연구자를 연기한다. 반드시 너의 분야의 방법·증거에서만 논증하고, "
            "비위맞추기를 하지 말라. 다른 분야의 주장과 너의 분야를 잇거나 반박하라. "
            "JSON만 출력하라."
        )
        inspiration = ""
        if scripted is not None:
            inspiration = (
                f"\n참고용 시드 입장(그대로 베끼지 말고 발전시켜라): {scripted.claim}"
            )
        user = (
            f"{researcher.persona_brief()}\n\n"
            f"[공유 그래프에서 최근 남들이 남긴 흔적]\n{context}\n"
            f"{inspiration}\n\n"
            "다음 형식의 JSON 하나만:\n"
            '{"concept":"<짧은 개념 id, 영문 snake_case>","concept_label":"<한글 라벨>",'
            '"claim":"<한 문장 주장>","connects_to":["<관련 개념 id>"],'
            '"etype":"supports|builds_on|bridges|contradicts","evidence":"<코퍼스 근거 한 줄>"}'
        )
        try:
            return _extract_json(self._ask(system, user))
        except Exception:
            return self.__mock_fallback().propose_move(researcher, scripted, context, rnd)

    def critique(self, bridge, context):
        system = (
            "너는 회의주의자(Skeptic)다. 제안된 분야 간 다리가 열역학·스케일·생화학 제약을 "
            "위반하거나, 상관을 인과로 비약하거나, 이미 알려진 사실의 재포장인지 점검하라. JSON만."
        )
        user = (
            f"[다리 후보]\n{json.dumps(bridge, ensure_ascii=False)}\n\n[맥락]\n{context}\n\n"
            '{"violates": true|false, "reason": "<위반 시 한 줄 근거, 아니면 빈 문자열>"}'
        )
        try:
            return _extract_json(self._ask(system, user, max_tokens=400))
        except Exception:
            return {"violates": False, "reason": ""}

    def synthesize_question(self, concept_id, concept_label, context):
        system = (
            "너는 여러 분야의 충돌을 읽고, 인류가 아직 답하지 못한 '우주·생명의 기원'에 관한 "
            "가장 근본적인 질문 하나를 벼려낸다. 답을 주지 말고, 반증/탐구의 방향이 보이는 "
            "날카로운 질문 한 문장을 한국어로 출력하라. 따옴표·접두사 없이 질문만."
        )
        user = (
            f"[합류·충돌 노드]\n{concept_id} — {concept_label}\n\n"
            f"[이 노드를 둘러싼 분야 간 주장·반박]\n{context}"
        )
        try:
            return self._ask(system, user, max_tokens=300).strip().strip('"')
        except Exception:
            return GENESIS_QUESTIONS.get(concept_id, f"{concept_label}에 관한 근본 질문은 무엇인가?")

    def score_question(self, question, disciplines, signatures):
        system = (
            "너는 심판이다. 다음 루브릭으로 0~10 정수 채점하고 JSON만 출력하라: "
            "depth(근본성), cross_disciplinarity(분야 융합도), tractability(가까운 미래에 "
            "관측·실험으로 접근 가능한 정도), novelty(기존 문헌 대비 신선함)."
        )
        user = (
            f"[질문]\n{question}\n\n[관련 분야]\n{', '.join(sorted(set(disciplines)))}\n"
            f"[그래프 시그니처]\n{json.dumps(signatures, ensure_ascii=False)}\n\n"
            '{"depth":int,"cross_disciplinarity":int,"tractability":int,"novelty":int,'
            '"rationale":"<한 줄>"}'
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
