#!/usr/bin/env python3
"""CLI for the OpenAlex ingestion pipeline.

Demo (1 researcher + 1 paper per discipline):
    python ingest.py
Larger roster (e.g. 5 researchers, 3 papers each):
    python ingest.py --per-discipline 5 --papers 3
"""

from __future__ import annotations

import argparse
import sys

from genesis.ingest import ingest, ingest_by_seeds


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Ingest real papers/authors from OpenAlex")
    p.add_argument("--mode", choices=["seeds", "concept"], default="seeds",
                   help="seeds = curated origin-relevant researchers (recommended); "
                        "concept = raw top-cited work per discipline concept")
    p.add_argument("--per-discipline", type=int, default=1, help="[concept mode] top-cited works per discipline")
    p.add_argument("--papers", type=int, default=1, help="papers cached per author")
    p.add_argument("--sleep", type=float, default=0.25, help="politeness delay between API calls (s)")
    args = p.parse_args(argv)

    if args.mode == "seeds":
        ingest_by_seeds(papers_per_author=args.papers, sleep=args.sleep)
    else:
        ingest(per_discipline=args.per_discipline, papers_per_author=args.papers, sleep=args.sleep)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
