# 17 Stage-3 Pre-registration: Human Validation, Cross-Model Sensitivity, External Cross-Check, and Replication on New Systems and a Second Benchmark

- Written: 2026-10-18, 11:07 (UTC+8). Committed to git before any of the following happened:
  - the two completed human annotation sheets were copied into this workspace or read;
  - any Spider pair was built, any Spider EX label was computed, or any method was run on Spider;
  - any method was run on the additional BIRD prediction sets;
  - any comparison with the Arcwise-Plat corrections of Jin et al. was computed.
- What has been looked at before writing (no outcome data):
  - file formats and line counts of the six Spider prediction files (all six have 1,034 entries in the order of `dev.json`);
  - the `db_id` order of the BIRD Mini-Dev prediction files against the Arcwise-Plat order (used only to design the mapping check in S3-E);
  - the Spider release file list.
- Stages 1 and 2 (documents 02 and 07, freezes `09de9cf` and `676cab9`) are unchanged. This document only adds Stage 3. All Stage-3 results will be reported whatever they are; negative results are reported as such.

Notation. Tiers use the paper's names, with the code names in parentheses: A_0 (L0), A_1 (L1), A_1f (L1f), A_2 (L2), A_Rq (Rq), A_R (R). "CG" is CaliberGraph (first freeze, `src/`, method `cgx`); "Fuzz" is the certified random fuzzer (`src/`, method `fuzz`); "CG-R" and "Fuzz-R" are the tier-R methods (`src_r/`, methods `cgx_r`, `fuzz_r`). "AI attribution" means the frozen annotator prompt `results/audit_protocol/annotator_prompt.md`, two blind passes and one adjudication pass on disagreements, with model `claude-opus-5-5`.

## S3-0 Integrity rules (apply to every part)

1. **Method code is frozen.** The files covered by `docs/FREEZE_SHA256.txt` and `docs/FREEZE_R_SHA256.txt` are not modified. For Spider, the frozen `src/` and `src_r/` trees are copied byte for byte into a separate data root (`spider/`). `tools/verify_freeze.py` checks the copies against both hash lists before and after the runs.
2. **Only adapters are new.** New code is limited to:
   - building Spider pairs and DDL;
   - computing EX;
   - mapping the Mini-Dev indices;
   - the Arcwise comparison;
   - analysis scripts.
   Adapters may be fixed during the smoke test (rule 3). After that, they are frozen at a commit recorded in `docs/FREEZE_S3.md`, with hashes in `docs/FREEZE_S3_SHA256.txt`. The Spider dev and Mini-Dev runs start only after that commit.
3. **Smoke test without outcome data.** The Spider adapters and the frozen methods are smoke-tested only on databases from Spider *train* (not dev): 30 synthetic pairs, each a train gold query and a mechanically mutated copy (drop DISTINCT, `>` to `>=`, or LIMIT 1 removed). Only crashes and run times are inspected.
4. **One run.** Each confirmatory run is executed once. If a run is interrupted, it is resumed with the same seeds and the same inputs; nothing is rerun selectively.
5. **Amendments.** Any change after this commit goes into `docs/en/17a_stage3_amendments.md`. Each entry has a timestamp and states whether it was made before or after the relevant outcome data were seen.
6. **Multiplicity.** The confirmatory p-value tests are listed in S3-F. They are Holm-corrected as one family at α = 0.05. Threshold hypotheses (κ ≥ 0.60) are judged on the point estimate and are reported with a 95% bootstrap CI.

## S3-A Human validation of the AI attribution (60 items, two annotators)

**Material.**
- `results/audit/human_validation/sheet_blind.md` (built 2026-10-16, seed 20261016) contains 60 items in shuffled order:
  - 30 items are a simple random sample from the first-stage attribution sample (CG, Fuzz, SpotIt, SpotIt+, ParSEval-L1 at A_1f);
  - 30 items are a simple random sample from the second-stage sample (CG-R, Fuzz-R at A_R).
- The sheets do not show the tool, the tier or the AI verdict.
- Two annotators labelled independent copies. The completed files are `sheet_annotator1.md` and `sheet_annotator2.md`, as supplied by the authors. The labels are the five verdicts of the annotator prompt.

**Scoring.**
- Scoring uses `src_r/human_validation.py score` (committed 2026-10-16, before the sheets were returned).
- Unfilled items are excluded and counted. Items with a label outside the five are also excluded and counted.

**Measures.**
- M-A1: human–human agreement and Cohen κ, on five labels and on the binary split `implausible_data` vs. other.
- M-A2: for each annotator vs. the AI final label, agreement and κ, on five labels and on the binary split.
- M-A3: `implausible_data` share by stage:
  - for each annotator;
  - for the AI;
  - for the human consensus (items where both annotators agree).
  Each share has a Wilson 95% CI.
- M-A4: the 5 × 5 confusion matrix of each human vs. the AI, and of human 1 vs. human 2.

**Hypotheses.**
- **H-A1 (threshold):** the binary human–human κ is ≥ 0.60.
- **H-A2 (threshold):** for each annotator, the binary human–AI κ is ≥ 0.60.
- **H-A3 (test):** for the human consensus labels, the `implausible_data` share is higher in the first stage than in the second. The test is a one-sided Fisher exact test on the consensus items.
  - Secondary: the same test for each annotator separately.

**Decision rules for the paper.**
- If H-A1 and H-A2 hold, the paper reports the AI attribution as validated on this sample, with the κ values.
- If either fails, the paper says so in the abstract-level summary. The attribution findings are then restated with human-consensus estimates next to the AI estimates, and the disagreement pattern (M-A4) is analysed in the threats section.

The direction of H-A3 is the paper's central attribution claim. If it fails, that claim is weakened accordingly in the text.

## S3-B Cross-model sensitivity of the AI attribution

**Annotator.**
- The model is `claude-sonnet-5-5`, a different model from the original annotator, invoked through the same agent harness.
- It uses the frozen prompt verbatim and receives the same item JSON (blind, without tool or tier).
- It makes one pass, with no adjudication.

**Sample.**
- The 60 human-validation items.
- Plus 140 further items drawn without replacement from the remaining first- and second-stage attribution items (`test_v4_*`, `test_r_*`, calibration items excluded), stratified 70/70 by stage, seed 20261018.
- Total: 200 items.

**Measures.**
- M-B1: agreement and κ between Sonnet and the Opus final label, on five labels and binary.
- M-B2: `implausible_data` share by stage under Sonnet labels.
- M-B3: on the 60 items, Sonnet vs. each human.

**Hypotheses.**
- **H-B1 (threshold):** the binary κ between Sonnet and the Opus final label is ≥ 0.60.
- **H-B2 (test):** under Sonnet labels, the first-stage `implausible_data` share exceeds the second-stage share. The test is a one-sided Fisher exact test on the 200 items.

**Stated limitation.** Both models come from the same vendor, and no other vendor's model is reachable from the study environment. The paper will say so.

## S3-C Cross-check against the corrected annotations of Jin et al. (Arcwise-Plat)

**Data.**
- Repository `uiuc-kang-lab/text_to_sql_benchmarks` at commit `fe76604`. Two files:
  - `data/arcwise_plat_sql_only_with_diff.json`, which corrects only the SQL;
  - `data/arcwise_plat_full_with_diff.json`, which corrects the question, the evidence and the SQL.
- Each file has 498 BIRD dev questions, keyed by BIRD `question_id`.

**Our list.**
- The 123 benchmark-issue questions in `results/audit/benchmark_issues_flags.json` (fixed 2026-10-16): 43 of kind `gold_wrong` and 80 of kind `ambiguous`.

**Population.**
- O = the Arcwise questions that lie in our held-out test split.
- The issue groups are `G` (our `gold_wrong` questions in O) and `A` (our `ambiguous` questions in O).
- The base group `N` is O minus all 123 issue questions.

**Definitions.**
- *SQL corrected*: the Arcwise-Plat-SQL query differs from the BIRD gold after whitespace and case normalisation, and its result on the official BIRD dev database differs from the gold result under set equality (30 s timeout; a timeout counts as "differs").
- *Question corrected*: in Arcwise-Plat-full, the question or the evidence text differs from BIRD dev after whitespace normalisation.

**Hypotheses.**
- **H-C1 (test):** the SQL-corrected rate is higher in `G` than in `N`. The test is a one-sided Fisher exact test.
- **H-C2 (test):** the question-corrected rate, or the SQL-corrected rate (either one), is higher in `A` than in `N`. The test is a one-sided Fisher exact test.

**Descriptive.**
- The full concordance table.
- Our issue questions that Arcwise left unchanged, which are candidate incremental findings. For these, the paper reports counts only and does not claim they are errors.
- Arcwise corrections on questions where our tools found no issue.

**Caveat stated in advance.** Our list comes only from questions where a witness was found and attributed. A non-overlap therefore does not imply disagreement.

## S3-D Replication on a second benchmark: Spider 1.0 dev

**Data.**
- Spider 1.0 release supplied by the authors (`spider.zip`, SHA-256 recorded in `docs/FREEZE_S3.md`): `dev.json` (1,034 questions, 20 databases) and the dev SQLite files.
- Gold = the `query` field.
- The Spider dev databases have not been used anywhere in the study so far, so this is a held-out benchmark for every design decision.

**Systems (six public prediction sets, all 1,034 entries in `dev.json` order).**
1. DAIL-SQL + GPT-4;
2. DAIL-SQL + GPT-4 + self-consistency;
3. Graphix-T5 (all three from the DAIL-SQL repository);
4. DIN-SQL (GPT-4);
5. GPT-4 few-shot;
6. GPT-4 zero-shot (all three from the DIN-SQL repository).

A file is used only if every row matches `dev.json` by position (and, for the CSV files, by question text and `db_id`).

**Pairs and EX.**
- One pair per question × system.
- EX is recomputed by us with the definition used in the paper: the result multisets are compared as sets, as in the BIRD evaluator; errors and timeouts (30 s) count as incorrect.
- The official Spider metrics (exact match, test-suite accuracy) are not used.
- Populations:
  - P_EXC = EX-correct pairs;
  - P_EXI = EX-incorrect pairs whose two queries both execute.
- Runs use distinct (question, prediction) representatives, as on BIRD. Pairs with identical normalised text are skipped, as on BIRD.

**Data profiles.** All are produced by the frozen miners on the Spider dev databases, with no parameter changes:
- DDL from `sqlite_master`;
- format profiles (`db_profile.py`, tier A_1f);
- tier-R profile (`mine_profile.py`, `mine_fd.py`);
- template rows (`sample_rows.py`);
- indexed copies (`build_realdb.py`).

Tier A_2 needs SpotIt's LLM realism constraints, which do not exist for Spider, so A_2 is not reported.

**Runs.** Budget 5 s per pair, two processes, seed 0 (as on BIRD).
- On P_EXC: CG and Fuzz (`src/`), CG-R and Fuzz-R (`src_r/`).
- On P_EXI: CG-R and Fuzz-R, for recall.
- Every witness is certified by the frozen certifiers. CG and Fuzz witnesses are also checked at A_R with `recertify_r.py`.

**Attribution.**
- Samples, each a simple random sample of distinct pairs drawn with seed 20261019 (all witnesses if fewer exist):
  - 60 CG witnesses certified at A_1f;
  - 60 CG-R witnesses certified at A_R;
  - 40 Fuzz-R witnesses certified at A_R.
- The samples are mixed and shuffled, and labelled with the AI attribution procedure.
- The prompt is used verbatim except for three mechanical substitutions:
  - "the BIRD natural-language question and its hint" becomes "the Spider natural-language question (Spider has no hint; evidence is empty)";
  - "BIRD's execution accuracy" becomes "the execution-accuracy metric";
  - the database path points to the Spider dev databases.

**Hypotheses.**
- **H-S1 (test, replicates H5):** on P_EXC, CG-R finds A_R-certified witnesses for more pairs than Fuzz-R. The test is a one-sided exact McNemar test on per-pair discordance, with a 95% CI from a bootstrap clustered by question (10,000 resamples).
- **H-S2 (test, replicates H7):** the `implausible_data` share among sampled CG-R witnesses at A_R is lower than among sampled CG witnesses at A_1f. The test is a one-sided Fisher exact test.
- **H-S3 (test, replicates H6 in direction):** the estimated number of meaningful A_R witnesses (meaningful share × count) is larger for CG-R than for Fuzz-R. The test is a one-sided parametric bootstrap on the difference (binomial resampling of both shares, 10,000 draws), as for H6.

**Descriptive (stated now, no test).**
- Witness counts per method and tier, recall on P_EXI, and the cost per pair.
- Profile statistics compared with BIRD:
  - share of columns with a stored domain;
  - number of UCCs and INDs per table;
  - value dependencies.

  The expectation is that small, partly synthetic Spider instances yield tighter, more accidental profiles. Tier A_R may therefore admit fewer witnesses on Spider than on BIRD. If so, this is reported as a finding about mining profiles from small instances, not as a method failure.
- The benchmark-issue list for Spider: questions whose witnesses are labelled `gold_wrong` or `ambiguous`.

## S3-E Additional systems on BIRD (BIRD Mini-Dev prediction sets)

**Data.**
- The thirteen SQLite prediction sets in `bird-bench/mini_dev`, `llm/exp_result`:
  - `TA_output`: 4 sets;
  - `sql_output_kg`: 9 sets.
- Each set has 500 predictions keyed by Mini-Dev index.

**Mapping.** Mini-Dev index → BIRD `question_id`, by one of two routes:
- (i) the official Mini-Dev JSON, if the authors can obtain it;
- otherwise (ii) the positional alignment with the Arcwise-Plat list (whose order matches Mini-Dev).

Route (ii) is validated in two ways:
- (a) the `db_id` carried by every prediction equals the `db_id` of the mapped question, for ≥ 99% of indices;
- (b) for at least 95% of indices whose prediction executes, the set of tables referenced by the prediction is a subset of the tables of the mapped question's database and shares at least one table with the BIRD gold.

Indices that fail are dropped and counted. If the validation fails overall, S3-E is not run, and the paper says so.

**Population.**
- Mapped questions in our held-out test split.
- New distinct (question, prediction) representatives only: representatives already run in Stage 2 are excluded, so no result is reused or double-counted.
- EX is recomputed on the official BIRD dev databases (same definition).

**Runs.** CG-R and Fuzz-R on P_EXC, at budget 5 s.

**Attribution.**
- A random sample of 40 CG-R witnesses at A_R (seed 20261020), labelled with the AI procedure.
- Descriptive comparison with the Stage-2 CG-R share.

**Hypothesis.**
- **H-E1 (test, replicates H5 on new systems):** CG-R finds A_R-certified witnesses for more pairs than Fuzz-R. The test is a one-sided exact McNemar test.

## S3-F Confirmatory family and reporting

- **p-value tests (Holm, α = 0.05):** H-A3, H-B2, H-C1, H-C2, H-S1, H-S2, H-S3, H-E1.
- **Threshold hypotheses:** H-A1, H-A2, H-B1.
- **Everything else is descriptive or exploratory**, and is labelled so in the paper.
- **Planned paper changes, whatever the outcome:**
  - a validation subsection with S3-A, S3-B and S3-C;
  - a "Second benchmark and new systems" subsection with S3-D and S3-E;
  - an updated threats section.
- **If H-S1 or H-S2 fails on Spider,** the paper reports that the BIRD result did not replicate, and adds a profile-based explanation from the descriptive statistics, labelled post hoc.

## S3-G Data and output locations

- `spider/` holds the Spider data root (frozen code copies, `data/`, `results/`). Paths are relative to the repository.
- `results/stage3/` holds the S3-A, S3-B, S3-C and S3-E outputs and the summary JSON files that are turned into paper macros.
- The licence notes for Spider (CC BY-SA 4.0), the DAIL-SQL and DIN-SQL prediction files, and Arcwise-Plat are added to `THIRD_PARTY_NOTICES.md` before release.
