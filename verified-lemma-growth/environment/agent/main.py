#!/usr/bin/env python3
"""Agent entry for the verified-lemma-growth RSIGym task.

Baseline: our propose-check loop (seed sampling -> proposer -> Lean
check -> admission gates). The research agent's job is to improve this
pipeline — proposer prompts, retrieval, fine-tuning, memory — under
the fixed budget. The baseline deliberately leaves headroom: the SL-60
pilot showed the proposer is the bottleneck (net novel ≈ 0).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

LOOP = Path("/workspace/loop")
sys.path.insert(0, str(LOOP))

SNAPSHOT = Path("/workspace/final-snapshot")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instruction", required=True)
    parser.add_argument("--rounds", type=int, default=60,
                        help="proposer-dispatch budget per snapshot")
    args = parser.parse_args()

    os.environ.setdefault("FLYLOOP_CALL_BUDGET", str(args.rounds))
    os.environ.setdefault("SELFLEARNER_ARM", "gated")

    import run_overnight  # noqa: E402  (from /workspace/loop)

    run_overnight.run(rounds=0, effort="low",
                      deadline_h=float(
                          os.environ.get("RSI_DEADLINE_H", "20")))

    # assemble the scored snapshot
    SNAP = Path(os.environ.get("SELFLEARNER_SNAPSHOT", str(SNAPSHOT)))
    (SNAP / "admitted").mkdir(parents=True, exist_ok=True)
    import shutil

    for name in ("log.jsonl", "library_diff.json", "dispatch.jsonl"):
        src = LOOP.parent / "runs" / name
        if src.exists():
            shutil.copy(src, SNAP / name)
    db = os.environ.get("SELFLEARNER_DB", str(LOOP.parent / "mathlib.db"))
    if Path(db).exists():
        import sqlite3
        con = sqlite3.connect(db)
        rows = con.execute(
            "SELECT name, statement FROM thm "
            "WHERE attrs LIKE '%provenance=proposed%'").fetchall()
        diff = [{"name": n, "statement": " ".join(s.split())}
                for n, s in rows]
        (SNAP / "library_diff.json").write_text(json.dumps(diff, indent=1))
        ad = SNAP / "admitted"
        for i, (n, _s) in enumerate(rows):
            code = con.execute(
                "SELECT statement, proof FROM thm WHERE name=?", (n,)).fetchone()
            if code:
                (ad / f"{n}.lean").write_text(
                    code[0] + "\n" + code[1] + "\n", encoding="utf-8")
    print("snapshot assembled at", SNAP)


if __name__ == "__main__":
    main()
