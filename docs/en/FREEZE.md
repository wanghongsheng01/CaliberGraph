> English translation of `docs/FREEZE.md`. The Chinese original is authoritative; it was first committed in 09de9cf on 2026-10-13 18:52:11 +0800 and last changed in 09de9cf on 2026-10-13 18:52:11 +0800 (see `git log --follow`).

# Code Freeze Record (before the test-set run)

- Freeze time: 2026-10-13 18:52 CST
- Freeze commit: `b4705cb07e6d15573f7099781a6750efee61d7cb`
- Method version: CaliberGraph v4 (development set: 621 L1f-certified on 2,341 EX-correct pairs; known-positive recall 97.5%)
- Per-file SHA-256 of the source code: see `FREEZE_SHA256.txt`
- Test run script: `results/queue_test.sh` (run once only; budget 5 s per distinct pair, A8)
- Format profile: at freeze time, the official-database value samples published by SpotIt+ (123 columns) are used. If the official BIRD database is obtained later, the **saved witnesses** will be recertified post hoc, more strictly, with a profile of all columns of the official database; this will be reported separately as a sensitivity analysis, without rerunning the search and without replacing the main results.
- No modification made to the method code after the freeze may be used to rerun the test set; if a fix is needed, it may only be listed separately as a "post-freeze exploratory result".
