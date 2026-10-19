> English translation of `docs/07_第二次冻结方案_R层与CaliberGraph-R.md`. The Chinese original is authoritative; it was first committed in 676cab9 on 2026-10-14 09:33:30 +0800 and last changed in 676cab9 on 2026-10-14 09:33:30 +0800 (see `git log --follow`).

# 07 Second Freeze Plan: Data-Profile Realism Admissibility Tier R and CaliberGraph-R (Pre-registration)

Drafted: 2026-10-14 (UTC+8). **This plan was written down before any tier-R method was run on the test set.** For the motivation see document 06: after blind-labeled attribution of the test-set witnesses of the first frozen version (v4), 40–70% hold only on data that would not occur in reality, and this is true of every method.

## 1. Realism admissibility tier R (data profile constraints)

Mined automatically from the official BIRD database (provided by the user) with standard data-profiling queries; the script is `src_r/mine_profile.py`, and the results are written to `data/official/profile_R.json`. On top of L1f, a witness must satisfy all of the following constraints simultaneously, on **all** of its tables and all columns.

**Single-value constraints**
- NULL is allowed only in columns in which NULL has occurred in the official column.
- Numeric values must fall within the observed range; columns that are all integers in the official data must be integers.
- Text values: in columns with no more than 5,000 observed distinct values, the value must be one of the observed values; other columns must satisfy three conditions: the lexical shape is one of the observed lexical shapes, the casing style is one of the observed styles, and there is no leading or trailing whitespace (except where the official data already has it).
- Temporal text must fall within the observed range.
- Primary key and foreign key columns (key columns) allow new identifiers: numeric keys must have a consistent type and integrality, and text keys must have a consistent lexical shape.

**Unique column combinations (UCC)**
- Single columns: all columns are checked.
- Two columns: mined only among foreign key columns, primary key member columns and discrete columns (no more distinct values than half the number of rows).
- The table must have at least 20 rows.

**Inclusion dependencies (IND)**
- Undeclared foreign keys: the values of a same-named column are contained in a unique column of the other table, except for generic names (id, name, type, etc.).
- Total participation: every row of the parent table has at least one child row. Dictionary-table parents are excepted.
- Symmetric relations and no self-loops: checked when two foreign key columns in the same table point to the same column.

**Dictionary tables**: for a table that satisfies all three of the following, only official original rows may appear in a witness.
- No more than 200 rows;
- No more than 3 columns;
- Referenced by a foreign key.

**Year–date consistency**: for an integer column named year, if in the official data it always equals the year of some date column in the same table, then the two must also be equal in the witness.

For tier R we also compute two composite admissibility tiers:
- R = L1f + the constraints above;
- R2 = L2 + the constraints above.

## 2. Methods

### CaliberGraph-R (code in `src_r/`)
Retains all mechanisms of v4: difference anchoring, join-graph completion, SQLite value domain, isolation and controlled growth, mutation search. On top of these it adds:
- **Value-pool filtering and augmentation**: the value pool is first filtered by the tier-R constraints and then supplemented with observed real values. Candidates that "satisfy a query predicate" are also searched for among the real values.
- **Real-row templates**: 60 official real rows are pre-extracted for each table. Columns not involved in the query are taken directly from the template, so the whole row is consistent with reality.
- **Key values**: numeric keys use new identifiers; text keys use real values that have not yet been used; keys of dictionary tables are taken only from the official keys.
- **Tier-R repair**:
  - Rows of dictionary tables are replaced with official rows, remapping keys if necessary;
  - On a unique column combination conflict, non-critical columns are rewritten; if that does not work, the row is deleted;
  - Parent rows for undeclared foreign keys are added;
  - Child rows required for total participation are added, preferring to reuse existing parent rows;
  - Symmetric rows are added and self-loops deleted;
  - Year–date consistency is fixed.
- **Acceptance condition**: certifier in the loop, requiring both L1f and all tier-R constraints.

### Baselines: fully equal information and budget
- **Random fuzzing-R (fuzz_r)**: each row starts from an official real row; the columns involved in the query are drawn at random from the literals, observed values or NULL; keys are drawn from a small three-value domain so that joins can happen. It uses the same DDL and the same tier-R repair; the acceptance condition is L1f plus tier R, consistent with the certifier in the loop. It does not use the join graph, anchoring, isolation or the growth operators.
- **ParSEval-R**: the generator is the official original; the value chooser prefers observed real values; the acceptance condition is L1f plus tier R, and it keeps changing seeds until the budget is used up.
- **Recertification of existing results**: existing results (the v4 methods, SpotIt, SpotIt+) are all recertified under tier R and recorded in the `cert_R` field, without changing the original `cert`.

## 3. Development and freeze

- Tier-R methods are debugged only on the **development set**, using the development set's EX-correct pairs and known-positive pairs; no tier-R results on the test set are looked at.
- When debugging ends, SHA256 hashes are recorded and written to `docs/FREEZE_R.md`, and the following are then run **once** on the test set:
  - CGX-R, fuzz-R, ParSEval-R: on all 6,456 distinct EX-correct pairs, 5 s per pair;
  - CGX-R, fuzz-R: on the known-positive pairs.

## 4. Hypotheses and decision criteria (test set)

- **H5 (mechanical endpoint)**: On EX-correct pairs, the number of tier-R certified witnesses of CGX-R is greater than that of fuzz-R and also greater than that of ParSEval-R. Uses the paired exact McNemar test, a 95% CI from a bootstrap clustered by question, and Holm correction.
- **H6 (semantic endpoint)**: From the tier-R witnesses of CGX-R, fuzz-R and ParSEval-R, randomly sample 100 distinct pairs each for blind labeling. Blind labeling follows the unified procedure (Section 5). The number of meaningful witnesses is estimated as "meaningful proportion × number of witnesses"; the estimate for CGX-R should be greater than that of each baseline. The 95% CI of the difference is obtained by parametric bootstrap, i.e. binomial resampling of the two methods' proportions.
- **H7 (realism improvement)**: The proportion of CGX-R witnesses judged implausible_data is lower than the same proportion for v4 at tier L1f. The latter is given by the two-pass labeling in document 06; for the formal version it will be relabeled following the unified procedure. The test is a two-proportion test.
- **Secondary measures**: known-positive recall (tier R); EX correction and ranking per system; the composition of pred_wrong and gold_wrong in the attribution; a list of benchmark annotation problems (gold_wrong).
- **Negative results allowed**: if H5–H7 do not hold, this is reported as is.

## 5. Unified attribution labeling procedure

- For each method, 100 distinct pairs are sampled at random (fixed seed). Method names are hidden during labeling; each batch is labeled separately by two independent subagents, both using the same instructions.
- Labelers may run read-only SQL on the official database to check "whether a certain kind of data occurs in reality". This rule is the same for all batches, including the batches that relabel v4, SpotIt, ParSEval and fuzz.
- Items on which the two passes disagree are adjudicated by a third pass. The agreement rate and κ between the two passes are reported.
- The authors manually spot-check 30 items; the spot-check sheet is `results/test/audit/human_check.md`. The paper reports the agreement rate between the authors' and the AI's judgments.
- The paper states that the attribution judgments were made with AI assistance and spot-checked by the authors.

## 6. Handling of the first freeze's results

- All pre-registered results of v4 (H1–H4) are reported as is and positioned as "schema-level" results.
- The post-hoc L1n, O1f and O1n serve as sensitivity analyses.
- The certifier-in-the-loop correction of the fuzzing baseline (P2) runs as planned.
- P3 (the nullability-aware versions) is cancelled because it has been superseded by tier R.
