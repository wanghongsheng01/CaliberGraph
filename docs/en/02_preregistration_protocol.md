> English translation of `docs/02_研究方案与预注册协议.md`. The Chinese original is authoritative; it was first committed in e75d778 on 2026-10-13 13:56:45 +0800 and last changed in e75d778 on 2026-10-13 13:56:45 +0800 (see `git log --follow`).

# 02 Research Plan and Pre-registered Evaluation Protocol (CGX-Protocol v1)

Date: 2026-10-13　　Status: **Pre-registered version, frozen before the test-set run** (the freeze git hash is recorded in `docs/FREEZE.md`; the test set is run only once)

---

## 0. Research questions

Text-to-SQL systems are usually scored by "execution accuracy" (EX: comparing the result sets of the predicted SQL and the gold SQL on one official database). Two non-equivalent SQL queries may happen to give the same result on this database, so EX overestimates accuracy. Existing remedies:

* **SpotIt / SpotIt+** (ICLR 2026; arXiv 2603.04334) — bounded formal verification (extending VeriEQL); SpotIt+ additionally adds mined realism constraints;
* **ParSEval** — coverage-guided symbolic generation of test databases;
* **Test-suite accuracy** (Zhong et al., EMNLP 2020) — random/distilled database suites;
* **XData / EvoSQL** — test-data generation targeting SQL mutants or coverage goals.

**RQ1 (method)**: Can a witness synthesis method that depends only on the DDL and executes under real SQLite semantics, "difference anchoring + masking isolation + join-graph completion" (CGX), refute more predictions that are "judged correct by EX but actually non-equivalent" than the baselines above, **under the same certifier, the same comparison contract and the same realism threshold**?
**RQ2 (protocol)**: How sensitive are the conclusions of existing evaluators to the **comparison contract** and to the **witness realism threshold**?
**RQ3 (knowledge)**: What transferable SQL-semantic causes underlie the non-equivalences that EX misses (masking, LIMIT ties, integer division, empty aggregates, NULL, type affinity, JOIN duplication, ...)? How are they distributed across 10 models and 11 schemas? How do they affect model rankings?

---

## 1. Data and split (generated deterministically by `src/build_dataset.py`)

* Questions: BIRD dev (2024-06-27 revision), 1534 questions, 11 schemas; the DDL is the original `CREATE TABLE` statements from ParSEval's official artifacts.
* Prediction sources: the 10 method predictions published in the SpotIt+ repository (alpha, chess, csc-7b, csc-32b, gena_submission_1/2, gsr, omni-32-majority, rsl, slm); the 11th set of predictions in the ParSEval artifacts (old-version gold, previously exposed) is used only for development.
* EX labels: the per-question EX computed on the official BIRD database and published by the SpotIt+ authors (this sandbox cannot download the official database; stated as is).
* **Split (pre-registered, fixed salt)**:
  * Held-out schemas: the 3 with the smallest `sha256("cgx-holdout-schema-v1|"+schema)` → **superhero, toxicology, formula_1**, all of which go into the test set;
  * The remaining 8 schemas are stratified by (schema, difficulty) and sorted by `sha256("cgx-question-split-v1|schema|qid")`; the first 30% go into the development set;
  * The 43 questions previously exposed to the team: in non-held-out schemas they are forced into the development set; in held-out schemas they are excluded (11 questions, not part of any evaluation).
  * Result: 349 development questions, 1174 test questions, 11 excluded; 11,740 test pairs (of which 7,995 are EX-correct).
* During development **only development-set questions may be viewed**; the test set is run once only, after the freeze.

## 2. Evaluation populations

* **P_EXC** (main population): (question, model) pairs in the test set with EX = correct. The ground truth is unknown; the goal is refutation.
* **P_EXI** (known positives): pairs in the test set with EX = incorrect. The official database already distinguishes the two queries, so they are **necessarily non-equivalent under the set contract**. They are used to measure each tool's **recall**, with no need for human labels.
* **Deduplication basis**: predicted SQL that is identical after normalization under the same question is treated as the same "distinct pair"; the main table reports raw pairs, and the supplementary table reports deduplicated results.

## 3. Certifier (shared by all methods, independently implemented)

A witness database W that claims "non-equivalent" is **certified** if and only if:
1. In a fresh in-memory SQLite, the **original** DDL is executed (without rewriting case, identifiers or literals), with `PRAGMA foreign_keys=ON`, and all inserts of W succeed (PK, NOT NULL, UNIQUE and FK are all satisfied);
2. The original gold SQL and the original predicted SQL both execute successfully on W (an error on either side does not count as a witness);
3. The results differ under the selected **comparison contract**.

Comparison contracts (all are reported; **primary contract = C_set**):
* **C_set**: the definition of BIRD's official EX, `set(rows_pred) == set(rows_gold)`;
* **C_bag**: multiset equality (ignoring order, keeping duplicates);
* **C_lenient**: on top of C_set, treats "empty result" and "a single all-NULL row" as equal, and compares numbers with 1e-9 relative error (used to test whether the conclusions depend on corner-case semantics).

## 4. Witness realism grading

* **L0**: passes certification (satisfies all constraints declared in the DDL).
* **L1**: L0 + type-faithful (INTEGER/REAL columns store only numbers, TEXT columns store only text, DATE/DATETIME columns are ISO text that `date()`/`datetime()` can parse) + at least 1 row in every table referenced by the two queries.
* **L2**: L1 + satisfies the realism constraints that the SpotIt+ authors mined for this database and checked with an LLM (range, categorical, not-null, functional dependencies; read directly from their public JSON). The witnesses of all methods are checked with **the opponent's own constraints**.
* **The primary endpoint uses L1**; L0 and L2 are reported side by side in the same table.

## 5. Methods compared

| Method | How it is run | Budget |
|---|---|---|
| **CGX (this work)** | Frozen version, rerun on the same machine | 10 s wall-clock per pair, single core |
| CGX + SC | CGX additionally obeys the SpotIt+ constraints during generation (compared with SpotIt+ under the same conditions) | Same as above |
| SpotIt (vanilla) | Uses the authors' published per-question results and counterexamples; its counterexamples are rechecked by this certifier after column-name mapping; both the "author-reported" and the "rechecked by this certifier" bases are reported | Authors' settings (cumulative per question can reach several hundred seconds, bound 1–5) — **an advantage conceded to the baseline** |
| SpotIt+ (LLM constraints) | Same as above, uses the authors' published results | Same as above |
| ParSEval | Fixed commit, rerun on the same machine; the databases it generates are handed to this certifier | 10 s per pair |
| Random fuzzing (Test-suite style) | DDL-valid random databases; value domains taken from the literals of the two queries and from type-random values; FK-consistent | 10 s per pair |
| EX | Official database (authors' published results) | — |

## 6. Hypotheses and decision criteria

* **H1**: On P_EXC, the number of L1 / C_set certified witnesses of CGX > SpotIt (author-reported basis).
* **H2**: On P_EXC, the number of L2 / C_set certified witnesses of CGX+SC > SpotIt+ (author-reported basis).
* **H3**: On P_EXI, the recall of CGX > SpotIt and ParSEval.
* **H4 (ablation)**: Removing any one of the components "difference anchoring", "masking isolation", "join-graph completion" and "SQLite value domain" significantly decreases the number of witnesses on P_EXC.
* Statistics: paired exact McNemar test (per pair, whether a witness is found); bootstrap 95% CI with **the question as the cluster unit** (10,000 resamples); Holm correction for H1–H3, α = 0.05.
* **False positives**: the number of cases in which any method "claims non-equivalence but fails certification" is reported separately; the design target for CGX is 0.
* **Negative results allowed**: if H1/H2 do not hold, this is reported as is; the focus of the paper then shifts to the protocol and RQ2/RQ3, and no selective experiments are added.

## 7. Secondary analyses

* Each model's "corrected accuracy" = the proportion of its EX-correct pairs not refuted by any method (an upper bound), and the change in Kendall τ ranking;
* Cause taxonomy: automatically label the difference-anchor category of every certified witness, and manually spot-check 100 to verify the labeling accuracy;
* **Residual audit**: from the P_EXC pairs that no method can refute, randomly sample 100, stratified by model, and judge each one manually (AI-assisted, stated as such) as truly equivalent or not, to estimate each tool's false-EQ rate and its Wilson CI;
* Cost: per-pair time distribution (median, p95), and the proportions of timeouts, errors and unsupported cases.

## 8. Stopping and integrity rules

* After the freeze, the CGX code must not be modified and then rerun on the test set; if a defect is found, it may only be disclosed in the report, with a "post-freeze fixed version" listed separately as an exploratory result.
* All denominators are retained: errors, timeouts, unsupported cases and certification failures are all counted.
* Development-set results are not called test results; AI labels are not called human expert labels.
* Third-party data/code licenses: BIRD (CC BY-SA 4.0), ParSEval (Apache-2.0) and SpotIt+ (according to its repository LICENSE) are each stated in the paper and in the data documentation.
