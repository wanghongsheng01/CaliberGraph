# 17a Stage-3 Amendment and Event Log

Each entry has a timestamp (UTC+8) and states whether the relevant outcome data had been seen.

## E1 (2026-10-18 11:08) Pre-registration committed
Commit `89c103e`.

## E2 (2026-10-18 11:09–11:12) Human sheets read and S3-A scored as pre-registered
- **Files.** `sheet_annotator1.md` (SHA-256 `59a4d494…`) and `sheet_annotator2.md` (SHA-256 `90048789…`), as supplied by the authors.
  - Apart from the verdict and reason lines, both are identical to `sheet_blind.md`.
  - All 60 items carry a valid label in both sheets.
- **Scoring.** Output in `results/stage3/s3a_human.json`, produced by `src_s3/s3a_human.py`, which implements S3-A exactly as pre-registered.
- **Outcomes of the pre-registered hypotheses:**
  - **H-A1 not met.** Binary κ (implausible vs. other) between the two annotators = −0.05, with 54/60 agreement. Each annotator used `implausible_data` 3 times, on different items. On the five labels, κ = 0.74 (95% CI 0.58–0.88), with 51/60 agreement.
  - **H-A2 not met.** Binary κ against the AI = 0.00 (annotator 1) and 0.18 (annotator 2). Five-label κ = 0.20 and 0.26.
  - **H-A3 not met.** Among consensus items, `implausible_data` was used 0/27 times in stage 1 and 0/24 in stage 2 (Fisher p = 1.0). The AI shares are 14/30 and 7/30.
- **Descriptive.** Of the 21 items the AI labelled `implausible_data`, annotator 1 labelled 11 `gold_wrong` and 9 `pred_wrong`; annotator 2 labelled 9 `gold_wrong`, 8 `pred_wrong` and 3 `implausible_data`. On consensus items, the human labels were: stage 1, 18 `gold_wrong`, 8 `pred_wrong`, 1 `ambiguous`; stage 2, 11 `gold_wrong`, 11 `pred_wrong`, 1 `ambiguous`, 1 `both_wrong`.
- **Post-hoc observation (made after seeing the data; not a pre-registered analysis).**
  - The AI annotator queried the official BIRD databases. Its `implausible_data` reasons cite facts such as "Currency is never NULL in the official DB".
  - The human instructions made database access optional, and the annotators did not have the databases.
  - Several human reasons describe the same witness feature but resolve it as an error of one query *on the witness*. For example: "The witness alignment table labels id=3 as 'Bad' though the evidence says id=3 means Neutral". The construct measured by the two groups may therefore differ.
  - This explanation is a hypothesis and is not used to discount the result.
- **Consequence under the pre-registered decision rule.** The paper must state that the AI attribution was *not* validated by the human check. The attribution findings must be reported with the human estimates next to the AI estimates.
- **Pending.** The authors were asked how the annotations were produced: by whom, with which tools, and with or without database access. The answer determines how the paper describes S3-A.

## E3 (2026-10-18 11:18) How the human annotations were produced (author statement)
- The authors state that the two sheets were completed **independently by two people, without using any AI assistant**.
- The paper will describe S3-A accordingly: two human annotators, independent, without access to the official databases.
- The pre-registered decision rule of E2 applies.
- The authors chose the following follow-up:
  - **(A)** report the S3-A outcome as is and re-centre the paper on the mechanical tier evidence;
  - **(C)** add an annotator-free *repair test* (E4);
  - **(B)** if time permits, run a second human round whose material shows the relevant facts of the real data (to be pre-registered separately before it starts).

## E4 (2026-10-18 11:18) Exploratory analysis X1, the repair test: specification written before it is run
**Status.**
- X1 is exploratory. It was designed after the S3-A outcome was seen, and the paper will label it so.
- It does not replace S3-A.
- The specification below is fixed before any repair is computed.

**Question.** For a certified witness W of a pair (gold G, prediction P), does the difference between G and P depend on the features of W that violate the mined data profile (tier A_R)?

**Population.**
1. All 700 attributed test witnesses (`test_v4_blind.json`, 500, first stage; `test_r_blind.json`, 200, second stage, calibration items excluded).
2. In particular, the 60 human-validation items.

The witnesses are taken from the blind files, which store the full rows of every table.

**Procedure** (`src_s3/x1_repair.py`; uses the frozen `src_r/cgx/profile_r.py`, `profile_R.json`, `profile_FD.json` and the official databases, read-only):
- **Initial state.** If W already satisfies A_R (`ProfileR.ok(W)`), the outcome is `realistic_as_is`.
- **Repair attempts.** Otherwise, K = 20 independent attempts are made (seeds 0..19). Each attempt repeatedly takes one violation (in random order) and applies one local repair:
  - **value:** replace the cell by a value drawn uniformly from up to 500 distinct real values of that column;
  - **lookup row:** replace it by the real lookup row with the same first-column value, or, if there is none, by a random real lookup row;
  - **UCC duplicate:** redraw the UCC columns of the later duplicate from real values;
  - **missing foreign-key parent:** set the child value to an existing parent value in W, or, if the parent table is empty, add a real template parent row carrying the child's value;
  - **total participation:** add a real template child row that references the parent;
  - **symmetric:** add the mirrored row;
  - **irreflexive:** redraw the second column;
  - **FD:** set the dependent column to the official mapped value;
  - **cross-table agreement:** set the child column to the parent's value;
  - **year/date:** set the year to the date's year (or redraw an invalid date).
- **Stopping.** An attempt stops when `ProfileR.ok` holds (*repaired*) or after 200 steps (*failed*).
- **Survival check.** For each repaired variant, G and P are executed on it, and the attempt is recorded as *survives* if the frozen certifier still reports a set difference (`differ.C_set`).

**Outcome per witness.**
- `realistic_as_is`;
- `survives`: at least one repaired variant still differs;
- `vanishes`: at least one variant was repaired, and none differs;
- `unrepairable`: no attempt succeeded.

The survival share (surviving variants divided by repaired variants) is recorded too.

**Pair-level measure.** Whether any A_R-certified witness exists for the pair in the stage-2 runs of CG-R or Fuzz-R (`cert_R.ok`), mapped through the distinct (question, normalised prediction) representative.

**Reported (all descriptive, no tests):**
- Outcome × AI final label, over the 700 witnesses and over the 60.
- Outcome × human-consensus label and × each annotator, over the 60.
- Outcome shares by stage and by tool.
- The same cross-tabulations for the pair-level measure.

**Pre-stated reading.**
- If the AI `implausible_data` labels are right, those witnesses should mostly be `vanishes`.
- If the human labels are right, AI-`implausible_data` witnesses should mostly be `survives` or `realistic_as_is`, or be backed by a pair-level A_R witness.
- Either pattern will be reported.

**Known limitation.** The profile is a proxy for "realistic": it is mined, so it may miss real constraints and may contain accidental ones. Repairs are local, so a variant is one realistic database, not all of them.

## E5 (2026-10-18 11:21) X1 procedure changed after a 12-item smoke run (outcomes of those 12 items were seen)
- **What the smoke run showed.**
  - The first-stage witnesses carry 60–330 profile violations each, because most cells are synthetic.
  - With a fixed cap of 200 steps, repairs ran out of steps. The `unrepairable` outcome then reflected the step cap, not the data.
- **Changes**, all before the full run:
  1. **Fill step.** Before any local repair, cells of columns that neither query references are set to the values of one random real template row of the same table. These cells cannot change either query's result.
  2. **Step cap.** The cap becomes 200 + 5 × (violations remaining after the fill step).
  3. **FD violations.** When the dependent column is referenced by a query and the determinant is not, the determinant is redrawn among the official keys that map to the current dependent value. Otherwise the dependent value is set to the official value, as before.
  4. **Cross-table violations.** When the child column is referenced and the parent column is not, the parent is aligned to the child. Otherwise the child is set to the parent value, as before.
- **Direction of the bias.** Changes 3 and 4 keep query-referenced values where the profile allows it. This makes a `survives` outcome *more* likely, which works against the AI `implausible_data` labels and therefore against the paper's original claim.
- **Smoke-run outcomes (12 first-stage items, before → after the changes):**
  - before: 5 `unrepairable`, 6 `vanishes`, 1 `survives`;
  - after: 1 `unrepairable`, 8 `vanishes`, 3 `survives`.
- **Reporting.** The full run uses the changed procedure. These 12 items are included in it, and the paper reports this amendment.

## E6 (2026-10-18 11:35) Clarifications for S3-D and S3-E, fixed before any Spider dev or Mini-Dev method run
No Spider dev EX label, witness or count had been seen when these were written.
1. **"Fuzz" on Spider is the paper's Fuzz baseline.** That baseline is the stage-1 fuzzer with the post-hoc certifier-in-the-loop correction (amendment P2): pairs where `fuzz` found a witness not certified at A_1f are re-run with `fuzz_cert` (same seed, same budget) and merged. Pre-registration S3-D says "(`src/`, method `fuzz`)". The re-run uses the frozen `src_r/run_method.py`, whose `fuzz_cert` code path is identical to the one used for BIRD (`src_v5`).
2. **Format profiles come from the frozen `src_r/db_profile.py`.** It differs from `src/db_profile.py` only in the output path (`data/format_profiles.json`, the location both frozen `run_method.py` copies read).
3. **Pairs whose gold query fails on the Spider database** (`gold_error`, `gold_timeout`) belong to neither P_EXC nor P_EXI. Their number is reported.
4. **Smoke test (rule S3-0.3) done.**
   - Material: 30 synthetic pairs on six Spider *train* databases.
   - Steps: the frozen miners, CG, Fuzz, CG-R, Fuzz-R and `recertify_r.py` were all run.
   - Result: no crash or error record. No adapter change was needed after the smoke test.
5. **Mini-Dev mapping.** The supplementary literal-overlap diagnostic (string literals of each prediction compared with the mapped question, its evidence and its BIRD gold, at offsets −2 to +2) is reported next to the pre-registered checks (a) and (b). It is not used as a decision criterion.
6. **No concurrency.** The Spider and Mini-Dev runs execute on the same 2-CPU machine with `--procs 2`, as on BIRD, with no other CPU-heavy job running.

## E7 (2026-10-18 11:39) Spider build failure and adapter fix (no outcome seen)
- **What happened.**
  - The first queue start (11:37) built the Spider pairs.
  - The frozen `db_profile.py` then stopped with `Could not decode to UTF-8` on `wta_1`. Two TEXT cells of that database (out of 87,059) are not valid UTF-8; the smoke-test train databases had none.
  - Because the build section lacked a fail-fast check, the queue went on and started CG without format or tier-R profiles.
  - CG wrote 18 records before the queue was stopped. These records are invalid. They were moved unread to `spider/aborted_20261018_1140/` and are not used.
- **Fix (adapter only; the method code is unchanged).**
  - The builder now copies the 20 dev databases instead of linking them.
  - Text cells that are not valid UTF-8 are re-decoded with `errors='replace'`. The number of fixed cells is recorded in `data/manifest.json`.
  - The build section of the queue now stops on any error, and checks that every profile file exists before any method runs.
- **EX labels** are recomputed on the copies. No EX label of the first build had been read.
- **Freeze.** `docs/FREEZE_S3_SHA256.txt` is updated for `spider_build.py` and `queue_spider.sh`.

## E8 (2026-10-18 14:20) Run interruptions and attribution adapters for S3-D (no Spider outcome seen)
- **Interruption and resumption.**
  - The first queue process was stopped by the environment's two-hour limit for background jobs at 13:39, after 3,634 of 3,702 CG runs.
  - The queue was resumed at 13:39 by `src_s3/run_chunk.sh`, which runs the resumable queues in segments of at most 105 minutes. Before resuming, it removes a possibly truncated last line of a result file (none so far).
  - Pairs that were running when a segment stopped are run again from the start, with the same seed and budget.
  - Each later resumption is listed in `spider/results/queue.log` and `minidev/results/queue.log`.
- **Question file for the frozen sampler.**
  - The frozen `src_r/audit_build.py` reads questions from `data/raw/bird_dev_20240627.json`, indexed by question id.
  - For Spider, this file is generated from `dev.json` by `src_s3/spider_devjson.py`, with the fields question, db_id and gold SQL; `evidence` is the empty string.
- **Prompt and blind files.**
  - The Spider annotator prompt is `results/audit_protocol/annotator_prompt_spider.md`. It is the frozen prompt with exactly the three substitutions pre-registered in S3-D, generated by script and checked by `diff`.
  - The blind batches are stored under `results/stage3/s3d/`.

## E9 (2026-10-18 18:25) Round-2 sheets received; scored as pre-registered; provenance query
**Receipt.** The authors supplied `sheet_r2_annotator1.md` (SHA-256 `ba5be0e2…`) and `sheet_r2_annotator2.md` (SHA-256 `55547edc…`) at 18:18, about 6.5 hours after the material was sent.

**Integrity check: the sheets differ from `sheet_blind.md` outside the verdict and reason lines.**
- **Both sheets:** non-breaking spaces in two evidence lines are replaced by ordinary spaces.
- **Annotator 2's sheet:** the line `[End of file.]` is inserted at three places, after source lines 1180, 2091 and 3025.
- **Annotator 1's sheet:**
  - `[End of file.]` is appended at the end;
  - two witness cells are changed: "Civil and Environmental Engineering Department" → "Civil Engineering Department", and "Wicomico County" → "Wicomico";
  - "NULL occurs 0x" is removed from one fact line.
- Such markers and content changes are typical of text that has passed through an automated tool, not of manual editing.
- The authors were asked how the sheets were produced, as 17b requires. Until they answer, round 2 is **not** used in the paper.

**Pre-registered scoring** (`src_s3/s3a_human.py` with round-2 arguments → `results/stage3/s3a_human_r2.json`):
- `implausible_data` labels: 32 by each annotator; 27 by the AI.
- **H-R2-1 met.** Binary human–human κ = 0.80 (CI 0.63–0.93). Five-label κ = 0.75, with 51/60 agreement.
- **H-R2-2 not met.** Binary human–AI κ = 0.44 for each annotator (CI about 0.20–0.66). Five-label κ = 0.24.
- **H-R2-3 met.** Consensus `implausible_data` share: stage 1, 20/25; stage 2, 9/26 (one-sided Fisher p = 0.0012).
- The AI's own shares on these items are 16/30 and 11/30.

## E10 (2026-10-18 18:40) Author statement on round-2 provenance
- **Statement.** The authors state that both round-2 sheets were judged by the two human annotators without any AI tool. The `[End of file.]` markers and the changed cells were introduced by an editing or format-conversion tool, which they did not name. The authors also confirm that round 1 was done entirely by hand.
- **Use in the paper.** Round 2 is reported as a human annotation, according to this statement.
- **Release.** The sheets are released exactly as received, and this log documents the deviations.
- **Affected items.**
  - The changed cells concern items 30 (two witness cells) and 46 (one fact line) of annotator 1's sheet.
  - Both annotators agree on item 30 and on item 46.
  - Excluding the two items leaves the outcomes of H-R2-1 to H-R2-3 unchanged (sensitivity check in `results/stage3/s3a_human_r2_excl.json`).

## E11 (2026-10-18 18:40) Correction to E10
- The authors corrected their statement of E10. The edits outside the label fields (the `[End of file.]` lines and the changed cells) were made **by hand**, not by an editing or conversion tool.
- They confirm that the round-2 annotation was done entirely by hand, and they agree that round 2 is reported in the paper.
- The paper's description is adjusted accordingly.

## E12 (2026-10-18 20:55) Concurrency during the Mini-Dev CG-R run (deviation from E6.6)
- **What overlapped.** During roughly the first 20 minutes of the Mini-Dev CG-R run (20:31–20:50), the following ran on the same machine:
  - the Spider analysis (`analyze_r.py`, about 24 CPU-seconds);
  - the profile comparison;
  - the Spider attribution annotators (light read-only SQL).
- **Possible effect.** Contention can shorten the effective 5 s search budget of some CG-R pairs in that window.
- **Handling.** By rule S3-0.4, no pair is re-run selectively. The deviation is reported instead.
- **Direction of the bias.** The bias, if any, works against CG-R in H-E1. The Fuzz-R run that follows will have the machine to itself.

## E13 (2026-10-19, corrected 14:50) Chunked execution of the SpotIt run (document 17d)
- **What happened.** The SpotIt queue (`src_s3/queue_spotit.sh`) runs in chunks of at most 6,300 s, as the Stage-3 queues do since E8, because background jobs on this machine are limited to 2 h. The first chunk started at 11:19 and reached its limit at 13:04, during the test run, after 1,868 test pairs; the second chunk reached its limit at 14:49, after 5,349 test pairs. (An earlier version of this entry called the first stop "external"; the times show it was the chunk limit. The exit code 144 came from the clean-up command of the wrapper.) No test result was read or analysed between chunks.
- **Handling.** After each stop, every written record was checked to parse completely (none was dropped) and the run was resumed with the same frozen command. The harness skips pairs already present in its output, so every pair is run exactly once; the record being processed at the stop is not written and is run again from the start. By rule S3-0.4, no pair is re-run selectively. Each resumption is logged in `results/stage3/spotit/queue.log`.
- **Possible effect.** None on verdicts, because each pair has its own wall-clock budget and the pairs are independent.

## E14 (2026-10-19 15:35) Round 3 (document 17c): process check, authors' decision, scoring
- **Return.** All three sheets were received at 14:52 on 2026-10-19, the day of distribution, and are archived as received in `results/audit/human_validation_r3/`.
- **Process check** (`src_s3/hv3_check.py` → `results/stage3/s3a_human_r3_check.json`), done before any scoring:
  - all 150 items present in every sheet, in the distributed order; every Verdict is one of the five labels; every Reason is filled in;
  - line by line, every item differs from the blank sheet. After undoing pure Markdown re-formatting (blank lines, table padding, escapes, emphasis style, auto-links), sheets A and C have no content change. In sheet B, an editor removed tag-like values (`<r>`, `<sampling>`, `<data-mining>`, ...) from witness cells and fact lines of items R3-035 and R3-113, and turned one URL into a link (R3-098);
  - recorded times: A 14:30–16:15 (the finish time is later than the return of the file at 14:52); B 10:00–14:42 (the start time is earlier than the creation of the sheets at 10:32); C 11:30–13:59. The estimated effort was seven to nine hours per annotator;
  - reasons: A gave 24 distinct reasons for 150 items, most of them generic templates (e.g., one sentence stating that further analysis would be required, 34 times); B 138 and C 149 distinct reasons, specific to the item;
  - all three declared no use of AI tools.
- **Decision.** The check was reported to the authors with the recommendation to verify the process with the annotators before scoring. The authors decided to adopt all three sheets (A, B and C). The round is therefore scored as pre-registered, and the paper reports the process findings above.
- **Scoring** (`src_s3/s3a_human_r3.py` → `results/stage3/s3a_human_r3.json`):
  - H-R3-1 not met: Fleiss' κ = 0.17 (five labels), 0.03 (binary; CI −0.05 to 0.12);
  - H-R3-2 not met: majority vs AI, binary κ = 0.15 (116 items with a majority; 34 without);
  - H-R3-3 met: majority `implausible_data` 10/52 in stage 1 vs 0/64 in stage 2 (one-sided Fisher p = 0.0002);
  - H-R3-4 met: stage-2 prediction errors 18 (majority) vs 10 (AI) of 64 (exact McNemar p = 0.0078).
- **Post hoc sensitivity** (not pre-registered): without annotator A, B and C agree on the binary judgement with κ = 0.05; the conclusions do not change.
- **Pre-stated rules applied.**
  - Rule 1: the human-majority shares are reported next to the AI shares (Table `tab:humanai`, RQ2, RQ4).
  - Rule 2: the error-weighted EX effect is reported with both error rates and their intervals.
  - Rules 3 and 4 together: H-R3-2 fails, and the human judgement is not reliable even in binary form (κ < 0.60). The abstract and introduction therefore make no claim about the distribution of meaningful witnesses from either annotator, and say that it remains open.
  - Rule 5: rounds 1–3 are all reported.
- **Key.** The key file is published with the sheets, as 17c provides.

## E15 (2026-10-19 15:35) SpotIt re-run (document 17d): outcomes
- **Run.** The run finished at 15:25; all 6,456 distinct test pairs were run once (E13).
- **Analysis** (`src_s3/s3g_spotit.py` → `results/stage3/spotit/s3g_spotit.json`):
  - H-SP1 met: at A_1f, CaliberGraph 1,979 vs re-run SpotIt 101 (1,878 vs 0 discordant; CI +1,699 to +2,057);
  - H-SP2 met: at A_0, 1,979 vs 680 (1,312 vs 13 discordant; CI +1,146 to +1,452);
  - one-sided exact McNemar p < 10^-300 for both, Holm-adjusted over the two.
- **Descriptive.**
  - The re-run claims 1,242 pairs. Its counterexamples are certified for 680 pairs at A_0, 101 at A_1f, 7 at Rq and 0 at A_R.
  - It reproduces 1,094 of the 1,268 released non-equivalence claims (distinct pairs).
  - It agrees with the released verdict on 98% of distinct pairs that neither run reports as an error.
  - 58% of the distinct pairs exhaust the 5 s budget.
  - The diagnostic re-cased certification gives fewer pairs (438 at A_0, 61 at A_1f).
