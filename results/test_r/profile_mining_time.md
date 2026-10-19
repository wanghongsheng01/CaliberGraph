# Profile mining time (reported as 258 s in the ICDE paper)

| Step | Script | Time | Source |
|---|---|---|---|
| Domains, nullability, UCCs, inclusion dependencies, lookup tables, year-date (`profile_R.json`) | `src_r/mine_profile.py` | 192 s | sum of the per-database times in `data/official/mine_profile.log`; the log reports 340 raw UCCs, equal to the UCC count of the frozen `profile_R.json` (185 remain after the measure-column filter of `cgx/profile_r.py`) |
| Value dependencies (`profile_FD.json`) | `src_r/mine_fd.py` | 66 s | re-run on 2026-10-16 into a scratch file on the same 2-core VM; output identical to the frozen `profile_FD.json` (the original run was not timed) |
| Total | | 258 s | one core, 11 BIRD dev databases, 75 tables, 3,932,735 rows |
