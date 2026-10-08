## Proposal: add a Data-track task — `verified-lemma-growth`

Hi — we'd like to contribute a new RSIGym task. TL;DR: **grow a Lean 4
(mathlib) theorem library with genuinely new, machine-verified lemmas
under a fixed, provider-attested proposer budget.** It's a Data-track
problem (the headroom is in *what data the proposer sees and learns
from*), and it exercises an RSI axis your current five benchmarks don't
cover: **knowledge-base growth with verifier-gated admission**.

### Why it fits RSIGym

- **Verifier-backed, zero-cost ground truth**: a lemma "exists" iff it
  compiles under `lake env lean` against a pinned mathlib olean cache
  and depends only on Lean's four standard Prover axioms. No LLM judge
  in the reward path.
- **Provider-side budget attestation**: the proposer gateway records a
  per-dispatch ledger (prompt hash, provider-reported token usage,
  output hash — the ARK Responses API returns a `usage` object we
  verified against the live API). The snapshot must carry it; the
  Judge cross-checks the spend chain against the ledger and forces
  score 0 on mismatch. This is exactly the `key.json` +
  service-budget philosophy of RSIGym, applied at the dispatch level.
- **Large, measurable headroom**: our pilot (60-dispatch gated loop,
  glm-5.3-flash proposer) produced **zero net-novel lemmas across both
  arms** — the proposer is the bottleneck, not the verifier. The
  Data-track intervention space (fine-tuning on 66k tactic proofs,
  retrieval-augmented prompting, memory/self-update mechanisms) is
  exactly where the improvement must come from, and it's measurable.

### What exists already (contributor repos)

- [aujurd22/selflearner](https://github.com/aujurd22/selflearner) —
  reference implementation: 181,316 parsed mathlib theorems (66,217
  with full tactic proofs) in SQLite+FTS5; a propose-check loop with
  compile/axiom/novelty admission gates; a Lean judge scorer; pilot
  logs and judge reports.
- Pilot data: SL-60 gated loop (2026-10-06), 60 dispatches, judge
  adjudication reports, `baseline_snapshot/` with 18 lemmas.
- Task skeleton for RSIGym:
  [aujurd22/rsigym-verified-lemma](https://github.com/aujurd22/rsigym-verified-lemma)
  — mirrors `rsi_task/joint/minimal-aime-opus-5` layout
  (instruction.md, key.json with budget_usd=50, task.toml,
  environment/Dockerfile with Lean v4.35 + mathlib olean cache,
  agent/main.py baseline loop, audit/run.py replaying the
  reconciliation gate).

### Open questions for the maintainers

1. **Task packaging**: should a math/Lean task live under
   `rsi_task/joint/` with its own benchmark service dataset, or is a
   self-contained verifier (local `lake env lean`) acceptable in place
   of a benchmark_server dataset?
2. **Budget semantics**: we enforce the budget via the gateway ledger +
   Judge-side reconciliation (exclusion-based). Is that consistent
   with how RSIGym's auth_server accounting is meant to be consumed by
   task audits, or should the task simply rely on `budget_usd` capping
   model_server spend?
3. **Fine-tuning**: the target model starts from
   `Qwen3.5-35B-A3B-Base` like the AIME task; our Data-track intervention
   is fine-tuning the proposer on mined tactic-proof data. Any
   constraints on dataset size / training server usage we should
   design around?

Happy to restructure to match house conventions. The task is
CPU-only, one node, zero GPUs for the loop itself (training would use
train_server).
