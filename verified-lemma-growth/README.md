# verified-lemma-growth — RSIGym Data-track task

Improve an agent system that grows a Lean 4 (mathlib) theorem library
with machine-verified, admitted-only writes. See `instruction.md` for
the research objective and `../../../intuition-mechanism` /
`../../../selflearner` (contributor repos) for the reference
implementation and pilot data.

## Layout (mirrors rsi_task/joint/minimal-aime-opus-5)

```
verified-lemma-growth/
├── instruction.md        # research objective + submission rules
├── key.json              # per-run budget + service permissions
├── task.toml             # Harbor task manifest
├── environment/
│   ├── Dockerfile        # Lean toolchain v4.35 + library + loop + agent
│   └── agent/main.py     # baseline propose-check loop (improvable)
├── tests/                # scorer: Lean reverify + axiom policy + novelty
└── audit/                # post-run red-lines: budget + dispatch ledger
```

## Why this fits RSIGym's Data track

The scored artifact is produced by an agent that must improve *how*
candidates are generated — seed selection, retrieval, prompt assembly,
fine-tuning on the 66k tactic-proof library, memory/self-update
mechanisms — under a fixed, provider-attested dispatch budget. The
pilot (SL-60, 2026-10-06) showed the proposer is the bottleneck
(net novel ≈ 0 across both arms), so the headroom for Data-track
interventions is large and measurable.
