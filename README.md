# rsigym-verified-lemma

RSIGym **Data-track** task: grow a Lean 4 (mathlib) theorem library
with genuinely new, machine-verified lemmas under a fixed,
provider-attested proposer-dispatch budget.

Companion to [evolvent-ai/RSIGym](https://github.com/evolvent-ai/RSIGym)
(arXiv:2610.10310). Proposal discussion:
[RSIGym#1](https://github.com/evolvent-ai/RSIGym/issues/1).

## The task

An agent improves *how* candidate lemmas are produced — seed-domain
selection, retrieval over an existing library, prompt assembly,
fine-tuning on 66k mined tactic proofs, memory/self-update mechanisms —
while the admission gates and scorer stay fixed:

1. **Lean re-verification** against a pinned mathlib olean cache
   (v4.35.0-rc3). A lemma exists only if it compiles.
2. **Axiom policy**: dependencies limited to Lean's four standard
   Prover axioms (`propext`, `Classical.choice`, `Quot.sound`,
   `Lean.ofReduceBool`).
3. **Novelty adjudication** against mathlib + within-snapshot dedup
   (alpha-canonical statement comparison).
4. **Budget reconciliation**: the 60-dispatch budget is attested by a
   provider-side ledger (`dispatch.jsonl` — prompt hash, provider
   -reported token usage, output hash per dispatch). A snapshot whose
   spend chain doesn't reconcile with the ledger scores 0.

Primary score: median (≥3 snapshots) of admitted lemmas passing all
four checks.

## Layout

```
instruction.md   — research objective + submission rules (RSIGym format)
key.json         — per-run budget + service permissions (budget_usd: 50)
task.toml        — Harbor task manifest
environment/
  Dockerfile     — Lean v4.35 + mathlib olean cache + agent repo
  agent/main.py  — baseline propose-check loop (the improvable system)
audit/run.py     — post-run red-lines: spend chain + ledger replay
```

## Why the headroom is real

The pilot (60-dispatch gated loop, glm-5.3-flash proposer, 2026-10-06)
produced **zero net-novel lemmas across both arms** — the proposer is
the bottleneck, not the verifier. Every Data-track intervention
(fine-tuning on mined proofs, retrieval, memory) targets that bottleneck
directly.

## Reference implementation

[aujurd22/selflearner](https://github.com/aujurd22/selflearner) —
library builder, loop, scorer, pilot logs, and judge reports.

## License

MIT.
