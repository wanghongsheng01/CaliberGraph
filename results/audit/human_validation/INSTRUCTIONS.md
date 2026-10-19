# 人工归因标注说明 / Instructions for human attribution

## 中文说明（给标注者）

**目的**：检验论文中 AI 标注的可靠性。审稿人最可能攻击的就是这一点，所以这是投稿前最值得补做的一项实验。

**材料**：`sheet_blind.md`，共 60 条。
- 随机抽样，不分层：30 条来自第一阶段的样本，30 条来自第二阶段的样本。
- 顺序已打乱。
- 不显示工具、层级和 AI 的判定。

**标注规则**
1. **不要提前看答案**：标注前不要打开 `key_DO_NOT_OPEN_BEFORE_ANNOTATING.json`，也不要查看仓库里的其他标注文件。
2. **每条做什么**：阅读问题、evidence、两条 SQL、见证数据库和两个结果，然后把 `**Verdict:** ____` 中的 `____` 替换为下面五个标签之一，并写一句理由。
   - `pred_wrong`：在这个见证上，gold 的结果才是问题要的，预测的结果不是（预测误解了问题，或有 bug）。
   - `gold_wrong`：预测的结果才是问题要的，gold 误解了问题（基准标注问题）。
   - `both_wrong`：两个结果都不对。
   - `ambiguous`：问题（加上 evidence）确实允许两种理解，两种结果都说得通。例如：并列怎么处理没说明、NULL 怎么处理、重复行怎么算。
   - `implausible_data`：差异只因为见证里有该领域现实中不会出现的数据，尽管它满足 schema。例如：常填字段为 NULL、现实中唯一的东西出现了重复、不合理的值或格式、记录前后不一致。
     - 只有当这种不现实正是造成差异的决定性原因时才选它。
     - 与差异无关的列出现怪值，不算。
3. **可以查原始数据（可选）**：如果你手上有 BIRD 官方开发库，可以查询某类数据现实中是否出现（AI 标注者也有这一权限）。
4. **只显示相关列**：表格只列出两条查询引用到的列，其余列已省略，与差异无关。
5. **预计用时**：约 2–3 小时。

**两位标注者（推荐）**
- 如能请一位懂 SQL 的同学或同事独立再标一遍（各用一份副本，互不交流），就能同时报告人-人一致性（Cohen κ）。这是审稿人最看重的指标。

**完成后**
- 把填好的文件发给我（例如 `sheet_annotator1.md`、`sheet_annotator2.md`）。
- 我会运行下面的命令，并把结果写进论文：
  ```
  python src_r/human_validation.py score --dir results/audit/human_validation sheet_annotator1.md [sheet_annotator2.md]
  ```

## English (for annotators)
Purpose: validate the AI attribution used in the paper.

`sheet_blind.md` holds 60 items:
- a simple random sample, 30 from the first-stage samples and 30 from the second-stage samples;
- shuffled;
- shown without the producing tool, the tier or the AI verdicts.

For each item:
- Replace `____` after **Verdict:** with one of `pred_wrong`, `gold_wrong`, `both_wrong`, `ambiguous` or `implausible_data`, using the definitions above.
- Add a one-sentence reason.
- Choose `implausible_data` only when unrealistic data is the decisive reason for the difference.

Rules:
- Do not open the key file or other annotation files before finishing.
- If two annotators participate, they must work independently.
