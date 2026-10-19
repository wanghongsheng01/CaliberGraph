# 17c Pre-registration: Third Human Validation Round (three annotators, 150 items)

- **Written** 2026-10-19, before the material was sent to any annotator.
- **External timestamp.** This document, together with the SHA-256 of the key file, is pushed to the public repository https://github.com/wanghongsheng01/CaliberGraph before the sheets are distributed. The key itself is withheld until all three sheets have been returned.
- **Why a third round.** Rounds 1 and 2 (documents 17, 17a, 17b) used two annotators and 60 items each. Round 2 passed two of its three hypotheses but not agreement with the AI. An independent review of the manuscript found that the human annotators also differ from the AI in the non-implausible labels: they call many more witnesses prediction errors and almost none ambiguous. The reviewer asked for at least three annotators and 150–200 items, with a documented process. Rounds 1 and 2 remain reported in full.

## Material
- **Sample.** `results/audit/human_validation_r3/`, built by `src_s3/hv3_build.py` with seed 20261022:
  - 150 attributed test items, 75 first-stage (schema tiers) and 75 second-stage ($\mathcal A_R$);
  - none used in rounds 1–2;
  - item codes R3-001 to R3-150.
- **Sheets.** Three sheets with identical items in different orders (annotator A, B, C; order seeds 1, 2, 3). Tool, tier and AI verdict are not shown.
- **Facts.** Each item carries the same mechanically generated facts from the official database as in round 2.
- **Instructions** (`INSTRUCTIONS.md`):
  - the five label definitions given to the AI annotator, **verbatim**;
  - unlike round 2, no additional decision order is imposed.
- **Annotators.** Three data analysts or engineers who are familiar with SQL, recruited by the authors and working independently, without AI tools.
- **Process record.**
  - Each annotator records start and finish times in the sheet header, and whether any AI tool was used.
  - Returned sheets are compared line by line with the blank sheets. Any change outside the Verdict and Reason lines is reported in the paper.
- **Key file.** `key_DO_NOT_OPEN_BEFORE_ANNOTATING.json`. Its SHA-256 is listed in `docs/en/17c_key_sha256.txt`.

## Measures
- **M-R3-1.** Fleiss' κ of the three annotators, on the five labels and on the binary split implausible vs. other. Pairwise Cohen's κ is reported too.
- **M-R3-2.** The human majority label: the label chosen by at least two of the three annotators. Items without a majority are reported as "no majority".
- **M-R3-3.** Cohen's κ between the human majority and the AI final label, on five labels and binary, over items with a majority.
- **M-R3-4.** Label shares by stage for the human majority and for the AI, with 95% intervals from a bootstrap over items (10,000 resamples, seed 20261022).

## Hypotheses
- **H-R3-1 (threshold).** Fleiss' binary κ ≥ 0.60.
- **H-R3-2 (threshold).** Binary κ between the human majority and the AI ≥ 0.60.
- **H-R3-3 (test).** The human-majority `implausible_data` share is higher in the first stage than in the second. One-sided Fisher exact test, α = 0.05.
- **H-R3-4 (test).** The human-majority share of prediction errors (`pred_wrong` + `both_wrong`) among second-stage items differs from the AI's share on the same items. Exact McNemar test on paired indicators, two-sided, α = 0.05.

## Pre-stated use in the paper
1. **Primary human estimates.** The human-majority label shares (M-R3-4) become the primary human estimates of what witnesses show. They are reported next to the AI's shares in every place where the paper reports meaning-related shares.
2. **Effect on EX.** The error-weighted effect on EX is reported with both error rates, the AI's and the human majority's, each with its bootstrap interval.
3. **If H-R3-2 fails,** claims about the distribution of meaningful witnesses (prediction error vs. gold defect vs. ambiguity) are stated only with the human-majority estimates in the abstract and introduction; the AI estimates move to the body.
4. **If H-R3-1 fails,** the paper states that the five-label attribution is not reliably reproducible by humans, and restricts its human-based claims to the binary implausible-vs-other judgement if that judgement has κ ≥ 0.60.
5. **Rounds 1–3 are all reported.** None replaces another.
