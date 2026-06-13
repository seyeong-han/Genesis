"""Seed corpus: researcher archetypes spanning the fields that touch *origins*.

Each researcher is an epistemic persona (what they believe, how they argue, what
they accept as evidence, where they are blind) plus a set of grounded "moves" — the
claims they will lay onto the shared graph, round by round. Real-paper corpora
(via OpenAlex/Semantic Scholar) can later replace these seeds without changing the
engine: the personas and moves are the only swappable part.

Shared CONCEPT ids are deliberately reused across researchers — that reuse is what
makes nodes become *cross-disciplinary bridges* on the graph.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# Canonical shared concepts. When two different disciplines both touch one of these,
# the node becomes a confluence point — a candidate for a fundamental question.
CONCEPTS = {
    "information_fundamental": "정보가 물질·시공간보다 근본적인가 (it-from-bit)",
    "observer_measurement": "관찰/측정과 실재의 관계",
    "entropy_arrow": "엔트로피와 시간의 화살, 낮은 엔트로피 초기조건",
    "self_organization": "자기조직화 / 흩어지는 구조(dissipative structure)",
    "emergence": "창발 — 부분에 없던 성질이 전체에서",
    "fine_tuning": "물리상수의 미세조정",
    "computation_universe": "우주는 계산하는가 / 계산으로서의 물리",
    "consciousness": "의식의 본성과 기원",
    "time_origin": "시간 자체의 시작",
    "symmetry_breaking": "대칭 깨짐에서 구조의 출현",
}


@dataclass
class Move:
    """One trace a researcher lays onto the graph in a given round."""
    concept: str            # concept id this move centers on (shared or own)
    concept_label: str      # human label if it's a new concept
    claim: str              # natural-language statement, grounded in their corpus
    connects_to: list[str]  # other concept ids this move links to
    etype: str = "supports"  # supports | builds_on | bridges | contradicts
    evidence: str = ""       # one-line corpus grounding


@dataclass
class Researcher:
    name: str
    discipline: str
    stance: str             # core beliefs / worldview
    method: str             # how they argue
    accepts_as_evidence: str
    blind_spot: str
    moves: list[Move] = field(default_factory=list)

    def persona_brief(self) -> str:
        return (
            f"{self.name} — {self.discipline}\n"
            f"  믿음: {self.stance}\n"
            f"  방법: {self.method}\n"
            f"  증거관: {self.accepts_as_evidence}\n"
            f"  사각지대: {self.blind_spot}"
        )


def seed_researchers() -> list[Researcher]:
    return [
        Researcher(
            name="Dr. Aria Vance",
            discipline="우주론",
            stance="우주는 양자요동에서 인플레이션으로 태어났고, 가장 큰 미스터리는 '왜 초기 엔트로피가 그토록 낮았는가'다.",
            method="장방정식·초기조건·관측 정합성으로 논증",
            accepts_as_evidence="CMB, 대규모 구조, 정량적 우주모형",
            blind_spot="생명·의식을 물리 너머의 우연으로 치부하는 경향",
            moves=[
                Move("time_origin", "시간의 시작", "인플레이션 이전 '시간'은 정의되지 않을 수 있다 — t=0은 좌표가 아니라 경계다.", ["entropy_arrow"], "supports", "CMB의 등방성·평탄성"),
                Move("entropy_arrow", "엔트로피 화살", "우주는 극도로 낮은 엔트로피 상태로 시작했고, 이 초기조건이 시간의 화살을 만든다.", ["time_origin"], "builds_on", "Past Hypothesis, CMB"),
                Move("fine_tuning", "미세조정", "우주상수·초기조건은 생명을 허용하는 좁은 창에 있다 — 다중우주 선택효과로 설명 시도.", ["entropy_arrow"], "supports", "Λ 값의 미세함"),
            ],
        ),
        Researcher(
            name="Dr. Niels Okonkwo",
            discipline="양자기초론",
            stance="측정·관찰자 문제는 부수적 기술이 아니라 실재의 핵심이다. 정보가 상태를 정의한다.",
            method="사고실험·정보이론·해석 비교로 논증",
            accepts_as_evidence="벨 부등식 위배, 양자정보 실험",
            blind_spot="거시적 생물학·화학의 구체 메커니즘에 둔감",
            moves=[
                Move("observer_measurement", "관찰과 측정", "측정 전 상태는 '실재'가 아니라 가능성의 정보다 — 관찰이 사실을 고정한다.", ["information_fundamental"], "supports", "벨 실험"),
                Move("information_fundamental", "근본으로서의 정보", "물리량은 결국 '예/아니오' 정보로 환원된다 (it-from-bit).", ["observer_measurement"], "builds_on", "양자정보 이론"),
                Move("observer_measurement", "관찰과 측정", "관찰자가 없던 초기 우주의 '상태'는 어떤 의미였는가 — 측정 없는 실재는 정의 가능한가?", ["time_origin", "information_fundamental"], "bridges", "측정문제의 우주론적 확장"),
            ],
        ),
        Researcher(
            name="Dr. Mara Lindqvist",
            discipline="생명기원 화학",
            stance="생명은 초자연이 아니라, 자유에너지 기울기를 착취하는 물질의 자기조직화다. 대사가 먼저다.",
            method="반응속도·열역학·실험 재현으로 논증",
            accepts_as_evidence="열수구 실험, 자가촉매 사이클",
            blind_spot="정보·의식 같은 비물질 개념을 과소평가",
            moves=[
                Move("self_organization", "자기조직화", "생명은 비평형에서 에너지를 흘려보내며 질서를 유지하는 흩어지는 구조다.", ["entropy_arrow"], "supports", "Prigogine, 열수구"),
                Move("self_organization", "자기조직화", "대사 네트워크(자가촉매)가 유전정보보다 먼저 출현했을 수 있다.", ["information_fundamental"], "contradicts", "metabolism-first 가설"),
                Move("entropy_arrow", "엔트로피 화살", "생명은 엔트로피 증가를 '가속'하는 배수로다 — 우주의 엔트로피 화살이 생명을 선호한다.", ["self_organization"], "bridges", "MEP 원리"),
            ],
        ),
        Researcher(
            name="Dr. Theo Sasaki",
            discipline="복잡계 과학",
            stance="같은 자기조직화·창발 법칙이 은하·세포·뇌·사회를 관통한다. 스케일은 달라도 논리는 하나다.",
            method="모형·보편성 클래스·시뮬레이션으로 논증",
            accepts_as_evidence="멱법칙, 상전이, 임계성",
            blind_spot="구체 도메인의 예외를 보편성으로 덮어버림",
            moves=[
                Move("emergence", "창발", "부분의 상호작용에서 부분에 없던 질서가 임계점에서 출현한다 — 스케일 불변.", ["self_organization"], "supports", "상전이·임계성"),
                Move("computation_universe", "계산하는 우주", "자연은 국소 규칙의 반복 계산처럼 행동한다 — 생명·인지는 그 계산의 특수 모드.", ["emergence", "information_fundamental"], "bridges", "셀룰러 오토마타, 보편성"),
                Move("emergence", "창발", "의식도 충분한 통합·임계성에서 창발하는 또 하나의 상전이일 수 있다.", ["consciousness"], "supports", "임계성 가설"),
            ],
        ),
        Researcher(
            name="Dr. Lina Hartmann",
            discipline="의식 이론",
            stance="의식은 단순 부산물이 아니다. 통합된 정보가 있는 곳에 경험이 있다 — 의식은 거의 기본 성분에 가깝다.",
            method="공리·정보적 측정(Φ)·현상학으로 논증",
            accepts_as_evidence="신경 상관자, 정보통합 측정",
            blind_spot="검증가능성·반증 설계가 약함",
            moves=[
                Move("consciousness", "의식의 본성", "의식은 시스템의 통합정보(Φ)의 내재적 성질이다 — 창발이 아니라 근본 속성에 가깝다.", ["information_fundamental"], "contradicts", "IIT"),
                Move("observer_measurement", "관찰과 측정", "만약 관찰이 실재를 고정한다면, 경험하는 주체의 출현은 우주가 '실재화'되는 사건과 연결될 수 있다.", ["consciousness", "information_fundamental"], "bridges", "관찰자-의식 연결"),
                Move("consciousness", "의식의 본성", "의식이 창발이라면 어디서 '켜지는가'? 그 경계가 없다는 점이 창발설의 빈틈이다.", ["emergence"], "contradicts", "hard problem"),
            ],
        ),
        Researcher(
            name="Dr. Kenji Adeyemi",
            discipline="정보물리학",
            stance="비트가 먼저다. 시공간·물질은 정보의 처리에서 떠오른 현상이며, 엔트로피는 곧 정보다.",
            method="홀로그래피·열역학·정보이론으로 논증",
            accepts_as_evidence="블랙홀 엔트로피, 홀로그래픽 경계",
            blind_spot="실험적 직접검증과 거리가 멈",
            moves=[
                Move("information_fundamental", "근본으로서의 정보", "엔트로피 = 정보다. 블랙홀 엔트로피는 면적(경계 정보량)에 비례한다.", ["entropy_arrow"], "builds_on", "Bekenstein-Hawking"),
                Move("computation_universe", "계산하는 우주", "시공간은 얽힘 정보의 패턴에서 창발한다 — 기하보다 정보가 선행.", ["information_fundamental", "emergence"], "bridges", "ER=EPR, 홀로그래피"),
                Move("information_fundamental", "근본으로서의 정보", "정보가 물질보다 선행한다면 '태초'는 에너지 사건이 아니라 비트 사건이었다.", ["time_origin"], "contradicts", "물질 우선 모형과 충돌"),
            ],
        ),
        Researcher(
            name="Dr. Sofia Reyes",
            discipline="과학철학",
            stance="'왜 무가 아니라 무언가 있는가'가 근본 질문이다. 인간원리와 설명의 한계를 직시해야 한다.",
            method="개념 분석·논증 구조·반증가능성 검토",
            accepts_as_evidence="논리 정합성, 설명력, 반증가능성",
            blind_spot="정량 모형을 직접 만들지는 못함",
            moves=[
                Move("fine_tuning", "미세조정", "미세조정 설명은 다중우주(선택효과)와 더 깊은 단일원리 사이에서 미결이다.", ["emergence"], "supports", "인간원리 논쟁"),
                Move("observer_measurement", "관찰과 측정", "관찰자 의존 실재와 관찰자 독립 실재 중 무엇이 더 적은 가정을 요구하는가?", ["consciousness"], "bridges", "오컴·실재론 논쟁"),
                Move("emergence", "창발", "창발이 '설명'인지 '설명 포기의 이름'인지 — 강한 창발은 환원 불가를 주장한다.", ["computation_universe", "consciousness"], "contradicts", "강한 vs 약한 창발"),
            ],
        ),
    ]


# Authored Genesis Questions keyed by the concept node that becomes a top tension
# site. Used by the mock brain (and as fallback) so the engine produces coherent
# fundamental questions even with no LLM. The live brain generates these dynamically.
GENESIS_QUESTIONS = {
    "observer_measurement": (
        "관찰자 없는 우주는 '실재'했는가? 측정이 사실을 고정한다면, 관찰·경험하는 "
        "주체의 출현은 우주 생성(cosmogenesis)의 사후 부록이 아니라 그 일부인가 — "
        "즉 우주의 기원과 의식의 기원은 같은 사건의 두 단면인가?"
    ),
    "information_fundamental": (
        "정보(비트)는 물질·시공간보다 존재론적으로 선행하는가? 그렇다면 '태초'는 "
        "에너지의 사건이 아니라 구별(distinction)의 사건이며, 우주는 처음부터 "
        "'계산'이었는가?"
    ),
    "entropy_arrow": (
        "왜 우주는 극도로 낮은 엔트로피로 시작했는가? 그리고 생명은 그 초기조건의 "
        "필연적 귀결(엔트로피를 가속하는 배수로)인가, 아니면 통계적 우연인가?"
    ),
    "consciousness": (
        "의식은 복잡계의 창발인가, 아니면 정보·관찰자처럼 우주의 기본 성분인가? "
        "이 둘을 원리적으로 가를 수 있는 관측·실험은 존재하는가, 아니면 영원히 "
        "미결인가?"
    ),
    "emergence": (
        "'창발'은 진짜 새로운 인과의 출현인가, 아니면 우리가 미시법칙을 못 풀어서 "
        "붙인 이름인가? 강한 창발이 참이라면 환원주의적 기원 서사는 어디서 무너지는가?"
    ),
    "fine_tuning": (
        "물리상수의 미세조정은 다중우주의 선택효과인가, 더 깊은 단일 원리의 그림자인가? "
        "그리고 이 질문 자체는 원리적으로 답할 수 있는가?"
    ),
    "computation_universe": (
        "우주가 '계산'한다면 그 계산은 무엇을, 무엇 위에서 수행하는가? 시공간이 "
        "정보의 창발이라면 기원의 무대 자체가 파생물인가?"
    ),
    "time_origin": (
        "시간 자체에 '시작'이 있는가, 아니면 시작이라는 개념이 시간 안에서만 "
        "정의되는 범주오류인가?"
    ),
}
