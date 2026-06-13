#!/usr/bin/env python3
"""Drive the full Genesis loop against the running Docker stack (localhost:5001),
starting from an already-ontology-generated project. Prints each stage + the final
hypothesis brief, novelty audit verdict, and contributor (glow) weights.

Usage: python run_demo_loop.py <project_id>
"""
import json, sys, time, urllib.request

API = "http://localhost:5001"


def _req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json", "Accept-Language": "en"}
    req = urllib.request.Request(f"{API}{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def post(path, body): return _req("POST", path, body)
def get(path): return _req("GET", path)


def poll_task(path, label, post_body=None, interval=8, timeout=1200):
    deadline = time.time() + timeout
    last = ""
    while time.time() < deadline:
        r = post(path, post_body) if post_body is not None else get(path)
        d = r.get("data") or r
        st = str(d.get("status", "")).lower()
        prog = d.get("progress", d.get("progress_percent", ""))
        msg = f"  [{label}] {st} {prog}"
        if msg != last:
            print(msg, flush=True); last = msg
        if st in ("completed", "success"):
            return r
        if st in ("failed", "error"):
            raise RuntimeError(f"{label} FAILED: {d.get('error') or d.get('message')}")
        time.sleep(interval)
    raise TimeoutError(f"{label} timed out")


def main(project_id):
    print(f"=== Genesis full loop for {project_id} ===", flush=True)

    print("\n[2] Build Zep graph...", flush=True)
    r = post("/api/graph/build", {"project_id": project_id, "graph_name": "ml-hybrid"})
    task_id = r["data"]["task_id"]
    poll_task(f"/api/graph/task/{task_id}", "graph-build")
    graph_id = get(f"/api/graph/project/{project_id}")["data"]["graph_id"]
    print(f"  graph_id: {graph_id}", flush=True)

    print("\n[3] Create + prepare simulation...", flush=True)
    sim = post("/api/simulation/create", {
        "project_id": project_id, "graph_id": graph_id,
        "enable_reddit": True, "enable_twitter": False})
    sim_id = sim["data"]["simulation_id"]
    print(f"  simulation_id: {sim_id}", flush=True)
    prep = post("/api/simulation/prepare", {"simulation_id": sim_id, "use_llm_for_profiles": True})
    ptask = prep["data"].get("task_id")
    poll_task("/api/simulation/prepare/status", "prepare", post_body={"task_id": ptask}, timeout=1200)

    print("\n[4] Run simulation (reddit, 4 rounds)...", flush=True)
    post("/api/simulation/start", {
        "simulation_id": sim_id, "platform": "reddit",
        "max_rounds": 4, "enable_graph_memory_update": True})
    poll_task(f"/api/simulation/{sim_id}/run-status", "sim-run", interval=12, timeout=1800)

    print("\n[5] Generate hypothesis brief + novelty audit...", flush=True)
    rep = post("/api/report/generate", {"simulation_id": sim_id})
    report_id = rep["data"]["report_id"]; rtask = rep["data"].get("task_id")
    poll_task("/api/report/generate/status", "report", post_body={"task_id": rtask}, timeout=1800)
    report = get(f"/api/report/{report_id}")["data"]

    print("\n" + "=" * 70)
    print("HYPOTHESIS BRIEF (first 1500 chars):")
    print("=" * 70)
    print((report.get("markdown_content") or "")[:1500])
    print("\n--- NOVELTY AUDIT ---")
    na = report.get("novelty_audit") or {}
    print("verdict:", na.get("verdict"), "|", (na.get("explanation") or "")[:250])
    print("\n--- CONTRIBUTORS (glow) ---")
    for name, w in sorted((report.get("contributors") or {}).items(), key=lambda x: -x[1]):
        print(f"  {name}: {w}")
    print("\nDONE. report_id:", report_id, "graph_id:", graph_id)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "")
