# FREEZE_S3: adapter freeze for Stage-3 runs (S3-D Spider dev, S3-E Mini-Dev systems)

- **Time:** 2026-10-18 11:37 (UTC+8). After this commit, the files listed in `docs/FREEZE_S3_SHA256.txt` are not modified, and each queue runs once (`src_s3/queue_spider.sh`, `src_s3/queue_minidev.sh`).
- **Method code:** `spider/src`, `spider/src_r` and `minidev/src_r` are byte-for-byte copies of the frozen `src/` and `src_r/`. `tools/verify_freeze.py` passes on the originals, and `diff -r` against the copies is empty.
- **Spider release:** `spider.zip` as supplied by the authors. Its SHA-256 and that of `dev.json` are in the hash list.
- **Smoke test:** done on Spider train databases. See amendment E6 in `docs/en/17a_stage3_amendments.md`.
- **Mini-Dev mapping validation passed** (`minidev/data/mapping_report.json`) on all 13 prediction sets:
  - (a) db_id agreement 100%;
  - (b) 98.9–100% of checked indices pass;
  - literal overlap at offset 0 is 0.88–0.93, against at most 0.15 at offsets ±1, ±2.
- **Mini-Dev pairs:** 4,029 new distinct (question, prediction) representatives on held-out test questions. Dropped: 1,482 not in the test split, 963 already in the study or duplicated.
- **Not seen before this freeze:** no Spider dev EX label, and no Mini-Dev EX label distribution. The builders do not print them.
