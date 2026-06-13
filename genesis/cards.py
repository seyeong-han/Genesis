"""Render Genesis Questions as legible "Genesis Question Cards" (terminal + markdown)."""

from __future__ import annotations

from .brain_types import GenesisQuestion


def render_card_text(q: GenesisQuestion, rank: int) -> str:
    s = q.scores
    bar = lambda v: "█" * int(v) + "░" * (10 - int(v))  # noqa: E731
    lines = [
        f"┌─ Genesis Question #{rank}  ── confluence node: {q.label}",
        f"│ ❓ {q.question}",
        f"│",
        f"│ Fields bridged: {' ⨯ '.join(q.disciplines)}",
        f"│ Contributing researchers: {', '.join(q.contributors)}",
        f"│",
        f"│ Supporting evidence:",
    ]
    for sup in q.supporting:
        lines.append(f"│   • {sup}")
    if q.tensions:
        lines.append("│ Tensions / rebuttals:")
        for t in q.tensions:
            lines.append(f"│   ✗ {t}")
    lines += [
        "│",
        f"│ Depth        {bar(s.get('depth',0))} {s.get('depth',0)}/10",
        f"│ Cross-disc.  {bar(s.get('cross_disciplinarity',0))} {s.get('cross_disciplinarity',0)}/10",
        f"│ Tractability {bar(s.get('tractability',0))} {s.get('tractability',0)}/10",
        f"│ Novelty      {bar(s.get('novelty',0))} {s.get('novelty',0)}/10",
        f"│ → Total {q.total:.0f}/40",
        f"└{'─' * 60}",
    ]
    return "\n".join(lines)


def render_card_markdown(q: GenesisQuestion, rank: int) -> str:
    s = q.scores
    md = [
        f"### Genesis Question #{rank} — confluence node `{q.label}`",
        "",
        f"> **{q.question}**",
        "",
        f"- **Fields bridged**: {' ⨯ '.join(q.disciplines)}",
        f"- **Contributing researchers**: {', '.join(q.contributors)}",
        f"- **Scores**: depth {s.get('depth',0)} / cross-disc. {s.get('cross_disciplinarity',0)} / "
        f"tractability {s.get('tractability',0)} / novelty {s.get('novelty',0)}  (total {q.total:.0f}/40)",
        "",
        "**Supporting evidence**",
    ]
    md += [f"- {x}" for x in q.supporting] or ["- (none)"]
    md.append("")
    md.append("**Tensions / rebuttals**")
    md += [f"- {x}" for x in q.tensions] or ["- (none)"]
    if s.get("rationale"):
        md += ["", f"_Referee note: {s['rationale']}_"]
    md.append("")
    return "\n".join(md)
