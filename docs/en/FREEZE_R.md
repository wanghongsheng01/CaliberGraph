> English translation of `docs/FREEZE_R.md`. The Chinese original is authoritative; it was first committed in 676cab9 on 2026-10-14 09:33:30 +0800 and last changed in 29222ff on 2026-10-15 03:18:03 +0800 (see `git log --follow`).

# FREEZE_R — Second Freeze (Tier R: CaliberGraph-R and its baselines)

- Freeze time: 2026-10-14 09:40 (UTC+8). From then on, the method code in `src_r/` is not modified, and the test set is run only once (`results/queue_test_r.sh`).
- The file hashes are in `docs/FREEZE_R_SHA256.txt` and cover the following:
  - all code under `src_r/`;
  - the data profile files: profile_R, profile_FD, sample_rows;
  - the split files and the pair files;
  - the test subsamples;
  - the queue script;
  - the file sizes of the index copies.
- For the pre-registered hypotheses and decision criteria, see `docs/07_第二次冻结方案_R层与CaliberGraph-R.md`.

## Final state on the development set (round 2, development subsamples of 600/300 pairs, 5 s per pair)

| | CaliberGraph-R | Random fuzzing-R | ParSEval-R | v4 |
|---|---|---|---|---|
| EX-correct pairs: tier-R witness count | 125 | 106 (round 1) | 0 | 1 (181 at tier L1f) |
| Known positives: tier-R recall | 97.2% (round 1) | 91.5% | — | 1.4% |

## Plan amendments before the freeze (made before any tier-R test-set run)

| ID | Content | Reason |
|---|---|---|
| R-A1 | **ParSEval-R is run only on the 1,000-pair test-set subsample** (the same subsample as the ablations), not on the full set. | On the 600-pair development subsample ParSEval-R scored 0: the numbers and dates its constraint solver produces fall outside the observed ranges, while its acceptance condition stays the same. A full run would take about 2.3 hours, and the expected result would still be about 0. The paper will state this and report the subsample results. |
| R-A2 | **Tier-R ablations are run on the 1,000-pair subsample**, four in total: remove the real sub-database stage, remove the synthesis stage, remove anchoring, remove join completion. | Compute. |
| R-A3 | **Tiers R and Rq backfilled for existing results**: computed with `recertify_r.py`, covering the v4 methods, SpotIt, SpotIt+ and CGX+SC; the results are written to the `cert_R` field, without changing the original `cert`. | Consistent with document 07. |
| R-A4 | **Labeling batch for H6**: 100 items of CaliberGraph-R and 100 items of random fuzzing-R are sampled at random, plus 50 items drawn from the already-labeled v4 batch as drift calibration. The three are mixed and blind-labeled in two passes, with a third pass for adjudication. | Consistent with document 07; the calibration items are used to check whether there is drift between the earlier and the later labeling. |

## Addendum (2026-10-14 21:30, written after the independent review): refinement of the tier-R definition before the freeze

| ID | Content | Time and evidence |
|---|---|---|
| R-A5 | Document 07 pre-registered the definition of tier R. During debugging on the development set, before the second freeze, three refinements were made to it:<br>(1) **The condition under which values must belong to the observed value set was tightened.** It was originally "columns with no more than 5,000 distinct values"; it was changed to apply only to categorical columns: text columns with no more than 100 distinct values or no more than 1% of the number of rows, and numeric columns with no more than 20 distinct values. Other columns use range, integrality, lexical-shape and casing constraints instead.<br>(2) **Measure columns do not participate in unique column combinations**, including reals, dates and non-code integers with many values.<br>(3) **Value dependencies added**: intra-table functional dependencies and one-to-one mappings, and consistency of redundant attributes across foreign keys (`profile_FD.json`). | The changes were made at about 07:30–08:15 on October 14, all before the second freeze (09:40). The freeze commit 676cab9 already contains these files, and `FREEZE_R_SHA256.txt` also contains their hashes, so this can be verified.<br>Reason: checks on the development set found two kinds of problem. First, the value-set constraint was too strict; for example, a new regional average salary of 8000 would be judged invalid. Second, there were accidental unique combinations; for example, the amounts of 682 loans happen to be all distinct, which would rule out ties that occur in reality. The value dependencies target problems still present in the pilot attribution, such as "the same school having inconsistent county names in two tables".<br>This amendment was not recorded at the time and is recorded retroactively here. The retroactive record was made after the second test run, but the amendment itself was made entirely before the freeze. |
