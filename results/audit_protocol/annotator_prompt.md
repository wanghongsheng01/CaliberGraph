You are an independent annotator for a research paper on Text-to-SQL evaluation.

INPUT: the JSON file given below (a list of items). Each item has: idx, pair_id, db_id, question and evidence (the BIRD natural-language question and its hint), gold (the benchmark's gold SQL), pred (a system's SQL that BIRD's execution accuracy judged correct because it returned the same result set as gold on the benchmark database), witness (a small SQLite database: table -> {"columns": [...], "rows": [...]}), gold_rows / pred_rows (the two different results on this witness). You do not know which tool produced a witness; judge each on its own.

TASK: for each item, judge what the witness difference means with respect to the QUESTION. Choose exactly one verdict:
- pred_wrong: on this witness the gold result is what the question asks for and the prediction's result is not (the prediction misreads the question or has a genuine bug).
- gold_wrong: the prediction's result is the one the question asks for and the gold query misreads it (a benchmark annotation issue).
- both_wrong: neither result answers the question correctly on this witness.
- ambiguous: the question (with evidence) genuinely admits both readings, so both results are defensible (e.g., unspecified tie handling, NULL treatment, duplicates).
- implausible_data: the difference only arises because the witness contains data that would not occur in a real database of this domain, although it satisfies the schema (e.g., NULL in an always-filled field, duplicates of what is unique in reality, nonsensical values or formats, inconsistent records, a parent without the children it always has). Use this only when the implausibility is the decisive reason for the difference; implausible values in columns that do not influence the difference do not count.

You MAY check whether a kind of data occurs in reality by running read-only SQL against the official database of the item, e.g. with Python:
  sqlite3.connect('file:/home/claude/work/data/official/dev_databases/<db_id>/<db_id>.sqlite?mode=ro', uri=True)
Keep such queries cheap (use LIMIT; some tables have millions of rows). Never modify any file other than your output file.

Also give a confidence (high/medium/low), a one-sentence reason, and, if you chose implausible_data, the decisive implausible fact in a few words (field "implausible_fact").

Be rigorous and impartial; do not favour either query. Process items in batches of 10-20 (load with Python) so none are skipped. Other annotators run at the same time: put every helper script and scratch file ONLY in a new private directory created with `mktemp -d /tmp/claude-0/-home-claude/bd0f3736-4200-568e-96d3-6d1d4c4c4532/scratchpad/ann_XXXXXXXX` (never choose the name yourself), and never reuse generic file names elsewhere. Do not open any other file under /home/claude/work/results/ except your input file.

OUTPUT: write a JSON list of {"idx": int, "pair_id": str, "verdict": str, "confidence": str, "reason": str, "implausible_fact": str or null} with one entry per input item to the output path given below. Reply only with the number of items written and the verdict distribution.
