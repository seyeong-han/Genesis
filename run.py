#!/usr/bin/env python3
"""Genesis Engine CLI.

Mock (default, zero deps):
    python run.py
Live (Claude Opus 4.8 brain):
    python run.py --live --rounds 5
Write a markdown report:
    python run.py --out examples/last_run.md
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from genesis.cards import render_card_markdown, render_card_text
from genesis.llm import make_brain
from genesis.loop import GenesisResult, run_genesis

DIVIDER = "─" * 64


def _load_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(Path(__file__).parent / ".env")
    except Exception:
        pass


def make_printer(slow: float):
    def printer(event: str, data: dict) -> None:
        if event == "start":
            print(f"\n{DIVIDER}\n  GENESIS ENGINE — discovering the deepest *questions* about origins")
            print(f"  Researcher roster: {', '.join(data['researchers'])}")
            print(f"  Starting {data['rounds']}-round co-discovery on the shared graph\n{DIVIDER}")
        elif event == "move":
            tag = {"contradicts": "⚔", "bridges": "🌉"}.get(data["etype"], "•")
            print(f"  {tag} [{data['discipline']}] {data['author']}: {data['claim']}")
        elif event == "bridge":
            print(f"    🔗 Confluence node lights up! '{data['node']}' ← {' ⨯ '.join(data['disciplines'])}")
        elif event == "critique":
            print(f"    ⚠ Skeptic: rebuts '{data['label']}' → {data['reason']}")
        elif event == "round_end":
            st = data["stats"]
            extra = f", expired {data['expired']}" if data["expired"] else ""
            print(
                f"  ── Round {data['round']} done: nodes {st['nodes']}, valid edges "
                f"{st['edges_valid']}, contradictions {st['contradictions']}{extra}\n"
            )
        elif event == "scanning":
            print(f"{DIVIDER}\n  TENSION SCAN — which node is a question worth solving\n{DIVIDER}")
        elif event == "tension":
            print(f"  ▣ {data['label']}  (tension {data['score']}) — {data['why']}")
        elif event == "done":
            print(f"\n{DIVIDER}\n  Generated {data['questions']} GENESIS QUESTIONS\n{DIVIDER}\n")
        if slow:
            time.sleep(slow)

    return printer


def write_report(result: GenesisResult, path: Path, mode: str) -> None:
    md = [
        "# Genesis Engine — Run Report",
        "",
        f"- brain: `{mode}`",
        f"- graph: {json.dumps(result.stats(), ensure_ascii=False)}",
        f"- rounds: {len(result.rounds)}",
        "",
        "## Discovered Genesis Questions (by score)",
        "",
    ]
    for i, q in enumerate(result.questions, 1):
        md.append(render_card_markdown(q, i))
    md.append("## Per-round co-discovery log\n")
    for t in result.rounds:
        md.append(f"### Round {t.rnd}")
        for m in t.moves:
            md.append(f"- ({m['discipline']}) {m['author']} [{m['etype']}]: {m['claim']}")
        for b in t.bridges:
            md.append(f"  - 🔗 confluence: **{b['node']}** ← {' ⨯ '.join(b['disciplines'])}")
        for c in t.critiques:
            if c["violates"]:
                md.append(f"  - ⚠ Skeptic rebuttal @ {c['label']}: {c['reason']}")
        if t.expired:
            md.append(f"  - 🕒 {t.expired} old belief(s) expired")
        md.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(md), encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Genesis Engine — origin-question discovery")
    parser.add_argument("--live", action="store_true", help="use Claude Opus 4.8 brain (needs API key)")
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--top", type=int, default=5, help="how many Genesis Questions to surface")
    parser.add_argument("--out", type=str, default="", help="write markdown report to this path")
    parser.add_argument("--model", type=str, default="", help="override Anthropic model slug")
    parser.add_argument("--slow", type=float, default=0.0, help="pause between events (demo pacing)")
    parser.add_argument("--quiet", action="store_true", help="suppress streaming trace")
    args = parser.parse_args(argv)

    _load_env()
    mode = "live" if args.live else "mock"
    try:
        brain = make_brain(mode, model=args.model or None)
    except Exception as e:  # e.g. anthropic not installed
        print(f"[live mode init failed: {e}] → falling back to mock mode", file=sys.stderr)
        mode, brain = "mock", make_brain("mock")

    printer = None if args.quiet else make_printer(args.slow)
    result = run_genesis(brain, rounds=args.rounds, top_k=args.top, on_event=printer)

    print("\n" + DIVIDER)
    print("  GENESIS QUESTION CARDS")
    print(DIVIDER + "\n")
    for i, q in enumerate(result.questions, 1):
        print(render_card_text(q, i))
        print()

    if args.out:
        out = Path(args.out)
        if not out.is_absolute():
            out = Path(__file__).parent / out
        write_report(result, out, mode)
        print(f"Report saved: {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
