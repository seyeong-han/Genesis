"""Render Genesis Questions as legible "Genesis Question Cards" (terminal + markdown)."""

from __future__ import annotations

from .brain_types import GenesisQuestion


def render_card_text(q: GenesisQuestion, rank: int) -> str:
    s = q.scores
    bar = lambda v: "█" * int(v) + "░" * (10 - int(v))  # noqa: E731
    lines = [
        f"┌─ Genesis Question #{rank}  ── 합류 노드: {q.label}",
        f"│ ❓ {q.question}",
        f"│",
        f"│ 잇는 분야: {' ⨯ '.join(q.disciplines)}",
        f"│ 기여 연구자: {', '.join(q.contributors)}",
        f"│",
        f"│ 지지 근거:",
    ]
    for sup in q.supporting:
        lines.append(f"│   • {sup}")
    if q.tensions:
        lines.append("│ 긴장/반박:")
        for t in q.tensions:
            lines.append(f"│   ✗ {t}")
    lines += [
        "│",
        f"│ 근본성   {bar(s.get('depth',0))} {s.get('depth',0)}/10",
        f"│ 융합도   {bar(s.get('cross_disciplinarity',0))} {s.get('cross_disciplinarity',0)}/10",
        f"│ 탐구가능 {bar(s.get('tractability',0))} {s.get('tractability',0)}/10",
        f"│ 신규성   {bar(s.get('novelty',0))} {s.get('novelty',0)}/10",
        f"│ → 총점 {q.total:.0f}/40",
        f"└{'─' * 60}",
    ]
    return "\n".join(lines)


def render_card_markdown(q: GenesisQuestion, rank: int) -> str:
    s = q.scores
    md = [
        f"### Genesis Question #{rank} — 합류 노드 `{q.label}`",
        "",
        f"> **{q.question}**",
        "",
        f"- **잇는 분야**: {' ⨯ '.join(q.disciplines)}",
        f"- **기여 연구자**: {', '.join(q.contributors)}",
        f"- **점수**: 근본성 {s.get('depth',0)} / 융합도 {s.get('cross_disciplinarity',0)} / "
        f"탐구가능 {s.get('tractability',0)} / 신규성 {s.get('novelty',0)}  (총 {q.total:.0f}/40)",
        "",
        "**지지 근거**",
    ]
    md += [f"- {x}" for x in q.supporting] or ["- (없음)"]
    md.append("")
    md.append("**긴장 / 반박**")
    md += [f"- {x}" for x in q.tensions] or ["- (없음)"]
    if s.get("rationale"):
        md += ["", f"_심판 코멘트: {s['rationale']}_"]
    md.append("")
    return "\n".join(md)
