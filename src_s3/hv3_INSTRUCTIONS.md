# 第三轮人工归因标注说明 / Instructions for human attribution, round 3

## 中文说明（给标注者）

**目的**：用更大的样本和三位标注者，检验论文中 AI 归因的可靠性。论文会把你们的多数意见作为主要的人工估计报告。

**材料**：每人一份标注表（`sheet_r3_annotatorA/B/C_blank.md`）。
- 共 150 条：第一阶段 75 条、第二阶段 75 条，与前两轮都不重复。
- 三份表的条目相同，但顺序各不相同。
- 不显示工具、层级和 AI 的判定。
- 每条附"真实数据库中的事实"，由程序从 BIRD 官方库机械生成，每条的事实种类相同。

**五个标签**：下面是 AI 标注者得到的**原文定义**，第三轮人工使用同一套定义，以便人和 AI 判的是同一件事。
- `pred_wrong`：on this witness the gold result is what the question asks for and the prediction's result is not (the prediction misreads the question or has a genuine bug).
- `gold_wrong`：the prediction's result is the one the question asks for and the gold query misreads it (a benchmark annotation issue).
- `both_wrong`：neither result answers the question correctly on this witness.
- `ambiguous`：the question (with evidence) genuinely admits both readings, so both results are defensible (e.g., unspecified tie handling, NULL treatment, duplicates).
- `implausible_data`：the difference only arises because the witness contains data that would not occur in a real database of this domain, although it satisfies the schema (e.g., NULL in an always-filled field, duplicates of what is unique in reality, nonsensical values or formats, inconsistent records, a parent without the children it always has). Use this only when the implausibility is the decisive reason for the difference; implausible values in columns that do not influence the difference do not count.

"真实数据库中的事实"是 AI 标注者在查询官方库时能看到的信息的一个固定子集，供判断某类数据在现实中是否出现。

**规则**
1. **独立完成**：三人各自独立标注，交回之前不讨论任何条目；不打开 key 文件或仓库里的其他标注文件。
2. **不使用任何 AI 工具**：包括聊天助手、代码助手、翻译工具。
3. **只改两处**：每条只修改 `**Verdict:** ____` 和 `**Reason (one sentence):**` 两处。不要改动表格、事实或其他任何文字，也不要用会自动改写文件的工具打开文件。交回的文件会自动与原件逐行比对，任何其他改动都会记录在案并写进论文。
4. **填写表头**：开始和结束时间，以及是否使用了 AI 工具。
5. **预计用时**：每人约 7–9 小时，可以分几次完成。
6. **完成时间**：建议 **11 月 12 日前**交回。

**完成后**：把文件另存为 `sheet_r3_annotatorA.md`、`sheet_r3_annotatorB.md`、`sheet_r3_annotatorC.md` 交回。

## English (for annotators)
- **Material.** 150 new items (75 first-stage and 75 second-stage), the same items for all three annotators, each annotator in a different order. Tool, tier and AI verdict are not shown. Each item carries facts from the official database.
- **Labels.** The five definitions above are the ones the AI annotator received, verbatim.
- **Rules.**
  - Work alone and do not use any AI tool.
  - Change only the Verdict and Reason lines; every other change is detected and reported.
  - Fill in the header with start and finish time, and AI-tool use.
