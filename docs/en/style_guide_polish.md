# Style guide for polishing the manuscript (derived from published PVLDB papers in the area)

## What the reference papers do
Two papers were studied: Jin et al., "Pervasive Annotation Errors Break Text-to-SQL Benchmarks and Leaderboards" (PVLDB 19), and Chen et al., "ParSEval" (PVLDB 18).

- **Introductions follow a fixed order.** Context, then the problem, then a concrete example, then why prior work falls short, then the approach, then the headline findings, then a numbered contribution list. Each paragraph has one job and opens with a topic sentence that states it.
- **Sentences are 15–30 words.** Long sentences join at most two clauses. Transitions are explicit: "However", "In contrast", "As a result", "To address this, we ...". Short sentences are used for emphasis.
- **Numbers are precise and appear in plain sentences.** For example: "CaliberGraph certifies 1,979 of the 7,995 pairs (24.8%)", "12 of the 16 systems improve", "X is 21× faster than Y". A statistic is followed by a plain-language verdict: "the difference is significant", "the effect is weak".
- **Parentheses are used for a few things only.** They hold abbreviations at first use, short labels such as (i) and (ii), and one compact statistic. Other asides become a separate sentence, an appositive set off by commas, or a colon. Parentheses never appear in section titles.
- **Quotation marks are rare.** They mark quoted wording or a term used ironically. New terms are introduced with italics (`\emph{}`), not quotation marks.
- **Run-in paragraph headings** are short noun phrases in bold, followed by a period.

## Rules for this edit
1. **Preserve content exactly.**
   - Do not change any claim, number, hedge, statistical result, hypothesis outcome (met/not met/weak), pre-registration status (pre-registered/post hoc), caveat, or limitation.
   - Do not add claims or results.
   - Every `\V{...}`, `\ref{...}`, `\cite{...}`, `\label{...}`, `\Tab{...}`, math expression and table/figure environment must survive unchanged. Only its position in the sentence may change.
2. **Fewer parentheses.**
   - Use at most one parenthetical per sentence, and never nest them.
   - Turn explanatory asides into their own sentence or into an appositive.
   - Keep parentheses for: a statistic after its claim, e.g. `(95\,\% CI ...)` or `($p=...$)`; an abbreviation; `e.g.`/`i.e.` lists of one to three items; a section, table or figure pointer.
   - Remove parentheses from all section and subsection titles. If a title carried "(post hoc)" or "(Stage 3)", state that in the first sentence of the section instead.
3. **Shorter sentences.**
   - Split any sentence over about 35 words.
   - Use at most one semicolon per sentence; prefer two sentences.
   - Avoid chains of "X; Y; Z".
4. **Topic sentences.** Each paragraph opens with its point; the evidence follows.
5. **English punctuation and quotation marks.**
   - Use LaTeX English quotes ``like this'' only. Never use Unicode quotes (“ ” ‘ ’), straight double quotes ("), or full-width punctuation.
   - Use `--` for ranges and `---` (no spaces) for dashes.
   - Write `e.g.,` and `i.e.,` with a comma.
   - Use American spelling consistently. The current text mixes some British forms ("materialisation", "labelled", "summarise", "behaviour"); convert them all to American ("materialization", "labeled", "summarize", "behavior").
6. **Terminology.** Keep every technical term exactly as defined: tier names ($\mathcal A_0$, ..., $\mathcal A_R$), tool names (CaliberGraph, CaliberGraph-R, fuzzing-R, ParSEval-L1, SpotIt, SpotIt+), "witness", "certified", "admissible", "attribution", "implausible", "meaningful".
7. **Voice.** Use "we" for the authors' actions and the present tense for results ("CaliberGraph certifies ...").
8. **Do not edit**:
   - the subsection "Use of AI models in this study" (`\label{sec:aiuse}`) in `sections/protocol.tex`, which the authors wrote themselves;
   - the front matter and declarations in `main.tex`;
   - the generated files `numbers*.tex`, `tables/humanai.tex`, `tables/profile_icde.tex`, `tables/systems_icde.tex`, `tables/contracts.tex` and `tables/taxonomy.tex`.
