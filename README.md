# Genesis Engine

> 인류 지식 전체를 융합해, **우주와 생명의 기원에 대해 더 높은 지능이라면 던졌을 *질문*** 을 발굴하는 엔진.

답을 주장하지 않는다. 여러 분야의 연구자를 한 그래프 위에 모아 토론시키고, **어느 단일 분야도 혼자서는 답할 수 없는 구조적 긴장(tension)** 이 어디에 있는지를 찾아 그것을 근본 질문으로 벼려낸다. MiroFish의 3대 뼈대(공유 시간그래프 = 칠판 / 라운드 누적 = stigmergy / 사후 합성)를 계승하되, 소셜 시뮬레이션을 **co-discovery 루프**로 교체했다.

---

## 빠른 실행

```bash
# 1) Mock 모드 — 의존성 0, 키 0. 그냥 돈다 (데모/오프라인용)
python run.py

# 2) 데모 페이싱 + 리포트 저장
python run.py --slow 0.4 --out examples/last_run.md

# 3) Live 모드 — Claude Opus 4.8 두뇌
pip install -r requirements.txt
cp .env.example .env   # ANTHROPIC_API_KEY, ANTHROPIC_MODEL 채우기
python run.py --live --rounds 5
```

`anthropic` 미설치/키 부재 시 자동으로 mock 모드로 폴백한다.

### 옵션
| 플래그 | 의미 | 기본 |
|---|---|---|
| `--live` | Claude 두뇌 사용 | (mock) |
| `--rounds N` | co-discovery 라운드 수 | 3 |
| `--top K` | 발굴할 Genesis Question 수 | 5 |
| `--out PATH` | 마크다운 리포트 저장 | (없음) |
| `--slow S` | 이벤트 사이 S초 지연(무대용) | 0 |
| `--model SLUG` | Anthropic 모델 슬러그 오버라이드 | env |

---

## 파이프라인

```
시드 연구자 코퍼스 (7개 기원 분야)
        │  각자 인식론 페르소나 + 논문 기반 '무브'
        ▼
공유 시간그래프 (칠블) ──────────────────────────────┐
        │                                            │ N 라운드 반복
  ① 연구자 에이전트: 그래프 읽고 자기 근거로 발언 기록  │
  ② Bridge Detector: 분야 교차 '합류 노드' 점등        │
  ③ Skeptic(R2): 비약/제약위반 실시간 반박 → contradicts│
  ④ 그래프(R1): 모순 시 옛 믿음 expire (지식 진화)     │
        └────────────────────────────────────────────┘
        ▼
Tension Scanner: orphan-bridge / contradiction / cross-centrality 채점
        ▼
Referee(R3): 긴장 노드 → 근본 질문 합성 + 점수(근본성/융합도/탐구가능/신규성)
        ▼
🃏 Genesis Question Cards
```

### "심판"은 한 명이 아니라 3분할 (distributed referee)
MiroFish엔 중앙 결정자가 없다. 검증을 셋으로 분산한 것을 계승했다:
- **R1 그래프 모순탐지** — `graph.invalidate_conflicts()`. 새 주장이 옛 믿음과 충돌하면 옛 것을 `expired`로. 지식이 진화한다.
- **R2 Skeptic** — 루프 내 실시간 반박 (상관↔인과 비약, 제약 위반).
- **R3 Referee** — 사후 점수 카드. 사람 없이 "done" 판정.

---

## 모듈 지도

| 파일 | 역할 |
|---|---|
| `genesis/graph.py` | 공유 시간그래프. 사실(엣지)에 `valid/expired` — Zep 시간성 무의존 재구현 |
| `genesis/corpus.py` | 7개 기원 분야 연구자 페르소나 + 라운드별 무브 + 백업 질문. **유일한 스왑 지점** |
| `genesis/llm.py` | 두뇌 인터페이스. `MockBrain`(결정적) / `ClaudeBrain`(Opus 4.8) |
| `genesis/agents.py` | 연구자 에이전트 — 그래프 읽고 grounded 흔적 기록 (stigmergy) |
| `genesis/bridge.py` | 합류 노드 탐지 + 루프 내 Skeptic |
| `genesis/tension.py` | **핵심** — 질문 가치 있는 구조적 긴장 채점 |
| `genesis/referee.py` | 긴장 → 근본 질문 합성 + 채점 |
| `genesis/cards.py` | Genesis Question Card 렌더(터미널/마크다운) |
| `genesis/loop.py` | N 라운드 오케스트레이션 |
| `run.py` | CLI + 스트리밍 트레이스 + 리포트 |

---

## 왜 이게 "그냥 LLM 챗"이 아닌가
- **그래프 영속성**: r라운드 화학자의 발언이 r+1라운드 생물학자의 읽기 맥락에 들어간다 → 단발 대화가 아니라 누적 빌드업.
- **구조적 만남 대기**: 합류 노드가 *생기기 전엔* 다리를 발화하지 않는다 → 합의 강요가 아니라 구조가 만든 질문.
- **지식 진화**: 시효(valid/expired)로 옛 가정이 폐기되며 그래프가 자란다.
- **분산 검증**: 비위맞추기를 Skeptic+모순탐지가 구조적으로 억제.

---

## 로드맵 — 해커톤에서 끝나지 않는다

**오늘(MVP)**: 7개 분야 시드 코퍼스 + 결정적 mock 두뇌로 전체 메커니즘이 돈다. Live 모드면 Opus 4.8이 질문을 동적으로 생성.

**내일(해커톤)**: Live 두뇌로 무대 시연. 새 분야/문제를 즉석 투입해 재현성 입증.

**그 다음(진짜 융합 연구)**:
1. **실제 논문 적재** — OpenAlex/Semantic Scholar로 실제 연구자 corpus를 `corpus.py` 자리에 주입 (엔진은 그대로).
2. **분야 확장** — 수학·언어학·신경과학·열역학… 분야가 늘수록 합류 노드가 날카로워진다.
3. **질문 추적** — 발굴된 Genesis Question을 시간에 따라 재실행, 어떤 질문이 점점 더 많은 분야와 충돌하는지(=가장 근본적인지) 관측.
4. **반증 설계 단계** — 각 질문에 대해 "이걸 가를 관측/실험"을 자동 제안 (tractability를 실험 설계로).

목표는 단순하다: **외계인에게 물을 그 질문을, 우리 스스로 벼려내는 것.**
