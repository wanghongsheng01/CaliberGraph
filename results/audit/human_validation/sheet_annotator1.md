# Human attribution sheet (blind)

For each item, read the question, evidence, both queries, the witness database and the two results, then replace `____` after **Verdict:** with exactly one of: `pred_wrong`, `gold_wrong`, `both_wrong`, `ambiguous`, `implausible_data`. See INSTRUCTIONS.md. Do not consult any other file of the repository while annotating.


---

## Item 1 (codebase_community)

**Question:** State all the tags used by Mark Meckes in his posts that doesn't have comments.

**Evidence:** used by Mark Meckes refers to DisplayName = 'Mark Meckes'; Doen't have comments refers to CommentCount = 0;

**Gold SQL:**
```sql
SELECT T3.Tags FROM users AS T1 INNER JOIN postHistory AS T2 ON T1.Id = T2.UserId INNER JOIN posts AS T3 ON T3.Id = T2.PostId WHERE T1.DisplayName = 'Mark Meckes' AND T3.CommentCount = 0
```
**Predicted SQL:**
```sql
SELECT DISTINCT Tags FROM posts JOIN users ON posts.OwnerUserId = users.Id WHERE users.DisplayName = 'Mark Meckes' AND posts.CommentCount = 0
```

**Witness database:**

*postHistory* (7 unreferenced columns omitted)

| PostId | UserId |
|---|---|
| 1014 | 1015 |

*posts* (17 unreferenced columns omitted)

| Id | OwnerUserId | Tags | CommentCount |
|---|---|---|---|
| 1002 | 1003 | b | 0 |
| 1014 | 1015 | NULL | 0 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 1003 | Mark Meckes |
| 1015 | Mark Meckes |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[['b'], [None]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** Predicted joins posts.OwnerUserId=users, including Mark Meckes' own post 1002 tagged 'b' (CommentCount 0), whereas Gold routes through postHistory.UserId and only returns post 1014's NULL tags, missing post 1002.


---

## Item 2 (superhero)

**Question:** Find the average weight of the heroes who are aliens.

**Evidence:** average = AVG(weight_kg); aliens refers to race = 'Alien';

**Gold SQL:**
```sql
SELECT CAST(SUM(T1.weight_kg) AS REAL) / COUNT(T1.id) FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T2.race = 'Alien'
```
**Predicted SQL:**
```sql
SELECT AVG(superhero.weight_kg) AS average_weight FROM superhero INNER JOIN race ON superhero.race_id = race.id WHERE race.race = 'Alien';
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 2 | Bad |
| 1 | Good |
| 3 | Good |

*colour*

| id | colour |
|---|---|
| 1 | Alien |
| 2 | Alien |
| 3 | Alien |

*gender*

| id | gender |
|---|---|
| 1 | NULL |
| 2 | Male |

*publisher*

| id | publisher_name |
|---|---|
| 2 | HarperCollins |
| 1 | George Lucas |
| 3 | HarperCollins |

*race*

| id | race |
|---|---|
| 1 | Alien |
| 3 | Alien |
| 2 | x1 |

*superhero* (9 unreferenced columns omitted)

| id | race_id | weight_kg |
|---|---|---|
| 2 | 3 | 100 |
| 3 | 2 | 10 |
| 1 | 1 | NULL |

**Gold result on the witness:** `[[50.0]]`  
**Predicted result on the witness:** `[[100.0]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** AVG(weight_kg) ignores the NULL-weight alien hero and yields 100, while Gold divides the summed weight by the full alien count (2) to get 50, wrongly treating the unknown-weight hero as zero.


---

## Item 3 (codebase_community)

**Question:** Identify the total views on the post 'Computer Game Datasets'. Name the user who posted it last time.

**Evidence:** total views refer to ViewCount; Name the user refers to DisplayName; post 'Computer Game Datasets' refers to Text = 'Computer Game Datasets';

**Gold SQL:**
```sql
SELECT T2.ViewCount, T3.DisplayName FROM postHistory AS T1 INNER JOIN posts AS T2 ON T1.PostId = T2.Id INNER JOIN users AS T3 ON T2.LastEditorUserId = T3.Id WHERE T1.Text = 'Computer Game Datasets'
```
**Predicted SQL:**
```sql
SELECT T1.ViewCount, T2.DisplayName FROM posts AS T1 JOIN users AS T2 ON T1.LastEditorUserId = T2.Id WHERE T1.Title = 'Computer game datasets'
```

**Witness database:**

*postHistory* (7 unreferenced columns omitted)

| PostId | Text |
|---|---|
| 1 | <pca> |
| 2 | Computer Game Datasets |
| 1 | {"Voters":[{"Id":-1,"DisplayName":"Community"}]} |
| 3 | What are the most valuable Statistical Analysis open source  |

*posts* (17 unreferenced columns omitted)

| Id | ViewCount | Title | LastEditorUserId |
|---|---|---|---|
| 3 | 28 | NULL | 1 |
| 1 | 18 | Computer Game Datasets | 3 |
| 2 | 27 | Maximum number of independent variables that can be entered  | 2 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 1 | Computer Game Datasets |
| 2 | Computer game datasets |
| 3 | Jarrod Dixon |
| 18 | grokus |

**Gold result on the witness:** `[[27, 'Computer game datasets']]`  
**Predicted result on the witness:** `[]`

**Verdict:** pred_wrong  
**Reason (one sentence):** Evidence identifies the post via postHistory.Text='Computer Game Datasets' (post 2, views 27), but Predicted filters posts.Title with a case-sensitive literal 'Computer game datasets' that matches nothing, returning empty.


---

## Item 4 (codebase_community)

**Question:** What is the display name of the user who has obtained the most number of badges?

**Evidence:** who obtained the most number of badges refers to UserID with Max(Count(Id))

**Gold SQL:**
```sql
SELECT T2.DisplayName FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id GROUP BY T2.DisplayName ORDER BY COUNT(T1.Id) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T2.DisplayName FROM badges AS T1 JOIN users AS T2 ON T1.UserId = T2.Id GROUP BY T1.UserId ORDER BY COUNT(T1.Id) DESC LIMIT 1
```

**Witness database:**

*badges* (2 unreferenced columns omitted)

| Id | UserId |
|---|---|
| 13353 | 4673 |
| 81335 | 48030 |
| 73258 | 44011 |
| 6230 | 3443 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 45466 | freddyfree |
| 13979 | Julian |
| 37654 | Just A Name |
| 4673 | user4673 |
| 48030 | NassibBueno |
| 44011 | user2448064 |
| 3443 | Matt Munson |

**Gold result on the witness:** `[['user4673']]`  
**Predicted result on the witness:** `[['NassibBueno']]`

**Verdict:** ambiguous  
**Reason (one sentence):** All four badge recipients have exactly one badge, a four-way tie for the maximum, so Gold's user4673 and Predicted's NassibBueno are both arbitrary LIMIT-1 picks with no specified tie-breaker.


---

## Item 5 (superhero)

**Question:** How many superheroes have a neutral alignment?

**Evidence:** neutral alignment refers to alignment_id = 3;

**Gold SQL:**
```sql
SELECT COUNT(T1.id) FROM superhero AS T1 INNER JOIN alignment AS T2 ON T1.alignment_id = T2.id WHERE T2.alignment = 'Neutral'
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM `superhero` WHERE `alignment_id` = 3
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 3 | Bad |

*attribute*

| id | attribute_name |
|---|---|
| 1 | Durability |

*colour*

| id | colour |
|---|---|
| 1 | 2147483648 |

*gender*

| id | gender |
|---|---|
| 1 | Female |

*publisher*

| id | publisher_name |
|---|---|
| 1 | 2147483648 |

*race*

| id | race |
|---|---|
| 1 | 2147483648 |

*superhero* (10 unreferenced columns omitted)

| id | alignment_id |
|---|---|
| 1 | 3 |

*hero_attribute*

| hero_id | attribute_id | attribute_value |
|---|---|---|
| 1 | 1 | 0 |

*superpower*

| id | power_name |
|---|---|
| 1 | 2147483648 |

*hero_power*

| hero_id | power_id |
|---|---|
| 1 | 1 |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The evidence defines a neutral alignment as alignment_id=3 and the only superhero has alignment_id=3, so the count is 1; Gold instead filters the literal label 'Neutral' (witness id3 stored as 'Bad') and wrongly returns 0.


---

## Item 6 (codebase_community)

**Question:** What is the name of tags used by John Salvatier's?

**Evidence:** DisplayName = 'John Salvatier';

**Gold SQL:**
```sql
SELECT T3.Tags FROM users AS T1 INNER JOIN postHistory AS T2 ON T1.Id = T2.UserId INNER JOIN posts AS T3 ON T2.PostId = T3.Id WHERE T1.DisplayName = 'John Salvatier'
```
**Predicted SQL:**
```sql
SELECT DISTINCT posts.tags FROM posts INNER JOIN users ON posts.owneruserid = users.id WHERE users.displayname = 'John Salvatier'
```

**Witness database:**

*postHistory* (7 unreferenced columns omitted)

| PostId | UserId |
|---|---|
| 2 | 3 |
| 2 | 2 |
| 1 | 3 |
| 3 | 3 |

*posts* (18 unreferenced columns omitted)

| Id | OwnerUserId | Tags |
|---|---|---|
| 1 | 3 | <neural-networks> |
| 3 | 1 | <statistical-significance> |
| 2 | 24 | <distributions><normality> |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 3 | John Salvatier |
| 2 | Geoff Dalgas |
| 24 | A Lion |
| 88 | mbq |
| 8 | csgillespie |
| 1 | Will |

**Gold result on the witness:** `[['<distributions><normality>'], ['<neural-networks>'], ['<statistical-significance>']]`  
**Predicted result on the witness:** `[['<neural-networks>']]`

**Verdict:** gold_wrong  
**Reason (one sentence):** Predicted takes tags on posts John Salvatier owns (only post 1), while Gold joins via postHistory and also returns tags of posts John merely edited but owned by other users (posts 2 and 3).


---

## Item 7 (toxicology)

**Question:** Name the atoms' elements that form bond TR000_2_3.

**Evidence:** element = 'cl' means Chlorine; element = 'c' means Carbon; element = 'h' means Hydrogen; element = 'o' means Oxygen, element = 's' means Sulfur; element = 'n' means Nitrogen, element = 'p' means Phosphorus, element = 'na' means Sodium, element = 'br' means Bromine, element = 'f' means Fluorine; element = 'i' means Iodine; element = 'sn' means Tin; element = 'pb' means Lead; element = 'te' means Tellurium; element = 'ca' means Calcium

**Gold SQL:**
```sql
SELECT T2.element FROM connected AS T1 INNER JOIN atom AS T2 ON T1.atom_id = T2.atom_id WHERE T1.bond_id = 'TR000_2_3'
```
**Predicted SQL:**
```sql
SELECT DISTINCT T2.element FROM connected AS T1 INNER JOIN atom AS T2 ON T1.atom_id = T2.atom_id OR T1.atom_id2 = T2.atom_id WHERE T1.bond_id = 'TR000_2_3'
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| atom_id | element |
|---|---|
| TR000_3 | cl |
| TR000_2 | c |
| TR005_12 | c |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
| TR000_2_3 | TR000 | - |
| TR004_7_16 | TR049 | - |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| TR000_3 | TR000_2 | TR000_2_3 |
| TR000_2 | TR000_3 | TR004_7_16 |

*molecule*

| molecule_id | label |
|---|---|
| TR000 | + |
| TR049 | - |

**Gold result on the witness:** `[['cl']]`  
**Predicted result on the witness:** `[['c'], ['cl']]`

**Verdict:** gold_wrong  
**Reason (one sentence):** Bond TR000_2_3 connects two atoms, TR000_3(cl) and TR000_2(c); Predicted matches both endpoints via atom_id OR atom_id2 and returns c and cl, while Gold matches only atom_id and misses the carbon atom.


---

## Item 8 (thrombosis_prediction)

**Question:** What sex is the patient who in a medical examination was diagnosed with PSS and in a laboratory examination had a blood level of C-reactive protein de 2+, createnine 1 and LDH 123?

**Evidence:** PSS' refers to diagnosis; blood level of C-reactive protein de 2+refers to CRP > 2; createnine 1 refers to CRE = 1; LDH 123 refers to LDH = 123

**Gold SQL:**
```sql
SELECT T1.SEX FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID INNER JOIN Laboratory AS T3 ON T3.ID = T2.ID WHERE T2.Diagnosis = 'PSS' AND T3.CRP = '2+' AND T3.CRE = 1.0 AND T3.LDH = 123
```
**Predicted SQL:**
```sql
SELECT DISTINCT patient.sex FROM patient INNER JOIN examination ON patient.id = examination.id INNER JOIN laboratory ON patient.id = laboratory.id WHERE examination.diagnosis = 'PSS' AND laboratory.cre = 1
```

**Witness database:**

*Examination* (11 unreferenced columns omitted)

| ID | Diagnosis |
|---|---|
| 1070 | PSS |

*Laboratory* (40 unreferenced columns omitted)

| ID | LDH | CRE | CRP |
|---|---|---|---|
| 1070 | 137 | 1.0 | 0.5 |

*Patient* (5 unreferenced columns omitted)

| ID | SEX |
|---|---|
| 1070 | F |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['F']]`

**Verdict:** pred_wrong  
**Reason (one sentence):** The laboratory row has CRP=0.5 (not 2+) and LDH=137 (not 123), so no patient meets every condition and the answer is empty; Predicted drops the CRP and LDH predicates and wrongly returns sex F.


---

## Item 9 (thrombosis_prediction)

**Question:** Please list a patient's platelet level if it is within the normal range and if he or she is diagnosed with MCTD.

**Evidence:** PLT > 100 and PLT < 400 means platelet level is within the normal range; PLT < 100 and PLT > 400 means platelet level is not within the normal range; diagnosed with MCTD refers to Diagnosis = 'MCTD';

**Gold SQL:**
```sql
SELECT T2.PLT FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'MCTD' AND T2.PLT BETWEEN 100 AND 400
```
**Predicted SQL:**
```sql
SELECT lab.PLT FROM Laboratory AS lab INNER JOIN Patient AS pat ON lab.ID = pat.ID WHERE pat.Diagnosis = 'MCTD' AND lab.PLT > 100 AND lab.PLT < 400
```

**Witness database:**

*Patient* (5 unreferenced columns omitted)

| ID | Diagnosis |
|---|---|
| 1 | MCTD |
| 31 | MCTD |

*Laboratory* (42 unreferenced columns omitted)

| ID | PLT |
|---|---|
| 1 | 100 |
| 31 | 100 |
| 1 | 101 |
| 1 | NULL |

**Gold result on the witness:** `[[100], [101], [100]]`  
**Predicted result on the witness:** `[[101]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The evidence defines normal platelets strictly as PLT>100 AND PLT<400, so boundary PLT=100 is excluded; Predicted returns only 101, while Gold's inclusive BETWEEN wrongly adds the two PLT=100 rows.


---

## Item 10 (financial)

**Question:** For the female client who was born in 1976/1/29, which district did she opened her account?

**Evidence:** Female refers to gender = 'F'; A2 refers to district names

**Gold SQL:**
```sql
SELECT T1.A2 FROM district AS T1 INNER JOIN client AS T2 ON T1.district_id = T2.district_id WHERE T2.birth_date = '1976-01-29' AND T2.gender = 'F'
```
**Predicted SQL:**
```sql
SELECT district.A2 FROM district INNER JOIN account ON district.district_id = account.district_id INNER JOIN client ON district.district_id = client.district_id WHERE client.gender = 'F' AND client.birth_date = '1976-01-29';
```

**Witness database:**

*account* (3 unreferenced columns omitted)

| district_id |
|---|
| 1 |
| 1 |

*card*

| card_id | disp_id | type | issued |
|---|---|---|---|
| 0 | 1 | gold | 0001-01-01 |
| 1 | 1 | gold | 0001-01-01 |

*client* (1 unreferenced columns omitted)

| gender | birth_date | district_id |
|---|---|---|
| F | 1976-01-29 | 1 |
| F | 1976-01-29 | 2 |

*disp*

| disp_id | client_id | account_id | type |
|---|---|---|---|
| 1 | 1 | 2 | DISPONENT |
| 2 | 1 | 2 | DISPONENT |

*district* (14 unreferenced columns omitted)

| district_id | A2 |
|---|---|
| 2 | 2147483648 |
| 1 | 2147483649 |

*loan* (3 unreferenced columns omitted)

| loan_id | account_id | date | amount |
|---|---|---|---|
| 1 | 2 | 0001-01-01 | 0 |
| 2 | 2 | 0001-01-01 | 0 |

*order* (2 unreferenced columns omitted)

| order_id | account_id | bank_to | account_to |
|---|---|---|---|
| 1 | 2 | 2147483648 | 0 |
| 2 | 2 | 2147483648 | 0 |

*trans* (6 unreferenced columns omitted)

| trans_id | account_id | date | type |
|---|---|---|---|
| 1 | 2 | 0001-01-01 | PRIJEM |
| 2 | 1 | 0001-01-01 | PRIJEM |

**Gold result on the witness:** `[['2147483648'], ['2147483649']]`  
**Predicted result on the witness:** `[['2147483649'], ['2147483649']]`

**Verdict:** pred_wrong  
**Reason (one sentence):** Two matching female clients belong to districts 1 and 2 and Gold returns both districts; Predicted's extra INNER JOIN to the account table (accounts exist only in district 1) drops the district-2 client and duplicates district 1.


---

## Item 11 (codebase_community)

**Question:** How many posts with votes that were created in 2011 have a bounty of 50?

**Evidence:** created in 2012 refers YEAR(CreationDate) = 2011; BountyAmount = 50;

**Gold SQL:**
```sql
SELECT COUNT(T1.Id) FROM posts AS T1 INNER JOIN votes AS T2 ON T1.Id = T2.PostId WHERE T2.BountyAmount = 50 AND STRFTIME('%Y', T2.CreationDate) = '2011'
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT `posts`.`id`) FROM `posts` INNER JOIN `votes` ON `posts`.`id` = `votes`.`postid` WHERE strftime('%Y', `votes`.`creationdate`) = '2011' AND `votes`.`bountyamount` = 50
```

**Witness database:**

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 24055 | 5 | 8800 | 31c24c57-e007-4466-8e26-0e1eb6834d4c |

*posts* (20 unreferenced columns omitted)

| Id |
|---|
| 8800 |

*users* (10 unreferenced columns omitted)

| Id | Reputation | CreationDate | DisplayName |
|---|---|---|---|
| 3270 | 221 | 2011-02-16 05:35:20.0 | berkay |

*votes* (3 unreferenced columns omitted)

| PostId | CreationDate | BountyAmount |
|---|---|---|
| 8800 | 2011-03-28 | 50 |
| 8800 | 2011-03-28 | 50 |

**Gold result on the witness:** `[[2]]`  
**Predicted result on the witness:** `[[1]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** Both matching rows are votes on the single post 8800, so the distinct post count is 1 (Predicted's COUNT DISTINCT), while Gold counts vote rows and wrongly reports 2.


---

## Item 12 (california_schools)

**Question:** Among the schools with the SAT test takers of over 500, please list the schools that are magnet schools or offer a magnet program.

**Evidence:** Magnet schools or offer a magnet program means that Magnet = 1

**Gold SQL:**
```sql
SELECT T2.School FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.Magnet = 1 AND T1.NumTstTakr > 500
```
**Predicted SQL:**
```sql
SELECT sname FROM satscores INNER JOIN schools ON satscores.cds = schools.CDSCode WHERE NumTstTakr > 500 AND Magnet = 1;
```

**Witness database:**

*satscores* (8 unreferenced columns omitted)

| cds | sname | NumTstTakr |
|---|---|---|
| 10621580000000 | Mountain View High | 501 |

*schools* (46 unreferenced columns omitted)

| CDSCode | School | Magnet |
|---|---|---|
| 10621580000000 | Sequoia Elementary | 1 |

**Gold result on the witness:** `[['Sequoia Elementary']]`  
**Predicted result on the witness:** `[['Mountain View High']]`

**Verdict:** implausible_data  
**Reason (one sentence):** The same CDSCode carries two incompatible names ('Mountain View High' in satscores versus 'Sequoia Elementary' in schools), and this inconsistent record alone is why Gold and Predicted output different school names.


---

## Item 13 (financial)

**Question:** For the branch which located in the south Bohemia with biggest number of inhabitants, what is the percentage of the male clients?

**Evidence:** Percentage of the male clients = DIVIDE(COUNT(male clients), COUNT(clients)) * 100; Male refers to gender = 'M', A3 is the region name. A4 contains the information about inhabitants.

**Gold SQL:**
```sql
SELECT CAST(SUM(T1.gender = 'M') AS REAL) * 100 / COUNT(T1.client_id) FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A3 = 'south Bohemia' GROUP BY T2.A4 ORDER BY T2.A4 DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT CAST(SUM(CASE WHEN client.gender = 'M' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(client.client_id) AS male_percentage FROM client INNER JOIN district ON client.district_id = district.district_id WHERE district.a3 = 'south Bohemia' AND district.a4 = (SELECT MAX(a4) FROM district WHERE a3 = 'south Bohemia')
```

**Witness database:**

*account*

| account_id | district_id | frequency | date |
|---|---|---|---|
| 866 | 9 | POPLATEK MESICNE | 1993-01-10 |
| 899 | 72 | POPLATEK MESICNE | 1993-06-21 |
| 1725 | 72 | POPLATEK PO OBRATU | 1995-07-03 |

*client* (1 unreferenced columns omitted)

| client_id | gender | district_id |
|---|---|---|
| 1082 | M | 9 |
| 1044 | F | 9 |
| 2092 | M | 72 |

*disp*

| disp_id | client_id | account_id | type |
|---|---|---|---|
| 1082 | 1082 | 899 | OWNER |
| 1044 | 1044 | 866 | OWNER |
| 2092 | 2092 | 1725 | OWNER |

*district* (13 unreferenced columns omitted)

| district_id | A3 | A4 |
|---|---|---|
| 9 | central Bohemia | 81344 |
| 72 | north Moravia | 226122 |

*trans* (6 unreferenced columns omitted)

| trans_id | account_id | date | type |
|---|---|---|---|
| 252771 | 866 | 1997-07-08 | VYDAJ |
| 262941 | 899 | 1995-12-31 | VYDAJ |
| 505001 | 1725 | 1998-11-10 | PRIJEM |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Verdict:** pred_wrong  
**Reason (one sentence):** No district is in south Bohemia, so there is no such branch and Gold's grouped query correctly returns no row; Predicted's scalar aggregate over an empty set spuriously emits one NULL row.


---

## Item 14 (financial)

**Question:** In the branch where the second-highest number of crimes were committed in 1995 occurred, how many male clients are there?

**Evidence:** Male refers to gender = 'M'; A15 stands for no. of commited crimes 1995

**Gold SQL:**
```sql
SELECT COUNT(T1.client_id) FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.gender = 'M' AND T2.A15 = (SELECT T3.A15 FROM district AS T3 ORDER BY T3.A15 DESC LIMIT 1, 1)
```
**Predicted SQL:**
```sql
SELECT COUNT(client_id) FROM client WHERE district_id = (SELECT district_id FROM district ORDER BY a15 DESC LIMIT 1 OFFSET 1) AND gender = 'M'
```

**Witness database:**

*account*

| account_id | district_id | frequency | date |
|---|---|---|---|
| 650 | 3 | POPLATEK MESICNE | 1995-01-28 |
| 1082 | 2 | POPLATEK MESICNE | 1996-06-08 |
| 1623 | 1 | POPLATEK MESICNE | 1996-02-04 |
| 1 | 18 | POPLATEK MESICNE | 1995-03-24 |
| 2 | 1 | POPLATEK MESICNE | 1993-02-26 |
| 3250 | 1 | POPLATEK MESICNE | 1995-01-06 |
| 3192 | 18 | POPLATEK MESICNE | 1996-07-28 |

*client* (1 unreferenced columns omitted)

| client_id | gender | district_id |
|---|---|---|
| 1 | F | 3 |
| 2 | F | 2 |
| 3931 | F | 1 |
| 780 | M | 3 |
| 1299 | F | 2 |
| 1968 | M | 1 |
| 3859 | M | 18 |

*disp*

| disp_id | client_id | account_id | type |
|---|---|---|---|
| 1 | 1 | 1 | OWNER |
| 2 | 2 | 2 | OWNER |
| 3931 | 3931 | 3250 | DISPONENT |
| 780 | 780 | 650 | OWNER |
| 1299 | 1299 | 1082 | OWNER |
| 1968 | 1968 | 1623 | DISPONENT |
| 3859 | 3859 | 3192 | DISPONENT |

*district* (14 unreferenced columns omitted)

| district_id | A15 |
|---|---|
| 3 | 1845 |
| 2 | 1740 |
| 1 | 1003 |
| 18 | 1740 |

*trans* (6 unreferenced columns omitted)

| trans_id | account_id | date | type |
|---|---|---|---|
| 3551957 | 650 | 1995-11-30 | PRIJEM |
| 3566202 | 1082 | 1998-03-31 | PRIJEM |
| 476295 | 1623 | 1997-05-29 | VYDAJ |
| 3530463 | 1 | 1997-05-31 | PRIJEM |
| 3530535 | 2 | 1997-07-31 | PRIJEM |
| 3638005 | 3250 | 1997-04-30 | PRIJEM |
| 935350 | 3192 | 1998-01-31 | VYDAJ |

**Gold result on the witness:** `[[1]]`  
**Predicted result on the witness:** `[[0]]`

**Verdict:** pred_wrong  
**Reason (one sentence):** The second-highest 1995 crime value is 1740, shared by districts 2 and 18; Gold matches that value and counts the male clients in both (=1, from district 18), while Predicted picks an arbitrary single tied district (id 2) and finds 0 males.


---

## Item 15 (codebase_community)

**Question:** What is the display name of the user who is the owner of the most valuable post?

**Evidence:** most valuable post refers to Max(FavoriteCount)

**Gold SQL:**
```sql
SELECT T2.DisplayName FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id ORDER BY T1.FavoriteCount DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT users.DisplayName FROM users INNER JOIN posts ON users.Id = posts.OwnerUserId WHERE posts.FavoriteCount = (SELECT MAX(FavoriteCount) FROM posts);
```

**Witness database:**

*badges*

| Id | UserId | Name | Date |
|---|---|---|---|
| 2 | 1 | 2147483648 | 0001-01-01 |
| 1 | 1 | 2147483648 | 0001-01-01 |

*comments* (3 unreferenced columns omitted)

| Id | PostId | Score | Text |
|---|---|---|---|
| 1 | 2 | 0 | 2147483648 |
| 2 | 1 | 0 | 2147483648 |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 1 | 10 | 1 | 2147483648 |
| 2 | 1 | 1 | 2147483648 |

*postLinks* (1 unreferenced columns omitted)

| Id | CreationDate | PostId | RelatedPostId |
|---|---|---|---|
| 2 | 0001-01-01 | 1 | 1 |
| 1 | 0001-01-01 | 1 | 1 |

*posts* (19 unreferenced columns omitted)

| OwnerUserId | FavoriteCount |
|---|---|
| 2 | 1 |
| 1 | 1 |

*tags* (1 unreferenced columns omitted)

| Id | TagName | Count | ExcerptPostId |
|---|---|---|---|
| 1 | 2147483648 | 0 | 1 |
| 2 | 2147483649 | 0 | 2 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 2 | 2147483649 |
| 1 | 2147483648 |

*votes* (2 unreferenced columns omitted)

| Id | PostId | VoteTypeId | CreationDate |
|---|---|---|---|
| 2 | 1 | 1 | 0001-01-01 |
| 1 | 1 | 1 | 0001-01-01 |

**Gold result on the witness:** `[['2147483649']]`  
**Predicted result on the witness:** `[['2147483649'], ['2147483648']]`

**Verdict:** gold_wrong  
**Reason (one sentence):** Both posts tie for max FavoriteCount=1 and are owned by users 1 and 2; Predicted returns both owners via FavoriteCount=MAX, while Gold's ORDER BY...LIMIT 1 arbitrarily keeps only one owner.


---

## Item 16 (toxicology)

**Question:** What is the ratio of Hydrogen elements in molecule ID TR006? List the ratio with its label.

**Evidence:** hydrogen refers to element = 'h'; ratio = DIVIDE(SUM(element = 'h'), count(element)) where molecule_id = 'TR006' ; label = '+' mean molecules are carcinogenic; label = '-' means molecules are non-carcinogenic

**Gold SQL:**
```sql
WITH SubQuery AS (SELECT DISTINCT T1.atom_id, T1.element, T1.molecule_id, T2.label FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.molecule_id = 'TR006') SELECT CAST(COUNT(CASE WHEN element = 'h' THEN atom_id ELSE NULL END) AS REAL) / (CASE WHEN COUNT(atom_id) = 0 THEN NULL ELSE COUNT(atom_id) END) AS ratio, label FROM SubQuery GROUP BY label
```
**Predicted SQL:**
```sql
SELECT CAST(SUM(CASE WHEN `atom`.`element` = 'h' THEN 1 ELSE 0 END) AS REAL) / COUNT(`atom`.`element`) AS ratio, `molecule`.`label` FROM `atom` INNER JOIN `molecule` ON `atom`.`molecule_id` = `molecule`.`molecule_id` WHERE `atom`.`molecule_id` = 'TR006'
```

**Witness database:**

*atom*

| atom_id | molecule_id | element |
|---|---|---|
| TR000_3 | TR060 | c |
| TR000_2 | TR496 | h |
| TR338_32 | TR338 | c |
| TR060_49 | TR060 | h |
| TR496_56 | TR496 | h |
| TR338_91 | TR338 | h |
| TR060_5 | TR060 | c |
| TR496_7 | TR496 | c |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
| TR338_32_91 | TR338 | - |
| TR060_5_49 | TR060 | - |
| TR496_7_56 | TR496 | - |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| TR338_91 | TR338_32 | TR338_32_91 |
| TR060_5 | TR060_49 | TR060_5_49 |
| TR496_7 | TR496_56 | TR496_7_56 |
| TR338_32 | TR338_91 | TR338_32_91 |
| TR060_49 | TR060_5 | TR060_5_49 |
| TR496_56 | TR496_7 | TR496_7_56 |

*molecule*

| molecule_id | label |
|---|---|
| TR338 | + |
| TR060 | - |
| TR496 | + |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None, None]]`

**Verdict:** pred_wrong  
**Reason (one sentence):** Molecule TR006 has no rows in the witness, so the faithful answer is an empty result set; Predicted's aggregate-over-empty set spuriously returns a single (NULL,NULL) row while Gold's GROUP BY correctly yields no rows.


---

## Item 17 (codebase_community)

**Question:** How many comments and answers were left by the users on the post with the title 'Clustering 1D data'?

**Evidence:** -

**Gold SQL:**
```sql
SELECT CommentCount, AnswerCount FROM posts WHERE Title = 'Clustering 1D data'
```
**Predicted SQL:**
```sql
SELECT (SELECT COUNT(*) FROM comments WHERE PostId = (SELECT Id FROM posts WHERE Title = 'Clustering 1D data')) AS CommentCount, (SELECT COUNT(*) FROM posts WHERE PostTypeId = 2 AND ParentId = (SELECT Id FROM posts WHERE Title = 'Clustering 1D data')) AS AnswerCount;
```

**Witness database:**

*comments* (5 unreferenced columns omitted)

| Id | PostId |
|---|---|
| 26834 | 14829 |
| 68660 | 34459 |
| 135297 | 69930 |
| 115826 | 60402 |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 308146 | 2 | 91681 | a7217ddc-8ff4-41a6-a02f-4d20125b980b |
| 336688 | 2 | 100366 | 5eceab2a-fe0a-4786-9334-6be83f9d3d44 |
| 60137 | 6 | 19792 | a60266ee-6130-4aa8-8fde-8a9b95d7d05c |
| 43433 | 2 | 14829 | 695a2ac6-b18b-4128-b0b8-1e5f72665b50 |
| 110561 | 2 | 34459 | 9cb9db28-07f7-440e-9d62-3bf1e520dea1 |
| 232167 | 5 | 69930 | ac42f7bd-bd4c-4966-8480-9a61fb4712e7 |
| 195976 | 5 | 60402 | ad7fc749-e0ff-4a4b-850c-e9ca238e270c |

*posts* (16 unreferenced columns omitted)

| PostTypeId | Title | AnswerCount | CommentCount | ParentId |
|---|---|---|---|---|
| 2 | NULL | NULL | 0 | 91337 |
| 2 | NULL | NULL | 0 | 100348 |
| 1 | Constrained Optimization library for equality and inequality | 1 | 4 | NULL |
| 2 | NULL | NULL | 4 | 14822 |
| 1 | Bayesian models and exchangeability | 2 | 3 | NULL |
| 1 | Band pass filter giving ‘wrong’ turning point | 0 | 8 | NULL |
| 1 | Variance in a known population | 0 | 6 | NULL |

*users* (10 unreferenced columns omitted)

| Id | Reputation | CreationDate | DisplayName |
|---|---|---|---|
| 776 | 1895 | 2010-08-05 19:40:44.0 | Brandon Bertelsen |
| 13002 | 217 | 2012-07-31 20:07:57.0 | singelton |
| 21240 | 790 | 2013-02-25 11:17:06.0 | fredrikhs |
| 805 | 65272 | 2010-08-07 08:40:07.0 | Glen_b |
| 4598 | 8814 | 2011-05-13 10:02:56.0 | cbeleites |
| 36041 | 2538 | 2013-12-11 15:34:17.0 | Aksakal |
| 8101 | 748 | 2011-12-19 18:46:57.0 | Quant Guy |
| 30252 | 6 | 2013-09-13 09:01:26.0 | Aidan |
| 26286 | 11 | 2013-05-30 02:03:02.0 | NuclearAlchemist |
| 7409 | 129 | 2011-11-16 14:32:09.0 | Nicolas Kaiser |
| 88 | 14082 | 2010-07-19 19:35:37.0 | mbq |
| 6029 | 5837 | 2011-08-28 21:08:33.0 | Gala |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[0, 0]]`

**Verdict:** pred_wrong  
**Reason (one sentence):** No post titled 'Clustering 1D data' exists in the witness, so there are no CommentCount/AnswerCount values to report; Predicted's NULL-propagating scalar subqueries fabricate 0,0 while Gold's direct column lookup correctly returns no row.


---

## Item 18 (formula_1)

**Question:** For the race happened on 2015/11/29, how many drivers finished the game?

**Evidence:** game and race are synonyms; drivers who finished the race should have record in time;

**Gold SQL:**
```sql
SELECT COUNT(T2.driverId) FROM races AS T1 INNER JOIN results AS T2 ON T2.raceId = T1.raceId WHERE T1.date = '2015-11-29' AND T2.time IS NOT NULL
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT driverId) FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T2.date = '2015-11-29' AND T1.time IS NOT NULL
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 24 | yas_marina | Yas Marina Circuit | Abu Dhabi |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 10 | force_india | Force India | Indian |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 815 | perez | 11 | PER |
| 807 | hulkenberg | 27 | HUL |

*races* (6 unreferenced columns omitted)

| raceId | date |
|---|---|
| 945 | 2015-11-29 |

*results* (15 unreferenced columns omitted)

| raceId | driverId | time |
|---|---|---|
| 945 | 815 | +1:03.952 |
| 945 | 807 | +1:33.618 |
| 945 | 815 | +1:03.952 |

*seasons*

| year | url |
|---|---|
| 2015 | http://en.wikipedia.org/wiki/2015_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 1 | Finished |

**Gold result on the witness:** `[[3]]`  
**Predicted result on the witness:** `[[2]]`

**Verdict:** implausible_data  
**Reason (one sentence):** The results table contains a pure duplicate row for driver 815 in race 945 (identical time), an artifact that would never occur in a real F1 results table and is the sole reason Gold's row count is 3 versus Predicted's distinct count of 2.


---

## Item 19 (codebase_community)

**Question:** Among posts by Harvey Motulsky and Noah Snyder, which one has higher popularity?

**Evidence:** Has higher popularity means the post has higher view count ; calculation = MAX(SUM(ViewCount)) where DisplayName = 'Harvey Motulsky' OR DisplayName = 'Noah Snyder';

**Gold SQL:**
```sql
SELECT T1.DisplayName FROM users AS T1 INNER JOIN postHistory AS T2 ON T1.Id = T2.UserId INNER JOIN posts AS T3 ON T2.PostId = T3.Id WHERE T1.DisplayName = 'Harvey Motulsky' OR T1.DisplayName = 'Noah Snyder' GROUP BY T1.DisplayName ORDER BY SUM(T3.ViewCount) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT `users`.`displayname` FROM `users` INNER JOIN `posts` ON `users`.`id` = `posts`.`owneruserid` WHERE `users`.`displayname` IN ('Harvey Motulsky', 'Noah Snyder') GROUP BY `users`.`displayname` ORDER BY SUM(`posts`.`viewcount`) DESC LIMIT 1
```

**Witness database:**

*postHistory* (7 unreferenced columns omitted)

| PostId | UserId |
|---|---|
| 2 | 1 |
| 2 | 2 |
| 1 | 3 |
| 3 | 1 |

*posts* (18 unreferenced columns omitted)

| Id | ViewCount | OwnerUserId |
|---|---|---|
| 2 | 30 | 2 |
| 3 | 38 | 2 |
| 1 | 1278 | 8 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 1 | 1 |
| 3 | Noah Snyder |
| 2 | Geoff Dalgas |
| 8 | csgillespie |

**Gold result on the witness:** `[['Noah Snyder']]`  
**Predicted result on the witness:** `[]`

**Verdict:** gold_wrong  
**Reason (one sentence):** "Posts by" a user means posts owned by that user (OwnerUserId), which Predicted joins on; Gold instead joins through postHistory, wrongly attributing to Noah Snyder a post he merely edited while neither target user owns any post in the witness.


---

## Item 20 (european_football_2)

**Question:** What is the average number of goals made by Parma as the away team while playing in Italy?

**Evidence:** Parma refers to team_long_name = 'Parma'; average number of goals refers to AVG(away_team_goal)

**Gold SQL:**
```sql
SELECT CAST(SUM(T1.away_team_goal) AS REAL) / COUNT(T1.id) FROM "Match" AS T1 INNER JOIN TEAM AS T2 ON T1.away_team_api_id = T2.team_api_id INNER JOIN Country AS T3 ON T1.country_id = T3.id WHERE T2.team_long_name = 'Parma' AND T3.name = 'Italy'
```
**Predicted SQL:**
```sql
SELECT AVG("Match"."away_team_goal") AS average_away_goals FROM "Country" INNER JOIN "Match" ON "Country"."id" = "Match"."country_id" INNER JOIN "Team" ON "Match"."away_team_api_id" = "Team"."team_api_id" WHERE "Country"."name" = 'Italy' AND "Team"."team_long_name" = 'Parma'
```

**Witness database:**

*Country*

| id | name |
|---|---|
| 2 | Italy |
| 1 | Italy |
| 286 | aa |

*Team* (3 unreferenced columns omitted)

| team_api_id | team_long_name |
|---|---|
| 1 | Parma |
| 6 | n |
| NULL | Parma |
| 165 | Parma |
| 0 | Parma |

*Match* (111 unreferenced columns omitted)

| id | country_id | away_team_api_id | away_team_goal |
|---|---|---|---|
| 3 | 2 | 1 | 8 |
| 67 | 2 | 1 | 8 |
| 115 | 2 | NULL | 116 |
| 131 | 2 | 1 | NULL |
| 166 | NULL | 165 | NULL |
| 287 | 286 | 0 | 8 |

**Gold result on the witness:** `[[5.333333333333333]]`  
**Predicted result on the witness:** `[[8.0]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The evidence defines the metric as AVG(away_team_goal), which ignores the row with NULL goals; Predicted computes 8.0 while Gold divides by COUNT(id)=3, wrongly counting the NULL-goal match in the denominator.


---

## Item 21 (financial)

**Question:** List out the accounts who have the earliest trading date in 1995 ?

**Evidence:** -

**Gold SQL:**
```sql
SELECT account_id FROM trans WHERE STRFTIME('%Y', date) = '1995' ORDER BY date ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.account_id FROM account AS T1 INNER JOIN trans AS T2 ON T1.account_id = T2.account_id WHERE STRFTIME('%Y', T2.date) = '1995' GROUP BY T1.account_id ORDER BY MIN(T2.date) LIMIT 1
```

**Witness database:**

*account* (3 unreferenced columns omitted)

| account_id |
|---|
| 2723 |
| 3638 |
| 8321 |
| 1619 |
| 8625 |
| 1937 |
| 325 |
| 1610 |
| 153 |
| 8475 |
| 1341 |
| 2851 |

*client*

| client_id | gender | birth_date | district_id |
|---|---|---|---|
| 397 | M | 1930-03-27 | 75 |
| 1952 | F | 1971-03-09 | 52 |
| 185 | M | 1954-05-30 | 77 |
| 3289 | F | 1977-06-09 | 75 |
| 4387 | M | 1946-02-18 | 52 |
| 10276 | M | 1976-11-16 | 77 |
| 1963 | M | 1945-06-12 | 38 |
| 10636 | M | 1971-08-03 | 64 |
| 2353 | F | 1929-09-17 | 4 |
| 1623 | M | 1963-07-09 | 36 |
| 10459 | F | 1964-08-09 | 17 |
| 3445 | F | 1979-03-26 | 17 |

*disp*

| disp_id | client_id | account_id | type |
|---|---|---|---|
| 397 | 397 | 325 | OWNER |
| 1952 | 1952 | 1610 | OWNER |
| 185 | 185 | 153 | OWNER |
| 3289 | 3289 | 2723 | OWNER |
| 4387 | 4387 | 3638 | OWNER |
| 9968 | 10276 | 8321 | DISPONENT |
| 1963 | 1963 | 1619 | OWNER |
| 10328 | 10636 | 8625 | OWNER |
| 2353 | 2353 | 1937 | OWNER |
| 1623 | 1623 | 1341 | OWNER |
| 10151 | 10459 | 8475 | OWNER |
| 3445 | 3445 | 2851 | OWNER |

*district* (12 unreferenced columns omitted)

| district_id | A2 | A3 | A4 |
|---|---|---|---|
| 75 | Prerov | north Moravia | 138032 |
| 52 | Usti nad Orlici | east Bohemia | 139012 |
| 77 | Vsetin | north Moravia | 148545 |
| 38 | Louny | north Bohemia | 85852 |
| 64 | Zlin | south Moravia | 197099 |
| 36 | Liberec | north Bohemia | 159617 |
| 4 | Kladno | central Bohemia | 149893 |
| 17 | Pelhrimov | south Bohemia | 74062 |

*trans* (8 unreferenced columns omitted)

| account_id | date |
|---|---|
| 1619 | 1998-05-14 |
| 8625 | 1996-09-12 |
| 1937 | 1997-10-12 |
| 2723 | 1995-06-30 |
| 3638 | 1996-07-08 |
| 8321 | 1995-06-30 |
| 325 | 1997-02-28 |
| 1610 | 1996-10-28 |
| 153 | 1998-04-07 |
| 8475 | 1994-08-12 |
| 1341 | 1998-04-30 |
| 2851 | 1996-11-26 |

**Gold result on the witness:** `[[8321]]`  
**Predicted result on the witness:** `[[2723]]`

**Verdict:** both_wrong  
**Reason (one sentence):** Two accounts (2723 and 8321) share the earliest 1995 date of 1995-06-30, so the question asks for both, but each query uses LIMIT 1 and arbitrarily returns only one of the tied accounts.


---

## Item 22 (card_games)

**Question:** Please provide top three sets that don't appear in Magic: The Gathering Online, along with their names in in alphabetical order.

**Evidence:** don't appear in Magic: The Gathering Online refers to mtgoCode is NULL or mtgoCode = ''

**Gold SQL:**
```sql
SELECT name FROM sets WHERE mtgoCode IS NULL ORDER BY name LIMIT 3
```
**Predicted SQL:**
```sql
SELECT name FROM sets WHERE mtgoCode IS NULL OR mtgoCode = '' ORDER BY name ASC LIMIT 3
```

**Witness database:**

*cards* (70 unreferenced columns omitted)

| id | artist | asciiName | availability |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | arena,mtgo,paper |

*foreign_data* (4 unreferenced columns omitted)

| id | flavorText | language | multiverseid |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | 0 |

*legalities*

| id | format | status | uuid |
|---|---|---|---|
| 1 | 2147483648 | Restricted | 2147483648 |

*sets* (19 unreferenced columns omitted)

| mtgoCode | name |
|---|---|
|  | 2147483648 |

*set_translations*

| id | language | setCode | translation |
|---|---|---|---|
| 1 | French | 2147483648 | 2147483648 |

*rulings*

| id | date | text | uuid |
|---|---|---|---|
| 1 | 0001-01-01 | 2147483648 | 2147483648 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2147483648']]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The evidence explicitly treats "not on MTGO" as mtgoCode IS NULL OR mtgoCode='', and the witness set has an empty-string mtgoCode; Predicted includes it while Gold's IS-NULL-only filter misses the empty-string row.


---

## Item 23 (thrombosis_prediction)

**Question:** Please list a patient's platelet level if it is within the normal range and if he or she is diagnosed with MCTD.

**Evidence:** PLT > 100 and PLT < 400 means platelet level is within the normal range; PLT < 100 and PLT > 400 means platelet level is not within the normal range; diagnosed with MCTD refers to Diagnosis = 'MCTD';

**Gold SQL:**
```sql
SELECT T2.PLT FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'MCTD' AND T2.PLT BETWEEN 100 AND 400
```
**Predicted SQL:**
```sql
SELECT L.PLT FROM Laboratory AS L INNER JOIN Patient AS P ON L.ID = P.ID WHERE P.Diagnosis = 'MCTD' AND L.PLT > 100 AND L.PLT < 400;
```

**Witness database:**

*Examination* (9 unreferenced columns omitted)

| ID | Examination Date | aCL IgG | aCL IgM |
|---|---|---|---|
| 1 | 0001-01-01 | 0 | 0 |

*Patient* (5 unreferenced columns omitted)

| ID | Diagnosis |
|---|---|
| 1 | MCTD |

*Laboratory* (42 unreferenced columns omitted)

| ID | PLT |
|---|---|
| 1 | 100 |

**Gold result on the witness:** `[[100]]`  
**Predicted result on the witness:** `[]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The evidence defines normal platelets as strictly PLT>100 and PLT<400, so a PLT of exactly 100 is not normal; Predicted's strict inequality correctly returns nothing while Gold's BETWEEN wrongly includes the 100 endpoint.


---

## Item 24 (toxicology)

**Question:** Which element is the least numerous in non-carcinogenic molecules?

**Evidence:** label = '-' means molecules are non-carcinogenic; least numerous refers to MIN(COUNT(element));

**Gold SQL:**
```sql
SELECT T.element FROM (SELECT T1.element, COUNT(DISTINCT T1.molecule_id) FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '-' GROUP BY T1.element ORDER BY COUNT(DISTINCT T1.molecule_id) ASC LIMIT 1) t
```
**Predicted SQL:**
```sql
SELECT `atom`.`element` FROM `atom` INNER JOIN `molecule` ON `atom`.`molecule_id` = `molecule`.`molecule_id` WHERE `molecule`.`label` = '-' GROUP BY `atom`.`element` ORDER BY COUNT(`atom`.`element`) ASC LIMIT 1
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| molecule_id | element |
|---|---|
| TR338 | ca |
| TR060 | c |
| TR496 | c |
| TR338 | c |
| TR496 | h |
| TR060 | h |
| TR338 | h |
| TR060 | c |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
| TR338_32_91 | TR338 | - |
| TR496_7_56 | TR496 | - |
| TR060_5_49 | TR060 | - |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| TR338_91 | TR338_32 | TR338_32_91 |
| TR496_7 | TR496_56 | TR496_7_56 |
| TR060_5 | TR060_49 | TR060_5_49 |
| TR338_32 | TR338_91 | TR338_32_91 |
| TR496_56 | TR496_7 | TR496_7_56 |
| TR060_49 | TR060_5 | TR060_5_49 |

*molecule*

| molecule_id | label |
|---|---|
| TR338 | + |
| TR496 | - |
| TR060 | - |

**Gold result on the witness:** `[['c']]`  
**Predicted result on the witness:** `[['h']]`

**Verdict:** gold_wrong  
**Reason (one sentence):** "Least numerous" means the element occurring in the fewest atom rows (c appears 3 times, h appears 2 among non-carcinogenic molecules), matching Predicted's COUNT(element)=h; Gold's COUNT(DISTINCT molecule_id) ties both elements at 2.


---

## Item 25 (toxicology)

**Question:** List down two molecule id of triple bond non carcinogenic molecules with element carbon.

**Evidence:** carbon refers to element = 'c'; triple bond refers to bond_type = '#'; label = '-' means molecules are non-carcinogenic

**Gold SQL:**
```sql
SELECT DISTINCT T2.molecule_id FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id INNER JOIN bond AS T3 ON T2.molecule_id = T3.molecule_id WHERE T3.bond_type = '#' AND T1.element = 'c' AND T2.label = '-'
```
**Predicted SQL:**
```sql
SELECT T1.molecule_id FROM molecule AS T1 INNER JOIN atom AS T2 ON T1.molecule_id = T2.molecule_id INNER JOIN bond AS T3 ON T1.molecule_id = T3.molecule_id WHERE T2.element = 'c' AND T3.bond_type = '#' AND T1.label = '-' LIMIT 2
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| molecule_id | element |
|---|---|
| TR377 | c |
| TR377 | c |
| TR377 | n |
| TR377 | n |
| TR377 | c |
| TR056 | c |

*bond* (1 unreferenced columns omitted)

| molecule_id | bond_type |
|---|---|
| TR377 | # |
| TR056 | # |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| TR377_3 | TR377_5 | TR377_3_5 |
| TR377_4 | TR377_6 | TR377_4_6 |
| TR377_5 | TR377_3 | TR377_3_5 |
| TR377_6 | TR377_4 | TR377_4_6 |

*molecule*

| molecule_id | label |
|---|---|
| TR377 | - |
| TR056 | - |

**Gold result on the witness:** `[['TR056'], ['TR377']]`  
**Predicted result on the witness:** `[['TR377'], ['TR377']]`

**Verdict:** pred_wrong  
**Reason (one sentence):** The question asks for two distinct molecule IDs satisfying the criteria; Gold's DISTINCT correctly returns TR056 and TR377, while Predicted's missing DISTINCT lets the three carbon atoms of TR377 multiply rows so LIMIT 2 returns TR377 twice.


---

## Item 26 (superhero)

**Question:** How many heroes have the highest attribute value in strength?

**Evidence:** highest attribute value in strength refers to MAX(attribute_value) WHERE attribute_name = 'Strength';

**Gold SQL:**
```sql
SELECT COUNT(T1.hero_id) FROM hero_attribute AS T1 INNER JOIN attribute AS T2 ON T1.attribute_id = T2.id WHERE T2.attribute_name = 'Strength' AND T1.attribute_value = ( SELECT MAX(attribute_value) FROM hero_attribute )
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM hero_attribute AS T1 INNER JOIN attribute AS T2 ON T1.attribute_id = T2.id WHERE T2.attribute_name = 'Strength' AND T1.attribute_value = (SELECT MAX(T3.attribute_value) FROM hero_attribute AS T3 INNER JOIN attribute AS T4 ON T3.attribute_id = T4.id WHERE T4.attribute_name = 'Strength')
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 13 | Good |
| 22 | Good |

*attribute*

| id | attribute_name |
|---|---|
| 1 | Strength |
| 5 | Intelligence |
| 25 | Strength |
| 10 | Strength |
| 14 | NULL |

*colour*

| id | colour |
|---|---|
| 7 | f |
| 8 | h |
| 9 | k |
| 17 | n |
| 18 | o |
| 19 | q |

*gender*

| id | gender |
|---|---|
| 6 | Male |
| 16 | Male |

*publisher*

| id | publisher_name |
|---|---|
| 12 | ABC Studios |
| 21 | ABC Studios |

*race*

| id | race |
|---|---|
| 11 | j |
| 20 | p |

*superhero* (8 unreferenced columns omitted)

| id | superhero_name | full_name | gender_id |
|---|---|---|---|
| 4 | c | d | 6 |
| 2 | l | m | 16 |
| 1 | l | m | 16 |

*hero_attribute*

| hero_id | attribute_id | attribute_value |
|---|---|---|
| 2 | 1 | 10 |
| 4 | 5 | 10 |
| 2 | 25 | 10 |
| 4 | 5 | 10 |
| 2 | 1 | 26 |
| 4 | 5 | 26 |
| 2 | 1 | 26 |
| 4 | 5 | 26 |
| 2 | NULL | 10 |
| 4 | 5 | 10 |
| NULL | 10 | NULL |
| 4 | 5 | NULL |
| NULL | 10 | 26 |

**Gold result on the witness:** `[[2]]`  
**Predicted result on the witness:** `[[3]]`

**Verdict:** pred_wrong  
**Reason (one sentence):** Predicted's COUNT(*) includes a hero_attribute row with a NULL hero_id that represents no superhero, inflating the count to 3; Gold's COUNT(hero_id) correctly excludes that non-hero row.


---

## Item 27 (financial)

**Question:** How often does account number 3 request an account statement to be released? What was the aim of debiting 3539 in total?

**Evidence:** k_symbol refers to the purpose of payments

**Gold SQL:**
```sql
SELECT T1.frequency, T2.k_symbol FROM account AS T1 INNER JOIN (SELECT account_id, k_symbol, SUM(amount) AS total_amount FROM `order` GROUP BY account_id, k_symbol) AS T2 ON T1.account_id = T2.account_id WHERE T1.account_id = 3 AND T2.total_amount = 3539
```
**Predicted SQL:**
```sql
SELECT `account`.`frequency`, `order`.`k_symbol` FROM `account` INNER JOIN `order` ON `account`.`account_id` = `order`.`account_id` WHERE `account`.`account_id` = 3 AND `order`.`amount` = 3539
```

**Witness database:**

*account* (2 unreferenced columns omitted)

| account_id | frequency |
|---|---|
| 2 | POPLATEK MESICNE |
| 1 | POPLATEK MESICNE |
| 3 | POPLATEK MESICNE |
| 269 | POPLATEK MESICNE |
| 8628 | POPLATEK PO OBRATU |
| 1623 | POPLATEK MESICNE |
| 1049 | POPLATEK MESICNE |

*client*

| client_id | gender | birth_date | district_id |
|---|---|---|---|
| 325 | M | 1960-02-21 | 3 |
| 10639 | M | 1954-01-29 | 2 |
| 2 | M | 1945-02-04 | 1 |
| 1 | F | 1970-12-13 | 18 |
| 4 | M | 1956-12-01 | 5 |
| 1968 | M | 1960-08-13 | 1 |
| 1259 | M | 1966-09-29 | 18 |

*disp*

| disp_id | client_id | account_id | type |
|---|---|---|---|
| 325 | 325 | 269 | OWNER |
| 10331 | 10639 | 8628 | OWNER |
| 2 | 2 | 2 | OWNER |
| 1 | 1 | 1 | OWNER |
| 4 | 4 | 3 | OWNER |
| 1968 | 1968 | 1623 | DISPONENT |
| 1259 | 1259 | 1049 | OWNER |

*district* (12 unreferenced columns omitted)

| district_id | A2 | A3 | A4 |
|---|---|---|---|
| 3 | Beroun | central Bohemia | 75232 |
| 2 | Benesov | central Bohemia | 88884 |
| 5 | Kolin | central Bohemia | 95616 |
| 1 | Hl.m. Praha | Prague | 1204953 |
| 18 | Pisek | south Bohemia | 70699 |

*order* (3 unreferenced columns omitted)

| account_id | amount | k_symbol |
|---|---|---|
| 3 | 3539.0 | LEASING |
| 3 | 3.0 | LEASING |
| 1 | 7781.0 | POJISTNE |

*trans* (6 unreferenced columns omitted)

| trans_id | account_id | date | type |
|---|---|---|---|
| 3530535 | 2 | 1997-07-31 | PRIJEM |
| 3530463 | 1 | 1997-05-31 | PRIJEM |
| 938 | 3 | 1997-12-28 | VYDAJ |
| 80278 | 269 | 1998-03-06 | VYDAJ |
| 2611775 | 8628 | 1997-01-05 | VYDAJ |
| 476295 | 1623 | 1997-05-29 | VYDAJ |
| 307733 | 1049 | 1998-09-30 | VYDAJ |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['POPLATEK MESICNE', 'LEASING']]`

**Verdict:** pred_wrong  
**Reason (one sentence):** "Debiting 3539 in total" requires summing debits grouped by k_symbol; for account 3 the LEASING orders sum to 3542 (3539+3), so no k_symbol totals 3539 and Gold's empty result is correct, whereas Predicted naively matches a single 3539 order.


---

## Item 28 (debit_card_specializing)

**Question:** What percentage of KAM customers pay in euros?

**Evidence:** Percentage of KAM uses Euro = (Total of KAM uses Euro / Total of KAM) * 100%.

**Gold SQL:**
```sql
SELECT CAST(SUM(Currency = 'EUR') AS FLOAT) * 100 / COUNT(CustomerID) FROM customers WHERE Segment = 'KAM'
```
**Predicted SQL:**
```sql
SELECT CAST(SUM(IIF(`segment` = 'KAM' AND `currency` = 'EUR', 1, 0)) AS REAL) * 100 / SUM(IIF(`segment` = 'KAM', 1, 0)) FROM `customers`
```

**Witness database:**

*customers*

| CustomerID | Segment | Currency |
|---|---|---|
| -2147483648 | KAM | NULL |

*gasstations*

| GasStationID | ChainID | Country | Segment |
|---|---|---|---|
| -2147483648 | -2147483648 | 2147483648 | 2147483648 |

*products*

| ProductID | Description |
|---|---|
| -2147483648 | 2147483648 |

*transactions_1k* (5 unreferenced columns omitted)

| TransactionID | Date | Time | CustomerID |
|---|---|---|---|
| -2147483648 | 1000-01-01 | 2147483648 | -2147483648 |

*yearmonth*

| CustomerID | Date | Consumption |
|---|---|---|
| -2147483648 | 2147483648 | 0 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[0.0]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The lone KAM customer has NULL currency, so no KAM customer uses euros (0 of 1); Predicted's IIF flags correctly yield 0.0% while Gold's SUM over the unknown NULL comparison propagates NULL instead of counting zero euro-users.


---

## Item 29 (codebase_community)

**Question:** Under the vote type of 8, provide the display names and websites URLs of the user who got the highest bounty amount.

**Evidence:** vote type of 8 refers to VoteTypeId = 8; the highest bounty amount refers to MAX(BountyAmount);

**Gold SQL:**
```sql
SELECT DisplayName, WebsiteUrl FROM users WHERE Id = ( SELECT UserId FROM votes WHERE VoteTypeId = 8 ORDER BY BountyAmount DESC LIMIT 1 )
```
**Predicted SQL:**
```sql
SELECT users.displayname, users.websiteurl FROM votes INNER JOIN users ON votes.userid = users.id WHERE votes.bountyamount = (SELECT MAX(bountyamount) FROM votes WHERE votetypeid = 8) AND votes.votetypeid = 8
```

**Witness database:**

*posts* (17 unreferenced columns omitted)

| Id | PostTypeId | AcceptedAnswerId | CreaionDate |
|---|---|---|---|
| 14 | 16 | 17 | 2000-01-09 00:00:00 |
| 4 | 44 | 45 | 2000-02-09 00:00:00 |

*users* (11 unreferenced columns omitted)

| Id | DisplayName | WebsiteUrl |
|---|---|---|
| 1 | c | d |
| 15 | t | v |
| 24 | aa | ac |
| 20 | ah | aj |
| 52 | bf | bh |
| 48 | bm | bo |
| 83 | bv | bw |
| 116 | cs | ct |

*votes* (3 unreferenced columns omitted)

| VoteTypeId | UserId | BountyAmount |
|---|---|---|
| 8 | 1 | 10 |
| 8 | 15 | 10 |
| 8 | 1 | 72 |
| 8 | 15 | 72 |
| 8 | 1 | 78 |
| 8 | 15 | 78 |
| 8 | 83 | 78 |
| 8 | 15 | 78 |
| 8 | NULL | 78 |
| 8 | 15 | 78 |
| 8 | 1 | 78 |
| NULL | 15 | 78 |
| 8 | 116 | NULL |
| 8 | 15 | NULL |

**Gold result on the witness:** `[['c', 'd']]`  
**Predicted result on the witness:** `[['c', 'd'], ['t', 'v'], ['bv', 'bw'], ['t', 'v'], ['t', 'v'], ['c', 'd']]`

**Verdict:** gold_wrong  
**Reason (one sentence):** Multiple users (1, 15, and 83) tie at the maximum bounty of 78; Predicted's equality to MAX(bountyamount) correctly returns all tied users, whereas Gold's ORDER BY...LIMIT 1 arbitrarily picks just one tied user.


---

## Item 30 (superhero)

**Question:** Count the good female superheroes.

**Evidence:** good refers to alignment.id = 1; female refers to gender.id = 2;

**Gold SQL:**
```sql
SELECT COUNT(T1.id) FROM superhero AS T1 INNER JOIN alignment AS T2 ON T1.alignment_id = T2.id INNER JOIN gender AS T3 ON T1.gender_id = T3.id WHERE T2.alignment = 'Good' AND T3.gender = 'Female'
```
**Predicted SQL:**
```sql
SELECT COUNT(superhero.id) FROM superhero INNER JOIN alignment ON superhero.alignment_id = alignment.id INNER JOIN gender ON superhero.gender_id = gender.id WHERE alignment.id = 1 AND gender.id = 2
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 2 | Bad |
| 1 | N/A |
| 3 | N/A |

*colour*

| id | colour |
|---|---|
| 2 | x1 |
| 1 | Good |
| 3 | 1 |

*gender*

| id | gender |
|---|---|
| 1 | Male |
| 2 | Male |

*publisher*

| id | publisher_name |
|---|---|
| 3 | DC Comics |
| 2 | NULL |
| 1 | ABC Studios |

*race*

| id | race |
|---|---|
| 3 | 1 |
| 2 | Female |
| 1 | 1 |

*superhero* (9 unreferenced columns omitted)

| id | gender_id | alignment_id |
|---|---|---|
| 3 | 1 | 2 |
| 1 | 2 | 1 |
| 2 | 1 | 3 |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The evidence explicitly defines good as alignment.id=1 and female as gender.id=2, so Predicted's ID-based filter correctly counts superhero 1; Gold filters on the string labels 'Good'/'Female', which match no row in the witness and returns 0.


---

## Item 31 (card_games)

**Question:** Please provide top three sets that don't appear in Magic: The Gathering Online, along with their names in in alphabetical order.

**Evidence:** don't appear in Magic: The Gathering Online refers to mtgoCode is NULL or mtgoCode = ''

**Gold SQL:**
```sql
SELECT name FROM sets WHERE mtgoCode IS NULL ORDER BY name LIMIT 3
```
**Predicted SQL:**
```sql
SELECT name FROM sets WHERE mtgoCode = '' OR mtgoCode IS NULL ORDER BY name ASC LIMIT 3
```

**Witness database:**

*cards* (70 unreferenced columns omitted)

| id | artist | asciiName | availability |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | arena |

*foreign_data* (4 unreferenced columns omitted)

| id | flavorText | language | multiverseid |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | 0 |

*legalities*

| id | format | status | uuid |
|---|---|---|---|
| 1 | 2147483648 | Restricted | 2147483648 |

*sets* (19 unreferenced columns omitted)

| mtgoCode | name |
|---|---|
|  | 2147483648 |

*set_translations*

| id | language | setCode | translation |
|---|---|---|---|
| 1 | Chinese Traditional | 2147483648 | 2147483648 |

*rulings*

| id | date | text | uuid |
|---|---|---|---|
| 1 | 0001-01-01 | 2147483648 | 2147483648 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2147483648']]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The evidence says missing MTGO means mtgoCode IS NULL OR empty string, and the witness row has an empty string, so predicted correctly includes it while gold only checks IS NULL.


---

## Item 32 (superhero)

**Question:** Between DC and Marvel Comics, which publisher has published more superheroes? Find the difference in the number of superheroes they have published.

**Evidence:** DC refers to publisher_name = 'DC Comics'; Marvel Comics refers to publisher_name = 'Marvel Comics'; calculation = SUBTRACT(SUM(publisher_name = 'Marvel Comics'), SUM(publisher_name = 'DC Comics'))

**Gold SQL:**
```sql
SELECT SUM(CASE WHEN T2.publisher_name = 'Marvel Comics' THEN 1 ELSE 0 END) - SUM(CASE WHEN T2.publisher_name = 'DC Comics' THEN 1 ELSE 0 END) FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id
```
**Predicted SQL:**
```sql
SELECT COUNT(CASE WHEN p.publisher_name = 'Marvel Comics' THEN s.id ELSE NULL END) - COUNT(CASE WHEN p.publisher_name = 'DC Comics' THEN s.id ELSE NULL END) AS difference FROM publisher p JOIN superhero s ON p.id = s.publisher_id WHERE p.publisher_name IN ('Marvel Comics', 'DC Comics');
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 1 | Good |

*colour*

| id | colour |
|---|---|
| 1 | No Colour |

*gender*

| id | gender |
|---|---|
| 2 | Female |

*publisher*

| id | publisher_name |
|---|---|
| 6 | Hanna-Barbera |
| 5 | George Lucas |
| 12 | J. R. R. Tolkien |
| 21 | SyFy |

*race*

| id | race |
|---|---|
| 24 | Human |

*superhero* (10 unreferenced columns omitted)

| id | publisher_id |
|---|---|
| 613 | NULL |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[0]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** With zero superheroes from either publisher the numeric difference is 0 (predicted COUNT), not NULL (gold SUM over an empty inner join).


---

## Item 33 (california_schools)

**Question:** What is the lowest grade for the District Special Education Consortia School with National Center for Educational Statistics school district identification number of 0613360?

**Evidence:** District Special Education Consortia School refers to EdOpsCode = 'SPECON'.

**Gold SQL:**
```sql
SELECT MIN(T1.`Low Grade`) FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.NCESDist = '0613360' AND T2.EdOpsCode = 'SPECON'
```
**Predicted SQL:**
```sql
SELECT T2.`Low Grade` FROM schools AS T1 INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.NCESDist = '0613360' AND T1.EdOpsName = 'District Special Education Consortia School' ORDER BY T2.`Low Grade` ASC LIMIT 1
```

**Witness database:**

*frpm* (27 unreferenced columns omitted)

| CDSCode | Low Grade |
|---|---|
| 30666476030043 | 7 |
| 41689166043780 | 6 |
| 31668943132453 | 9 |
| 01611766000830 | K |

*schools* (45 unreferenced columns omitted)

| CDSCode | NCESDist | EdOpsCode | EdOpsName |
|---|---|---|---|
| 19646676108393 | 0620880 | TRAD | Traditional |
| 37684116098065 | 0638640 | NULL | NULL |
| 06616146103576 | 0630360 | TRAD | Traditional |
| 30666476030043 | 0630660 | TRAD | Traditional |
| 41689166043780 | 0618870 | TRAD | Traditional |
| 31668943132453 | 0630750 | TRAD | Traditional |
| 01611766000830 | 0614400 | TRAD | Traditional |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[]`

**Verdict:** pred_wrong  
**Reason (one sentence):** The question asks for the lowest grade (MIN); gold uses MIN returning a scalar NULL, while predicted's ORDER BY LIMIT 1 returns no rows when the school is absent.


---

## Item 34 (formula_1)

**Question:** What was the fastest lap speed among all drivers in the 2009 Spanish Grand Prix?

**Evidence:** the fastest lap speed among all refers to max(fastestLapSpeed); Spanish Grand Prix refers to races.name = 'Spanish Grand Prix';

**Gold SQL:**
```sql
SELECT T2.fastestLapSpeed FROM races AS T1 INNER JOIN results AS T2 ON T2.raceId = T1.raceId WHERE T1.name = 'Spanish Grand Prix' AND T1.year = 2009 AND T2.fastestLapSpeed IS NOT NULL ORDER BY T2.fastestLapSpeed DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT MAX(`results`.`fastestlapspeed`) FROM `results` INNER JOIN `races` ON `results`.`raceid` = `races`.`raceid` WHERE `races`.`year` = 2009 AND `races`.`name` = 'Spanish Grand Prix'
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 6 | monaco | Circuit de Monaco | Monte-Carlo |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 18 | minardi | Minardi | Italian |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 69 | badoer | NULL | BAD |

*races* (5 unreferenced columns omitted)

| raceId | year | name |
|---|---|---|
| 178 | 1999 | Monaco Grand Prix |

*results* (16 unreferenced columns omitted)

| raceId | fastestLapSpeed |
|---|---|
| 178 | NULL |

*seasons*

| year | url |
|---|---|
| 1999 | http://en.wikipedia.org/wiki/1999_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 6 | Gearbox |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The evidence defines fastest as MAX(fastestLapSpeed); predicted uses MAX returning a scalar NULL, while gold's ORDER BY DESC LIMIT 1 returns no rows.


---

## Item 35 (toxicology)

**Question:** Among all the atoms from 21 to 25, list all the molecules that are carcinogenic.

**Evidence:** atoms from 21 to 25 refers to SUBSTR(atom_id, 7, 2) between '21' and '25'; label = '+' mean molecules are carcinogenic

**Gold SQL:**
```sql
SELECT DISTINCT T2.molecule_id FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE SUBSTR(T1.atom_id, -2) BETWEEN '21' AND '25' AND T2.label = '+'
```
**Predicted SQL:**
```sql
SELECT DISTINCT a.molecule_id FROM atom a JOIN (SELECT molecule_id FROM molecule WHERE label = '+') m ON a.molecule_id = m.molecule_id WHERE SUBSTR(a.atom_id, 7, 2) BETWEEN '21' AND '25' ORDER BY a.molecule_id
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| atom_id | molecule_id |
|---|---|
| 4444424 | 4 |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
|  | 4 |  |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| 4444424 | 4444424 |  |

*molecule*

| molecule_id | label |
|---|---|
| 4 | + |

**Gold result on the witness:** `[['4']]`  
**Predicted result on the witness:** `[]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The evidence defines the atom range via SUBSTR(atom_id,7,2); predicted uses that expression while gold incorrectly uses SUBSTR(atom_id,-2).


---

## Item 36 (thrombosis_prediction)

**Question:** For the patients with an abnormal Ig M level, what is the most common disease they are diagnosed with?

**Evidence:** abnormal Ig M level refers to IGM <=40 OR IGM >= 400; most common disease refers to MAX(COUNT(Diagnosis));

**Gold SQL:**
```sql
SELECT T1.Diagnosis FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.IGM NOT BETWEEN 40 AND 400 GROUP BY T1.Diagnosis ORDER BY COUNT(T1.Diagnosis) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT `patient`.`diagnosis` FROM `laboratory` INNER JOIN `patient` ON `laboratory`.`id` = `patient`.`id` WHERE `laboratory`.`igm` <= 40 OR `laboratory`.`igm` >= 400 GROUP BY `patient`.`diagnosis` ORDER BY COUNT(`patient`.`diagnosis`) DESC LIMIT 1
```

**Witness database:**

*Examination* (9 unreferenced columns omitted)

| ID | Examination Date | aCL IgG | aCL IgM |
|---|---|---|---|
| 1 | 0001-01-01 | 0 | 0 |

*Patient* (5 unreferenced columns omitted)

| ID | Diagnosis |
|---|---|
| 1 | 2147483648 |

*Laboratory* (42 unreferenced columns omitted)

| ID | IGM |
|---|---|
| 1 | 400 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2147483648']]`

**Verdict:** gold_wrong  
**Reason (one sentence):** Abnormal IgM is inclusive (<=40 OR >=400 per evidence); predicted includes IGM=400, while gold's NOT BETWEEN 40 AND 400 wrongly excludes the endpoint 400.


---

## Item 37 (student_club)

**Question:** Which college do most of the members go to?

**Evidence:** college most members go refers to MAX(COUNT(major.college))

**Gold SQL:**
```sql
SELECT T2.college FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id GROUP BY T2.major_id ORDER BY COUNT(T2.college) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT major.college FROM member JOIN major ON member.link_to_major = major.major_id GROUP BY major.college ORDER BY COUNT(member.member_id) DESC LIMIT 1
```

**Witness database:**

*event* (3 unreferenced columns omitted)

| event_id | event_name | event_date | type |
|---|---|---|---|
| 2147483648 | 2147483648 | 2147483648 | 2147483648 |
| 2147483651 | 2147483648 | 2147483648 | 2147483648 |
| 2147483650 | 2147483648 | 2147483648 | 2147483648 |
| 2147483649 | 2147483648 | 2147483648 | 2147483648 |

*major* (2 unreferenced columns omitted)

| major_id | college |
|---|---|
| 2147483648 | NULL |
| 2147483649 | NULL |
| 2147483650 | NULL |
| 2147483651 | 2147483649 |

*zip_code* (2 unreferenced columns omitted)

| zip_code | type | city | county |
|---|---|---|---|
| 0 | 2147483648 | 2147483648 | 2147483648 |
| -1 | 2147483648 | 2147483648 | 2147483648 |
| 2 | 2147483648 | 2147483648 | 2147483648 |
| 1 | 2147483648 | 2147483648 | 2147483648 |

*attendance*

| link_to_event | link_to_member |
|---|---|
| 2147483650 | 2147483650 |
| 2147483649 | 2147483648 |
| 2147483651 | 2147483651 |
| 2147483648 | 2147483649 |

*budget* (3 unreferenced columns omitted)

| budget_id | category | spent | remaining |
|---|---|---|---|
| 2147483650 | 2147483648 | 0 | 0 |
| 2147483651 | 2147483648 | 0 | 0 |
| 2147483649 | 2147483648 | 0 | 0 |
| 2147483648 | 2147483648 | 0 | 0 |

*expense* (3 unreferenced columns omitted)

| expense_id | expense_description | expense_date | cost |
|---|---|---|---|
| 2147483648 | 2147483648 | 2147483648 | 0 |
| 2147483649 | 2147483648 | 2147483648 | 0 |
| 2147483650 | 2147483648 | 2147483648 | 0 |
| 2147483651 | 2147483648 | 2147483648 | 0 |

*income* (2 unreferenced columns omitted)

| income_id | date_received | amount | source |
|---|---|---|---|
| 2147483650 | 2147483648 | 0 | 2147483648 |
| 2147483648 | 2147483648 | 0 | 2147483648 |
| 2147483649 | 2147483648 | 0 | 2147483648 |
| 2147483651 | 2147483648 | 0 | 2147483648 |

*member* (7 unreferenced columns omitted)

| member_id | link_to_major |
|---|---|
| 2147483651 | 2147483649 |
| 2147483650 | 2147483650 |
| 2147483648 | 2147483651 |
| 2147483649 | 2147483650 |

**Gold result on the witness:** `[['2147483649']]`  
**Predicted result on the witness:** `[[None]]`

**Verdict:** pred_wrong  
**Reason (one sentence):** Members with NULL college do not belong to any college; gold counts non-NULL colleges, while predicted counts all members including the NULL-college group.


---

## Item 38 (debit_card_specializing)

**Question:** Which country's gas station had the first paid cusomer in 2012/8/25?

**Evidence:** '2012/8/25' can be represented by '2012-08-25'

**Gold SQL:**
```sql
SELECT T2.Country FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T1.Date = '2012-08-25' ORDER BY T1.Time DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT `gasstations`.`country` FROM `transactions_1k` INNER JOIN `gasstations` ON `transactions_1k`.`gasstationid` = `gasstations`.`gasstationid` WHERE `transactions_1k`.`date` = '2012-08-25' ORDER BY `transactions_1k`.`time` ASC LIMIT 1
```

**Witness database:**

*customers*

| CustomerID | Segment | Currency |
|---|---|---|
| 1336 | SME | CZK |
| 1344 | SME | CZK |
| 30895 | LAM | CZK |
| 48664 | LAM | CZK |

*gasstations* (2 unreferenced columns omitted)

| GasStationID | Country |
|---|---|
| 1337 | SVK |
| 1345 | CZE |

*products*

| ProductID | Description |
|---|---|
| 1338 | Pelovy filt. |
| 1346 | Pelovy filt. |

*transactions_1k* (6 unreferenced columns omitted)

| Date | Time | GasStationID |
|---|---|---|
| 2012-08-25 | 13:52:00 | 1337 |
| 2012-08-25 | 08:26:00 | 1345 |

**Gold result on the witness:** `[['SVK']]`  
**Predicted result on the witness:** `[['CZE']]`

**Verdict:** gold_wrong  
**Reason (one sentence):** "First" customer means earliest time (ASC); predicted uses ASC to get 08:26 CZE, while gold's DESC gets the latest 13:52 SVK.


---

## Item 39 (codebase_community)

**Question:** How many users were awarded with 'Citizen Patrol' badge?

**Evidence:** Citizen Patrol' is the name of the badge;

**Gold SQL:**
```sql
SELECT COUNT(id) FROM badges WHERE `Name` = 'Citizen Patrol'
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT UserId) AS NumberOfUsers FROM badges WHERE Name = 'Citizen Patrol'
```

**Witness database:**

*badges* (1 unreferenced columns omitted)

| Id | UserId | Name |
|---|---|---|
| 3 | 3 | Citizen Patrol |
| 1 | 3 | Citizen Patrol |

*users* (10 unreferenced columns omitted)

| Id | Reputation | CreationDate | DisplayName |
|---|---|---|---|
| 3 | -1 | 2010-06-15 12:30:00 | b |

**Gold result on the witness:** `[[2]]`  
**Predicted result on the witness:** `[[1]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The question asks for the number of distinct users; predicted's COUNT(DISTINCT UserId)=1 is correct, while gold counts badge award records (=2).


---

## Item 40 (card_games)

**Question:** Which card costs more converted mana, "Serra Angel" or "Shrine Keeper"?

**Evidence:** "Serra Angel" refers to name = 'Serra Angel'; "Shrine Keeper" refers to name = 'Shrine Keeper'; card costs more converted mana when the value of convertedManaCost is greater

**Gold SQL:**
```sql
SELECT name FROM cards WHERE name IN ('Serra Angel', 'Shrine Keeper') ORDER BY convertedManaCost DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT CASE WHEN ( SELECT T1.convertedManaCost FROM cards AS T1 WHERE T1.name = 'Serra Angel' ) > ( SELECT T1.convertedManaCost FROM cards AS T1 WHERE T1.name = 'Shrine Keeper' ) THEN 'Serra Angel' ELSE 'Shrine Keeper' END
```

**Witness database:**

*cards* (72 unreferenced columns omitted)

| convertedManaCost | name |
|---|---|
| 1.0 | Serra Angel |
| NULL | Serra Angel |
| NULL | Shrine Keeper |
| NULL | Shrine Keeper |
| NULL | NULL |

**Gold result on the witness:** `[['Serra Angel']]`  
**Predicted result on the witness:** `[['Shrine Keeper']]`

**Verdict:** pred_wrong  
**Reason (one sentence):** Serra Angel has cost 1.0 while Shrine Keeper is all NULL; gold's ORDER BY DESC correctly picks Serra Angel, while predicted's multi-row scalar subquery falls through to ELSE Shrine Keeper.


---

## Item 41 (student_club)

**Question:** What is the amount of the funds that the Vice President received?

**Evidence:** 'Vice President' is a position of Student Club; funds received refers to amount.

**Gold SQL:**
```sql
SELECT T2.amount FROM member AS T1 INNER JOIN income AS T2 ON T1.member_id = T2.link_to_member WHERE T1.position = 'Vice President'
```
**Predicted SQL:**
```sql
SELECT SUM(income.amount) AS total_funds FROM income INNER JOIN member ON income.link_to_member = member.member_id WHERE member.position = 'Vice President'
```

**Witness database:**

*major*

| major_id | major_name | department | college |
|---|---|---|---|
| recxK3MHQFbR9J5uO | q | r | College of Agriculture and Applied Sciences |

*zip_code* (2 unreferenced columns omitted)

| zip_code | type | city | county |
|---|---|---|---|
| 3 | Unique | u | v |
| 1 | Unique | aa | ab |

*income* (4 unreferenced columns omitted)

| amount | link_to_member |
|---|---|
| 2 | a |
| 4 | a0 |
| 4 | ab |
| 5 | NULL |
| NULL | ao |

*member* (7 unreferenced columns omitted)

| member_id | position |
|---|---|
| a | Vice President |
| a0 | Vice President |
| ab | Vice President |
| ao | Vice President |

**Gold result on the witness:** `[[2], [4], [4], [None]]`  
**Predicted result on the witness:** `[[10]]`

**Verdict:** pred_wrong  
**Reason (one sentence):** The evidence maps funds received to the amount column with no aggregation; gold lists the amounts, while predicted incorrectly sums them.


---

## Item 42 (european_football_2)

**Question:** When is the birthday of the football player who has the highest overall rating?

**Evidence:** football player who has the highest overall rating refers to MAX(overall_rating);

**Gold SQL:**
```sql
SELECT t1.birthday FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id ORDER BY t2.overall_rating DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T2.birthday FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_fifa_api_id = T2.player_fifa_api_id ORDER BY T1.overall_rating DESC LIMIT 1
```

**Witness database:**

*Player_Attributes* (39 unreferenced columns omitted)

| player_fifa_api_id | player_api_id | overall_rating |
|---|---|---|
| 1 | 2625 | 0 |
| 0 | 2625 | 1 |

*Player* (4 unreferenced columns omitted)

| player_api_id | player_fifa_api_id | birthday |
|---|---|---|
| 2624 | 0 | 2147483649 |
| 2625 | 1 | 2147483648 |

*League*

| id | country_id | name |
|---|---|---|
| 0 | 0 | 2147483648 |
| 1 | 0 | 2147483648 |

*Country*

| id | name |
|---|---|
| 1 | 2147483648 |
| 0 | 2147483648 |

*Team* (1 unreferenced columns omitted)

| id | team_api_id | team_fifa_api_id | team_long_name |
|---|---|---|---|
| 2 | -1 | 0 | 2147483648 |
| 1 | 0 | 1 | 2147483649 |

*Team_Attributes* (21 unreferenced columns omitted)

| id | team_fifa_api_id | team_api_id | date |
|---|---|---|---|
| 1 | 0 | -1 | 2147483648 |
| 2 | 1 | 0 | 2147483648 |

*Match* (111 unreferenced columns omitted)

| id | country_id | league_id | season |
|---|---|---|---|
| 2 | 1 | 1 | 2147483648 |
| 1 | 1 | 1 | 2147483648 |

**Gold result on the witness:** `[['2147483648']]`  
**Predicted result on the witness:** `[['2147483649']]`

**Verdict:** pred_wrong  
**Reason (one sentence):** The correct join between Player and Player_Attributes is player_api_id; gold uses it, while predicted wrongly joins on player_fifa_api_id.


---

## Item 43 (european_football_2)

**Question:** In the 2015–2016 season, how many games were played in the Italian Serie A league?

**Evidence:** In the 2015–2016 season refers to season = '2015/2016'

**Gold SQL:**
```sql
SELECT COUNT(t2.id) FROM League AS t1 INNER JOIN Match AS t2 ON t1.id = t2.league_id WHERE t1.name = 'Italy Serie A' AND t2.season = '2015/2016'
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM Match WHERE season = '2015/2016' AND league_id = (SELECT id FROM League WHERE name = 'Italy Serie A');
```

**Witness database:**

*Country*

| id | name |
|---|---|
| 10257 | Italy |

*League* (1 unreferenced columns omitted)

| id | name |
|---|---|
| 1001 | Italy Serie A |
| 10257 | Italy Serie A |

*Match* (112 unreferenced columns omitted)

| id | league_id | season |
|---|---|---|
| 12947 | 10257 | 2015/2016 |
| 13272 | 10257 | 2015/2016 |
| 1002 | 10257 | 2015/2016 |
| 1003 | 10257 | 2015/2016 |

*Team* (1 unreferenced columns omitted)

| id | team_api_id | team_fifa_api_id | team_long_name |
|---|---|---|---|
| 20518 | 10233 | 110556 | Genoa |
| 20527 | 9882 | 1837 | Sampdoria |

*Team_Attributes* (21 unreferenced columns omitted)

| id | team_fifa_api_id | team_api_id | date |
|---|---|---|---|
| 491 | 110556 | 10233 | 2010-02-22 00:00:00 |
| 1125 | 1837 | 9882 | 2010-02-22 00:00:00 |

**Gold result on the witness:** `[[4]]`  
**Predicted result on the witness:** `[[0]]`

**Verdict:** pred_wrong  
**Reason (one sentence):** The Italy Serie A league (id 10257) has 4 matches; gold's JOIN counts 4, while predicted's scalar subquery picks the duplicate id 1001 which has no matches.


---

## Item 44 (thrombosis_prediction)

**Question:** What is the most common sign of patients with SLE disease?

**Evidence:** the most common sign refers to MAX(symptoms); 'SLE' refers to diagnosis

**Gold SQL:**
```sql
SELECT Symptoms FROM Examination WHERE Diagnosis = 'SLE' GROUP BY Symptoms ORDER BY COUNT(Symptoms) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.Symptoms FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T2.Diagnosis = 'SLE' GROUP BY T1.Symptoms ORDER BY COUNT(T1.Symptoms) DESC LIMIT 1
```

**Witness database:**

*Examination* (10 unreferenced columns omitted)

| ID | Diagnosis | Symptoms |
|---|---|---|
| 1 | 2147483648 | 2147483648 |

*Patient* (5 unreferenced columns omitted)

| ID | Diagnosis |
|---|---|
| 1 | SLE |

*Laboratory* (40 unreferenced columns omitted)

| ID | Date | GOT | GPT |
|---|---|---|---|
| 1 | 0001-01-01 | 0 | 0 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2147483648']]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The SLE diagnosis is on the Patient table; predicted joins Patient and filters Patient.Diagnosis='SLE', while gold filters Examination.Diagnosis which is not 'SLE'.


---

## Item 45 (student_club)

**Question:** Which college is the vice president of the Student_Club from?

**Evidence:** Vice President is a position of the Student Club

**Gold SQL:**
```sql
SELECT T2.college FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id WHERE T1.position LIKE 'vice president'
```
**Predicted SQL:**
```sql
SELECT m.college FROM member mb JOIN major m ON mb.link_to_major = m.major_id WHERE mb.position = 'Vice President';
```

**Witness database:**

*major* (2 unreferenced columns omitted)

| major_id | college |
|---|---|
| recxK3MHQFbR9J5uO | College of Agriculture and Applied Sciences |
| a | College of Agriculture and Applied Sciences |

*zip_code* (2 unreferenced columns omitted)

| zip_code | type | city | county |
|---|---|---|---|
| 1 | Unique | o | p |

*member* (7 unreferenced columns omitted)

| position | link_to_major |
|---|---|
| vice president | recxK3MHQFbR9J5uO |
| vice president | NULL |
| avice president | recxK3MHQFbR9J5uO |
| NULL | a |

**Gold result on the witness:** `[['College of Agriculture and Applied Sciences']]`  
**Predicted result on the witness:** `[]`

**Verdict:** pred_wrong  
**Reason (one sentence):** The position value is lowercase 'vice president'; gold's LIKE matches it, while predicted's case-sensitive equality with capital 'Vice President' matches nothing.


---

## Item 46 (formula_1)

**Question:** Which was Lewis Hamilton first race? What was his points recorded for his first race event?

**Evidence:** first race refers to min(Year); Lewis Hamiltonrefers to the full name of the driver; Full name of the driver refers to drivers.forename and drivers.surname;

**Gold SQL:**
```sql
SELECT T1.name, T2.points FROM races AS T1 INNER JOIN driverStandings AS T2 ON T2.raceId = T1.raceId INNER JOIN drivers AS T3 ON T3.driverId = T2.driverId WHERE T3.forename = 'Lewis' AND T3.surname = 'Hamilton' ORDER BY T1.year ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.name, T2.points FROM races AS T1 INNER JOIN results AS T2 ON T1.raceId = T2.raceId INNER JOIN drivers AS T3 ON T2.driverId = T3.driverId WHERE T3.forename = 'Lewis' AND T3.surname = 'Hamilton' ORDER BY T1.year LIMIT 1
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 3 | bahrain | Bahrain International Circuit | Sakhir |
| 17 | shanghai | Shanghai International Circuit | Shanghai |
| 19 | indianapolis | Indianapolis Motor Speedway | Indianapolis |
| 1 | reims | Reims-Gueux | Reims |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 1 | mclaren | McLaren | British |
| 2 | bmw_sauber | BMW Sauber | German |
| 20 | prost | Prost | French |

*driverStandings* (4 unreferenced columns omitted)

| raceId | driverId | points |
|---|---|---|
| 1 | 3 | 14.0 |
| 3 | 1 | 18.0 |

*drivers* (6 unreferenced columns omitted)

| driverId | forename | surname |
|---|---|---|
| 2 | Johnny | Lewis |
| 3 | Nico | Rosberg |
| 1 | Lewis | Hamilton |

*races* (5 unreferenced columns omitted)

| raceId | year | name |
|---|---|---|
| 2 | 1952 | South African Grand Prix |
| 1 | 2009 | Australian Grand Prix |
| 3 | 2009 | Chinese Grand Prix |
| 172 | 2000 | United States Grand Prix |

*results* (15 unreferenced columns omitted)

| raceId | driverId | points |
|---|---|---|
| 2 | 3 | 0.0 |
| 2 | 1 | 1.0 |
| 172 | 2 | 0.0 |

*seasons*

| year | url |
|---|---|
| 1952 | http://en.wikipedia.org/wiki/1952_Formula_One_season |
| 2009 | http://en.wikipedia.org/wiki/2009_Formula_One_season |
| 2000 | http://en.wikipedia.org/wiki/2000_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 1 | Finished |
| 3 | Accident |
| 2 | Disqualified |
| 11 | +1 Lap |

**Gold result on the witness:** `[['Chinese Grand Prix', 18.0]]`  
**Predicted result on the witness:** `[['South African Grand Prix', 1.0]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The predicted query correctly uses the results table for per-race participation and points earned in Hamilton's first race, while the gold incorrectly uses driverStandings which records cumulative championship standing points rather than race-event points.


---

## Item 47 (student_club)

**Question:** What are the zip codes that have post office boxes in the country of the country of San Juan Municipio whose state is Puerto Rico?

**Evidence:** zip codes that have post office boxes refers to type = 'PO Box'

**Gold SQL:**
```sql
SELECT zip_code FROM zip_code WHERE type = 'PO Box' AND county = 'San Juan Municipio' AND state = 'Puerto Rico'
```
**Predicted SQL:**
```sql
SELECT zip_code FROM zip_code WHERE type = 'PO Box' AND city = 'San Juan' AND county = 'San Juan Municipio' AND state = 'Puerto Rico'
```

**Witness database:**

*zip_code* (1 unreferenced columns omitted)

| zip_code | type | city | county | state |
|---|---|---|---|---|
| 1002 | PO Box | San Juan  | San Juan Municipio | Puerto Rico |

**Gold result on the witness:** `[[1002]]`  
**Predicted result on the witness:** `[]`

**Verdict:** pred_wrong  
**Reason (one sentence):** The predicted adds an extra city='San Juan' filter that the question and evidence never require, and it fails to match because the stored city value 'San Juan ' has a trailing space, yielding an empty result.


---

## Item 48 (financial)

**Question:** The average unemployment ratio of 1995 and 1996, which one has higher percentage?

**Evidence:** A12 refers to unemploymant rate 1995; A13 refers to unemploymant rate 1996

**Gold SQL:**
```sql
SELECT DISTINCT IIF(AVG(A13) > AVG(A12), '1996', '1995') FROM district
```
**Predicted SQL:**
```sql
SELECT CASE WHEN CAST(AVG(A12) AS FLOAT) > CAST(AVG(A13) AS FLOAT) THEN '1995' ELSE '1996' END AS year_with_higher_unemployment FROM district;
```

**Witness database:**

*account*

| account_id | district_id | frequency | date |
|---|---|---|---|
| 1 | 1 | POPLATEK TYDNE | 0001-01-01 |

*card*

| card_id | disp_id | type | issued |
|---|---|---|---|
| 0 | 1 | gold | 0001-01-01 |

*client*

| client_id | gender | birth_date | district_id |
|---|---|---|---|
| 1 | M | 0001-01-01 | 1 |

*disp*

| disp_id | client_id | account_id | type |
|---|---|---|---|
| 1 | 1 | 1 | DISPONENT |

*district* (14 unreferenced columns omitted)

| A12 | A13 |
|---|---|
| 0 | 0 |

*loan* (3 unreferenced columns omitted)

| loan_id | account_id | date | amount |
|---|---|---|---|
| 1 | 1 | 0001-01-01 | 0 |

*order* (2 unreferenced columns omitted)

| order_id | account_id | bank_to | account_to |
|---|---|---|---|
| 1 | 1 | 2147483648 | 0 |

*trans* (6 unreferenced columns omitted)

| trans_id | account_id | date | type |
|---|---|---|---|
| 1 | 1 | 0001-01-01 | VYBER |

**Gold result on the witness:** `[['1995']]`  
**Predicted result on the witness:** `[['1996']]`

**Verdict:** ambiguous  
**Reason (one sentence):** When the averaged unemployment rates are exactly equal (both 0), the two queries apply opposite tie-breaking defaults (gold defaults to 1995, predicted defaults to 1996), and the question does not specify how to handle a tie.


---

## Item 49 (european_football_2)

**Question:** Find the average number of long-shot done by Ahmed Samir Farag.

**Evidence:** average number of long shot = DIVIDE(SUM(long_shots), COUNT(player_fifa_api_id));

**Gold SQL:**
```sql
SELECT CAST(SUM(t2.long_shots) AS REAL) / COUNT(t2.`date`) FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t1.player_name = 'Ahmed Samir Farag'
```
**Predicted SQL:**
```sql
SELECT CAST(SUM(T1.long_shots) AS REAL) / COUNT(T1.player_fifa_api_id) FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.player_name = 'Ahmed Samir Farag'
```

**Witness database:**

*Player* (5 unreferenced columns omitted)

| player_api_id | player_name |
|---|---|
| -1 | Ahmed Samir Farag |
| -1 | Ahmed Samir Farag |
| -1 | Ahmed Samir Farag |

*Player_Attributes* (38 unreferenced columns omitted)

| player_fifa_api_id | player_api_id | date | long_shots |
|---|---|---|---|
| 1026 | -1 | NULL | 1029 |
| NULL | -1 | NULL | NULL |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[1029.0]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The evidence explicitly defines the denominator as COUNT(player_fifa_api_id), but the gold uses COUNT(date) which is 0 because all date values are NULL, causing division by zero; the predicted correctly uses COUNT(player_fifa_api_id)=3.


---

## Item 50 (formula_1)

**Question:** Which driver created the fastest lap speed in a Formula_1 race? Please give both his forename and surname.

**Evidence:** -

**Gold SQL:**
```sql
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId WHERE T2.fastestLapTime IS NOT NULL ORDER BY T2.fastestLapSpeed DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId ORDER BY T2.fastestLapSpeed DESC LIMIT 1
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 10 | hockenheimring | Hockenheimring | Hockenheim |
| 39 | zandvoort | Circuit Park Zandvoort | Zandvoort |
| 6 | monaco | Circuit de Monaco | Monte-Carlo |
| 18 | interlagos | Autódromo José Carlos Pace | São Paulo |
| 9 | silverstone | Silverstone Circuit | Silverstone |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 25 | tyrrell | Tyrrell | British |
| 4 | renault | Renault | French |
| 1 | mclaren | McLaren | British |
| 133 | hwm | HWM | British |
| 34 | brabham | Brabham | British |
| 151 | era | ERA | British |

*drivers* (6 unreferenced columns omitted)

| driverId | forename | surname |
|---|---|---|
| 758 | Dries | van der Lof |
| 132 | Giovanna | Amati |
| 666 | Tony | Rolt |
| 191 | Mike | Thackwell |
| 219 | Jean-Pierre | Jabouille |
| 57 | Mika | Häkkinen |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 446 | 1984 | 11 | 10 |
| 508 | 1980 | 11 | 39 |
| 260 | 1994 | 4 | 6 |
| 823 | 1952 | 7 | 39 |
| 291 | 1992 | 3 | 18 |
| 833 | 1950 | 1 | 9 |

*results* (15 unreferenced columns omitted)

| driverId | fastestLapTime | fastestLapSpeed |
|---|---|---|
| 191 | NULL | NULL |
| 219 | NULL | NULL |
| 57 | NULL | NULL |
| 758 | NULL | NULL |
| 132 | NULL | NULL |
| 666 | NULL | NULL |

*seasons*

| year | url |
|---|---|
| 1984 | http://en.wikipedia.org/wiki/1984_Formula_One_season |
| 1980 | http://en.wikipedia.org/wiki/1980_Formula_One_season |
| 1994 | http://en.wikipedia.org/wiki/1994_Formula_One_season |
| 1952 | http://en.wikipedia.org/wiki/1952_Formula_One_season |
| 1992 | http://en.wikipedia.org/wiki/1992_Formula_One_season |
| 1950 | http://en.wikipedia.org/wiki/1950_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 81 | Did not qualify |
| 64 | Handling |
| 4 | Collision |
| 62 | Not classified |
| 6 | Gearbox |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['Mika', 'Häkkinen']]`

**Verdict:** pred_wrong  
**Reason (one sentence):** All fastestLapSpeed values are NULL in the witness, so no valid fastest lap exists; the gold correctly filters with IS NOT NULL and returns empty, while the predicted returns an arbitrary driver (Mika Häkkinen) from ordering NULLs.


---

## Item 51 (thrombosis_prediction)

**Question:** For the patients with an abnormal Ig M level, what is the most common disease they are diagnosed with?

**Evidence:** abnormal Ig M level refers to IGM <=40 OR IGM >= 400; most common disease refers to MAX(COUNT(Diagnosis));

**Gold SQL:**
```sql
SELECT T1.Diagnosis FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.IGM NOT BETWEEN 40 AND 400 GROUP BY T1.Diagnosis ORDER BY COUNT(T1.Diagnosis) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT P.Diagnosis FROM Patient AS P INNER JOIN Laboratory AS L ON P.ID = L.ID WHERE L.IGM <= 40 OR L.IGM >= 400 GROUP BY P.Diagnosis ORDER BY COUNT(*) DESC LIMIT 1;
```

**Witness database:**

*Laboratory* (42 unreferenced columns omitted)

| ID | IGM |
|---|---|
| 1001 | 400 |

*Patient* (5 unreferenced columns omitted)

| ID | Diagnosis |
|---|---|
| 174116 | SLE, AIHA |
| 1001 | PM |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['PM']]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The evidence defines abnormal IgM as IGM >= 400 (inclusive), but the gold uses NOT BETWEEN 40 AND 400 which excludes the boundary value 400; the predicted correctly uses IGM <= 40 OR IGM >= 400 and includes patient ID 1001.


---

## Item 52 (formula_1)

**Question:** Which was the fastest lap for Lewis Hamilton in the 2008 Australian Grand Prix?

**Evidence:** -

**Gold SQL:**
```sql
SELECT T1.fastestLap FROM results AS T1 INNER JOIN races AS T2 on T1.raceId = T2.raceId INNER JOIN drivers AS T3 on T1.driverId = T3.driverId WHERE T2.name = 'Australian Grand Prix' AND T2.year = 2008 AND T3.forename = 'Lewis' AND T3.surname = 'Hamilton'
```
**Predicted SQL:**
```sql
SELECT lap FROM lapTimes JOIN races ON lapTimes.raceId = races.raceId JOIN drivers ON lapTimes.driverId = drivers.driverId WHERE races.year = 2008 AND races.name = 'Australian Grand Prix' AND drivers.forename = 'Lewis' AND drivers.surname = 'Hamilton' ORDER BY lapTimes.milliseconds LIMIT 1;
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 1065 | hungaroring | Hungaroring | Budapest |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 1066 | fry | Fry | British |

*drivers* (6 unreferenced columns omitted)

| driverId | forename | surname |
|---|---|---|
| 1067 | Lewis | Hamilton |

*lapTimes* (2 unreferenced columns omitted)

| raceId | driverId | lap | milliseconds |
|---|---|---|---|
| 1068 | 1067 | 1069 | 80450 |

*races* (5 unreferenced columns omitted)

| raceId | year | name |
|---|---|---|
| 1068 | 2008 | Australian Grand Prix |

*results* (15 unreferenced columns omitted)

| raceId | driverId | fastestLap |
|---|---|---|
| 1068 | 1067 | 40 |

*seasons*

| year | url |
|---|---|
| 2008 | http://en.wikipedia.org/wiki/2008_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 1 | Finished |

**Gold result on the witness:** `[[40]]`  
**Predicted result on the witness:** `[[1069]]`

**Verdict:** pred_wrong  
**Reason (one sentence):** The question asks for the fastest lap of the race as recorded in results.fastestLap (=40), but the predicted queries the lapTimes table and returns the lap number 1069 from a single lap-time row instead of the official race result.


---

## Item 53 (codebase_community)

**Question:** What is the average number of badges obtained by a user with over 200 views?

**Evidence:** user with over 200 views refers to Views > 200; average number of badges = Divide (Count(Id), Count(DisplayName))

**Gold SQL:**
```sql
SELECT CAST(COUNT(T1.Id) AS REAL) / COUNT(DISTINCT T2.DisplayName) FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.Views > 200
```
**Predicted SQL:**
```sql
SELECT CAST(COUNT(badges.id) AS REAL) / COUNT(DISTINCT badges.userid) AS averagebadges FROM badges INNER JOIN users ON badges.userid = users.id WHERE users.views > 200
```

**Witness database:**

*badges* (2 unreferenced columns omitted)

| Id | UserId |
|---|---|
| 17962 | 10026 |
| 83892 | 10026 |
| 1012 | 1011 |
| 1013 | 1011 |

*users* (11 unreferenced columns omitted)

| Id | DisplayName | Views |
|---|---|---|
| 10026 | gregmacfarlane | 214 |
| 1011 | gregmacfarlane | 214 |

**Gold result on the witness:** `[[4.0]]`  
**Predicted result on the witness:** `[[2.0]]`

**Verdict:** implausible_data  
**Reason (one sentence):** Two distinct users (Id 10026 and 1011) share the exact same DisplayName 'gregmacfarlane', which is unrealistic for a forum; this causes the gold's COUNT(DISTINCT DisplayName)=1 to differ from the predicted's COUNT(DISTINCT UserId)=2.


---

## Item 54 (toxicology)

**Question:** How many double bonds does TR006 have and is it carcinogenic?

**Evidence:** label = '+' mean molecules are carcinogenic; label = '-' means molecules are non-carcinogenic; double bond refers to bond_type = ' = ';

**Gold SQL:**
```sql
SELECT COUNT(T1.bond_id), T2.label FROM bond AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '=' AND T2.molecule_id = 'TR006' GROUP BY T2.label
```
**Predicted SQL:**
```sql
SELECT COUNT(*) AS double_bond_count, m.label FROM bond b JOIN molecule m ON b.molecule_id = m.molecule_id WHERE b.molecule_id = 'TR006' AND b.bond_type = '=';
```

**Witness database:**

*atom*

| atom_id | molecule_id | element |
|---|---|---|
| 2147483648 | 2147483648 | 2147483648 |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
| 2147483648 | 2147483648 | 2147483648 |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| 2147483648 | 2147483648 | 2147483648 |

*molecule*

| molecule_id | label |
|---|---|
| 2147483648 | 2147483648 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[0, None]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The gold uses GROUP BY label which returns no rows when TR006 has no matching bonds, but the question expects a count (0) and a carcinogenicity label; the predicted's aggregate without GROUP BY correctly returns [0, NULL].


---

## Item 55 (card_games)

**Question:** How many cards in the set Coldsnap have a black border color?

**Evidence:** card set Coldsnap refers to name = 'Coldsnap'; black border color refers to borderColor = 'black'

**Gold SQL:**
```sql
SELECT SUM(CASE WHEN T1.borderColor = 'black' THEN 1 ELSE 0 END) FROM cards AS T1 INNER JOIN sets AS T2 ON T2.code = T1.setCode WHERE T2.name = 'Coldsnap'
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM cards WHERE setCode = (SELECT code FROM sets WHERE name = 'Coldsnap') AND borderColor = 'black';
```

**Witness database:**

*cards* (71 unreferenced columns omitted)

| borderColor | name | setCode |
|---|---|---|
| BLACK | 2147483648 | 2147483648 |

*foreign_data* (4 unreferenced columns omitted)

| id | flavorText | language | multiverseid |
|---|---|---|---|
| 0 | 2147483648 | 2147483648 | 0 |

*legalities*

| id | format | status | uuid |
|---|---|---|---|
| 0 | 2147483648 | 2147483648 | 2147483648 |

*sets* (19 unreferenced columns omitted)

| code | name |
|---|---|
| 2147483649 | COLDSNAP |

*set_translations*

| id | language | setCode | translation |
|---|---|---|---|
| 0 | 2147483648 | 2147483649 | 2147483648 |

*rulings*

| id | date | text | uuid |
|---|---|---|---|
| 0 | 1000-01-01 | 2147483648 | 2147483648 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[0]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The gold's SUM(CASE...) over an empty joined set returns NULL, but the question asks "how many" which expects a numeric count; the predicted's COUNT(*) correctly returns 0 when no black-bordered Coldsnap cards match.


---

## Item 56 (california_schools)

**Question:** What is the free or reduced price meal count for ages 5 to 17 in the Youth Authority School with a mailing street address of PO Box 1040?

**Evidence:** -

**Gold SQL:**
```sql
SELECT T1.`FRPM Count (Ages 5-17)` FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.MailStreet = 'PO Box 1040' AND T2.SOCType = 'Youth Authority Facilities'
```
**Predicted SQL:**
```sql
SELECT T2.`FRPM Count (Ages 5-17)` FROM schools AS T1 INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.EdOpsName = 'Youth Authority School' AND T1.MailStreet = 'PO Box 1040'
```

**Witness database:**

*frpm* (27 unreferenced columns omitted)

| CDSCode | FRPM Count (Ages 5-17) |
|---|---|
| 34322760330027 | 5.0 |

*schools* (45 unreferenced columns omitted)

| CDSCode | MailStreet | SOCType | EdOpsName |
|---|---|---|---|
| 34322760330027 | PO Box 1040 | Preschool | Youth Authority School |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[5.0]]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The gold filters on SOCType='Youth Authority Facilities', but the school's actual SOCType is 'Preschool'; the question refers to "Youth Authority School" which matches EdOpsName='Youth Authority School' as used by the predicted query.


---

## Item 57 (codebase_community)

**Question:** When did 'chl' cast its first vote in a post?

**Evidence:** DisplayName = 'chl'; cast its first vote refers to MIN(CreationDate);

**Gold SQL:**
```sql
SELECT T2.CreationDate FROM users AS T1 INNER JOIN votes AS T2 ON T1.Id = T2.UserId WHERE T1.DisplayName = 'chl' ORDER BY T2.CreationDate LIMIT 1
```
**Predicted SQL:**
```sql
SELECT MIN(v.CreationDate) AS FirstVoteDate FROM users u JOIN votes v ON u.Id = v.UserId WHERE u.DisplayName = 'chl'
```

**Witness database:**

*posts* (17 unreferenced columns omitted)

| Id | PostTypeId | AcceptedAnswerId | CreaionDate |
|---|---|---|---|
| 1 | 1 | NULL | 2000-01-01 00:00:00 |
| 3 | 100 | 1 | 2010-06-15 12:30:00 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 1 | 1 |
| 3 | a |
| 2 | b |

*votes* (4 unreferenced columns omitted)

| CreationDate | UserId |
|---|---|
| NULL | 3 |
| 2000-01-01 | 1 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Verdict:** pred_wrong  
**Reason (one sentence):** No user with DisplayName='chl' exists, so the gold correctly returns an empty result; the predicted's MIN(CreationDate) over an empty set produces a spurious [[NULL]] row instead of no rows.


---

## Item 58 (formula_1)

**Question:** What was the fastest lap speed among all drivers in the 2009 Spanish Grand Prix?

**Evidence:** the fastest lap speed among all refers to max(fastestLapSpeed); Spanish Grand Prix refers to races.name = 'Spanish Grand Prix';

**Gold SQL:**
```sql
SELECT T2.fastestLapSpeed FROM races AS T1 INNER JOIN results AS T2 ON T2.raceId = T1.raceId WHERE T1.name = 'Spanish Grand Prix' AND T1.year = 2009 AND T2.fastestLapSpeed IS NOT NULL ORDER BY T2.fastestLapSpeed DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT MAX(T2.fastestLapSpeed) FROM races AS T1 JOIN results AS T2 ON T1.raceid = T2.raceid WHERE T1.name = 'Spanish Grand Prix' AND T1.year = 2009
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 6 | monaco | Circuit de Monaco | Monte-Carlo |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 18 | minardi | Minardi | Italian |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 69 | badoer | NULL | BAD |

*races* (5 unreferenced columns omitted)

| raceId | year | name |
|---|---|---|
| 178 | 1999 | Monaco Grand Prix |

*results* (16 unreferenced columns omitted)

| raceId | fastestLapSpeed |
|---|---|
| 178 | NULL |

*seasons*

| year | url |
|---|---|
| 1999 | http://en.wikipedia.org/wiki/1999_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 6 | Gearbox |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Verdict:** pred_wrong  
**Reason (one sentence):** No 2009 Spanish Grand Prix exists in the witness, so the gold correctly returns empty; the predicted's MAX(fastestLapSpeed) over an empty set produces a spurious [[NULL]] row instead of no rows.


---

## Item 59 (formula_1)

**Question:** For the race happened in 2015/11/29, how many drivers did not finish the game?

**Evidence:** game and race are synonyms; drivers who didn't finish the race should have record in time;

**Gold SQL:**
```sql
SELECT COUNT(T2.driverId) FROM races AS T1 INNER JOIN results AS T2 ON T2.raceId = T1.raceId WHERE T1.date = '2015-11-29' AND T2.time IS NULL
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM `results` INNER JOIN `races` ON `results`.`raceId` = `races`.`raceId` INNER JOIN `status` ON `results`.`statusId` = `status`.`statusId` WHERE `races`.`date` = '2015-11-29' AND `status`.`status` != 'Finished'
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 0 | 2147483648 | 2147483648 | 2147483648 |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 0 | 2147483648 | 2147483648 | 2147483648 |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 0 | 2147483648 | 0 | 2147483648 |

*seasons*

| year | url |
|---|---|
| 0 | 2147483648 |

*races* (6 unreferenced columns omitted)

| raceId | date |
|---|---|
| 0 | 2015-11-29 |

*constructorResults* (1 unreferenced columns omitted)

| constructorResultsId | raceId | constructorId | points |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

*constructorStandings* (3 unreferenced columns omitted)

| constructorStandingsId | raceId | constructorId | points |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

*driverStandings* (3 unreferenced columns omitted)

| driverStandingsId | raceId | driverId | points |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

*lapTimes* (2 unreferenced columns omitted)

| raceId | driverId | lap | position |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

*pitStops* (3 unreferenced columns omitted)

| raceId | driverId | stop | lap |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

*qualifying* (5 unreferenced columns omitted)

| qualifyId | raceId | driverId | constructorId |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

*status*

| statusId | status |
|---|---|
| 0 | 2147483648 |

*results* (14 unreferenced columns omitted)

| raceId | driverId | time | statusId |
|---|---|---|---|
| 0 | 0 | 2147483648 | 0 |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Verdict:** pred_wrong  
**Reason (one sentence):** The evidence indicates non-finishers are identified by a NULL time column, and the gold correctly counts drivers with time IS NULL (=0 since the row has a non-NULL time); the predicted incorrectly joins status and counts status != 'Finished'.


---

## Item 60 (thrombosis_prediction)

**Question:** What is the most common sign of patients with SLE disease?

**Evidence:** the most common sign refers to MAX(symptoms); 'SLE' refers to diagnosis

**Gold SQL:**
```sql
SELECT Symptoms FROM Examination WHERE Diagnosis = 'SLE' GROUP BY Symptoms ORDER BY COUNT(Symptoms) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT E.Symptoms FROM Patient AS P INNER JOIN Examination AS E ON P.ID = E.ID WHERE P.Diagnosis = 'SLE' GROUP BY E.Symptoms ORDER BY COUNT(E.Symptoms) DESC LIMIT 1
```

**Witness database:**

*Examination* (10 unreferenced columns omitted)

| ID | Diagnosis | Symptoms |
|---|---|---|
| 5416400 | Normal | NULL |
| 5206500 | SLE, SjS, Preg | NULL |
| 4513430 | NULL | NULL |
| 4528440 | SLE | NULL |

*Patient* (5 unreferenced columns omitted)

| ID | Diagnosis |
|---|---|
| 3839850 | SLE, SJS |
| 4528467 | McArdle |
| 5092228 | RA |
| 5416400 | SJS |
| 5206500 | Sle |
| 4513430 | MRA |
| 4528440 | SJS |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[]`

**Verdict:** gold_wrong  
**Reason (one sentence):** The gold filters Examination.Diagnosis='SLE' directly, but the question asks about patients with SLE whose diagnosis should come from the Patient table; the predicted correctly joins Patient to Examination on ID and filters Patient.Diagnosis='SLE'.
