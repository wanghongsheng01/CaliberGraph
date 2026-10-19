# 17b Pre-registration: Second Human Validation Round (with facts from the real database)

- **Written:** 2026-10-18, before the material was sent to the annotators.
- **Why there is a second round.** Round 1 (S3-A in document 17; amendments E2 and E3 in 17a) did not validate the AI attribution. Round 1 is reported in full whatever round 2 shows; round 2 does not replace it.
- **The difference tested.** The round-1 annotators had no access to the real data. The AI annotators did, and their `implausible_data` verdicts cite facts about the real data.
- **Question.** Do human annotators who are shown such facts agree with each other and with the AI on whether a witness difference rests on implausible data?

## Material
- **Sample.** `results/audit/human_validation_r2/sheet_blind.md`, built by `src_s3/hv2_build.py` with seed 20261021: 30 first-stage and 30 second-stage attributed test items, none of them used in round 1, shuffled.
- **What is not shown.** The sheet does not show tool, tier, AI verdict or repair-test (X1) outcome.
- **What is shown.** Each item carries the section "Facts from the real (official) database". It is generated mechanically and gives the same kinds of facts for every item:
  - for every column that either query references and that appears in the witness: rows, NULLs, distinct values and uniqueness in the official table;
  - how often each witness value of that column occurs in the official table;
  - the full content of referenced tables with at most 15 rows.
- **Instructions.** `results/audit/human_validation_r2/INSTRUCTIONS.md`. The five labels are unchanged. The decision order is made explicit:
  - first decide whether the difference arises only because of data that does not occur in the real database (`implausible_data`, even if one query is "more correct" on the witness);
  - otherwise use `pred_wrong`, `gold_wrong`, `both_wrong` or `ambiguous`.
- **Annotators.** The same two annotators, if available, working independently. The authors will state how the work was done and whether any AI tool was used.
- **Known before writing this document.** The AI labels and the X1 outcomes exist for every item of the pool, but the sample was drawn by seed only. The author running the study has not looked at the AI labels or X1 outcomes of the 60 sampled items.

## Measures and hypotheses
Scoring uses `src_s3/s3a_human.py`, pointed at the round-2 directory, with the same measures as S3-A (M-A1 to M-A4).

- **H-R2-1 (threshold):** the binary human–human κ (implausible vs. other) is ≥ 0.60.
- **H-R2-2 (threshold):** for each annotator, the binary human–AI κ is ≥ 0.60.
- **H-R2-3 (test):** among the human-consensus labels, the `implausible_data` share is higher in the first stage than in the second. The test is a one-sided Fisher exact test at α = 0.05; it is not Holm-adjusted together with document 17.

**Descriptive:**
- agreement of each annotator's `implausible_data` label with the X1 outcome `vanishes`, on first-stage items that X1 repaired;
- the human label distribution compared with round 1.

## Decision rules for the paper
- **If H-R2-1, H-R2-2 and H-R2-3 hold,** the paper reports both rounds. Its conclusion will be: annotators without the real data do not recognise implausible witnesses, and annotators given a fixed set of facts from the real data agree with each other and with the AI attribution.
- **If any of them fails,** the abstract and introduction drop the claim that the AI attribution is human-validated. The attribution findings are then presented as AI-annotator results, with the cross-model agreement (S3-B) and the annotator-free repair test (X1) as their support, and the human results as a stated limitation.
- **The mechanical results stand in either case:** witness counts per admissibility tier, CaliberGraph-R against Fuzz-R, and the Spider replication.
