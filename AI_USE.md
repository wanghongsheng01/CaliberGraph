# Use of Generative AI in This Study

This supplement documents the use of generative AI, as required by the PVLDB Code of Ethics (§3.2.3: such use "must be documented") and by the ACM policy on authorship, which asks for tools, versions, prompts and editing when whole sections are generated. The paper's acknowledgements carry a shorter disclosure.

## Tools and versions
- **Primary model.** Claude Opus 5.5 (Anthropic; model identifier `claude-opus-5-5`), used through an agentic coding environment (Claude, with file, shell and sub-agent tools) from October 2026 (first commit of the study repository: 2026-10-13) until submission.
- **Second model.** Claude Sonnet 5.5 (`claude-sonnet-5-5`), used only as the second annotator of the cross-model sensitivity analysis (S3-B).
- No other generative model was used.

## What the AI did
| Activity | Performed by | Human role |
|---|---|---|
| Study design, hypotheses | Drafted by the AI | Authors set the goals, agreed to each pre-registered stage and reviewed the documents |
| Pre-registration documents and amendment logs (`docs/en/02*`, `07*`, `17*`, `FREEZE*`) | Written by the AI | Authors reviewed |
| Code (CaliberGraph, CaliberGraph-R, certifier, profile miners, baseline harnesses, analysis scripts) | Written by the AI | Authors reviewed |
| Running all experiments and analyses | AI | Authors reviewed outputs |
| Attribution of witnesses (two blind passes and adjudication), root-cause labels, benchmark-issue list | AI (`claude-opus-5-5`), with the prompt reproduced below | See "Human checks" |
| Cross-model sensitivity annotation (S3-B) | `claude-sonnet-5-5`, same prompt | — |
| Paper text, tables, figures | Drafted and edited by the AI | Authors reviewed and take full responsibility |

## Annotator prompt (verbatim)
The prompt is stored in `results/audit_protocol/annotator_prompt.md` (SHA-256 `3c3934c4…`). Each annotation pass received this prompt, followed by the paths of one input file (a blind batch) and one output file. For Spider (S3-D), three mechanical substitutions were made; they are listed in `docs/en/17_stage3_preregistration.md`.

## Human checks
1. **First-author checks (stages 1–2).** The first author re-annotated two samples of 30 witnesses (`results/audit/human_check_R*`, and the pilot check described in the paper). The AI verdicts were printed on the same sheet, so these checks were not blind.
2. **Stage-3 round 1** (pre-registered, `docs/en/17` S3-A).
   - Two human annotators labelled 60 witnesses independently, blind to tool, tier and AI verdict, without access to the BIRD databases and without AI assistance (author statement, amendment E3).
   - They agreed with each other (five-label κ = 0.74) but not with the AI (κ = 0.20–0.26). The pre-registered validation therefore failed. It is reported in the paper.
3. **Stage-3 round 2** (pre-registered, `docs/en/17b`). The same design, with facts from the real database added to every item. Results: see the paper and `results/stage3/`.

## Editing process
- The AI produced each draft of the paper.
- The authors read the drafts, requested changes, and checked claims against the result files.
- Every number in the paper is generated from result files into macro files (`numbers*.tex`) by scripts in the repository, so the numbers are not typed by hand.
