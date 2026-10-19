# 17d Pre-registration: Local Re-run of the Original SpotIt under the Common Budget

- **Written** 2026-10-19, after a smoke test on 40 development pairs (`docs/spotit_rerun_feasibility.md`) and before any SpotIt run on test pairs.
- **Why.** The paper compares CaliberGraph with SpotIt's *released* results, which were obtained with up to 600 s per bound and are counted without certification. Two independent reviews asked for SpotIt under the same per-pair budget as our tools, certified by the same certifier.

## Setup (fixed)
- **Code.** atremante26/VeriEQL at commit `66d8343f3fa38f1c348548de1414836806c88615`, the code of the released SpotIt results, run without `--vanilla`, i.e., as SpotIt.
  - Constraints: BIRD primary and foreign keys only; no SpotIt+ constraints.
  - Solver: Z3 4.16.0, with SpotIt's patched `z3.py`.
- **Harness.** `src_s3/spotit_run.py` (frozen at the commit of this document). It applies SpotIt's own preprocessing (upper-casing, identifier clean-up) and configuration (MySQL dialect, `all_null_is_deleted`, date/string encoding switches as in `run.py`).
- **Bounds.** Bounds 1–5 run one after another within one wall-clock budget of **5 s per distinct pair** on one core (`--procs 2` on the 2-core machine), with a hard kill at the budget. A counterexample counts once SpotIt's own validation accepts it; the smallest validated bound is reported. SpotIt's cross-system reuse of counterexamples is not applied.
- **Hash seed.** `PYTHONHASHSEED=0`.
- **Certification.**
  - **Primary:** the frozen certifier (`cert`) at tiers A_0, A_1, A_1f and A_R. A_R is added with `recertify_r.py`.
  - **Diagnostic, not primary:** `cert_recased`, the certification after mapping upper-cased values back to the literals' original case.
- **Order of runs.**
  1. All distinct development EX-correct pairs, to check agreement with the released verdicts at scale. This run is descriptive.
  2. Then, once only, all distinct test EX-correct pairs (`--split test --subset exc --dedup --exclude-sources parseval_model --allow-test`).
- **Not run:** EX-incorrect pairs (recall) at test, because of cost.

## Hypotheses (test pairs, EX-correct; one family, Holm-adjusted)
- **H-SP1.** At A_1f, CaliberGraph (first freeze, stored outputs) certifies more pairs than locally re-run SpotIt. Exact McNemar test, one-sided, with a 95% CI from a bootstrap over questions.
- **H-SP2.** The same at A_0.

## Descriptive
- Re-run SpotIt's certified counts at all tiers, next to its released claims and re-certified released counterexamples.
- Agreement of the re-run verdict with the released verdict, on development and test pairs.
- Time to counterexample, errors, and budget exhaustion.
- The diagnostic re-cased certification.

## Use in the paper
- The local re-run replaces "SpotIt claims" as the budget-matched SpotIt baseline in the RQ1 comparison.
- Released claims and re-certified released counterexamples remain reported as before.
- H1, the comparison with the released claims, stays as pre-registered in stage 1.
- If H-SP1 or H-SP2 fails, the paper says so in RQ1 and in Table F1.
Harness SHA-256: 82268591d0b4dfb15728330c3675a4f5caaac879851e02af0246b1bc838a4ca1  src_s3/spotit_run.py
