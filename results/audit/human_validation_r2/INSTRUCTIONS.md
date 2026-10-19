# 第二轮人工归因标注说明 / Instructions for human attribution, round 2

## 中文说明（给标注者）

**与第一轮的区别**
1. **样本是新的 60 条**，与第一轮不重复：30 条来自第一阶段，30 条来自第二阶段，顺序已打乱。仍不显示工具、层级和 AI 的判定。
2. **每条都附有"真实数据库中的事实"**。这些事实由程序从 BIRD 官方开发库中机械生成，每条给的事实种类相同。包括：
   - 两条查询引用的每一列在真实表中的行数、NULL 数、不同值个数，以及是否唯一；
   - 见证里出现的每个取值在真实数据中出现了多少次；
   - 行数不超过 15 的小表（例如编码表、查找表）的真实内容。
3. **判定顺序有明确规定**，见下面"标注规则"第 2 条。

**标注规则**
1. **不要提前看答案**：不要打开 `key_DO_NOT_OPEN_BEFORE_ANNOTATING.json`，也不要查看仓库里的其他标注文件。**两位标注者独立完成，互不交流。**
2. **每条按以下顺序判定**，把 `**Verdict:** ____` 中的 `____` 替换为五个标签之一，并写一句理由：
   - **第一步：先问"这个差异在现实数据里会不会出现"。** 结合"真实数据库中的事实"，看两个结果之所以不同，是不是**只因为**见证里有现实中不会出现（或极罕见）的数据。例如：
     - 真实数据里这一列 0 个 NULL，见证里却是 NULL；
     - 查找表的编码与真实内容矛盾（真实表里 id 3 = 'Neutral'，见证里 id 3 = 'Bad'）；
     - 现实中唯一的东西出现了重复；
     - 前后记录不一致。

     如果是，标 `implausible_data`。**即使在这个见证上某一条查询"算得更对"，也标 `implausible_data`**，因为在现实数据上这个差异根本不会出现。只有当这种不现实正是造成差异的决定性原因时才选它；与差异无关的列出现怪值，不算。
   - **第二步：如果差异在现实数据里也可能出现**，再按第一轮的定义判断：
     - `pred_wrong`：gold 的结果才是问题要的；
     - `gold_wrong`：预测的结果才是问题要的；
     - `both_wrong`：两个结果都不对；
     - `ambiguous`：问题（加上 evidence）确实允许两种理解，两种结果都说得通。
3. **事实只是参考**：它们只说明真实数据的样子，不代表任何人的判定。是否构成"决定性原因"，由你判断。
4. **预计用时**：约 2.5–3.5 小时。

**完成后**：把文件另存为 `sheet_r2_annotator1.md` 和 `sheet_r2_annotator2.md` 发给我。请同时告诉我：两人是否独立完成，是否使用了任何 AI 工具。

## English (for annotators)

**What differs from round 1**
- The sample is 60 new items (30 first-stage and 30 second-stage), shuffled, and shown without tool, tier or AI verdict.
- Each item carries "Facts from the real (official) database", generated mechanically, with the same kinds of facts for every item.
- The decision order is fixed, as follows.

**Decision order**
1. **First**, decide whether the difference between the two results arises *only* because the witness contains data that does not (or almost never) occur in the real database of this domain. Use the facts for this. If it does, label `implausible_data`, **even if one query is "more correct" on this witness**. Choose it only when the implausible data is the decisive reason for the difference.
2. **Otherwise**, label `pred_wrong`, `gold_wrong`, `both_wrong` or `ambiguous`, as in round 1.

**Rules**
- Do not open the key file or any other annotation file before finishing.
- The two annotators must work independently.
- State afterwards whether any AI tool was used.
