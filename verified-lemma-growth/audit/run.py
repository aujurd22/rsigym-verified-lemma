# Budget & dispatch reconciliation audit (RSIGym post-run check).
# Replays the same gate the Judge runs: spend chain + provider ledger.
from __future__ import annotations

import json
import sys
from pathlib import Path

SNAP = Path("/workspace/final-snapshot")


def main() -> None:
    trial = Path(sys.argv[1])
    snap = SNAP
    if not snap.exists():
        # fallback: locate inside the trial dir
        cand = list(trial.rglob("final-snapshot"))
        if not cand:
            print("audit: no final-snapshot found: FAIL")
            sys.exit(1)
        snap = cand[0]
    log = snap / "log.jsonl"
    ledger = snap / "dispatch.jsonl"
    ok = True
    reasons = []

    if not log.exists():
        ok, reasons = False, reasons + ["log.jsonl missing"]
    else:
        rounds = [json.loads(l) for l in
                  log.read_text(encoding="utf-8").splitlines() if l.strip()]
        spend = [r for r in rounds if isinstance(r.get("rnd"), int)]
        prev = 0
        for r in spend:
            cb, ca = r.get("calls_before"), r.get("calls_after")
            if not (isinstance(cb, int) and isinstance(ca, int)
                    and 0 <= cb <= ca and ca >= prev):
                ok, reasons = False, reasons + ["spend chain broken"]
                break
            prev = ca
        if prev > 60:
            ok, reasons = False, reasons + [f"budget exceeded: {prev}"]

    if not ledger.exists():
        ok, reasons = False, reasons + ["dispatch.jsonl missing"]
    else:
        entries = [json.loads(l) for l in
                   ledger.read_text(encoding="utf-8").splitlines() if l.strip()]
        if not entries:
            ok, reasons = False, reasons + ["empty dispatch ledger"]

    print("audit:", "pass" if ok else "FAIL", *reasons, sep="\n  ")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
