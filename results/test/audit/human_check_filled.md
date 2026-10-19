# 人工抽查表：见证归因（30 条）——作者填写版

- 填表人：Hongsheng Wang（作者本人，先独立判定，后对照两遍 AI 标注）
- 填写日期：2026-10-14
- 判定类别：`pred_wrong`（预测答错）/ `gold_wrong`（gold 答错）/ `both_wrong`（都错）/ `ambiguous`（两种读法都成立）/ `implausible_data`（差异仅由现实中不会出现的数据引起）

## 抽样结构（与原表一致）

- 两遍 AI 标注不一致的 6 条：#4、#5、#6、#8、#10、#12
- 两遍都判 implausible 的 12 条：#11、#14、#15、#16、#17、#22、#25、#26、#27、#28、#29、#30
- 两遍都判"有意义"的 12 条：#1、#2、#3、#7、#9、#13、#18、#19、#20、#21、#23、#24

## 30 条判定明细

| 编号 | 题目 ID（数据集） | 问题摘要 | gold 结果 | pred 结果 | 我的判定 | 备注 | AI-A 判定 | AI-B 判定 |
|---|---|---|---|---|---|---|---|---|
| 1 | chess:867（formula_1） | 933 号比赛最快圈速车手的国籍 | `[]` | `[[null]]` | **pred_wrong** | 933 号比赛没有任何 fastestLapTime 记录，无人创下最快圈速，gold 空结果正确；pred 缺 NULL 守卫，返回任意车手（国籍为 NULL） | pred_wrong | pred_wrong |
| 2 | gsr:1202（thrombosis_prediction） | 1995–1997 检测、诊断 Behcet 且未住院的男性患者人数 | `[[2]]` | `[[1]]` | **gold_wrong** | 问的是"患者人数"；同一患者（ID 1001）有两条 Examination 记录，应去重计 1（pred 的 DISTINCT）；gold 按行计数把同一患者算了两次 | gold_wrong | gold_wrong |
| 3 | alpha:1145（european_football_2） | 2015/2016 赛季比赛最多的 top 4 联赛 | 西/葡/意/德 | 葡/德/法/西 | **ambiguous** | 5 个联赛各 1 场全部并列，"top 4"无唯一答案，两种截断都成立 | ambiguous | ambiguous |
| 4 | gena_submission_1:1342（student_club） | 2019/9/4 的 "Posters" 费用 | `[[1.5]]` | `[]` | **pred_wrong** | 题目只问该日期 Posters 这条 expense 的 cost；gold 直接查 expense 得 1.5 正确；pred 多加 budget/event join，因该行 link_to_budget 为 NULL 而丢弃 → 答错（即使该行数据可疑，join 设计本身也超出题意） | implausible_data | pred_wrong |
| 5 | csc-32b:637（codebase_community） | Mark Meckes 无评论帖子所用全部标签 | `[[null]]` | `[["b"],[null]]` | **gold_wrong** | "his posts"自然指其拥有的帖子（OwnerUserId）；gold 经 postHistory 通路漏掉 post 1002（Tags='b'），pred 按 OwnerUserId 更贴合题意 | implausible_data | gold_wrong |
| 6 | omni-32-majority:456（card_games） | 卡牌 "Molimo, Maro-Sorcerer" 的全部类型 | `[[null,null]]` | `[]` | **implausible_data** | 该牌在真实数据中 subtypes/supertypes 必有值（Legendary Creature—Elemental），见证库中两列均为 NULL；NULL 行 vs 空集的差异仅由这不现实的 NULL 造成（该行 asciiName 与 name 也不一致） | implausible_data | ambiguous |
| 7 | alpha:755（superhero） | 列出至少 5 个 Demi-God 英雄全名 | 6 个（含 null） | 5 个（LIMIT 5） | **ambiguous** | "at least five"：返回全部 6 个（gold）与恰好 5 个（pred）都满足题意 | ambiguous | ambiguous |
| 8 | chess:637（codebase_community） | 同 #5（Mark Meckes 无评论帖子标签） | `[[null]]` | `[["b"],[null]]` | **gold_wrong** | 同 #5：gold 经 postHistory 漏掉 Mark Meckes 拥有的 post 1002 | implausible_data | gold_wrong |
| 9 | chess:789（superhero） | 外星英雄的平均体重 | `[[539.5]]` | `[[1079.0]]` | **gold_wrong** | AVG 应忽略 NULL（pred 1079 正确）；gold 用 SUM/COUNT 把未知体重当作 0 计入，得 539.5，错误 | gold_wrong | gold_wrong |
| 10 | chess:260（toxicology） | 含三键分子中 P/Br 原子总数 | `[[1]]` | `[[2]]` | **implausible_data** | pred 的 2 来自 connected 中跨分子自环连接（atom v1007 属 molecule v1008，却连到 molecule v1064 的三键 v1009），化学上不可能；排除该异常数据后 gold=pred=1，分歧纯属数据产物 | implausible_data | pred_wrong |
| 11 | csc-7b:245（toxicology） | 碘原子的平均键数 | `[[1.0]]` | `[[2]]` | **implausible_data** | 碘原子的同一条 bond 出现两次且含自环（atom 连向自己），真实 connected 数据不存在；1.0 vs 2 仅由该数据造成 | implausible_data | implausible_data |
| 12 | alpha:1513（debit_card_specializing） | 2012/8/25 第一个付费客户所在国家 | `[["SVK"]]` | `[["CZE"]]` | **pred_wrong** | 见证库中唯一有支付信息（Time、Price）的交易是 1018（SVK 加油站）；1004 无时间无价格，不是"paid customer"。pred 按 transactionid 取到 1004 → CZE 答错；gold 的 SVK 是唯一可辩护答案（注：gold 按 Time DESC 排序语义可商榷，但结果正确） | gold_wrong | implausible_data |
| 13 | gena_submission_1:74（california_schools） | NCESDist=0613360 且 SPECON 学校的最低年级 | `[[null]]` | `[]` | **ambiguous** | 无学校匹配：gold 的 NULL MIN 与 pred 的空集都表示"无答案" | ambiguous | ambiguous |
| 14 | gsr:801（superhero） | 男/女超级英雄之比 | `[[null]]` | `[[0.0]]` | **implausible_data** | 见证库把 gender id=2 标为 Male，与真实 id 映射相反（证据按 gender_id=1 为 male）；仅此不匹配造成 NULL vs 0.0 | implausible_data | implausible_data |
| 15 | omni-32-majority:273（toxicology） | 致癌分子中氯元素百分比 | `[[null]]` | `[[0.0]]` | **implausible_data** | 唯一 atom 的 element 为 NULL（真实数据必有值）；gold 除以 COUNT(element)=0 得 NULL vs pred 0.0 仅由此产生 | implausible_data | implausible_data |
| 16 | csc-32b:260（toxicology） | 同 #10（三键分子中 P/Br 原子数） | `[[0]]` | `[[2]]` | **implausible_data** | 两个含三键的分子（v1002、v1080）在 atom 表中无任何原子；pred 的 2 来自跨分子自环连接（化学上不可能）；真实数据下 gold=pred=0 | implausible_data | implausible_data |
| 17 | rsl:1495（debit_card_specializing） | 2013 年 9 月消费最多的客户 | `[[1012]]` | `[[1002]]` | **implausible_data** | 两个客户 9 月 Consumption 均为 NULL，人为并列，gold/pred 各自任意取一个；真实 yearmonth 必有消费值 | implausible_data | implausible_data |
| 18 | csc-7b:426（card_games） | 不出现在 MTGO 的 top 3 系列（字母序） | `[]` | `[["y2"]]` | **gold_wrong** | 提示明确"不在 MTGO"= mtgoCode IS NULL 或空串；gold 漏掉空串情形（该行 mtgoCode=''），pred 正确 | gold_wrong | gold_wrong |
| 19 | csc-7b:1391（student_club） | 金融/物理专业学生之比 | `[[0]]` | `[[0.5]]` | **gold_wrong** | 1 个 Finance / 2 个 Physics，比率应为 0.5；gold 整数除法截断为 0 | gold_wrong | gold_wrong |
| 20 | csc-7b:107（financial） | 最高平均工资分行中最年长开户客户性别 | `[["M"]]` | `[["F"]]` | **pred_wrong** | pred 忽略"最高平均工资分行"（A11）条件，只按出生日期取最年长客户（F）；gold 限定 A11 最高分行（district 1005）后为 M | pred_wrong | pred_wrong |
| 21 | rsl:131（financial） | 活跃贷款最高的地区 | `[["south Bohemia"]]` | `[["south Moravia"]]` | **pred_wrong** | "highest active loan"指贷款金额最大：gold 按 SUM(amount)（3>1）得 south Bohemia 正确；pred 按贷款笔数排序并随意打破 1:1 并列 | pred_wrong | pred_wrong |
| 22 | gsr:1101（european_football_2） | Parma 客场在意大利比赛的平均进球 | `[[0.5]]` | `[[1.0]]` | **implausible_data** | 见证库中 Parma 客场进球存在 NULL（真实必有值），且含两个 Italy、两个 Parma、country/league 不一致等异常；0.5 vs 1.0 仅由 NULL 进球造成 | implausible_data | implausible_data |
| 23 | gsr:512（card_games） | duel deck A 中力量未知且无闪卡版的数量 | `[[null]]` | `[[0]]` | **gold_wrong** | 无卡片匹配时数量应为 0（pred 的 COUNT=0 正确）；gold 的 SUM 在空集上返回 NULL | gold_wrong | gold_wrong |
| 24 | gsr:98（financial） | 1997 年获批、金额最低且周结单的账户 | `[[1001]]` | `[[1001],[1010]]` | **gold_wrong** | 题目要求"list out"全部最低金额账户；两个账户并列（金额均 1），gold 的 LIMIT 1 漏掉 1010 | gold_wrong | gold_wrong |
| 25 | csc-7b:1013（formula_1） | 奥地利大奖赛赛道的最快圈速记录 | `[["2000-01-01"]]` | `[[null]]` | **implausible_data** | fastestLapTime 被存成日期串 '2000-01-01'、lapTimes.time 为 NULL 且 milliseconds=2，均为损坏数据，两个结果都不具意义 | implausible_data | implausible_data |
| 26 | rsl:695（codebase_community） | 获得 'Citizen Patrol' 徽章的用户数 | `[[2]]` | `[[1]]` | **implausible_data** | Citizen Patrol 为一次性徽章，见证库同一用户出现两条记录（真实数据不可能）；仅此重复造成 2 vs 1 | implausible_data | implausible_data |
| 27 | gena_submission_2:75（california_schools） | county 37 且 Breakfast Provision 2 学校的教育层级与校名 | `[["High School",null],["Adult","v1015"]]` | `[["High School",null],["Adult","v1014"]]` | **implausible_data** | 同一 CDSCode 在 schools.School 与 frpm."School Name" 中名称不一致（v1015 vs v1014），真实反范式数据应一致；仅此决定输出哪个校名 | implausible_data | implausible_data |
| 28 | omni-32-majority:112（financial） | 1976/1/29 出生的女性客户开户地区 | `[["c"],["v1040"]]` | `[["v1040"]]` | **implausible_data** | 客户 1003 所在 district 无任何 account（也无 disp 关联），真实金融库中客户必有账户；仅此使 pred 的账户 join 排除她 | implausible_data | implausible_data |
| 29 | alpha:1015（formula_1） | 奥地利赛道圈速记录在哪场比赛创造 | `[]` | `[["Austrian Grand Prix"]]` | **implausible_data** | 唯一 lapTimes 行的 time/milliseconds 均为 NULL（真实必有值），results.fastestLapTime 为 NULL；pred 据此返回一场没有圈速记录的比赛 | implausible_data | implausible_data |
| 30 | gena_submission_1:1057（european_football_2） | 波兰 2010/2011 主场平均进球 | `[[1.5]]` | `[[3.0]]` | **implausible_data** | 波兰 2010/2011 存在 home_team_goal 为 NULL 的场次（真实必有值），gold 的 SUM/COUNT 与 pred 的 AVG 仅因此不同 | implausible_data | implausible_data |

## 汇总统计

### 判定分布（30 条）

- pred_wrong：5 条（#1、#4、#12、#20、#21）
- gold_wrong：8 条（#2、#5、#8、#9、#18、#19、#23、#24）
- ambiguous：3 条（#3、#7、#13）
- implausible_data：14 条（#6、#10、#11、#14、#15、#16、#17、#22、#25、#26、#27、#28、#29、#30）
- both_wrong：0 条

### 与 AI 标注的一致率（论文用）

| 口径 | 一致条数 / 总数 | 一致率 |
|---|---|---|
| 与 AI 标注 A | 26 / 30 | 86.7% |
| 与 AI 标注 B | 27 / 30 | 90.0% |
| 两遍 AI 一致的 24 条 | 24 / 24 | 100% |
| 与至少一遍 AI 一致 | 29 / 30 | 96.7% |

不一致明细：
- 与 A 不一致（4 条）：#4、#5、#8（我判真实错误，A 判 implausible_data）、#12（A 判 gold_wrong，我判 pred_wrong）
- 与 B 不一致（3 条）：#6（B 判 ambiguous，我判 implausible_data）、#10（B 判 pred_wrong，我判 implausible_data）、#12（B 判 implausible_data，我判 pred_wrong）
- 唯一与两遍 AI 均不一致的是 #12（三方分歧：A=gold_wrong，B=implausible_data，我=pred_wrong）

### 论文可用表述

中文：作者对 30 条抽样独立人工复核，在两遍 AI 标注一致的 24 条上一致率为 100%（24/24）；与至少一遍 AI 标注的一致率为 96.7%（29/30）；分别与两遍标注的一致率为 86.7%（26/30）与 90.0%（27/30）。

English: The author independently re-annotated all 30 sampled cases. The agreement rate was 100% (24/24) on the cases where the two AI passes agreed, 96.7% (29/30) with at least one AI pass, and 86.7% (26/30) / 90.0% (27/30) with AI pass A / B respectively.

## 作者与单位信息确认

- 作者：**Hongsheng Wang**
- 第一单位：**College of Computer Science and Technology, Zhejiang University**
- 第二单位：**Artificial Intelligence Department, Loctek Ergonomic Technology Corp.**

署名格式建议（上标编号按投稿模板调整）：

```
Hongsheng Wang¹,²
¹ College of Computer Science and Technology, Zhejiang University
² Artificial Intelligence Department, Loctek Ergonomic Technology Corp.
```

注：如目标期刊模板要求补充城市/邮编（如 "Hangzhou, China"），请作者按投稿要求补充，本表不做臆造。
