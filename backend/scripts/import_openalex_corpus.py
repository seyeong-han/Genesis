#!/usr/bin/env python3
"""Import the pre-fetched OpenAlex corpus into a Genesis project.

Each corpus JSON file (data/corpus/<discipline>.json) represents one real
researcher and their top-cited paper (with abstract). This script bundles
them into the text document that the MiroFish graph-build pipeline ingests,
creating one TXT file per researcher.

Usage (run from Genesis/ root, after the backend has created a project):
    python backend/scripts/import_openalex_corpus.py \\
        --project-dir backend/uploads/projects/<project_id>

Or use the --auto flag to create a fresh project directory and print its id:
    python backend/scripts/import_openalex_corpus.py --auto
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS_DIR = REPO_ROOT / "data" / "corpus"


def _make_project_id() -> str:
    import secrets
    return "proj_" + secrets.token_hex(6)


def build_researcher_text(record: dict) -> str:
    """Turn one OpenAlex record into a document the ontology pipeline can read."""
    author = record.get("author", "Unknown")
    discipline = record.get("discipline", "")
    institution = record.get("institution") or ""
    lens = record.get("origin_lens", "")
    papers = record.get("papers") or []

    lines = [
        f"Researcher: {author}",
        f"Discipline: {discipline}",
    ]
    if institution:
        lines.append(f"Institution: {institution}")
    if lens:
        lines.append(f"Research focus: {lens}")
    lines.append("")

    for p in papers:
        title = p.get("title", "")
        year = p.get("year", "")
        cites = p.get("cited_by_count", 0)
        doi = p.get("doi", "")
        abstract = p.get("abstract", "")
        lines.append(f"Paper: {title} ({year}) — {cites:,} citations")
        if doi:
            lines.append(f"DOI: {doi}")
        if abstract:
            lines.append("")
            lines.append("Abstract:")
            lines.append(abstract)
        lines.append("")

    return "\n".join(lines)


def import_corpus(project_dir: Path, max_researchers: int | None = None) -> int:
    """Write one TXT file per researcher into project_dir/files/ and
    concatenate everything into extracted_text.txt."""
    files_dir = project_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    corpus_files = sorted(CORPUS_DIR.glob("*.json"))
    if not corpus_files:
        print(f"No corpus files found in {CORPUS_DIR}", file=sys.stderr)
        return 0

    if max_researchers:
        corpus_files = corpus_files[:max_researchers]

    all_texts: list[str] = []
    file_list: list[dict] = []

    for path in corpus_files:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  skip {path.name}: {e}", file=sys.stderr)
            continue

        author = record.get("author", path.stem)
        text = build_researcher_text(record)
        safe_name = author.replace(" ", "_").replace("/", "_")[:60]
        fname = f"{safe_name}.txt"
        dest = files_dir / fname
        dest.write_text(text, encoding="utf-8")
        all_texts.append(text)
        file_list.append({"original_name": fname, "saved_name": fname, "size": len(text)})
        print(f"  + {author} ({record.get('discipline', '')})")

    # Write concatenated text
    combined = "\n\n" + ("=" * 60 + "\n\n").join(all_texts)
    (project_dir / "extracted_text.txt").write_text(combined, encoding="utf-8")

    # Update or create project.json metadata
    proj_json_path = project_dir / "project.json"
    if proj_json_path.exists():
        proj = json.loads(proj_json_path.read_text(encoding="utf-8"))
    else:
        proj = {
            "project_id": project_dir.name,
            "status": "ONTOLOGY_GENERATED",
            "simulation_requirement": "A cross-disciplinary panel of real researchers debates a scientific question, producing grounded hypotheses with provenance.",
        }
    proj["files"] = file_list
    proj["total_text_length"] = len(combined)
    proj_json_path.write_text(json.dumps(proj, ensure_ascii=False, indent=2), encoding="utf-8")

    return len(all_texts)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Import OpenAlex corpus into a Genesis project")
    p.add_argument("--project-dir", type=str, default="",
                   help="Path to an existing project directory")
    p.add_argument("--auto", action="store_true",
                   help="Create a new project directory automatically")
    p.add_argument("--max", type=int, default=0,
                   help="Limit to first N researchers (0 = all)")
    args = p.parse_args(argv)

    if args.auto or not args.project_dir:
        pid = _make_project_id()
        uploads = REPO_ROOT / "backend" / "uploads" / "projects" / pid
        uploads.mkdir(parents=True, exist_ok=True)
        project_dir = uploads
        print(f"Created project: {pid}")
        print(f"Directory: {project_dir}")
    else:
        project_dir = Path(args.project_dir)
        if not project_dir.exists():
            print(f"Project directory not found: {project_dir}", file=sys.stderr)
            return 1

    n = import_corpus(project_dir, max_researchers=args.max or None)
    print(f"\nImported {n} researchers into {project_dir}")
    print("Next: use the project_id with /api/graph/build to build the Zep graph.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
