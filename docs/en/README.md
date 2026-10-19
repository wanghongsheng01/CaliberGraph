# English translations of the pre-registration documents

This folder holds English translations of the pre-registration, amendment and freeze documents in `docs/`. The Chinese originals are authoritative. Each translation starts with a note naming its original and the commits in which the original was first and last changed. The translations were made after both test runs and are not part of either freeze.

| Translation | Chinese original | What it is |
|---|---|---|
| [02_preregistration_protocol.md](02_preregistration_protocol.md) | `docs/02_研究方案与预注册协议.md` | First pre-registration (CGX-Protocol v1): research questions, data split, certifier and comparison contracts, realism tiers L0–L2, compared methods and budgets, hypotheses H1–H4, statistics, and stopping and integrity rules. It was fixed before the first test run (freeze commit 09de9cf). |
| [02a_protocol_amendments.md](02a_protocol_amendments.md) | `docs/02a_协议修订记录.md` | Amendment record for the first protocol: amendments A1–A9, made before the first freeze, and the entries made after it (post-hoc analyses P1–P3 and the P3 cancellation, the queue pause Q1, the tier-R refinement R-A5, and the P2 disclosure). |
| [07_second_freeze_preregistration.md](07_second_freeze_preregistration.md) | `docs/07_第二次冻结方案_R层与CaliberGraph-R.md` | Second pre-registration: data-profile admissibility tier R, CaliberGraph-R and its baselines, hypotheses H5–H7, and the unified attribution labeling procedure. It was fixed before the second test run (freeze commit 676cab9). |
| [FREEZE.md](FREEZE.md) | `docs/FREEZE.md` | Freeze record for the first test run. |
| [FREEZE_R.md](FREEZE_R.md) | `docs/FREEZE_R.md` | Freeze record for the second test run, with the pre-freeze amendments R-A1–R-A4 and the retroactive addendum R-A5. |

## Freeze commits

- **First freeze.** The record `docs/FREEZE.md` and the hash list `docs/FREEZE_SHA256.txt` were committed in 09de9cf (2026-10-13 18:52:11 +0800). The frozen code commit named in `FREEZE.md` is `b4705cb`, which is the parent of 09de9cf and has the same timestamp. Neither file has changed since.
- **Second freeze.** `docs/07_…md`, `docs/FREEZE_R.md` and the hash list `docs/FREEZE_R_SHA256.txt` were first committed in 676cab9 (2026-10-14 09:33:30 +0800). `07` and `FREEZE_R_SHA256.txt` have not changed since. `FREEZE_R.md` was later extended by the R-A5 addendum (see below).

## Amendment timestamps

Amendments are timestamped by git history. The dates in the amendment tables are the authors' own records. The commit in which an entry first appears is an independent upper bound on when it was written, and you can check it with `git log -p --follow -- docs/<file>`.

| Entries | First committed in | Relation to the test runs |
|---|---|---|
| A1–A6 (`02a`) | 6b57904, 2026-10-13 15:04:52 +0800 | Before the first freeze |
| A7–A9 (`02a`) | ceb4564, 2026-10-13 18:36:13 +0800 | Before the first freeze |
| P1, P2, P3, P3-correction, Q1 (`02a`); R-A1–R-A4 (`FREEZE_R.md`) | 676cab9, 2026-10-14 09:33:30 +0800 | After the first test run started, with the second freeze |
| R-A5 (`02a` and `FREEZE_R.md`), P2-disclosure (`02a`) | 29222ff, 2026-10-15 03:18:03 +0800 | After the second test run |

As R-A5 itself states, it was recorded retroactively after the second test run. It describes refinements to the tier-R definition made before the second freeze. The text of `07` has not changed since 676cab9, so it still gives the original definition (for example the 5,000-distinct-value threshold). The refinements are documented only in R-A5.
