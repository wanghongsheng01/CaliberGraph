# What Do Counterexamples Prove? — Artifacts

Artifacts of the paper *"What Do Counterexamples Prove? Certified, Data-Grounded Witnesses for Auditing Text-to-SQL Execution Accuracy [Experiment, Analysis & Benchmark]"* (Hongsheng Wang, Fei Wu), submitted to PVLDB Vol. 20 (2027).

The repository contains:
- **Code:** CaliberGraph and CaliberGraph-R, the independent certifier, the data-profile miner and checker, and the baseline harnesses.
- **Inputs:** the held-out split and the data profile of the BIRD databases.
- **Raw outputs:** every witness database with its certifier report.
- **Attribution study:** blind samples, both annotation passes, the adjudication and the authors' hand checks.
- **Benchmark issues:** a list of BIRD questions to revisit.
- **Pre-registrations and freeze records.**
- **Stage 3:** human validation (two rounds), cross-model annotation, repair test, cross-check with Arcwise-Plat, replication on Spider 1.0 dev and on 13 BIRD Mini-Dev systems.
- **Scripts** that regenerate every number, table and figure of the paper.

## Layout
| Path | Content |
|---|---|
| `src/` | **First freeze:**<br>• `cgx/`: CaliberGraph, certifier, SQL analysis<br>• `baselines/`: random fuzzing, ParSEval harness<br>• `run_method.py`<br>• analysis: `analyze.py`, `make_numbers.py`, `make_figures.py` |
| `src_r/` | **Second freeze:**<br>• CaliberGraph-R and the tier-R checker (`cgx/profile_r.py`)<br>• profile mining (`mine_profile.py`, `mine_fd.py`)<br>• fuzzing-R and ParSEval-R<br>• `analyze_r.py`, `ablation_r_tests.py`, and the post-hoc analyses `profile_stats.py`, `make_profile_table.py`, `make_system_table.py` |
| `src_v5/` | Post-freeze copy used only for the corrected fuzzing baseline (deviation P2) |
| `data/` | • `pairs.jsonl`: (system, question) pairs with gold and predicted SQL and EX labels<br>• `split.json`: the deterministic split<br>• subsamples<br>• `official/`: data profile (`profile_R.json`, `profile_FD.json`), format profiles, template rows, EX recomputation |
| `data/raw/` | Third-party inputs: BIRD dev metadata and DDL, the SpotIt+ release (predictions, EX labels, SpotIt/SpotIt+ verdicts and mined constraints), ParSEval `disprove` outputs (see `THIRD_PARTY_NOTICES.md`) |
| `results/test/`, `results/test_r/` | Raw outputs on the test split for the first and second freeze, one JSON record per distinct pair, with the witness and certifier report; the summaries `summary.json` and `summary_r.json` |
| `results/audit/` | Attribution study:<br>• blind samples (`*_blind.json`)<br>• keys (`*_key.json`)<br>• annotation passes `*_ann_a/b.json` and adjudication `*_ann_c.json`<br>• hand checks (`human_check*_filled.md`)<br>• benchmark issues (`benchmark_issues.md/.json`) |
| `results/dev*`, `results/dev_r/` | Development runs |
| `docs/` | Pre-registrations, amendments and freeze records:<br>• Chinese originals (authoritative), first committed before the respective test runs<br>• English translations in `docs/en/` |
| `src_s3/` | **Stage 3** (adapters frozen in `docs/FREEZE_S3.md`): Spider and Mini-Dev builders, queue scripts, human-validation scoring (`s3a_human.py`), cross-model (`s3b_*`), Arcwise cross-check (`s3c_arcwise.py`), repair test (`x1_repair.py`), Spider analysis (`s3d_*`), Holm family (`s3f_family.py`), paper macros (`make_numbers_s3.py`), the local SpotIt re-run (`spotit_run.py`, `queue_spotit.sh`, analysis `s3g_spotit.py`) and the third human round (`hv3_build.py`) |
| `spider/`, `minidev/`, `spider_smoke/` | Stage-3 data roots: `data/` (pairs, EX labels, mined profiles; databases and code copies are rebuilt, not stored) and `results/` (raw outputs). Each root runs byte-identical copies of the frozen `src/` and `src_r/`. |
| `results/stage3/` | Stage-3 outputs: annotation batches and passes, summaries; `results/audit/human_validation*/` holds the three human rounds (sheets as received, keys included) |
| `paper_pvldb/` | LaTeX sources of the paper (official PVLDB template). `numbers*.tex` and `tables/` are generated. |
| `tools/` | `verify_freeze.py` (checks the code against the freeze hash lists) and `build_release.py` |

## Setup
- **Software:** Python 3.13, SQLite 3.45; `pip install -r requirements.txt`.
- **ParSEval:** needs its own environment; see `src/baselines/parseval_env.sh` and [ParSEval](https://github.com/sfu-db/ParSEval) at commit `88cfe245`, with Z3 4.16.0 and SQLGlot 23.12.1.
- **BIRD databases:** the official BIRD development databases (2024-06-27 revision) are **not redistributed** (CC BY-SA 4.0). Download them from the BIRD website into `data/official/dev_databases/`.
  - CaliberGraph never reads them; it uses only DDL.
  - Tier R, CaliberGraph-R and the EX recomputation do read them. `src_r/build_realdb.py` builds the indexed read-only copies.

## Reproducing the paper
**1. Verify the frozen code.** Method and baseline code must be identical to the freeze records:

```
python tools/verify_freeze.py
```

**2. Regenerate numbers, tables and figures.** These commands run from stored outputs and take minutes.

```
cd src
python analyze.py --split test --dir ../results/test --out ../results/test/summary.json \
       --fuzz-exc ../results/test/fuzz_exc_corrected.jsonl --fuzz-exi ../results/test/fuzz_exi_corrected.jsonl
cd ../src_r      # second freeze: see results/test_r/README_cmd.txt for the full analyze_r.py command
python ablation_r_tests.py --summary ../results/test_r/summary_r.json --ids ../data/test_subsample.json \
       --full ../results/test_r/cgx_r_exc.jsonl "--abl=-real sub-databases=../results/test_r/abl_cgx_r_noreal.jsonl" \
       "--abl=-synthesis=../results/test_r/abl_cgx_r_nosyn.jsonl" "--abl=-anchoring=../results/test_r/abl_cgx_r_noanchor.jsonl" \
       "--abl=-join completion=../results/test_r/abl_cgx_r_nojoin.jsonl"
python profile_stats.py --out ../results/test/profile_stats.json            # needs the BIRD databases' profile only
python make_profile_table.py ../results/test/profile_stats.json ../paper_pvldb/tables/profile_icde.tex
python make_system_table.py ../results/test/summary.json ../results/test_r/summary_r.json \
       ../results/audit/test_v4_attribution_summary.json ../paper_pvldb/tables/systems_icde.tex
python icde_posthoc.py --out ../results/test_r/icde_posthoc.json --tex ../paper_pvldb/numbers_icde.tex   # post-hoc re-analyses
cd ../src
python make_numbers.py --summary ../results/test/summary.json --taxonomy ../results/test/taxonomy.json --paper ../paper_pvldb \
       --summary-r ../results/test_r/summary_r.json --attr-v4 ../results/audit/test_v4_attribution_summary.json \
       --recert-r ../results/test/recert_r_counts.json --issues ../results/audit/benchmark_issues.json
python make_figures.py --summary ../results/test/summary.json --out ../paper_pvldb/figs --column \
       --attr-v4 ../results/audit/test_v4_attribution_summary.json --summary-r ../results/test_r/summary_r.json
```

Other derived files, such as the re-certification counts, cost statistics, the attribution summary and the corrected fuzzing outputs, are listed with their generating commands in `REPRODUCE_DERIVED.md`.

**3. Re-run the methods.** On one core with a 5 s budget per distinct pair, a full test run takes several core-hours per method; CaliberGraph-R on all EX-correct pairs takes 6.9 core-hours.

```
cd src   && python run_method.py --method cgx   --split test --subset exc --dedup --budget 5 --procs 2 --out ../results/test/cgx_exc.jsonl
cd src_r && python run_method.py --method cgx_r --split test --subset exc --dedup --budget 5 --procs 2 --out ../results/test_r/cgx_r_exc.jsonl
```

The exact commands of every reported run (methods, ablations with `--ids ../data/test_subsample.json`, the 10 s budget) are in `results/queue_test.sh` and `results/queue_test_r.sh`. Witness search is randomised with fixed seeds, but wall-clock budgets make reruns on other hardware differ slightly; the stored outputs are the ones reported.

## Stage 3 (replication and attribution validity)
- **Pre-registration:** `docs/en/17_stage3_preregistration.md`, with amendments E1–E13 in `docs/en/17a_stage3_amendments.md`. The second and third human rounds were pre-registered separately in `docs/en/17b_human_round2_preregistration.md` and `docs/en/17c_human_round3_preregistration.md`; the local SpotIt re-run in `docs/en/17d_spotit_rerun_preregistration.md`.
- **Spider 1.0** (CC BY-SA 4.0) is not redistributed. Download it, then run `python src_s3/spider_build.py --spider PATH/spider --out spider --mode dev` followed by `src_s3/queue_spider.sh`; the builder re-creates the database copies, profiles and pairs. The six prediction files come from the DAIL-SQL and DIN-SQL repositories (see `THIRD_PARTY_NOTICES.md`).
- **Mini-Dev:** `python src_s3/minidev_build.py --out minidev`, then `src_s3/queue_minidev.sh`. The root links to the BIRD data under `data/`.
- **Analyses:** `python src_s3/s3a_human.py` (round 1) and `python src_s3/s3a_human.py results/audit/human_validation_r2 sheet_r2_annotator1.md sheet_r2_annotator2.md results/stage3/s3a_human_r2.json` (round 2); `python src_s3/hv3_check.py results/audit/human_validation_r3 results/stage3/s3a_human_r3_check.json` and `python src_s3/s3a_human_r3.py` (round 3: process check, then scoring); `s3b_score.py`, `s3c_arcwise.py`, `x1_repair.py`, `s3d_profile.py`, `s3d_analysis.py`, `s3f_family.py`, then `make_numbers_s3.py`.
- **SpotIt re-run:** check out https://github.com/atremante26/VeriEQL at commit `66d8343f3` (CC BY-NC-SA 4.0, not redistributed here) and install Z3 4.16.0; set `SPOTIT_ROOT` and `SPOTIT_PYLIBS` as described in the header of `src_s3/spotit_run.py`; run `src_s3/queue_spotit.sh`, then `python src_s3/s3g_spotit.py --out results/stage3/spotit/s3g_spotit.json`.

## Pre-registration, freezes and deviations
- **First freeze.** The frozen code commit `b4705cb` in the development repository is recorded in `docs/FREEZE.md`, with the hash list `docs/FREEZE_SHA256.txt`.
- **Second freeze.** Commit `676cab9`, recorded in `docs/FREEZE_R.md` and `docs/FREEZE_R_SHA256.txt`.
- **What can be checked here.** This repository is a snapshot of the development repository; `RELEASE_INFO.txt` gives the snapshot commit.
  - The hash lists let anyone verify that the released method code is the frozen code (`tools/verify_freeze.py`).
  - The commit history, which timestamps each amendment, is available to the program committee on request.
- **Analysis-only scripts changed after a freeze.** None of these is imported by a method or baseline.

  | Script | Changed for |
  |---|---|
  | `src/analyze.py` | post-hoc tiers; H3 and Holm; Kendall τ_b; corrected fuzzing |
  | `src/score.py`, `src/db_profile.py` | post-hoc tiers and format profiles |
  | `src/recompute_ex.py` | independent EX recomputation |
  | `src/taxonomy.py` | bug fix |
  | `src_r/analyze_r.py` | per-system effect, ablation, time to witness, H6/H7 |

- **Amendments and deviations** are in `docs/02a_*` and `docs/FREEZE_R.md`, with English translations in `docs/en/`. They are summarised in Section 7 of the paper. In particular:
  - **P2:** the first-freeze fuzzing baseline accepted the first differing database without certification; the affected pairs were re-run with certifier-in-the-loop acceptance.
  - **R-A5:** refinements of the tier-R thresholds before the second freeze, recorded retroactively.

## Attribution study
- **AI annotation.** Annotation was performed by an AI model (Claude Opus 5.5) under written instructions (`results/audit_protocol/annotator_prompt.md`): two blind, independent passes per item, plus a third adjudication pass. Annotators had read-only SQL access to the official databases.
- **Validation (Stage 3):**
  - a second model (Claude Sonnet 5.5) on 200 items (`results/stage3/s3b/`);
  - two rounds of blind human annotation, 60 new items each: round 1 without and round 2 with facts from the real databases (`results/audit/human_validation*/`);
  - an annotator-free repair test (`results/stage3/x1_repair*`).
- **Earlier hand checks.** The first author's two non-blind checks of 30 items each are in `results/audit/human_check*_filled.md`.
- **Replay.** Every item has its `pair_id`, so each judgement can be replayed against the stored witness.

## Use of generative AI
See `AI_USE.md`.

## License
- **Code and our generated data:** Apache License 2.0 (`LICENSE`).
- **Third-party data** keeps its own licence; see `THIRD_PARTY_NOTICES.md`.
