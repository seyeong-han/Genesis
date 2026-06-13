#!/usr/bin/env python3
"""Drive sim + report from an already-built graph. Persisted via nohup.
Usage: python run_sim_report.py <project_id> <graph_id>
"""
import json, sys, time, urllib.request

API = "http://localhost:5001"


def _req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json", "Accept-Language": "en"}
    req = urllib.request.Request(f"{API}{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def post(p, b): return _req("POST", p, b)
def get(p): return _req("GET", p)


def poll(path, label, post_body=None, interval=10, timeout=1800):
    deadline = time.time() + timeout
    last = ""
    while time.time() < deadline:
        try:
            r = post(path, post_body) if post_body is not None else get(path)
        except Exception as e:
            print(f"  [{label}] poll error: {e}", flush=True); time.sleep(interval); continue
        d = r.get("data") or r
        st = str(d.get("status", "")).lower()
        prog = d.get("progress", d.get("progress_percent", ""))
        msg = f"  [{label}] {st} {prog} {str(d.get('message',''))[:60]}"
        if msg != last:
            print(msg, flush=True); last = msg
        if st in ("completed", "success"):
            return r
        if st in ("failed", "error"):
            raise RuntimeError(f"{label} FAILED: {d.get('error') or d.get('message')}")
        time.sleep(interval)
    raise TimeoutError(f"{label} timed out")


def main(project_id, graph_id):
    print(f"=== sim+report: {project_id} / {graph_id} ===", flush=True)

    print("\n[3] Create + prepare simulation...", flush=True)
    sim = post("/api/simulation/create", {
        "project_id": project_id, "graph_id": graph_id,
        "enable_reddit": True, "enable_twitter": False})
    sim_id = sim["data"]["simulation_id"]
    print(f"  simulation_id: {sim_id}", flush=True)
    prep = post("/api/simulation/prepare", {
        "simulation_id": sim_id, "use_llm_for_profiles": True,
        "entity_types": ["Researcher"], "force_regenerate": True})
    poll("/api/simulation/prepare/status", "prepare",
         post_body={"task_id": prep["data"].get("task_id")}, timeout=1800)

    print("\n[4] Run simulation (reddit, 3 rounds)...", flush=True)
    post("/api/simulation/start", {
        "simulation_id": sim_id, "platform": "reddit",
        "max_rounds": 3, "enable_graph_memory_update": True})
    poll(f"/api/simulation/{sim_id}/run-status", "sim-run", interval=15, timeout=2400)

    print("\n[5] Generate hypothesis brief + novelty audit...", flush=True)
    rep = post("/api/report/generate", {"simulation_id": sim_id})
    report_id = rep["data"]["report_id"]
    poll("/api/report/generate/status", "report",
         post_body={"task_id": rep["data"].get("task_id")}, timeout=2400)
    report = get(f"/api/report/{report_id}")["data"]

    print("\n" + "=" * 70, flush=True)
    print("HYPOTHESIS BRIEF (first 2000 chars):", flush=True)
    print("=" * 70, flush=True)
    print((report.get("markdown_content") or "")[:2000], flush=True)
    print("\n--- NOVELTY AUDIT ---", flush=True)
    na = report.get("novelty_audit") or {}
    print("verdict:", na.get("verdict"), "|", (na.get("explanation") or "")[:300], flush=True)
    print("\n--- CONTRIBUTORS (glow) ---", flush=True)
    for name, w in sorted((report.get("contributors") or {}).items(), key=lambda x: -x[1]):
        print(f"  {name}: {w}", flush=True)
    print(f"\nALL DONE. report_id={report_id} sim_id={sim_id}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
