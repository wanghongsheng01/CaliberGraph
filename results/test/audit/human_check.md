# 人工抽查表：见证归因（30 条）

每条请在"你的判定"一栏填写：pred_wrong / gold_wrong / both_wrong / ambiguous / implausible_data。
可在"备注"写理由。各类定义如下：
- pred_wrong：预测答错了题
- gold_wrong：gold 答错了题
- both_wrong：两条都答错
- ambiguous：题目两种读法都成立
- implausible_data：差异只在现实中不会出现的数据上才出现

抽样方式：两遍 AI 标注不一致的 6 条，两遍都判 implausible 的 12 条，两遍都判"有意义"的 12 条，三层各自随机抽取。
**请先独立判断，再看 AI 的判定**（AI 判定列在每条的最后）。

## 1. chess:867（formula_1）

**问题**：For the driver who set the fastest lap speed in race No.933, where does he come from?
**提示**：fastest lap speed refers to MAX(fastestLapSpeed);

**gold**：
```sql
SELECT T1.nationality FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId WHERE T2.raceId = 933 AND T2.fastestLapTime IS NOT NULL ORDER BY T2.fastestLapSpeed DESC LIMIT 1
```
**pred**：
```sql
SELECT T2.nationality FROM results AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T1.raceId = 933 ORDER BY T1.fastestLapSpeed DESC LIMIT 1
```
**见证库**（每表的行，列序同 DDL）：
```
    circuits(circuitId, circuitRef, name, location, country, lat, lng, alt, url)
      [1183, "a", "A", null, null, null, null, null, "A"]
    constructors(constructorId, constructorRef, name, nationality, url)
      [1002, "b", "y2", "Canadian", "b"]
    drivers(driverId, driverRef, number, code, forename, surname, dob, nationality, url)
      [1003, "a", 10, null, "A", "y2", "2020-02-29", null, "c"]
    races(raceId, year, round, circuitId, name, date, time, url)
      [933, 1182, -1, 1183, "x1", "1995-12-31", "04:30:00", null]
    results(resultId, raceId, driverId, constructorId, number, grid, position, positionText, positionOrder, points, laps, time, milliseconds, fastestLap, rank, fastestLapTime, fastestLapSpeed, statusId)
      [1005, 933, 1003, 1002, null, 0, 0, "b", 100, 10.0, 100, null, null, null, null, null, "x1", 1006]
    seasons(year, url)
      [1182, "A"]
    status(statusId, status)
      [1006, "x1"]
```
**gold 结果**：`[]`　**pred 结果**：`[[null]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：pred_wrong（No result in the race has a fastest lap speed, so no driver set it; gold correctly returns nothing while pred returns an arbitrary driver.）<br>B：pred_wrong（No driver in race 933 has a recorded fastest lap speed, so gold's empty result is right while pred returns a driver whose speed is NULL because it lacks a NULL guard.）</details>

## 2. gsr:1202（thrombosis_prediction）

**问题**：How many male patients who underwent testing between 1995 and 1997 and were subsequently diagnosed with Behcet disease did not stay in the hospital for treatment?
**提示**：male refers to SEX = 'M'; underwent testing between 1995 and 1997 refers to `Examination Date` between '1995' and '1997'; Behcet refers to diagnosis; did not stay in the hospital refers to Admission = '-'

**gold**：
```sql
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T2.Diagnosis = 'Behcet' AND T1.SEX = 'M' AND STRFTIME('%Y', T2.`Examination Date`) BETWEEN '1995' AND '1997' AND T1.Admission = '-'
```
**pred**：
```sql
SELECT COUNT(DISTINCT e.ID) FROM Examination e JOIN Patient p ON e.ID = p.ID WHERE p.SEX = 'M' AND e.Diagnosis = 'Behcet' AND e.`Examination Date` BETWEEN '1995-01-01' AND '1997-12-31' AND p.Admission = '-';
```
**见证库**（每表的行，列序同 DDL）：
```
    Examination(ID, Examination Date, aCL IgG, aCL IgM, ANA, ANA Pattern, aCL IgA, Diagnosis, KCT, RVVT, LAC, Symptoms, Thrombosis)
      [1001, "1995-01-01", -1.5, null, 100, "P.S", 10, "Behcet", "-", "+", "-", null, null]
      [1001, "1995-01-01", -1.5, null, 100, "P.S", 10, "Behcet", "-", "+", "-", null, null]
    Patient(ID, SEX, Birthday, Description, First Date, Admission, Diagnosis)
      [1001, "M", "2020-02-29", "2015-03-20", null, "-", null]
```
**gold 结果**：`[[2]]`　**pred 结果**：`[[1]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：gold_wrong（The patient has two Behcet examination rows; question asks how many patients, so pred COUNT(DISTINCT ID)=1 is right and gold counts examinations.）<br>B：gold_wrong（The question counts patients, and one patient with two examination rows should be counted once (pred's DISTINCT), whereas gold counts examination rows.）</details>

## 3. alpha:1145（european_football_2）

**问题**：Which top 4 leagues had the most games in the 2015-2016 season?
**提示**：in the 2015-2016 season refers to season = '2015/2016'; league with most games refers to League.name where MAX(COUNT(id))

**gold**：
```sql
SELECT t1.name FROM League AS t1 INNER JOIN Match AS t2 ON t1.id = t2.league_id WHERE t2.season = '2015/2016' GROUP BY t1.name ORDER BY COUNT(t2.id) DESC LIMIT 4
```
**pred**：
```sql
SELECT l.name FROM league AS l INNER JOIN (SELECT league_id, COUNT(id) AS match_count FROM match WHERE season = '2015/2016' GROUP BY league_id) AS m ON l.id = m.league_id ORDER BY m.match_count DESC LIMIT 4
```
**见证库**（每表的行，列序同 DDL）：
```
    Country(id, name)
      [1001, "Poland"]
      [1073, "Netherlands"]
      [1078, "Netherlands"]
      [1083, "Poland"]
      [1088, "France"]
    League(id, country_id, name)
      [1002, 1001, "Portugal Liga ZON Sagres"]
      [1074, 1073, "Germany 1. Bundesliga"]
      [1079, 1078, "France Ligue 1"]
      [1084, 1083, "Spain LIGA BBVA"]
      [1089, 1088, "Italy Serie A"]
    Match(id, country_id, league_id, season, stage, date, match_api_id, home_team_api_id, away_team_api_id, home_team_goal, away_team_goal, home_player_X1, home_player_X2, home_player_X3, home_player_X4, home_player_X5, home_player_X6, home_player_X7, home_player_X8, home_player_X9, home_player_X10, home_player_X11, away_player_X1, away_player_X2, away_player_X3, away_player_X4, away_player_X5, away_player_X6, away_player_X7, away_player_X8, away_player_X9, away_player_X10, away_player_X11, home_player_Y1, home_player_Y2, home_player_Y3, home_player_Y4, home_player_Y5, home_player_Y6, home_player_Y7, home_player_Y8, home_player_Y9, home_player_Y10, home_player_Y11, away_player_Y1, away_player_Y2, away_player_Y3, away_player_Y4, away_player_Y5, away_player_Y6, away_player_Y7, away_player_Y8, away_player_Y9, away_player_Y10, away_player_Y11, home_player_1, home_player_2, home_player_3, home_player_4, home_player_5, home_player_6, home_player_7, home_player_8, home_player_9, home_player_10, home_player_11, away_player_1, away_player_2, away_player_3, away_player_4, away_player_5, away_player_6, away_player_7, away_player_8, away_player_9, away_player_10, away_player_11, goal, shoton, shotoff, foulcommit, card, cross, corner, possession, B365H, B365D, B365A, BWH, BWD, BWA, IWH, IWD, IWA, LBH, LBD, LBA, PSH, PSD, PSA, WHH, WHD, WHA, SJH, SJD, SJA, VCH, VCD, VCA, GBH, GBD, GBA, BSH, BSD, BSA)
      [1003, null, 1002, "2015/2016", null, null, null, null, 3, null, null, null, null, 3, null, null, 10, null, null, null, null, 100, null, null, null, 1, null, 1, null, 10, null, null, 0, 0, null, 100, null, 100, null, null, null, null, 0, 5, null, null, null, null, null, null, null, null, null, null, null, null, 1, -1, 5, null, null, null, null, -1, null, null, null, 10, null, null, null, null, 0, null, null, null, null, null, null, null, null, "b", null, null, "x1", null, null, null, null, 2.0, null, null, 1.0, null, null, 2.0, null, null, null, null, null, null, 2.0, null, null, null, null, null, null, null, 0.0, null, 100.0, 1.5, null]
      [1076, null, 1074, "2015/2016", null, null, null, null, 3, null, null, null, null, 3, null, null, 10, null, null, null, null, 100, null, null, null, 1, null, 1, null, 10, null, null, 0, 0, null, 100, null, 100, null, null, null, null, 0, 5, null, null, null, null, null, null, null, null, null, null, null, null, 1, -1, 5, null, null, null, null, -1, null, null, null, 10, null, null, null, null, 0, null, null, null, null, null, null, null, null, "b", null, null, "x1", null, null, null, null, 2.0, null, null, 1.0, null, null, 2.0, null, null, null, null, null, null, 2.0, null, null, null, null, null, null, null, 0.0, null, 100.0, 1.5, null]
      [1081, null, 1079, "2015/2016", null, null, null, null, 3, null, null, null, null, 3, null, null, 10, null, null, null, null, 100, null, null, null, 1, null, 1, null, 10, null, null, 0, 0, null, 100, null, 100, null, null, null, null, 0, 5, null, null, null, null, null, null, null, null, null, null, null, null, 1, -1, 5, null, null, null, null, -1, null, null, null, 10, null, null, null, null, 0, null, null, null, null, null, null, null, null, "b", null, null, "x1", null, null, null, null, 2.0, null, null, 1.0, null, null, 2.0, null, null, null, null, null, null, 2.0, null, null, null, null, null, null, null, 0.0, null, 100.0, 1.5, null]
      [1086, null, 1084, "2015/2016", null, null, null, null, 3, null, null, null, null, 3, null, null, 10, null, null, null, null, 100, null, null, null, 1, null, 1, null, 10, null, null, 0, 0, null, 100, null, 100, null, null, null, null, 0, 5, null, null, null, null, null, null, null, null, null, null, null, null, 1, -1, 5, null, null, null, null, -1, null, null, null, 10, null, null, null, null, 0, null, null, null, null, null, null, null, null, "b", null, null, "x1", null, null, null, null, 2.0, null, null, 1.0, null, null, 2.0, null, null, null, null, null, null, 2.0, null, null, null, null, null, null, null, 0.0, null, 100.0, 1.5, null]
      [1091, null, 1089, "2015/2016", null, null, null, null, 3, null, null, null, null, 3, null, null, 10, null, null, null, null, 100, null, null, null, 1, null, 1, null, 10, null, null, 0, 0, null, 100, null, 100, null, null, null, null, 0, 5, null, null, null, null, null, null, null, null, null, null, null, null, 1, -1, 5, null, null, null, null, -1, null, null, null, 10, null, null, null, null, 0, null, null, null, null, null, null, null, null, "b", null, null, "x1", null, null, null, null, 2.0, null, null, 1.0, null, null, 2.0, null, null, null, null, null, null, 2.0, null, null, null, null, null, null, null, 0.0, null, 100.0, 1.5, null]
```
**gold 结果**：`[["Spain LIGA BBVA"], ["Portugal Liga ZON Sagres"], ["Italy Serie A"], ["Germany 1. Bundesliga"]]`　**pred 结果**：`[["Portugal Liga ZON Sagres"], ["Germany 1. Bundesliga"], ["France Ligue 1"], ["Spain LIGA BBVA"]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：ambiguous（All five leagues tie with one match each, so which four are the top 4 is unspecified tie-breaking.）<br>B：ambiguous（All five leagues tie with one 2015/2016 match each, so the top 4 is not determined and both selections are valid.）</details>

## 4. gena_submission_1:1342（student_club）

**问题**：What was the cost for the "Posters" on 2019/9/4?
**提示**：'Poster' is an event description; on 2019/9/14 refers to event_date = '2019-09-04'

**gold**：
```sql
SELECT cost FROM expense WHERE expense_description = 'Posters' AND expense_date = '2019-09-04'
```
**pred**：
```sql
SELECT T1.cost FROM expense AS T1 INNER JOIN budget AS T2 ON T1.link_to_budget = T2.budget_id INNER JOIN event AS T3 ON T2.link_to_event = T3.event_id WHERE T1.expense_description = 'Posters' AND T1.expense_date = '2019-09-04'
```
**见证库**（每表的行，列序同 DDL）：
```
    budget(budget_id, category, spent, remaining, amount, event_status, link_to_event)
      ["v1001", "A", null, 100.0, null, null, "recI43CzsZ0Q625ma"]
      ["recKjd7dcURsmP0KY", "Food", 1.0, null, null, "Planning", "reczhS8wix6Kzbp9P"]
    event(event_id, event_name, event_date, type, notes, location, status)
      ["recI43CzsZ0Q625ma", null, null, "Guest Speaker", "Students can stop by the table to get information on the club and register.", "Campus Soccer/Lacrosse stadium", "Planning"]
      ["reczhS8wix6Kzbp9P", null, null, "Social", "Attend school Woman's Lacrosse game as a group.", "Conference Room BA 452", "Closed"]
      ["v1380", null, null, "a", "Semester social event. Optional attendance.", "Campus Football stadium", "Open"]
    expense(expense_id, expense_description, expense_date, cost, approved, link_to_member, link_to_budget)
      ["v1003", "Posters", "2019-09-04", 1.5, null, "recro8T1MPMwRadVH", null]
      ["v1378", "Posters", "2019-10-22", 1.0, null, "recro8T1MPMwRadVH", "recKjd7dcURsmP0KY"]
    major(major_id, major_name, department, college)
      ["recVeoVlIsO6k6iUM", null, null, "College of Science"]
    member(member_id, first_name, last_name, email, position, t_shirt_size, phone, zip, link_to_major)
      ["recro8T1MPMwRadVH", null, null, null, null, "Large", null, 1236, "recVeoVlIsO6k6iUM"]
    zip_code(zip_code, type, city, county, state, short_state)
      [1236, "Unique", null, null, null, "y2"]
```
**gold 结果**：`[[1.5]]`　**pred 结果**：`[]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（The Posters expense has NULL link_to_budget, which real expense records do not; only that makes pred unnecessary budget join drop it.）<br>B：pred_wrong（The question asks only for the cost of the 'Posters' expense on that date; pred's unnecessary join to budget/event drops this expense because it has no budget link.）</details>

## 5. csc-32b:637（codebase_community）

**问题**：State all the tags used by Mark Meckes in his posts that doesn't have comments.
**提示**：used by Mark Meckes refers to DisplayName = 'Mark Meckes'; Doen't have comments refers to CommentCount = 0;

**gold**：
```sql
SELECT T3.Tags FROM users AS T1 INNER JOIN postHistory AS T2 ON T1.Id = T2.UserId INNER JOIN posts AS T3 ON T3.Id = T2.PostId WHERE T1.DisplayName = 'Mark Meckes' AND T3.CommentCount = 0
```
**pred**：
```sql
SELECT DISTINCT Tags FROM posts JOIN users ON posts.OwnerUserId = users.Id WHERE users.DisplayName = 'Mark Meckes' AND posts.CommentCount = 0
```
**见证库**（每表的行，列序同 DDL）：
```
    postHistory(Id, PostHistoryTypeId, PostId, RevisionGUID, CreationDate, UserId, Text, Comment, UserDisplayName)
      [1013, 0, 1014, null, "2020-02-29 23:59:59", 1015, null, "x1", "A"]
    posts(Id, PostTypeId, AcceptedAnswerId, CreaionDate, Score, ViewCount, Body, OwnerUserId, LasActivityDate, Title, Tags, AnswerCount, CommentCount, FavoriteCount, LastEditorUserId, LastEditDate, CommunityOwnedDate, ParentId, ClosedDate, OwnerDisplayName, LastEditorDisplayName)
      [1002, null, null, "2010-06-15 12:30:00", null, null, null, 1003, null, "y2", "b", null, 0, null, 1003, "2015-03-20 08:00:00", null, null, null, null, "x1"]
      [1014, null, null, null, null, 0, "x1", 1015, null, null, null, null, 0, null, 1015, null, null, 1, null, null, null]
    users(Id, Reputation, CreationDate, DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, AccountId, Age, ProfileImageUrl)
      [1003, null, "2015-03-20 08:00:00", "Mark Meckes", null, "a", null, "y2", 1, null, 10, null, null, "b"]
      [1015, null, null, "Mark Meckes", "2000-01-01 00:00:00", "y2", "x1", null, 5, null, null, null, null, "A"]
```
**gold 结果**：`[[null]]`　**pred 结果**：`[["b"], [null]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（Mark Meckes owns post 1002 but has no postHistory row for it, while real posts always have creation history by their owner.）<br>B：gold_wrong（'His posts' means posts Mark Meckes owns; pred includes his owned post 1002, while gold only reaches posts through postHistory and misses it.）</details>

## 6. omni-32-majority:456（card_games）

**问题**：What's the list of all types for the card "Molimo, Maro-Sorcerer"?
**提示**：card "Molimo, Maro-Sorcerer" refers to name = 'Molimo, Maro-Sorcerer'; list of all types refers to subtypes,supertypes

**gold**：
```sql
SELECT DISTINCT subtypes, supertypes FROM cards WHERE name = 'Molimo, Maro-Sorcerer'
```
**pred**：
```sql
SELECT subtypes, supertypes FROM cards WHERE name = 'Molimo, Maro-Sorcerer' AND (subtypes IS NOT NULL OR supertypes IS NOT NULL);
```
**见证库**（每表的行，列序同 DDL）：
```
    cards(id, artist, asciiName, availability, borderColor, cardKingdomFoilId, cardKingdomId, colorIdentity, colorIndicator, colors, convertedManaCost, duelDeck, edhrecRank, faceConvertedManaCost, faceName, flavorName, flavorText, frameEffects, frameVersion, hand, hasAlternativeDeckLimit, hasContentWarning, hasFoil, hasNonFoil, isAlternative, isFullArt, isOnlineOnly, isOversized, isPromo, isReprint, isReserved, isStarter, isStorySpotlight, isTextless, isTimeshifted, keywords, layout, leadershipSkills, life, loyalty, manaCost, mcmId, mcmMetaId, mtgArenaId, mtgjsonV4Id, mtgoFoilId, mtgoId, multiverseId, name, number, originalReleaseDate, originalText, originalType, otherFaceIds, power, printings, promoTypes, purchaseUrls, rarity, scryfallId, scryfallIllustrationId, scryfallOracleId, setCode, side, subtypes, supertypes, tcgplayerProductId, text, toughness, type, types, uuid, variations, watermark)
      [1002, null, "Lim-Dul's High Guard", "paper", "white", null, null, null, "G", null, null, "b", null, null, null, "Godzilla, King of the Monsters", null, null, "a", "2", 3, 100, 2, -1, 10, 100, 3, 0, 1, 3, 10, 2, 100, 1, -1, "x1", "adventure", "{'brawl': False, 'commander': True, 'oathbreaker': True}", "-5", "3", null, null, null, null, "c", null, null, null, "Molimo, Maro-Sorcerer", "x1", null, null, null, "a", "1", null, null, null, "mythic", null, "x1", null, null, "d", null, null, null, "x1", null, null, null, "A", null, "A"]
```
**gold 结果**：`[[null, null]]`　**pred 结果**：`[]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（The card Molimo, Maro-Sorcerer has both subtypes and supertypes NULL, unrealistic for this legendary creature; that is the only reason for the empty-vs-NULL-row difference.）<br>B：ambiguous（The card has NULL subtypes and supertypes, and the question does not say whether to return a row of NULLs (gold) or nothing (pred).）</details>

## 7. alpha:755（superhero）

**问题**：List down at least five full name of Demi-God superheroes.
**提示**：Demi-God superheroes refers to race = 'Demi-God'

**gold**：
```sql
SELECT T1.full_name FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T2.race = 'Demi-God'
```
**pred**：
```sql
SELECT superhero.full_name FROM superhero INNER JOIN race ON superhero.race_id = race.id WHERE race.race = 'Demi-God' LIMIT 5
```
**见证库**（每表的行，列序同 DDL）：
```
    alignment(id, alignment)
      [1001, "Bad"]
      [1106, "Good"]
      [1113, "N/A"]
      [1120, "Bad"]
      [1127, "N/A"]
      [1134, "N/A"]
    colour(id, colour)
      [1002, null]
      [1107, null]
      [1114, null]
      [1121, null]
      [1128, null]
      [1135, null]
    gender(id, gender)
      [1003, "Female"]
      [1108, "N/A"]
      [1115, "N/A"]
      [1122, "N/A"]
      [1129, "Female"]
      [1136, "Male"]
    publisher(id, publisher_name)
      [1004, "IDW Publishing"]
      [1109, "Universal Studios"]
      [1116, "Icon Comics"]
      [1123, "George Lucas"]
      [1130, "c"]
      [1137, "DC Comics"]
    race(id, race)
      [1005, "Demi-God"]
      [1110, "Demi-God"]
      [1117, "Demi-God"]
      [1124, "Demi-God"]
      [1131, "Demi-God"]
      [1138, "Demi-God"]
    superhero(id, superhero_name, full_name, gender_id, eye_colour_id, hair_colour_id, skin_colour_id, race_id, publisher_id, alignment_id, height_cm, weight_kg)
      [1006, "c", null, 1003, 1002, 1002, 1002, 1005, 1004, 1001, 3, null]
      [1111, "c", "v1112", 1108, 1107, 1107, 1107, 1110, 1109, 1106, 3, null]
      [1118, "c", "v1119", 1115, 1114, 1114, 1114, 1117, 1116, 1113, 3, null]
      [1125, "c", "v1126", 1122, 1121, 1121, 1121, 1124, 1123, 1120, 3, null]
      [1132, "c", "v1133", 1129, 1128, 1128, 1128, 1131, 1130, 1127, 3, null]
      [1139, "c", "v1140", 1136, 1135, 1135, 1135, 1138, 1137, 1134, 3, null]
```
**gold 结果**：`[[null], ["v1112"], ["v1119"], ["v1126"], ["v1133"], ["v1140"]]`　**pred 结果**：`[[null], ["v1112"], ["v1119"], ["v1126"], ["v1133"]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：ambiguous（The question asks for at least five names; both returning all six (gold) and exactly five (pred) satisfy it.）<br>B：ambiguous（'At least five' is satisfied by both gold's six names and pred's five.）</details>

## 8. chess:637（codebase_community）

**问题**：State all the tags used by Mark Meckes in his posts that doesn't have comments.
**提示**：used by Mark Meckes refers to DisplayName = 'Mark Meckes'; Doen't have comments refers to CommentCount = 0;

**gold**：
```sql
SELECT T3.Tags FROM users AS T1 INNER JOIN postHistory AS T2 ON T1.Id = T2.UserId INNER JOIN posts AS T3 ON T3.Id = T2.PostId WHERE T1.DisplayName = 'Mark Meckes' AND T3.CommentCount = 0
```
**pred**：
```sql
SELECT DISTINCT T2.Tags FROM users AS T1 INNER JOIN posts AS T2 ON T1.Id = T2.OwnerUserId WHERE T1.DisplayName = 'Mark Meckes' AND T2.CommentCount = 0
```
**见证库**（每表的行，列序同 DDL）：
```
    postHistory(Id, PostHistoryTypeId, PostId, RevisionGUID, CreationDate, UserId, Text, Comment, UserDisplayName)
      [1013, 0, 1014, null, "2020-02-29 23:59:59", 1015, null, "x1", "A"]
    posts(Id, PostTypeId, AcceptedAnswerId, CreaionDate, Score, ViewCount, Body, OwnerUserId, LasActivityDate, Title, Tags, AnswerCount, CommentCount, FavoriteCount, LastEditorUserId, LastEditDate, CommunityOwnedDate, ParentId, ClosedDate, OwnerDisplayName, LastEditorDisplayName)
      [1002, null, null, "2010-06-15 12:30:00", null, null, null, 1003, null, "y2", "b", null, 0, null, 1003, "2015-03-20 08:00:00", null, null, null, null, "x1"]
      [1014, null, null, null, null, 0, "x1", 1015, null, null, null, null, 0, null, 1015, null, null, 1, null, null, null]
    users(Id, Reputation, CreationDate, DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, AccountId, Age, ProfileImageUrl)
      [1003, null, "2015-03-20 08:00:00", "Mark Meckes", null, "a", null, "y2", 1, null, 10, null, null, "b"]
      [1015, null, null, "Mark Meckes", "2000-01-01 00:00:00", "y2", "x1", null, 5, null, null, null, null, "A"]
```
**gold 结果**：`[[null]]`　**pred 结果**：`[["b"], [null]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（Mark Meckes owns post 1002 but has no postHistory row for it, while real posts always have creation history by their owner.）<br>B：gold_wrong（'His posts' means posts Mark Meckes owns; pred includes his owned post 1002, while gold only reaches posts through postHistory and misses it.）</details>

## 9. chess:789（superhero）

**问题**：Find the average weight of the heroes who are aliens.
**提示**：average = AVG(weight_kg); aliens refers to race = 'Alien';

**gold**：
```sql
SELECT CAST(SUM(T1.weight_kg) AS REAL) / COUNT(T1.id) FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T2.race = 'Alien'
```
**pred**：
```sql
SELECT AVG(T2.weight_kg) FROM race AS T1 INNER JOIN superhero AS T2 ON T1.id = T2.race_id WHERE T1.race = 'Alien'
```
**见证库**（每表的行，列序同 DDL）：
```
    alignment(id, alignment)
      [1001, "Bad"]
      [1073, "Bad"]
    colour(id, colour)
      [1002, null]
      [1074, null]
    gender(id, gender)
      [1003, "Female"]
      [1075, "a"]
    publisher(id, publisher_name)
      [1004, "Hanna-Barbera"]
      [1076, null]
    race(id, race)
      [1005, "Alien"]
      [1077, "Alien"]
    superhero(id, superhero_name, full_name, gender_id, eye_colour_id, hair_colour_id, skin_colour_id, race_id, publisher_id, alignment_id, height_cm, weight_kg)
      [1006, "c", null, 1003, 1002, 1002, 1002, 1005, 1004, 1001, 3, null]
      [1078, "c", null, 1075, 1074, 1074, 1074, 1077, 1076, 1073, 3, 1079]
```
**gold 结果**：`[[539.5]]`　**pred 结果**：`[[1079.0]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：gold_wrong（One alien has unknown (NULL) weight; average weight (evidence: AVG) should ignore it, while gold treats it as 0.）<br>B：gold_wrong（The average weight should ignore the alien with unknown (NULL) weight, giving 1079 (pred), whereas gold counts it as zero in SUM/COUNT.）</details>

## 10. chess:260（toxicology）

**问题**：Calculate the total atoms with triple-bond molecules containing the element phosphorus or bromine.
**提示**：triple bond refers to bond_type = '#'; phosphorus refers to element = 'p'; bromine refers to element = 'br'

**gold**：
```sql
SELECT COUNT(T1.atom_id) FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id INNER JOIN bond AS T3 ON T2.molecule_id = T3.molecule_id WHERE T3.bond_type = '#' AND T1.element IN ('p', 'br')
```
**pred**：
```sql
SELECT COUNT(DISTINCT T1.bond_id) FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id INNER JOIN atom AS T3 ON T2.atom_id = T3.atom_id WHERE T1.bond_type = '#' AND (T3.element = 'p' OR T3.element = 'br')
```
**见证库**（每表的行，列序同 DDL）：
```
    atom(atom_id, molecule_id, element)
      ["v1007", "v1008", "p"]
      ["v1055", "v1056", "br"]
    bond(bond_id, molecule_id, bond_type)
      ["v1009", "v1064", "#"]
      ["v1057", "v1056", "#"]
    connected(atom_id, atom_id2, bond_id)
      ["v1007", "v1007", "v1009"]
      ["v1055", "v1055", "v1057"]
    molecule(molecule_id, label)
      ["v1008", "-"]
      ["v1056", "-"]
      ["v1064", "+"]
```
**gold 结果**：`[[1]]`　**pred 结果**：`[[2]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（connected links atoms to triple bonds in different molecules via self-loop rows, inconsistent data that alone makes pred count 2.）<br>B：pred_wrong（The question asks for atoms in triple-bond molecules with P/Br; pred counts distinct bonds (one of them connected across molecules), while gold's count of 1 atom is right on this witness.）</details>

## 11. csc-7b:245（toxicology）

**问题**：What is the average number of bonds the atoms with the element iodine have?
**提示**：atoms with the element iodine refers to element = 'i'; average = DIVIDE(COUND(bond_id), COUNT(atom_id)) where element = 'i'

**gold**：
```sql
SELECT CAST(COUNT(T2.bond_id) AS REAL) / COUNT(T1.atom_id) FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id WHERE T1.element = 'i'
```
**pred**：
```sql
SELECT COUNT(*) / COUNT(DISTINCT T1.atom_id) AS average_bonds FROM connected AS T1 INNER JOIN atom AS T2 ON T1.atom_id = T2.atom_id WHERE T2.element = 'i'
```
**见证库**（每表的行，列序同 DDL）：
```
    atom(atom_id, molecule_id, element)
      ["v1001", "v1002", "i"]
      ["v1085", "v1086", "c"]
    bond(bond_id, molecule_id, bond_type)
      ["v1003", "v1084", "#"]
    connected(atom_id, atom_id2, bond_id)
      ["v1001", "v1001", "v1003"]
      ["v1001", "v1085", "v1003"]
    molecule(molecule_id, label)
      ["v1002", "+"]
      ["v1084", "+"]
      ["v1086", "+"]
```
**gold 结果**：`[[1.0]]`　**pred 结果**：`[[2]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（connected contains a self-loop row for the iodine atom plus duplicate same-bond rows, unrealistic data that alone makes pred count 2 bonds.）<br>B：implausible_data（The iodine atom's bond appears twice, including a self-connection (atom connected to itself), which real connected data never has, and this inflates pred's count.）</details>

## 12. alpha:1513（debit_card_specializing）

**问题**：Which country's gas station had the first paid cusomer in 2012/8/25?
**提示**：'2012/8/25' can be represented by '2012-08-25'

**gold**：
```sql
SELECT T2.Country FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T1.Date = '2012-08-25' ORDER BY T1.Time DESC LIMIT 1
```
**pred**：
```sql
SELECT gasstations.country FROM transactions_1k INNER JOIN gasstations ON transactions_1k.gasstationid = gasstations.gasstationid WHERE transactions_1k.date = '2012-08-25' ORDER BY transactions_1k.transactionid ASC LIMIT 1
```
**见证库**（每表的行，列序同 DDL）：
```
    gasstations(GasStationID, ChainID, Country, Segment)
      [1003, null, "CZE", "b"]
      [1017, 100, "SVK", "Discount"]
    transactions_1k(TransactionID, Date, Time, CustomerID, CardID, GasStationID, ProductID, Amount, Price)
      [1004, "2012-08-25", null, null, 10, 1003, null, null, null]
      [1018, "2012-08-25", "2000-01-01", null, null, 1017, 1, null, 10.0]
```
**gold 结果**：`[["SVK"]]`　**pred 结果**：`[["CZE"]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：gold_wrong（Gold orders by Time DESC and so picks the last customer rather than the first; pred picks the earliest transaction.）<br>B：implausible_data（One transaction has NULL time and NULL amount/price, so 'first paid' cannot be determined meaningfully; the divergence rests on this unrealistic row.）</details>

## 13. gena_submission_1:74（california_schools）

**问题**：What is the lowest grade for the District Special Education Consortia School with National Center for Educational Statistics school district identification number of 0613360?
**提示**：District Special Education Consortia School refers to EdOpsCode = 'SPECON'.

**gold**：
```sql
SELECT MIN(T1.`Low Grade`) FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.NCESDist = '0613360' AND T2.EdOpsCode = 'SPECON'
```
**pred**：
```sql
SELECT T1.`Low Grade` FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.NCESDist = '0613360' AND T2.EdOpsCode = 'SPECON' ORDER BY T1.`Low Grade` ASC LIMIT 1
```
**见证库**（每表的行，列序同 DDL）：
```
    frpm(CDSCode, Academic Year, County Code, District Code, School Code, County Name, District Name, School Name, District Type, School Type, Educational Option Type, NSLP Provision Status, Charter School (Y/N), Charter School Number, Charter Funding Type, IRC, Low Grade, High Grade, Enrollment (K-12), Free Meal Count (K-12), Percent (%) Eligible Free (K-12), FRPM Count (K-12), Percent (%) Eligible FRPM (K-12), Enrollment (Ages 5-17), Free Meal Count (Ages 5-17), Percent (%) Eligible Free (Ages 5-17), FRPM Count (Ages 5-17), Percent (%) Eligible FRPM (Ages 5-17), 2013-14 CALPADS Fall 1 Certification Status)
      ["v1016", "a", null, null, "a", null, null, null, "Elementary School District", "b", "A", "Provision 2", null, null, "Directly funded", null, "9", "Post Secondary", null, null, null, -1.5, 100.0, -1.5, null, null, 1.0, null, null]
    schools(CDSCode, NCESDist, NCESSchool, StatusType, County, District, School, Street, StreetAbr, City, Zip, State, MailStreet, MailStrAbr, MailCity, MailZip, MailState, Phone, Ext, Website, OpenDate, ClosedDate, Charter, CharterNum, FundingType, DOC, DOCType, SOC, SOCType, EdOpsCode, EdOpsName, EILCode, EILName, GSoffered, GSserved, Virtual, Magnet, Latitude, Longitude, AdmFName1, AdmLName1, AdmEmail1, AdmFName2, AdmLName2, AdmEmail2, AdmFName3, AdmLName3, AdmEmail3, LastUpdate)
      ["v1016", "a", null, "Merged", "A", "c", null, null, null, null, "b", null, "a", "A", null, null, "y2", null, null, "c", null, null, null, null, "Directly funded", "34", "State Special Schools", null, "County Community", "ROP", "Continuation School", "ELEMHIGH", "Ungraded", null, "y2", "F", null, null, -1.5, null, "y2", "a", null, null, null, null, null, null, "2000-01-01"]
```
**gold 结果**：`[[null]]`　**pred 结果**：`[]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：ambiguous（No school matches, so empty result (pred) and NULL MIN (gold) both mean no answer.）<br>B：ambiguous（No school matches the filter, so both results express 'no answer' (NULL MIN vs empty set).）</details>

## 14. gsr:801（superhero）

**问题**：Find the ratio between male superheroes and female superheroes.
**提示**：ratio = DIVIDE(SUM(gender_id = 1) / SUM(gender_id = 2)); male superheroes refers to gender = 'Female'; female superheroes refers to gender = 'Male';

**gold**：
```sql
SELECT CAST(COUNT(CASE WHEN T2.gender = 'Male' THEN T1.id ELSE NULL END) AS REAL) / COUNT(CASE WHEN T2.gender = 'Female' THEN T1.id ELSE NULL END) FROM superhero AS T1 INNER JOIN gender AS T2 ON T1.gender_id = T2.id
```
**pred**：
```sql
SELECT (SUM(CASE WHEN gender_id = 1 THEN 1 ELSE 0 END) * 1.0) / SUM(CASE WHEN gender_id = 2 THEN 1 ELSE 0 END) AS ratio FROM superhero;
```
**见证库**（每表的行，列序同 DDL）：
```
    alignment(id, alignment)
      [1011, "A"]
    colour(id, colour)
      [1012, null]
    gender(id, gender)
      [2, "Male"]
    publisher(id, publisher_name)
      [1013, "DC Comics"]
    race(id, race)
      [1014, null]
    superhero(id, superhero_name, full_name, gender_id, eye_colour_id, hair_colour_id, skin_colour_id, race_id, publisher_id, alignment_id, height_cm, weight_kg)
      [1015, null, "c", 2, 1012, 1012, 1012, 1014, 1013, 1011, null, null]
```
**gold 结果**：`[[null]]`　**pred 结果**：`[[0.0]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（gender id 2 is labelled Male, contrary to the real id mapping the evidence relies on; only this mismatch separates the queries.）<br>B：implausible_data（The witness maps gender id 2 to 'Male', contrary to the real database (and the evidence's id-based definition), and that alone causes the divergence.）</details>

## 15. omni-32-majority:273（toxicology）

**问题**：What is the percentage of element chlorine in carcinogenic molecules?
**提示**：chlorine refers to element = 'cl'; label = '+' mean molecules are carcinogenic; percentage = DIVIDE(SUM(element = 'pb'); COUNT(molecule_id)) as percentage where label = '+'

**gold**：
```sql
SELECT CAST(COUNT( CASE WHEN T1.element = 'cl' THEN T1.element ELSE NULL END) AS REAL) * 100 / COUNT(T1.element) FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '+'
```
**pred**：
```sql
SELECT CAST(SUM(CASE WHEN a.element = 'cl' THEN 1 ELSE 0 END) AS REAL) * 100.0 / COUNT(m.molecule_id) AS percentage FROM molecule m INNER JOIN atom a ON m.molecule_id = a.molecule_id WHERE m.label = '+';
```
**见证库**（每表的行，列序同 DDL）：
```
    atom(atom_id, molecule_id, element)
      ["v1424", "v1425", null]
    molecule(molecule_id, label)
      ["v1425", "+"]
```
**gold 结果**：`[[null]]`　**pred 结果**：`[[0.0]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（The only atom has a NULL element, unrealistic; gold divides by COUNT(element)=0.）<br>B：implausible_data（An atom with NULL element (never present in real data) makes COUNT(element) 0 for gold and produces NULL vs 0.0.）</details>

## 16. csc-32b:260（toxicology）

**问题**：Calculate the total atoms with triple-bond molecules containing the element phosphorus or bromine.
**提示**：triple bond refers to bond_type = '#'; phosphorus refers to element = 'p'; bromine refers to element = 'br'

**gold**：
```sql
SELECT COUNT(T1.atom_id) FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id INNER JOIN bond AS T3 ON T2.molecule_id = T3.molecule_id WHERE T3.bond_type = '#' AND T1.element IN ('p', 'br')
```
**pred**：
```sql
SELECT COUNT(DISTINCT a.atom_id) FROM atom a JOIN connected c ON a.atom_id = c.atom_id JOIN bond b ON c.bond_id = b.bond_id WHERE b.bond_type = '#' AND a.element IN ('p', 'br')
```
**见证库**（每表的行，列序同 DDL）：
```
    atom(atom_id, molecule_id, element)
      ["v1037", "v1038", "p"]
      ["v1001", "v1079", "p"]
    bond(bond_id, molecule_id, bond_type)
      ["v1003", "v1002", "#"]
      ["v1039", "v1080", "#"]
    connected(atom_id, atom_id2, bond_id)
      ["v1037", "v1037", "v1039"]
      ["v1001", "v1001", "v1003"]
    molecule(molecule_id, label)
      ["v1038", "+"]
      ["v1002", "-"]
      ["v1079", null]
      ["v1080", "+"]
```
**gold 结果**：`[[0]]`　**pred 结果**：`[[2]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（connected links atoms to triple bonds of other molecules through self-loops, inconsistent data that alone separates the counts.）<br>B：implausible_data（Atoms are connected to triple bonds that belong to other molecules, which is chemically and structurally impossible in real data, and this causes the divergence.）</details>

## 17. rsl:1495（debit_card_specializing）

**问题**：Which client ID consumed the most in September 2013?
**提示**：September 2013 refers to yearmonth.date = '201309'

**gold**：
```sql
SELECT T1.CustomerID FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE T2.Date = '201309' GROUP BY T1.CustomerID ORDER BY SUM(T2.Consumption) DESC LIMIT 1
```
**pred**：
```sql
SELECT `customerid` FROM `yearmonth` WHERE `date` = '201309' ORDER BY `consumption` DESC LIMIT 1
```
**见证库**（每表的行，列序同 DDL）：
```
    customers(CustomerID, Segment, Currency)
      [1002, null, "CZK"]
      [1012, "b", "CZK"]
    yearmonth(CustomerID, Date, Consumption)
      [1002, "201309", null]
      [1012, "201309", null]
```
**gold 结果**：`[[1012]]`　**pred 结果**：`[[1002]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（Both customers have NULL consumption, creating an artificial tie broken differently.）<br>B：implausible_data（Both September consumptions are NULL, so the customers tie and each query picks one arbitrarily; real yearmonth rows always carry consumption.）</details>

## 18. csc-7b:426（card_games）

**问题**：Please provide top three sets that don't appear in Magic: The Gathering Online, along with their names in in alphabetical order.
**提示**：don't appear in Magic: The Gathering Online refers to mtgoCode is NULL or mtgoCode = ''

**gold**：
```sql
SELECT name FROM sets WHERE mtgoCode IS NULL ORDER BY name LIMIT 3
```
**pred**：
```sql
SELECT name FROM sets WHERE mtgoCode IS NULL OR mtgoCode = '' ORDER BY name LIMIT 3
```
**见证库**（每表的行，列序同 DDL）：
```
    sets(id, baseSetSize, block, booster, code, isFoilOnly, isForeignOnly, isNonFoilOnly, isOnlineOnly, isPartialPreview, keyruneCode, mcmId, mcmIdExtras, mcmName, mtgoCode, name, parentCode, releaseDate, tcgplayerGroupId, totalSetSize, type)
      [1001, -1, null, "A", "c", 10, 0, 5, 2, 5, "x1", 3, null, null, "", "y2", null, null, null, null, "starter"]
```
**gold 结果**：`[]`　**pred 结果**：`[["y2"]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：gold_wrong（The evidence defines not in MTGO as mtgoCode IS NULL or empty string, and gold ignores the empty-string case.）<br>B：gold_wrong（The evidence defines 'not on MTGO' as mtgoCode NULL or '', and gold omits the empty-string case that pred includes.）</details>

## 19. csc-7b:1391（student_club）

**问题**：What is the ratio between students majored in finance and physics?
**提示**：DIVDE(SUM(major_name = 'Finance'), SUM(major_name = 'Physics'))

**gold**：
```sql
SELECT SUM(CASE WHEN major_name = 'Finance' THEN 1 ELSE 0 END) / SUM(CASE WHEN major_name = 'Physics' THEN 1 ELSE 0 END) AS ratio FROM major
```
**pred**：
```sql
SELECT CAST(SUM(CASE WHEN major_name = 'Finance' THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN major_name = 'Physics' THEN 1 ELSE 0 END) AS ratio FROM major
```
**见证库**（每表的行，列序同 DDL）：
```
    major(major_id, major_name, department, college)
      ["v1003", "Physics", null, "College of Engineering"]
      ["v1010", "Finance", "A", "College of the Arts"]
      ["v1032", "Physics", null, "School of Business"]
```
**gold 结果**：`[[0]]`　**pred 结果**：`[[0.5]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：gold_wrong（Gold integer division truncates the Finance/Physics ratio 1/2 to 0; the ratio is 0.5.）<br>B：gold_wrong（Gold uses integer division and returns 0 for 1/2, whereas the true ratio is 0.5 (pred).）</details>

## 20. csc-7b:107（financial）

**问题**：What is the gender of the oldest client who opened his/her account in the highest average salary branch?
**提示**：Earlier birthdate refers to older age; A11 refers to average salary

**gold**：
```sql
SELECT T2.gender FROM district AS T1 INNER JOIN client AS T2 ON T1.district_id = T2.district_id ORDER BY T1.A11 DESC, T2.birth_date ASC LIMIT 1
```
**pred**：
```sql
SELECT T1.gender FROM client AS T1 INNER JOIN account AS T2 ON T1.district_id = T2.district_id INNER JOIN district AS T3 ON T2.district_id = T3.district_id ORDER BY T1.birth_date ASC LIMIT 1
```
**见证库**（每表的行，列序同 DDL）：
```
    account(account_id, district_id, frequency, date)
      [1004, 1005, "POPLATEK TYDNE", "2000-01-01"]
      [1025, 1026, "POPLATEK PO OBRATU", "2000-01-01"]
    client(client_id, gender, birth_date, district_id)
      [1006, "M", "2015-03-20", 1005]
      [1027, "F", "2000-01-01", 1026]
    district(district_id, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16)
      [1005, "a", "west Bohemia", "b", "A", "c", "10", 5, 10, 0.0, 5, null, -1.5, 0, null, 3]
      [1026, "y2", "south Bohemia", "y2", "x1", "b", "1", -1, 100, 10.0, 2, null, 0.0, 5, null, 3]
```
**gold 结果**：`[["M"]]`　**pred 结果**：`[["F"]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：pred_wrong（Pred ignores the highest-average-salary (A11) condition and just returns the oldest client overall.）<br>B：pred_wrong（Pred ignores the highest-average-salary condition and returns the oldest client overall, whereas gold correctly restricts to the top-A11 district.）</details>

## 21. rsl:131（financial）

**问题**：Which district has highest active loan?
**提示**：A3 refers to district names; Active loan refers to running contracts; Status = 'C' stands for running contract, OK so far; Status = 'D' stands for running contract, client in debt

**gold**：
```sql
SELECT T2.A3 FROM account AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id INNER JOIN loan AS T3 ON T1.account_id = T3.account_id WHERE T3.status IN ('C', 'D') GROUP BY T2.A3 ORDER BY SUM(T3.amount) DESC LIMIT 1
```
**pred**：
```sql
SELECT `district`.`a3` FROM `loan` INNER JOIN `account` ON `loan`.`account_id` = `account`.`account_id` INNER JOIN `district` ON `account`.`district_id` = `district`.`district_id` WHERE `loan`.`status` IN ('C', 'D') GROUP BY `district`.`a3` ORDER BY COUNT(`loan`.`loan_id`) DESC LIMIT 1
```
**见证库**（每表的行，列序同 DDL）：
```
    account(account_id, district_id, frequency, date)
      [1093, 1094, "POPLATEK TYDNE", "2010-06-15"]
      [1099, 1100, "POPLATEK PO OBRATU", "2000-01-01"]
    district(district_id, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16)
      [1094, "y2", "south Moravia", "b", "c", "A", "18", 10, 1, 1.5, 1, 0.0, 100.0, 1, 2, 2]
      [1100, "y2", "south Bohemia", "y2", "A", "y2", "9", 3, -1, 100.0, 0, null, 0.0, 1, 1, 2]
    loan(loan_id, account_id, date, amount, duration, payments, status)
      [1095, 1093, "1995-12-31", 1, 1, 3.25, "C"]
      [1101, 1099, "2015-03-20", 3, 5, 3.25, "C"]
```
**gold 结果**：`[["south Bohemia"]]`　**pred 结果**：`[["south Moravia"]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：pred_wrong（Highest active loan most naturally means the largest loan amount (gold) and not the most loans; pred also breaks a count tie arbitrarily.）<br>B：pred_wrong（'Highest active loan' refers to loan amount; gold ranks districts by summed amount, while pred ranks by loan count and breaks a 1-1 tie arbitrarily.）</details>

## 22. gsr:1101（european_football_2）

**问题**：What is the average number of goals made by Parma as the away team while playing in Italy?
**提示**：Parma refers to team_long_name = 'Parma'; average number of goals refers to AVG(away_team_goal)

**gold**：
```sql
SELECT CAST(SUM(T1.away_team_goal) AS REAL) / COUNT(T1.id) FROM "Match" AS T1 INNER JOIN TEAM AS T2 ON T1.away_team_api_id = T2.team_api_id INNER JOIN Country AS T3 ON T1.country_id = T3.id WHERE T2.team_long_name = 'Parma' AND T3.name = 'Italy'
```
**pred**：
```sql
SELECT AVG(Match.away_team_goal) FROM Match JOIN Team ON Match.away_team_api_id = Team.team_api_id JOIN League ON Match.league_id = League.id JOIN Country ON League.country_id = Country.id WHERE Team.team_long_name = 'Parma' AND Country.name = 'Italy';
```
**见证库**（每表的行，列序同 DDL）：
```
    Country(id, name)
      [7725, "Italy"]
      [7733, "Italy"]
    League(id, country_id, name)
      [7726, 7725, "Portugal Liga ZON Sagres"]
      [7734, 7733, "Italy Serie A"]
    Match(id, country_id, league_id, season, stage, date, match_api_id, home_team_api_id, away_team_api_id, home_team_goal, away_team_goal, home_player_X1, home_player_X2, home_player_X3, home_player_X4, home_player_X5, home_player_X6, home_player_X7, home_player_X8, home_player_X9, home_player_X10, home_player_X11, away_player_X1, away_player_X2, away_player_X3, away_player_X4, away_player_X5, away_player_X6, away_player_X7, away_player_X8, away_player_X9, away_player_X10, away_player_X11, home_player_Y1, home_player_Y2, home_player_Y3, home_player_Y4, home_player_Y5, home_player_Y6, home_player_Y7, home_player_Y8, home_player_Y9, home_player_Y10, home_player_Y11, away_player_Y1, away_player_Y2, away_player_Y3, away_player_Y4, away_player_Y5, away_player_Y6, away_player_Y7, away_player_Y8, away_player_Y9, away_player_Y10, away_player_Y11, home_player_1, home_player_2, home_player_3, home_player_4, home_player_5, home_player_6, home_player_7, home_player_8, home_player_9, home_player_10, home_player_11, away_player_1, away_player_2, away_player_3, away_player_4, away_player_5, away_player_6, away_player_7, away_player_8, away_player_9, away_player_10, away_player_11, goal, shoton, shotoff, foulcommit, card, cross, corner, possession, B365H, B365D, B365A, BWH, BWD, BWA, IWH, IWD, IWA, LBH, LBD, LBA, PSH, PSD, PSA, WHH, WHD, WHA, SJH, SJD, SJA, VCH, VCD, VCA, GBH, GBD, GBA, BSH, BSD, BSA)
      [7727, 7725, 7726, "2012/2013", null, null, 3, 5, 5, null, 1, 2, null, 0, -1, null, 2, 5, 5, 2, 3, null, null, 10, null, null, null, null, null, null, null, null, null, null, null, 1, null, null, null, null, null, null, null, null, null, null, null, 10, null, 1, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 10, 1, -1, null, null, null, null, -1, null, null, null, null, null, null, null, null, null, null, null, 10.0, null, null, null, null, null, null, 0.0, null, 2.0, null, 3.25, null, null, null, 100.0, null, null, null, null, null, null, 0.0, null, null, null, 2.0, null, null]
      [7735, 7733, 7734, "2010/2011", null, null, null, 10, 10, null, null, null, null, 1, null, 1, 3, 0, null, 3, null, null, null, -1, null, null, 5, null, null, null, null, null, null, null, -1, null, null, null, null, null, null, null, null, null, 100, null, 0, 10, null, null, null, 2, null, null, null, 100, null, 2, null, 5, null, null, null, null, null, null, null, 2, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, -1.5, null, null, null, null, null, 10.0, null, null, null, null, null, null, null, 1.5, 1.5, null, null, null, null, 2.0, null, 10.0, null, 2.0, 3.25, null, null, 0.0, -1.5]
    Team(id, team_api_id, team_fifa_api_id, team_long_name, team_short_name)
      [7728, 5, 100, "Parma", null]
      [7736, 10, null, "Parma", null]
```
**gold 结果**：`[[0.5]]`　**pred 结果**：`[[1.0]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（A Parma away match with NULL away_team_goal is unrealistic; gold SUM/COUNT vs AVG differ only on it.）<br>B：implausible_data（The witness has two countries named Italy, duplicate Parma teams and a match whose country and league disagree, which is unrealistic and causes the divergence.）</details>

## 23. gsr:512（card_games）

**问题**：How many cards with unknown power that can't be found in foil is in duel deck A?
**提示**：unknown power refers to power IS NULL or power = '*'; can't be found in foil refers to hasFoil = 0; duel deck A refers to duelDeck = 'a'

**gold**：
```sql
SELECT SUM(CASE WHEN power = '*' OR power IS NULL THEN 1 ELSE 0 END) FROM cards WHERE hasFoil = 0 AND duelDeck = 'a'
```
**pred**：
```sql
SELECT COUNT(*) FROM cards WHERE (power IS NULL OR power = '*') AND hasFoil = 0 AND duelDeck = 'a';
```
**见证库**（每表的行，列序同 DDL）：
```
    cards(id, artist, asciiName, availability, borderColor, cardKingdomFoilId, cardKingdomId, colorIdentity, colorIndicator, colors, convertedManaCost, duelDeck, edhrecRank, faceConvertedManaCost, faceName, flavorName, flavorText, frameEffects, frameVersion, hand, hasAlternativeDeckLimit, hasContentWarning, hasFoil, hasNonFoil, isAlternative, isFullArt, isOnlineOnly, isOversized, isPromo, isReprint, isReserved, isStarter, isStorySpotlight, isTextless, isTimeshifted, keywords, layout, leadershipSkills, life, loyalty, manaCost, mcmId, mcmMetaId, mtgArenaId, mtgjsonV4Id, mtgoFoilId, mtgoId, multiverseId, name, number, originalReleaseDate, originalText, originalType, otherFaceIds, power, printings, promoTypes, purchaseUrls, rarity, scryfallId, scryfallIllustrationId, scryfallOracleId, setCode, side, subtypes, supertypes, tcgplayerProductId, text, toughness, type, types, uuid, variations, watermark)
      [1016, null, "c", "a", "borderless", null, null, null, "B,G", null, null, "a", 1, null, null, "Godzilla, Doom Inevitable", null, null, "1997", "-1", 1, 2, -1, 0, -1, 100, -1, 0, 1, 1, 5, 5, 100, 5, -1, "a", "split", "{'brawl': False, 'commander': True, 'oathbreaker': True}", "-5", "4", null, "y2", null, null, "c", null, null, null, null, null, null, null, null, null, "2", null, null, null, "mythic", null, null, null, null, "e", null, "Snow", null, null, "c", "y2", "a", "b", null, null]
```
**gold 结果**：`[[null]]`　**pred 结果**：`[[0]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：gold_wrong（No cards match, so the count is 0; gold SUM over no rows returns NULL.）<br>B：gold_wrong（No card matches, so the count should be 0 (pred), but gold's SUM over an empty set returns NULL.）</details>

## 24. gsr:98（financial）

**问题**：Among the accounts who have approved loan date in 1997, list out the accounts that have the lowest approved amount and choose weekly issuance statement.
**提示**：'POPLATEK TYDNE' stands for weekly issuance

**gold**：
```sql
SELECT T2.account_id FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id WHERE STRFTIME('%Y', T1.date) = '1997' AND T2.frequency = 'POPLATEK TYDNE' ORDER BY T1.amount LIMIT 1
```
**pred**：
```sql
SELECT account.account_id FROM account JOIN loan ON account.account_id = loan.account_id WHERE strftime('%Y', loan.date) = '1997' AND account.frequency = 'POPLATEK TYDNE' AND loan.amount = (SELECT MIN(loan.amount) FROM loan JOIN account ON account.account_id = loan.account_id WHERE strftime('%Y', loan.date) = '1997' AND account.frequency = 'POPLATEK TYDNE');
```
**见证库**（每表的行，列序同 DDL）：
```
    account(account_id, district_id, frequency, date)
      [1001, 1002, "POPLATEK TYDNE", "1995-12-31"]
      [1010, 1011, "POPLATEK TYDNE", "1995-12-31"]
    district(district_id, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16)
      [1002, "y2", "north Moravia", "y2", "x1", "x1", "0", 100, 100, -1.5, 2, 1.5, -1.5, -1, null, 1]
      [1011, "y2", "central Bohemia", "x1", "c", "b", "10", 1, 100, 2.0, 3, null, 10.0, 3, null, 1]
    loan(loan_id, account_id, date, amount, duration, payments, status)
      [1003, 1001, "1997-01-01", 1, -1, 1.0, "D"]
      [1012, 1010, "1997-01-01", 1, -1, 1.0, "D"]
```
**gold 结果**：`[[1001]]`　**pred 结果**：`[[1001], [1010]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：gold_wrong（The question asks for accounts (plural) with the lowest amount, and two tie; gold LIMIT 1 drops one.）<br>B：gold_wrong（The question asks to 'list out the accounts' with the lowest amount, and both accounts tie, so pred's list of both is right while gold's LIMIT 1 drops one.）</details>

## 25. csc-7b:1013（formula_1）

**问题**：What is the lap record for the Austrian Grand Prix Circuit?
**提示**：lap record means the fastest time recorded which refers to time

**gold**：
```sql
WITH fastest_lap_times AS ( SELECT T1.raceId, T1.fastestLapTime FROM results AS T1 WHERE T1.FastestLapTime IS NOT NULL) SELECT MIN(fastest_lap_times.fastestLapTime) as lap_record FROM fastest_lap_times INNER JOIN races AS T2 on fastest_lap_times.raceId = T2.raceId INNER JOIN circuits AS T3 on T2.circuitId = T3.circuitId WHERE T2.name = 'Austrian Grand Prix'
```
**pred**：
```sql
SELECT T1.time FROM lapTimes AS T1 JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T2.name = 'Austrian Grand Prix' ORDER BY T1.milliseconds ASC LIMIT 1
```
**见证库**（每表的行，列序同 DDL）：
```
    circuits(circuitId, circuitRef, name, location, country, lat, lng, alt, url)
      [1009, "y2", "c", null, null, null, null, 0, "c"]
    constructors(constructorId, constructorRef, name, nationality, url)
      [1010, "c", "A", "c", "y2"]
    drivers(driverId, driverRef, number, code, forename, surname, dob, nationality, url)
      [1011, "y2", null, null, "b", "c", null, null, "y2"]
    lapTimes(raceId, driverId, lap, position, time, milliseconds)
      [1012, 1011, 1013, null, null, 2]
    races(raceId, year, round, circuitId, name, date, time, url)
      [1012, 1014, 1, 1009, "Austrian Grand Prix", "2010-06-15", null, null]
    results(resultId, raceId, driverId, constructorId, number, grid, position, positionText, positionOrder, points, laps, time, milliseconds, fastestLap, rank, fastestLapTime, fastestLapSpeed, statusId)
      [1015, 1012, 1011, 1010, null, 1, null, "c", 2, 10.0, 1, null, null, null, 0, "2000-01-01", null, 1016]
    seasons(year, url)
      [1014, "A"]
    status(statusId, status)
      [1016, "x1"]
```
**gold 结果**：`[["2000-01-01"]]`　**pred 结果**：`[[null]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（fastestLapTime stored as a date string and lapTimes with NULL time are corrupted values that decide the difference.）<br>B：implausible_data（The lap record data is malformed (lapTimes time NULL with milliseconds 2, fastestLapTime '2000-01-01'), so neither value is meaningful and the divergence rests on unrealistic rows.）</details>

## 26. rsl:695（codebase_community）

**问题**：How many users were awarded with 'Citizen Patrol' badge?
**提示**：Citizen Patrol' is the name of the badge;

**gold**：
```sql
SELECT COUNT(id) FROM badges WHERE `Name` = 'Citizen Patrol'
```
**pred**：
```sql
SELECT COUNT(DISTINCT `badges`.`userid`) FROM `badges` WHERE `badges`.`name` = 'Citizen Patrol'
```
**见证库**（每表的行，列序同 DDL）：
```
    badges(Id, UserId, Name, Date)
      [1001, 1002, "Citizen Patrol", "2020-02-29 23:59:59"]
      [1033, 1002, "Citizen Patrol", "2020-02-29 23:59:59"]
    users(Id, Reputation, CreationDate, DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, AccountId, Age, ProfileImageUrl)
      [1002, null, null, null, null, null, "x1", null, null, null, null, null, 3, null]
```
**gold 结果**：`[[2]]`　**pred 结果**：`[[1]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（The same user holds Citizen Patrol twice, but it is a one-time badge in reality; otherwise both count 1.）<br>B：implausible_data（The same user has two 'Citizen Patrol' badges, a one-time badge in reality, and only this duplication separates badge count from user count.）</details>

## 27. gena_submission_2:75（california_schools）

**问题**：What is the educational level name for the schools with Breakfast Provision 2 in county code 37? Indicate the name of the school.
**提示**：

**gold**：
```sql
SELECT T2.EILName, T2.School FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`NSLP Provision Status` = 'Breakfast Provision 2' AND T1.`County Code` = 37
```
**pred**：
```sql
SELECT T1.EILName, T2."School Name" 
FROM schools AS T1 
INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode 
WHERE T2."County Code" = '37' AND T2."NSLP Provision Status" = 'Breakfast Provision 2';
```
**见证库**（每表的行，列序同 DDL）：
```
    frpm(CDSCode, Academic Year, County Code, District Code, School Code, County Name, District Name, School Name, District Type, School Type, Educational Option Type, NSLP Provision Status, Charter School (Y/N), Charter School Number, Charter Funding Type, IRC, Low Grade, High Grade, Enrollment (K-12), Free Meal Count (K-12), Percent (%) Eligible Free (K-12), FRPM Count (K-12), Percent (%) Eligible FRPM (K-12), Enrollment (Ages 5-17), Free Meal Count (Ages 5-17), Percent (%) Eligible Free (Ages 5-17), FRPM Count (Ages 5-17), Percent (%) Eligible FRPM (Ages 5-17), 2013-14 CALPADS Fall 1 Certification Status)
      ["v1001", "A", "37", null, "A", null, null, null, "Elementary School District", "County Community", "Juvenile Court School", "Breakfast Provision 2", null, null, "Not in CS funding model", 3, "9", "8", null, null, null, null, null, null, null, null, null, null, 1]
      ["v1013", "A", "37", null, "A", null, null, "v1014", "Elementary School District", "County Community", "Juvenile Court School", "Breakfast Provision 2", null, null, "Locally funded", 3, "9", "12", null, null, null, null, null, null, null, null, null, null, 1]
    schools(CDSCode, NCESDist, NCESSchool, StatusType, County, District, School, Street, StreetAbr, City, Zip, State, MailStreet, MailStrAbr, MailCity, MailZip, MailState, Phone, Ext, Website, OpenDate, ClosedDate, Charter, CharterNum, FundingType, DOC, DOCType, SOC, SOCType, EdOpsCode, EdOpsName, EILCode, EILName, GSoffered, GSserved, Virtual, Magnet, Latitude, Longitude, AdmFName1, AdmLName1, AdmEmail1, AdmFName2, AdmLName2, AdmEmail2, AdmFName3, AdmLName3, AdmEmail3, LastUpdate)
      ["v1001", null, "y2", "Active", "x1", "c", null, null, "b", "b", null, "x1", null, null, null, null, "a", null, null, null, null, "2010-06-15", 5, null, "Locally funded", "42", "Joint Powers Authority (JPA)", "70", "Juvenile Court Schools", "JUV", "County Community School", "a", "High School", "x1", null, "P", null, 0.0, -1.5, null, null, null, "c", null, null, null, null, "b", "2015-03-20"]
      ["v1013", null, "y2", "Pending", "x1", "c", "v1015", null, "b", "b", null, "x1", null, null, null, null, "a", null, null, null, null, "2010-06-15", 5, null, "Locally funded", "42", "Joint Powers Authority (JPA)", "08", "Juvenile Court Schools", "JUV", "County Community School", "a", "Adult", "x1", null, "P", null, 0.0, -1.5, null, null, null, "c", null, null, null, null, "b", "2015-03-20"]
```
**gold 结果**：`[["High School", null], ["Adult", "v1015"]]`　**pred 结果**：`[["High School", null], ["Adult", "v1014"]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（School name differs between schools.School and frpm School Name for the same CDSCode, inconsistent with real denormalized data.）<br>B：implausible_data（frpm and schools hold different school names for the same CDSCode, an inconsistency that alone decides which name is output.）</details>

## 28. omni-32-majority:112（financial）

**问题**：For the female client who was born in 1976/1/29, which district did she opened her account?
**提示**：Female refers to gender = 'F'; A2 refers to district names

**gold**：
```sql
SELECT T1.A2 FROM district AS T1 INNER JOIN client AS T2 ON T1.district_id = T2.district_id WHERE T2.birth_date = '1976-01-29' AND T2.gender = 'F'
```
**pred**：
```sql
SELECT district.A2 FROM district INNER JOIN account ON district.district_id = account.district_id INNER JOIN client ON district.district_id = client.district_id WHERE client.gender = 'F' AND client.birth_date = '1976-01-29';
```
**见证库**（每表的行，列序同 DDL）：
```
    account(account_id, district_id, frequency, date)
      [1037, 1038, "POPLATEK PO OBRATU", "2020-02-29"]
    client(client_id, gender, birth_date, district_id)
      [1003, "F", "1976-01-29", 1002]
      [1039, "F", "1976-01-29", 1038]
    district(district_id, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, A16)
      [1002, "c", "c", "b", "c", "a", "7", 3, 2, 10.0, 2, null, 0.0, 100, null, 1]
      [1038, "v1040", "c", "b", "c", "a", "7", 3, 2, 10.0, 2, null, 0.0, 100, null, 1]
      [1059, "c", "central Bohemia", "c", "A", "x1", "7", -1, 2, 10.0, 3, 1.0, 0.0, 100, -1, 2]
```
**gold 结果**：`[["c"], ["v1040"]]`　**pred 结果**：`[["v1040"]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（A client whose district has no accounts at all (and no dispositions) is unrealistic; only this makes pred district-level account join exclude her.）<br>B：implausible_data（The witness has clients but no disp rows, so no client can be linked to an account; the divergence comes from this unrealistic missing link.）</details>

## 29. alpha:1015（formula_1）

**问题**：In which Formula_1 race was the lap record for the Austrian Grand Prix Circuit set?
**提示**：lap record means the fastest time recorded which refers to time

**gold**：
```sql
WITH fastest_lap_times AS ( SELECT T1.raceId, T1.FastestLapTime, (CAST(SUBSTR(T1.FastestLapTime, 1, INSTR(T1.FastestLapTime, ':') - 1) AS REAL) * 60) + (CAST(SUBSTR(T1.FastestLapTime, INSTR(T1.FastestLapTime, ':') + 1, INSTR(T1.FastestLapTime, '.') - INSTR(T1.FastestLapTime, ':') - 1) AS REAL)) + (CAST(SUBSTR(T1.FastestLapTime, INSTR(T1.FastestLapTime, '.') + 1) AS REAL) / 1000) as time_in_seconds FROM results AS T1 WHERE T1.FastestLapTime IS NOT NULL ) SELECT T2.name FROM races AS T2 INNER JOIN circuits AS T3 on T2.circuitId = T3.circuitId INNER JOIN results AS T1 on T2.raceId = T1.raceId INNER JOIN ( SELECT MIN(fastest_lap_times.time_in_seconds) as min_time_in_seconds FROM fastest_lap_times INNER JOIN races AS T2 on fastest_lap_times.raceId = T2.raceId INNER JOIN circuits AS T3 on T2.circuitId = T3.circuitId WHERE T2.name = 'Austrian Grand Prix') AS T4 ON (CAST(SUBSTR(T1.FastestLapTime, 1, INSTR(T1.FastestLapTime, ':') - 1) AS REAL) * 60) + (CAST(SUBSTR(T1.FastestLapTime, INSTR(T1.FastestLapTime, ':') + 1, INSTR(T1.FastestLapTime, '.') - INSTR(T1.FastestLapTime, ':') - 1) AS REAL)) + (CAST(SUBSTR(T1.FastestLapTime, INSTR(T1.FastestLapTime, '.') + 1) AS REAL) / 1000) = T4.min_time_in_seconds WHERE T2.name = 'Austrian Grand Prix'
```
**pred**：
```sql
SELECT r.name FROM races AS r INNER JOIN laptimes AS l ON r.raceid = l.raceid WHERE r.name = 'Austrian Grand Prix' ORDER BY l.milliseconds ASC LIMIT 1
```
**见证库**（每表的行，列序同 DDL）：
```
    circuits(circuitId, circuitRef, name, location, country, lat, lng, alt, url)
      [1017, "y2", "y2", null, null, null, 10.0, null, "x1"]
    constructors(constructorId, constructorRef, name, nationality, url)
      [1018, "a", "c", "a", "y2"]
    drivers(driverId, driverRef, number, code, forename, surname, dob, nationality, url)
      [1019, "y2", null, null, "b", "A", null, null, "a"]
    lapTimes(raceId, driverId, lap, position, time, milliseconds)
      [1020, 1019, 1021, null, null, null]
    races(raceId, year, round, circuitId, name, date, time, url)
      [1020, 1022, 1, 1017, "Austrian Grand Prix", "2000-01-01", "07:00:00", null]
    results(resultId, raceId, driverId, constructorId, number, grid, position, positionText, positionOrder, points, laps, time, milliseconds, fastestLap, rank, fastestLapTime, fastestLapSpeed, statusId)
      [1023, 1020, 1019, 1018, 1, 100, null, "a", -1, 2.0, 3, "2012-02-22 00:00:00", -1, null, null, null, null, 1024]
    seasons(year, url)
      [1022, "b"]
    status(statusId, status)
      [1024, "y2"]
```
**gold 结果**：`[]`　**pred 结果**：`[["Austrian Grand Prix"]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（The lapTimes row has NULL milliseconds and results has a corrupted fastestLapTime, unrealistic values that decide the difference.）<br>B：implausible_data（The only lapTimes row has NULL milliseconds and time (never present in real data), so pred's ordering returns a race without any recorded lap time.）</details>

## 30. gena_submission_1:1057（european_football_2）

**问题**：Calculate the average home team goal in the 2010/2011 season in the country of Poland.
**提示**：average home team goal = AVG(home_team_goal)= SUM(home_team_goal) / COUNT(DISTINCT Match.id) WHERE name = 'Poland' and season = '2010/2011';

**gold**：
```sql
SELECT CAST(SUM(t2.home_team_goal) AS REAL) / COUNT(t2.id) FROM Country AS t1 INNER JOIN Match AS t2 ON t1.id = t2.country_id WHERE t1.name = 'Poland' AND t2.season = '2010/2011'
```
**pred**：
```sql
SELECT AVG(T1.home_team_goal) FROM Match AS T1 INNER JOIN Country AS T2 ON T1.country_id = T2.id WHERE T2.name = 'Poland' AND T1.season = '2010/2011'
```
**见证库**（每表的行，列序同 DDL）：
```
    Country(id, name)
      [1001, "Poland"]
      [1013, "Poland"]
    Match(id, country_id, league_id, season, stage, date, match_api_id, home_team_api_id, away_team_api_id, home_team_goal, away_team_goal, home_player_X1, home_player_X2, home_player_X3, home_player_X4, home_player_X5, home_player_X6, home_player_X7, home_player_X8, home_player_X9, home_player_X10, home_player_X11, away_player_X1, away_player_X2, away_player_X3, away_player_X4, away_player_X5, away_player_X6, away_player_X7, away_player_X8, away_player_X9, away_player_X10, away_player_X11, home_player_Y1, home_player_Y2, home_player_Y3, home_player_Y4, home_player_Y5, home_player_Y6, home_player_Y7, home_player_Y8, home_player_Y9, home_player_Y10, home_player_Y11, away_player_Y1, away_player_Y2, away_player_Y3, away_player_Y4, away_player_Y5, away_player_Y6, away_player_Y7, away_player_Y8, away_player_Y9, away_player_Y10, away_player_Y11, home_player_1, home_player_2, home_player_3, home_player_4, home_player_5, home_player_6, home_player_7, home_player_8, home_player_9, home_player_10, home_player_11, away_player_1, away_player_2, away_player_3, away_player_4, away_player_5, away_player_6, away_player_7, away_player_8, away_player_9, away_player_10, away_player_11, goal, shoton, shotoff, foulcommit, card, cross, corner, possession, B365H, B365D, B365A, BWH, BWD, BWA, IWH, IWD, IWA, LBH, LBD, LBA, PSH, PSD, PSA, WHH, WHD, WHA, SJH, SJD, SJA, VCH, VCD, VCA, GBH, GBD, GBA, BSH, BSD, BSA)
      [1002, 1001, -1, "2010/2011", null, "2012-02-22 00:00:00", null, null, null, null, null, 3, null, null, null, null, 3, null, null, 10, null, null, null, null, 100, null, null, null, 1, null, 1, null, 10, null, null, 0, 0, null, 100, null, 100, null, null, null, null, 0, 5, null, null, null, null, null, null, null, null, null, null, null, null, 1, -1, 5, null, null, null, null, -1, null, null, null, 10, null, null, null, null, 0, null, null, null, null, null, null, null, null, "b", null, null, 2.0, null, null, null, null, null, null, 1.0, null, null, 2.0, null, null, null, null, null, null, 2.0, null, null, null, null, null, null, null, 0.0, null, 100.0]
      [1014, 1013, null, "2010/2011", null, null, null, null, null, 3, null, null, 5, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 3, null, null, null, null, null, null, null, null, null, null, -1, null, -1, null, null, null, null, null, null, 1, 100, null, 1, -1, null, 2, 3, -1, -1, null, null, null, null, 2, null, null, null, null, null, null, null, 2, null, 2, 3, null, 10, null, null, "a", null, null, null, "x1", "a", "y2", null, null, null, null, null, 1.5, null, null, null, null, null, null, null, null, null, null, null, 3.25, null, 1.5, null, null, null, null, null, null, null, null, null, null]
```
**gold 结果**：`[[1.5]]`　**pred 结果**：`[[3.0]]`

你的判定：＿＿＿＿＿＿　备注：＿＿＿＿＿＿

<details><summary>AI 判定（先别看）</summary>A：implausible_data（A Polish match with NULL home_team_goal is unrealistic; gold SUM/COUNT vs AVG differ only on it.）<br>B：implausible_data（A match with NULL home_team_goal (never present in real data) makes gold's SUM/COUNT differ from AVG.）</details>
