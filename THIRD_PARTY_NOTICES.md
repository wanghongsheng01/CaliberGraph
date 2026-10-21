# Third-party material

This repository redistributes or derives data from the following sources under their licences. Our own code and generated data are under the Apache License 2.0 (`LICENSE`).

| Material | Files | Source | Licence |
|---|---|---|---|
| BIRD development set: questions, evidence, gold SQL, DDL | `data/raw/bird_dev_20240627.json`, `data/raw/bird_schema_ddl.json`, and the question/gold fields of `data/pairs.jsonl` | BIRD benchmark, J. Li et al., NeurIPS 2023 (https://bird-bench.github.io/) | CC BY-SA 4.0. Derived data in this repository that contains BIRD content is shared under the same licence. The BIRD databases themselves are **not** included. |
| Predictions of ten Text-to-SQL systems; EX labels; SpotIt and SpotIt+ verdicts and counterexamples; SpotIt+ mined constraints | `data/raw/spotit/`, `data/raw/ex/`, `data/raw/spotit_constraints/`, the prediction fields of `data/pairs.jsonl`, `results/test_spotit_*.jsonl`, `results/dev_spotit_*.jsonl` | SpotIt+ release, https://github.com/ai-ar-research/SpotIt-plus (commit recorded in `data/raw/SPOTIT_PLUS_COMMIT.txt`) | Modified BSD licence. Copyright (C) 2025-2026 by the SpotIt+ authors and contributors and their institutional affiliations. All rights reserved. Redistribution is permitted provided this notice is retained. The software is provided "as is" without warranty. |
| ParSEval (external dependency, not vendored; our harness is `src/baselines/parseval_*`) and its `disprove` outputs on BIRD | `data/raw/parseval_disprove_bird.jsonl` | https://github.com/sfu-db/ParSEval (commit `88cfe245`) | Apache License 2.0 |
| SpotIt / VeriEQL verifier (external dependency, **not vendored**; our harness is `src_s3/spotit_run.py`, which imports it from a separate checkout and re-implements, in a few lines, the counterexample-validation rules of its `evaluation/execute_sql.py`), and the outputs of our local re-run | `results/stage3/spotit/` | https://github.com/atremante26/VeriEQL (commit `66d8343f3fa38f1c348548de1414836806c88615`), run with Z3 4.16.0 (MIT) | The VeriEQL repository is licensed CC BY-NC-SA 4.0; users who install it to reproduce the re-run must follow that licence. No VeriEQL code is redistributed here. |
| Data profile mined from the BIRD databases | `data/official/profile_R.json`, `profile_FD.json`, `format_profiles.json`, `sample_rows.json`, `nullability.json` | Derived by our scripts from the BIRD databases | CC BY-SA 4.0 (derived from BIRD) |

The full modified-BSD licence text of SpotIt+ is reproduced below as its licence requires.

```
SpotIt+ is copyright (C) 2025-2026 by its
authors and contributors and their institutional
affiliations. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT OWNERS AND CONTRIBUTORS
''AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

## Stage-3 material

| Material | Where it appears here | Source | Licence |
|---|---|---|---|
| Spider 1.0 questions, gold SQL and database schemas (the databases themselves are **not** redistributed) | `spider/data/pairs.jsonl`, `spider/data/raw/`, `spider/data/official/*.json` (mined profiles), `results/stage3/s3d/` (witness rows derived from the databases) | Yu et al., EMNLP 2018, https://yale-lily.github.io/spider | CC BY-SA 4.0. Our derived files under these paths are shared under the same licence. |
| DAIL-SQL (GPT-4, with and without self-consistency) and Graphix-T5 predictions on Spider dev | `spider/data/pairs.jsonl` (field `pred`) | https://github.com/BeachWang/DAIL-SQL at commit `2061f68`, `results/` | Apache License 2.0 (full text in `LICENSE`) |
| DIN-SQL and GPT-4 few-/zero-shot predictions on Spider dev | `spider/data/pairs.jsonl` (field `pred`) | https://github.com/MohammadrezaPourreza/Few-shot-NL2SQL-with-prompting at commit `0474801`, `GPT4_results/` | MIT License (text below) |
| BIRD Mini-Dev SQLite prediction sets of 13 LLM configurations | `minidev/data/pairs.jsonl` (field `pred`) | https://github.com/bird-bench/mini_dev at commit `abd11b6`, `llm/exp_result/` | CC BY-SA 4.0 |
| Arcwise-Plat corrected annotations (used for the cross-check; only per-question flags are stored) | `results/stage3/s3c_arcwise.json` | Jin et al., PVLDB 19(5), https://github.com/uiuc-kang-lab/text_to_sql_benchmarks at commit `fe76604` | CC BY-SA 4.0 |

MIT License text, as shipped in the DIN-SQL repository (`LICENSE.txt`):

```
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
