# 人工抽查表 2：R 层见证归因（30 条）——作者填写版

- 填表人：Hongsheng Wang（作者本人，先独立判定，后对照 AI 判定）
- 填写日期：2026-10-14
- 判定类别：`pred_wrong` / `gold_wrong` / `both_wrong` / `ambiguous` / `implausible_data`
- 抽样结构：CaliberGraph-R 与随机模糊-R 各 15 条，每方法按 AI 最终判定分层抽 5 条"不现实数据"+10 条"有意义"；条目打乱，不标注来源。
- 填写方式：逐条先独立判定（先看问题、提示、gold/pred SQL 与见证库，后对照 AI 判定）。

## 30 条判定明细

| 编号 | 题目 ID（数据集） | 问题摘要 | gold 结果 | pred 结果 | 我的判定 | 备注 | AI 最终 | 与最终一致 |
|---|---|---|---|---|---|---|---|---|
| 1 | alpha:556（codebase_community） | 浏览量>200 的用户人均徽章数 | `[[4.0]]` | `[[2.0]]` | **gold_wrong** | 两个不同用户同名 'gregmacfarlane'（真实数据常见同名），人均徽章=徽章数/用户数=4/2=2（pred）；gold 按 DisplayName 去重（=1）得 4，错误 | gold_wrong | ✓ |
| 2 | csc-32b:1025（european_football_2） | 2016 赛季（2015/2016）进球最多的联赛 | `[["Portugal Liga ZON Sagres"]]` | `[]` | **implausible_data** | 2015/2016 进球最多的 match 引用的 league_id=24558 在 League 表中不存在（外键缺失，真实数据不可能）；gold 只在现存联赛里排（葡萄牙 0 球），pred 先 LIMIT 后 join 丢失，差异纯由缺失联赛造成 | implausible_data | ✓ |
| 3 | slm:459（card_games） | "Serra Angel"与"Shrine Keeper"谁的转换法术力更高 | `[]` | `[["Shrine Keeper"]×4]` | **pred_wrong** | 见证库中两张牌都不存在，gold 空结果正确；pred 的 CASE 子查询取 NULL，NULL>NULL 为假落入 ELSE，对每行输出 'Shrine Keeper'，凭空捏造答案 | pred_wrong | ✓ |
| 4 | slm:1084（european_football_2） | 1986 年前出生且防守积极率高的球员数（去重） | `[[1]]` | `[[2]]` | **gold_wrong** | 两个不同球员同名 'Eduardo'（真实数据常见同名），问题数球员数应为 2（pred 按 fifa_api_id 去重）；gold 按 player_name 去重得 1，少算 | gold_wrong | ✓ |
| 5 | chess:260（toxicology） | 含三键分子中 P/Br 原子总数 | `[[0]]` | `[[1]]` | **implausible_data** | 唯一三键 TR000_2_4 属 molecule TR496，却连着其他分子（TR060 的 br、TR338 的 i）；pred 经 connected 跨分子计入 br 原子。真实数据中 connected 只连接同分子原子 | implausible_data | ✓ |
| 6 | csc-32b:1263（thrombosis_prediction） | HCT 异常患者中 aCL IgA 最高者 ID | `[[1074]]` | `[]` | **pred_wrong** | 正常范围 29<HCT<52，HCT=52 属异常；pred 用严格 >52 排除该患者，gold 用 >=52 正确返回 1074 | pred_wrong | ✓ |
| 7 | slm:1458（student_club） | New Jersey 与 Vermont 会员占比之差 | `[[-50.0]]` | `[[-100.0]]` | **pred_wrong** | gold 将(NJ-VT)÷总会员数×100 得 -50%（NJ 0%、VT 50%，差 -50%）正确；pred 忘了给 VT 计数除以总人数，得 -100 | pred_wrong | ✓ |
| 8 | gena_submission_1:1255（thrombosis_prediction） | 异常 Ig M 患者最常见诊断 | `[]` | `[["SLE susp"]]` | **gold_wrong** | 异常 IGM 定义为 <=40 或 >=400，IGM=400 属异常；gold 的 NOT BETWEEN 40 AND 400 恰好排除 400 的患者，漏答 | gold_wrong | ✓ |
| 9 | rsl:751（superhero） | 列出至少 5 个男性英雄的超能力 | 5 行含重复（仅 4 个不同能力） | 5 个不同能力 | **gold_wrong** | 题目要"至少 5 个超能力"；gold 无 DISTINCT，Super Strength 出现两次，实际只有 4 个不同能力；pred 去重后给出 5 个，正确 | gold_wrong | ✓ |
| 10 | rsl:1183（thrombosis_prediction） | 1997/1/27 诊断 SLE 患者的初诊诊断 | `[]` | `[["PM/DM"]]` | **gold_wrong** | 提示明确 original diagnose=Patient.Diagnosis（PM/DM）；gold 额外要求存在 First Date 当天的检查记录，真实患者多不具备，返回空 | gold_wrong | ✓ |
| 11 | csc-7b:637（codebase_community） | Mark Meckes 无评论帖子所用全部标签 | `[["<sampling>"]]` | `[["<sampling>"],["<r>"]]` | **gold_wrong** | "his posts"按 OwnerUserId 理解，Mark Meckes 拥有无评论帖 <sampling> 与 <r>；gold 经 postHistory 漏掉 <r>。见证中创建历史行归于他人（数据异常），但题意与 pred 语义更贴合 | implausible_data | ✗ |
| 12 | alpha:786（superhero） | 力量属性值最高的英雄数 | `[[0]]` | `[[1]]` | **gold_wrong** | 最高 Strength 值=10（仅 hero 2 持有）；gold 用全局 MAX=25（Speed）比较得 0；pred 限定 Strength 内取 MAX 得 1，正确 | gold_wrong | ✓ |
| 13 | chess:1096（european_football_2） | Pietro Marino 的平均总评 | `[[46.33]]` | `[[69.5]]` | **gold_wrong** | Pietro Marino 有 3 条属性记录（NULL、71、68），平均应为 69.5（AVG 忽略 NULL，真实数据常见 NULL 评分）；gold SUM/COUNT(id) 把 NULL 当 0，得 46.33 | gold_wrong | ✓ |
| 14 | slm:641（codebase_community） | 2014 年获得 Commentator 徽章的用户数 | `[[2]]` | `[[1]]` | **implausible_data** | 同一用户两条完全相同的 Commentator 记录（同时间戳），真实数据中该徽章一次性授予；仅此重复造成 2 vs 1 | implausible_data | ✓ |
| 15 | gsr:936（formula_1） | Lewis Hamilton 2008 澳站最快圈 | `[[40]]` | `[[1069]]` | **implausible_data** | lapTimes 记录圈数 1069，超过 108 圈比赛（且 results.fastestLap=40），真实数据不可能；pred 据损坏行返回 1069，gold 的 40 才合理 | implausible_data | ✓ |
| 16 | csc-32b:939（formula_1） | 2008 澳站英国籍参赛车手数 | `[[2]]` | `[[1]]` | **implausible_data** | 同一车手在同一场次有两条完全相同的 results 行，真实 2008 数据不存在（仅 1979 年前共享驾驶才有）；gold COUNT(*)=2 vs pred DISTINCT=1 仅由此重复造成 | implausible_data | ✓ |
| 17 | gena_submission_1:101（financial） | 1995 年最早交易日期的账户 | `[[8321]]` | `[[2723]]` | **ambiguous** | 账户 2723 与 8321 的 1995 年最早交易日并列（均 1995-06-30），题目用复数"accounts"且未规定并列处理，两种 LIMIT 1 都是任意取其一 | ambiguous | ✓ |
| 18 | alpha:583（codebase_community） | Yevgeny 编辑帖子的总得分与网站 URL | `[]` | `[[null,null]]` | **ambiguous** | 见证库无名为 Yevgeny 的用户；gold 的 GROUP BY 空结果与 pred 的单行 NULL 都表示"无答案" | ambiguous | ✓ |
| 19 | gsr:173（financial） | 账户 3 的结算频率与扣款 3539 的目的 | `[]` | `[["POPLATEK MESICNE","LEASING"]]` | **ambiguous** | 账户 3 有两笔 LEASING（3539 与 3，合计 3542）；"debiting 3539 in total"可读作单笔 3539（pred）或按用途合计 3539（gold），两种读法都成立 | ambiguous | ✓ |
| 20 | alpha:67（california_schools） | 1989 年旧金山社区大学区关闭数量 | `[[1]]` | `[[2]]` | **implausible_data** | 两条关闭记录中一条 School 名为 NULL，gold COUNT(School) 跳过它；真实数据仅区级记录无 School 名、学校级必有名称，故该行不现实 | implausible_data | ✓ |
| 21 | rsl:284（toxicology） | 含碳化合物中形成的键型 | `[["="],["-"]]` | `[["="],["-"],["#"]]` | **implausible_data** | 三键 TR000_2_5 属 molecule TR060，却连着其他分子的碳（TR496 的 TR000_3）；pred 多出的 "#" 仅由此跨分子连接产生，真实数据不会出现 | implausible_data | ✓ |
| 22 | slm:91（financial） | 1995 与 1996 平均失业率何者更高 | `[["1995"]]` | `[["1996"]]` | **implausible_data** | 唯一 district 的 A12（1995 失业率）为 NULL，两个 AVG 比较均返回 NULL，gold/pred 各自落入默认分支；真实数据仅 1/77 个区缺 A12 | implausible_data | ✓ |
| 23 | alpha:512（card_games） | duel deck A 中力量未知且无闪卡版的数量 | `[[null]]` | `[[0]]` | **gold_wrong** | 无卡片满足条件时数量应为 0（pred COUNT=0 正确）；gold 的 SUM 在空集上返回 NULL | gold_wrong | ✓ |
| 24 | chess:1147（european_football_2） | 总评最高的球员（1 名） | Paulinho、Ross Wallace、Moussa Sow | Paulinho | **ambiguous** | 三名球员并列最高分 78；题目要"one player"，pred 返回任一有效球员，gold 列出全部并列者，两种处理都可辩护 | ambiguous | ✓ |
| 25 | gena_submission_1:1331（student_club） | Vice President 收到的资金额 | `[]` | `[[null]]` | **ambiguous** | 见证库没有 Vice President；gold 空结果与 pred 的 NULL 聚合行都表示"无此类资金" | ambiguous | ✓ |
| 26 | csc-32b:876（formula_1） | 2015/11/29 比赛未完成车手数 | `[[1]]` | `[[0]]` | **implausible_data** | 唯一车手是冠军（status Finished、position 1、milliseconds 7052790）却 time 为 NULL，内部矛盾（真实数据中 milliseconds 与 time 同现）；gold 按 time IS NULL 计为未完成得 1，pred 按 status 得 0，差异由损坏行造成 | gold_wrong | ✗ |
| 27 | gsr:1122（european_football_2） | 最强的球员名字 | 两名并列者 | LIMIT 1 取其一 | **ambiguous** | 两名球员并列最高分 71；题目单数未规定并列处理，gold 列全部、pred LIMIT 1 均可辩护 | ambiguous | ✓ |
| 28 | gsr:253（toxicology） | 所有三键的元素 | `[["h"]]` | `[["cl"],["h"]]` | **implausible_data** | 三键 TR000_2_5 在 connected 中只有单向行，gold 只读 atom_id 漏掉另一端的 cl；真实数据每条键必有双向行，差异由不现实存储造成 | implausible_data | ✓ |
| 29 | omni-32-majority:212（toxicology） | 非致癌分子中最少的元素 | `[["c"]]` | `[["h"]]` | **gold_wrong** | 非致癌分子 TR060 中 c 有 2 个原子、h 有 1 个，"最少"应为 h（pred）；gold 按不同分子数计数制造并列并任意取 c，错误 | gold_wrong | ✓ |
| 30 | csc-32b:303（toxicology） | TR006 的双键数与是否致癌 | `[]` | `[[0,null]]` | **ambiguous** | 见证库中不存在 molecule TR006；gold 空结果与 pred 的 (0, NULL) 行都表示"无答案" | ambiguous | ✓ |

## 汇总统计

### 判定分布（30 条）

- pred_wrong：3 条（#3、#6、#7）
- gold_wrong：10 条（#1、#4、#8、#9、#10、#11、#12、#13、#23、#29）
- ambiguous：7 条（#17、#18、#19、#24、#25、#27、#30）
- implausible_data：10 条（#2、#5、#14、#15、#16、#20、#21、#22、#26、#28）
- both_wrong：0 条

分布与 AI 最终判定完全相同（10/3/7/10），仅 #11 与 #26 在两个类别间互换。

### 与 AI 判定的一致率（论文用）

| 口径 | 一致条数 / 总数 | 一致率 |
|---|---|---|
| 与 AI 最终判定 | 28 / 30 | 93.3% |
| 与 AI-A 判定 | 28 / 30 | 93.3% |
| 与 AI-B 判定 | 28 / 30 | 93.3% |
| 与至少一遍 AI 一致 | 30 / 30 | 100% |

不一致明细：
- 与 AI 最终（及 A）不一致（2 条）：**#11**（最终=implausible_data，我=gold_wrong：题意上"his posts"应指其拥有的帖子，gold 经 postHistory 漏掉 <r>，我按语义判 gold 错）；**#26**（最终=gold_wrong，我=implausible_data：冠军车手 time 为 NULL 且 milliseconds 在场，行内矛盾，我判差异由不现实数据造成）。
- 与 AI-B 不一致（2 条）：**#19**（B=pred_wrong，我=ambiguous）、**#24**（B=gold_wrong，我=ambiguous）——均为并列/双读法问题，B 的判定也合理，我倾向 ambiguous。

### 与上一批（试点轮 30 条）对比

| 口径 | 试点轮 | R 层本批 |
|---|---|---|
| 与 AI-A 一致 | 26/30 = 86.7% | 28/30 = 93.3% |
| 与 AI-B 一致 | 27/30 = 90.0% | 28/30 = 93.3% |
| 两遍一致项上一致 | 24/24 = 100% | —（本批以最终判定为准） |
| 与至少一遍 AI 一致 | 29/30 = 96.7% | 30/30 = 100% |

### 论文可用表述

中文：作者对 R 层 30 条见证独立人工复核，与 AI 最终判定的一致率为 93.3%（28/30），判定类别分布与 AI 完全相同（pred_wrong 3、gold_wrong 10、ambiguous 7、implausible_data 10），与至少一遍 AI 判定的一致率为 100%。

English: The author independently re-annotated all 30 R-layer witness cases. The agreement rate with the final AI label was 93.3% (28/30), the category distribution exactly matched the AI's (3 pred_wrong / 10 gold_wrong / 7 ambiguous / 10 implausible_data), and agreement with at least one AI pass was 100% (30/30).

### 关于"有意义比例"的提醒（口径核对）

本批按 AI 最终判定分层抽取（每方法 5 条不现实 + 10 条有意义），因此抽查所得 20/30"有意义"是**抽样设计使然，不能直接作为 R 层总体"有意义比例"的无偏估计**。论文中"有意义比例 75%"若基于全量 R 层见证，建议单独核对计算口径与分母；本批抽查只用于验证人工与 AI 归因判定的一致性，而非估计该比例。
