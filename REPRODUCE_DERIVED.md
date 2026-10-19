# Regenerating derived result files

These derived files were first produced by ad-hoc inline snippets. Each one now has a script that regenerates it from the stored raw outputs. Every script below was run with output to a temporary directory, and the result was compared with the stored file using `cmp` (byte for byte). Python 3.13; standard library only, plus the repository's own `src/` and `src_r/` modules.

To verify without overwriting anything, set `OUT` to a scratch directory. Then compare each output with the stored file using `cmp $OUT/<name> <stored path>`. To regenerate in place, replace `$OUT/<name>` with the stored path.

| # | Derived file | Command | Verified identical |
|---|---|---|---|
| 1 | `results/test/recert_r_counts.json` | `cd src_r && python recert_r_counts.py --out $OUT/recert_r_counts.json` | yes (byte-identical) |
| 2 | `results/cost_and_distinct_pairs.json` | `cd src_r && python cost_distinct_pairs.py --out $OUT/cost_and_distinct_pairs.json` | yes (byte-identical) |
| 3 | `results/audit/test_v4_attribution_summary.json` | `cd src_r && python attribution_v4_summary.py --out $OUT/test_v4_attribution_summary.json` | yes (byte-identical) |
| 4a | `results/test/audit/human_check_summary.json` | `cd src_r && python human_check_summary.py v4 --out $OUT/human_check_summary.json` | yes (byte-identical) |
| 4b | `results/audit/human_check_R_summary.json` | `cd src_r && python human_check_summary.py R --out $OUT/human_check_R_summary.json` | yes (byte-identical) |
| 5 | `results/test/fuzz_exc_corrected.jsonl`, `results/test/fuzz_exi_corrected.jsonl` | `cd src && python repro_fuzz_corrected.py --out-dir $OUT --recertify-r` | yes, both byte-identical (exc only with `--recertify-r`, see below) |

## Dependency order

`fuzz_exc_corrected.jsonl` (item 5) is an input to items 1, 2 and 3. Item 3 recomputes the certified counts of item 1 internally.

## Notes per item

1. **`recert_r_counts.json`**
   - **Population:** EX-correct test pairs, excluding `source == parseval_model` (7,995 pairs).
   - **Expansion:** distinct-triple results are expanded to systems with `score.expand`.
   - **Tiers:** `score.is_cert(r, T, 'C_set', pair)` for T in L0, L1f, Rq, R. Rq and R read `cert_R.okq` and `cert_R.ok`.
   - **Method files:** "Fuzz" is the corrected baseline `fuzz_exc_corrected.jsonl`; the frozen `fuzz_exc.jsonl` gives L0 1713, L1f 1562, Rq 64, R 0, which does not match. SpotIt and SpotIt+ are `results/test_spotit_vanilla_null.jsonl` and `results/test_spotit_llm.jsonl`.
2. **`cost_and_distinct_pairs.json`**
   - **Counting:** over records of each result file (distinct pairs, not expanded).
   - **`certified_R`:** present only for files that carry `cert_R`.
   - **`no_witness_in_budget`:** distinct − found − timeout − identical − error.
   - **`hard_timeout` and `error`:** ParSEval `verdict` values TIMEOUT and ERROR; each key is written only when its count is > 0.
   - **`mean_search_s`:** mean over all records, with a missing or null `search_s` counted as 0.
   - **SpotIt/SpotIt+ claims:** counted per (system, question) record restricted to EX-correct pairs; "not recertified" means `author_claim` and not `is_cert` at L0 or L1f.
3. **`test_v4_attribution_summary.json`**
   - **Final verdict:** pass A if A == B, otherwise pass C (`test_v4_ann_c.json` covers exactly the 42 disagreements). This is the same rule as `analyze_r.py`.
   - **Agreement:** Cohen's κ of A against B; `adjudicated` = number of items in pass C.
   - **Intervals:** Wilson 95% CIs for the implausible, meaningful and error shares. "Errors" = pred_wrong + both_wrong.
   - **Certified counts:** from item 1 at the sampled tier.
   - **Estimates:** `est_*` = certified × share; their CIs are certified × share CI.
4. **Human-check summaries**
   - **Author's verdict:** the bold cell in column 6 of each table row of the filled sheets.
   - **Item order:** rows 1..30 map, in order, to `human_check_idx.json` and `human_check_R_idx.json`.
   - **AI verdicts:** taken from the annotation files: `results/test/audit/attribution_a/b.json` for the v4 sheet, and `results/audit/test_r_ann_a/b/c.json` for the R sheet. For the R sheet, final = A if A == B, else C.
   - **Cross-check:** the sheet's own AI columns are checked against these files, and no mismatches were found.
5. **Corrected fuzzing baseline (amendment P2).** Fuzzing is not re-run. The script reproduces these steps from `results/queue_posthoc.sh`:
   1. **Selection.** Re-selects the pairs whose frozen record has `found` true but is not L1f-certified: 132 exc and 259 exi. The selection is checked to be identical to `results/test/posthoc/fuzzcert_ids_{exc,exi}.json`.
   2. **Merge.** Every frozen record whose `pair_id` is in `results/test/posthoc/fuzz_cert_rerun_{exc,exi}.jsonl` is replaced by the re-run record, which was produced by `src_v5/run_method.py --method fuzz_cert`. All other records keep their order. This is the same rule as `src/merge_fuzzcert.py`, which writes into `results/test/` in place.
   3. **Tier-R recertification (exc only).** `src_r/recertify_r.py` is applied to the merged exc file. It adds `cert_R` to the 113 replaced records that have a witness. Without this step, the exc file differs from the stored one only in those 113 `cert_R` fields; the exi file is identical after the merge alone. `cert_official` is not recomputed: the replaced records have none, and neither do the stored ones.
   4. **Requirements.** Step 3 needs `data/official/profile_R.json` and `profile_FD.json`.

## Stored file checksums (SHA-256, first 16 hex digits) at verification time

| File | SHA-256 (prefix) |
|---|---|
| `results/test/recert_r_counts.json` | `0e795ff2f4c40210` |
| `results/cost_and_distinct_pairs.json` | `35d6c82b29eac7b3` |
| `results/audit/test_v4_attribution_summary.json` | `5bdacf2173436121` |
| `results/test/audit/human_check_summary.json` | `4e7adfbbca47929c` |
| `results/audit/human_check_R_summary.json` | `3fce1d8cf0bf3dca` |
| `results/test/fuzz_exc_corrected.jsonl` | `77a2bb04d03d069a` |
| `results/test/fuzz_exi_corrected.jsonl` | `846f0a195265855e` |
