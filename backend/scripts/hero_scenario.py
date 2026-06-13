#!/usr/bin/env python3
"""
Hero scenario setup for the Genesis demo.

This script pre-runs the full pipeline (import corpus → build graph → prepare sim
→ run sim → generate report → novelty audit) for the chosen hero question and
caches the result. On stage, replay with --replay to serve the cached output without
live network/API calls.

Hero question (origin domain):
  "Is consciousness a fundamental ingredient of the universe or does it emerge from
  complex information processing — and is there an observation or experiment that
  could decide between the two?"

Run (first time, needs ZEP + ANTHROPIC keys in .env):
    python backend/scripts/hero_scenario.py --run

Replay (on stage, no network needed):
    python backend/scripts/hero_scenario.py --replay

The script is a runbook; each step calls the Genesis API. You can run steps
individually with --step N (1-5).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

API = "http://localhost:5001"
CACHE = Path(__file__).parent.parent.parent / "data" / "hero_cache.json"

HERO_QUESTION = (
    "Is consciousness a fundamental ingredient of the universe or does it emerge from "
    "complex information processing — and is there an observation or experiment that "
    "could decide between the two? Bring in quantum foundations, complexity theory, "
    "philosophy of mind, neuroscience, and information physics."
)

HERO_DISCIPLINES = [
    "consciousness_studies",
    "quantum_foundations",
    "neuroscience",
    "complex_systems_self_organization",
    "philosophy_of_mind",
    "information_theory",
    "cognitive_science",
]


def _post(path: str, body: dict) -> dict:
    req = urllib.request.Request(
        f"{API}{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def _get(path: str) -> dict:
    req = urllib.request.Request(f"{API}{path}", headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def _poll(path: str, interval: int = 5, timeout: int = 600) -> dict:
    """Poll a GET status endpoint until it reports success or failure."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = _get(path)
        status = (result.get("data") or result).get("status", "")
        print(f"  status: {status}")
        if status in ("completed", "COMPLETED", "success"):
            return result
        if status in ("failed", "FAILED", "error"):
            raise RuntimeError(f"Step failed: {result}")
        time.sleep(interval)
    raise TimeoutError(f"Timed out polling {path}")


def _poll_post(path: str, body: dict, interval: int = 5, timeout: int = 600) -> dict:
    """Poll a POST-only status endpoint (task_id sent in JSON body)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = _post(path, body)
        status = (result.get("data") or result).get("status", "")
        print(f"  status: {status}")
        if status in ("completed", "COMPLETED", "success"):
            return result
        if status in ("failed", "FAILED", "error"):
            raise RuntimeError(f"Step failed: {result}")
        time.sleep(interval)
    raise TimeoutError(f"Timed out polling {path}")


def step1_import_corpus() -> str:
    """Import the OpenAlex corpus for hero disciplines → returns project_id."""
    print("\n=== Step 1: Import corpus ===")
    import subprocess
    script = Path(__file__).parent / "import_openalex_corpus.py"
    result = subprocess.run(
        [sys.executable, str(script), "--auto"],
        capture_output=True, text=True
    )
    print(result.stdout)
    for line in result.stdout.splitlines():
        if line.startswith("Created project:"):
            return line.split(":")[-1].strip()
    raise RuntimeError("Could not find project_id in import output")


def step2_build_graph(project_id: str) -> str:
    """Build the Zep graph from the imported corpus → returns graph_id."""
    print("\n=== Step 2: Build graph ===")
    resp = _post("/api/graph/build", {"project_id": project_id, "graph_name": "genesis-hero"})
    task_id = resp["data"]["task_id"]
    print(f"  task_id: {task_id}")
    _poll(f"/api/graph/task/{task_id}")
    proj = _get(f"/api/graph/project/{project_id}")
    graph_id = proj["data"]["graph_id"]
    print(f"  graph_id: {graph_id}")
    return graph_id


def step3_prepare_sim(project_id: str, graph_id: str) -> str:
    """Create and prepare the simulation → returns simulation_id."""
    print("\n=== Step 3: Prepare simulation ===")
    sim = _post("/api/simulation/create", {
        "project_id": project_id,
        "graph_id": graph_id,
        "enable_reddit": True,
        "enable_twitter": False,
    })
    sim_id = sim["data"]["simulation_id"]
    print(f"  simulation_id: {sim_id}")
    prep = _post("/api/simulation/prepare", {
        "simulation_id": sim_id,
        "use_llm_for_profiles": True,
    })
    task_id = prep["data"]["task_id"]
    # /api/simulation/prepare/status is POST-only; pass task_id in the body
    _poll_post("/api/simulation/prepare/status", {"task_id": task_id}, interval=10, timeout=600)
    return sim_id


def step4_run_sim(sim_id: str) -> None:
    """Run the simulation with the hero research question."""
    print("\n=== Step 4: Run simulation ===")
    _post("/api/simulation/start", {
        "simulation_id": sim_id,
        "platform": "reddit",
        "max_rounds": 6,
        "enable_graph_memory_update": True,
    })
    _poll(f"/api/simulation/{sim_id}/run-status", interval=10, timeout=900)


def step5_generate_report(sim_id: str) -> dict:
    """Generate the hypothesis brief + novelty audit → returns report dict."""
    print("\n=== Step 5: Generate report ===")
    resp = _post("/api/report/generate", {"simulation_id": sim_id})
    report_id = resp["data"]["report_id"]
    task_id = resp["data"]["task_id"]
    print(f"  report_id: {report_id}, task_id: {task_id}")
    # /api/report/generate/status is POST-only; pass task_id in the body
    _poll_post("/api/report/generate/status", {"task_id": task_id}, interval=10, timeout=900)
    report = _get(f"/api/report/{report_id}")
    return report["data"]


def run_all() -> None:
    project_id = step1_import_corpus()
    graph_id = step2_build_graph(project_id)
    sim_id = step3_prepare_sim(project_id, graph_id)
    step4_run_sim(sim_id)
    report = step5_generate_report(sim_id)

    cache = {
        "project_id": project_id,
        "graph_id": graph_id,
        "simulation_id": sim_id,
        "report": report,
        "hero_question": HERO_QUESTION,
    }
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✓ Hero scenario cached to {CACHE}")
    print("\n--- NOVELTY AUDIT VERDICT ---")
    na = (report.get("novelty_audit") or {})
    print(f"  {na.get('verdict', 'N/A')}: {na.get('explanation', '')[:200]}")
    print("\n--- TOP CONTRIBUTORS (glow) ---")
    for name, w in sorted((report.get("contributors") or {}).items(), key=lambda x: -x[1])[:5]:
        print(f"  {name}: {w}")


def replay() -> None:
    if not CACHE.exists():
        print("No cached hero run found. Run with --run first.", file=sys.stderr)
        sys.exit(1)
    data = json.loads(CACHE.read_text(encoding="utf-8"))
    report = data.get("report") or {}
    print("\n=== HERO SCENARIO REPLAY ===")
    print(f"Question: {data.get('hero_question', '')[:120]}")
    print(f"Graph: {data.get('graph_id')}  Sim: {data.get('simulation_id')}")
    print(f"Report: {report.get('report_id')}")
    print(f"\n--- Hypothesis Brief (first 600 chars) ---")
    print((report.get("markdown_content") or "")[:600])
    print("\n--- NOVELTY AUDIT ---")
    na = report.get("novelty_audit") or {}
    print(f"Verdict: {na.get('verdict', 'N/A')}")
    print(na.get("explanation", "")[:300])
    print("\n--- TOP CONTRIBUTORS (glow nodes) ---")
    for name, w in sorted((report.get("contributors") or {}).items(), key=lambda x: -x[1])[:5]:
        print(f"  {name}: {w}")


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Genesis hero scenario runner")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--run", action="store_true", help="Run the full pipeline and cache")
    g.add_argument("--replay", action="store_true", help="Show cached hero run (offline)")
    args = p.parse_args(argv)
    if args.run:
        run_all()
    else:
        replay()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
