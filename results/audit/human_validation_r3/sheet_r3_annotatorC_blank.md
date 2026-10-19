# Human attribution sheet, round 3 (blind) — annotator C

Fill in before you start and when you finish (local time):
- **Annotator ID:** C
- **Started (date, time):** ____
- **Finished (date, time):** ____
- **Did you use any AI tool (chat assistant, code assistant, translator) for this sheet?** ____ (yes/no; if yes, which and how)

For each item, read the question, evidence, both queries, the witness database, the two results and the facts from the real
database. Then replace `____` after **Verdict:** with exactly one of `pred_wrong`, `gold_wrong`, `both_wrong`, `ambiguous`,
`implausible_data`, and write one sentence after **Reason**. **Do not change anything else in this file**: the file is
checked automatically against the original, and any other change is reported. See INSTRUCTIONS.md for the definitions.
Work alone; do not discuss items with the other annotators until all three sheets are returned.

---

## Item R3-139 (formula_1)

**Question:** What is the lap record for the Austrian Grand Prix Circuit?

**Evidence:** lap record means the fastest time recorded which refers to time

**Gold SQL:**
```sql
WITH fastest_lap_times AS ( SELECT T1.raceId, T1.fastestLapTime FROM results AS T1 WHERE T1.FastestLapTime IS NOT NULL) SELECT MIN(fastest_lap_times.fastestLapTime) as lap_record FROM fastest_lap_times INNER JOIN races AS T2 on fastest_lap_times.raceId = T2.raceId INNER JOIN circuits AS T3 on T2.circuitId = T3.circuitId WHERE T2.name = 'Austrian Grand Prix'
```
**Predicted SQL:**
```sql
SELECT MIN(lt.time) FROM laptimes lt JOIN races r ON lt.raceId = r.raceId WHERE r.name = 'Austrian Grand Prix'
```

**Witness database:**

*circuits* (8 unreferenced columns omitted)

| circuitId |
|---|
| 23 |
| 11 |
| 7 |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 16 | bar | BAR | British |
| 28 | forti | Forti | Italian |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 41 | zonta | NULL | ZON |
| 64 | diniz | NULL | NULL |
| 35 | villeneuve | NULL | VIL |

*lapTimes* (4 unreferenced columns omitted)

| raceId | time |
|---|---|
| 183 | 1:15.136 |
| 183 | 1:15.916 |

*races* (5 unreferenced columns omitted)

| raceId | circuitId | name |
|---|---|---|
| 183 | 23 | Austrian Grand Prix |
| 185 | 11 | Hungarian Grand Prix |
| 245 | 7 | Canadian Grand Prix |

*results* (16 unreferenced columns omitted)

| raceId | fastestLapTime |
|---|---|
| 183 | NULL |
| 185 | NULL |
| 245 | NULL |

*seasons*

| year | url |
|---|---|
| 1999 | http://en.wikipedia.org/wiki/1999_Formula_One_season |
| 1995 | http://en.wikipedia.org/wiki/1995_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 86 | Halfshaft |
| 12 | +2 Laps |
| 6 | Gearbox |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[['1:15.136']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `circuits.circuitId`: 72 rows, 0 NULL, 72 distinct values, all non-NULL values unique. Witness values: 23 occurs 1x; 11 occurs 1x; 7 occurs 1x.
- `lapTimes.raceId`: 420,369 rows, 0 NULL, 389 distinct values. Witness values: 183 occurs 1,286x.
- `lapTimes.time`: 420,369 rows, 0 NULL, 67,578 distinct values. Witness values: '1:15.136' occurs 4x; '1:15.916' occurs 8x.
- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 183 occurs 1x; 185 occurs 1x; 245 occurs 1x.
- `races.circuitId`: 976 rows, 0 NULL, 72 distinct values. Witness values: 23 occurs 25x; 11 occurs 32x; 7 occurs 38x.
- `races.name`: 976 rows, 0 NULL, 42 distinct values. Witness values: 'Austrian Grand Prix' occurs 30x; 'Hungarian Grand Prix' occurs 32x; 'Canadian Grand Prix' occurs 48x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 183 occurs 22x; 185 occurs 22x; 245 occurs 24x.
- `results.fastestLapTime`: 23,657 rows, 18,389 NULL, 4,955 distinct values. Witness values: NULL occurs 18,389x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-127 (card_games)

**Question:** What is card number 4 in the set Coldsnap?

**Evidence:** card set Coldsnap refers to name = 'Coldsnap'; card number 4 refers to number = 4

**Gold SQL:**
```sql
SELECT T1.name FROM cards AS T1 INNER JOIN sets AS T2 ON T2.code = T1.setCode WHERE T2.name = 'Coldsnap' AND T1.number = 4
```
**Predicted SQL:**
```sql
SELECT name FROM cards WHERE number = 4 AND setCode = (SELECT code FROM sets WHERE name = 'Coldsnap');
```

**Witness database:**

*cards* (71 unreferenced columns omitted)

| name | number | setCode |
|---|---|---|
| Coldsnap | 3 | a |
| Coldsnap | 4 | y2 |

*sets* (19 unreferenced columns omitted)

| code | name |
|---|---|
| a | Coldsnap |
| y2 | Coldsnap |

**Gold result on the witness:** `[['Coldsnap']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `cards.name`: 56,822 rows, 0 NULL, 21,738 distinct values. Witness values: 'Coldsnap' occurs 0x.
- `cards.number`: 56,822 rows, 0 NULL, 6,621 distinct values. Witness values: '3' occurs 342x; '4' occurs 331x.
- `cards.setCode`: 56,822 rows, 0 NULL, 536 distinct values. Witness values: 'a' occurs 0x; 'y2' occurs 0x.
- `sets.code`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 'a' occurs 0x; 'y2' occurs 0x.
- `sets.name`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 'Coldsnap' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-130 (card_games)

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
| black | ac | a |
| black | ac | a |
| blacka | ac | a |
| black | dn | NULL |
| black | ac | ep |
| black | ac | a0 |

*sets* (19 unreferenced columns omitted)

| code | name |
|---|---|
| a | Coldsnap |
| ep | Coldsnap |
| a0 | ew |

**Gold result on the witness:** `[[3]]`  
**Predicted result on the witness:** `[[2]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `cards.borderColor`: 56,822 rows, 0 NULL, 5 distinct values. Witness values: 'black' occurs 49,729x; 'blacka' occurs 0x.
- `cards.name`: 56,822 rows, 0 NULL, 21,738 distinct values. Witness values: 'ac' occurs 0x; 'dn' occurs 0x.
- `cards.setCode`: 56,822 rows, 0 NULL, 536 distinct values. Witness values: 'a' occurs 0x; NULL occurs 0x; 'ep' occurs 0x; 'a0' occurs 0x.
- `sets.code`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 'a' occurs 0x; 'ep' occurs 0x; 'a0' occurs 0x.
- `sets.name`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 'Coldsnap' occurs 1x; 'ew' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-006 (european_football_2)

**Question:** List the top 10 players' names whose heights are above 180 in descending order of average heading accuracy.

**Evidence:** heights are above 180 refers to Player.height > 180; average heading accuracy = DIVIDE(SUM(heading_accuracy), COUNT(player_fifa_api_id));

**Gold SQL:**
```sql
SELECT t1.player_name FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t1.height > 180 GROUP BY t1.id ORDER BY CAST(SUM(t2.heading_accuracy) AS REAL) / COUNT(t2.`player_fifa_api_id`) DESC LIMIT 10
```
**Predicted SQL:**
```sql
SELECT T1.player_name FROM Player AS T1 JOIN Player_Attributes AS T2 ON T1.player_fifa_api_id = T2.player_fifa_api_id WHERE T1.height > 180 GROUP BY T2.player_api_id ORDER BY AVG(T2.heading_accuracy) DESC LIMIT 10
```

**Witness database:**

*Player_Attributes* (39 unreferenced columns omitted)

| player_fifa_api_id | player_api_id | heading_accuracy |
|---|---|---|
| -2147483648 | -2147483648 | NULL |
| -2147483648 | -2147483647 | 1 |

*Player* (2 unreferenced columns omitted)

| id | player_api_id | player_name | player_fifa_api_id | height |
|---|---|---|---|---|
| -2147483647 | -2147483648 | 2147483648 | -2147483647 | 181 |
| -2147483648 | -2147483647 | 2147483648 | -2147483648 | 180 |

*League*

| id | country_id | name |
|---|---|---|
| -2147483647 | -2147483648 | 2147483648 |
| -2147483648 | -2147483648 | 2147483648 |

*Country*

| id | name |
|---|---|
| -2147483648 | 2147483648 |
| -2147483647 | 2147483648 |

*Team* (1 unreferenced columns omitted)

| id | team_api_id | team_fifa_api_id | team_long_name |
|---|---|---|---|
| -2147483647 | -2147483648 | -2147483647 | 2147483648 |
| -2147483648 | -2147483647 | -2147483648 | 2147483648 |

*Team_Attributes* (21 unreferenced columns omitted)

| id | team_fifa_api_id | team_api_id | date |
|---|---|---|---|
| -2147483648 | -2147483647 | -2147483647 | 2147483648 |
| -2147483647 | -2147483647 | -2147483647 | 2147483648 |

*Match* (111 unreferenced columns omitted)

| id | country_id | league_id | season |
|---|---|---|---|
| -2147483648 | -2147483648 | -2147483648 | 2147483648 |
| -2147483647 | -2147483648 | -2147483648 | 2147483648 |

**Gold result on the witness:** `[['2147483648']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player_Attributes.player_fifa_api_id`: 183,978 rows, 0 NULL, 11,062 distinct values. Witness values: -2147483648 occurs 0x.
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: -2147483648 occurs 0x; -2147483647 occurs 0x.
- `Player_Attributes.heading_accuracy`: 183,978 rows, 836 NULL, 96 distinct values. Witness values: NULL occurs 836x; 1 occurs 3x.
- `Player.id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: -2147483647 occurs 0x; -2147483648 occurs 0x.
- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: -2147483648 occurs 0x; -2147483647 occurs 0x.
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: '2147483648' occurs 0x.
- `Player.player_fifa_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: -2147483647 occurs 0x; -2147483648 occurs 0x.
- `Player.height`: 11,060 rows, 0 NULL, 20 distinct values. Witness values: 181 occurs 0x; 180 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-086 (formula_1)

**Question:** What is full name of the racer who ranked 1st in the 3rd qualifying race held in the Marina Bay Street Circuit in 2008?

**Evidence:** Ranked 1st in the 3rd qualifying race refer to MIN(q3); 2008 is the year of race; full name of racer = forename, surname

**Gold SQL:**
```sql
SELECT T2.forename, T2.surname FROM qualifying AS T1 INNER JOIN drivers AS T2 on T1.driverId = T2.driverId INNER JOIN races AS T3 ON T1.raceid = T3.raceid WHERE q3 IS NOT NULL AND T3.year = 2008 AND T3.circuitId IN ( SELECT circuitId FROM circuits WHERE name = 'Marina Bay Street Circuit' ) ORDER BY CAST(SUBSTR(q3, 1, INSTR(q3, ':') - 1) AS INTEGER) * 60 + CAST(SUBSTR(q3, INSTR(q3, ':') + 1, INSTR(q3, '.') - INSTR(q3, ':') - 1) AS REAL) + CAST(SUBSTR(q3, INSTR(q3, '.') + 1) AS REAL) / 1000 ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN qualifying AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T2.raceId = T3.raceId INNER JOIN circuits AS T4 ON T3.circuitId = T4.circuitId WHERE T4.name = 'Marina Bay Street Circuit' AND T3.year = 2008 AND T2.position = 1 ORDER BY T2.q3 LIMIT 1
```

**Witness database:**

*circuits* (7 unreferenced columns omitted)

| circuitId | name |
|---|---|
| 15 | Marina Bay Street Circuit |
| 17 | Shanghai International Circuit |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 1 | mclaren | McLaren | British |
| 2 | bmw_sauber | BMW Sauber | German |
| 131 | mercedes | Mercedes | German |
| 4 | renault | Renault | French |

*drivers* (6 unreferenced columns omitted)

| driverId | forename | surname |
|---|---|---|
| 1 | Lewis | Hamilton |
| 9 | Robert | Kubica |

*qualifying* (5 unreferenced columns omitted)

| raceId | driverId | position | q3 |
|---|---|---|---|
| 32 | 1 | 2 | 1:45.465 |
| 32 | 9 | 4 | 1:45.779 |

*races* (5 unreferenced columns omitted)

| raceId | year | circuitId |
|---|---|---|
| 32 | 2008 | 15 |
| 928 | 2015 | 17 |
| 351 | 2010 | 15 |

*results* (14 unreferenced columns omitted)

| resultId | raceId | driverId | constructorId |
|---|---|---|---|
| 22576 | 928 | 1 | 131 |
| 20665 | 351 | 9 | 4 |

*seasons*

| year | url |
|---|---|
| 2008 | http://en.wikipedia.org/wiki/2008_Formula_One_season |
| 2015 | http://en.wikipedia.org/wiki/2015_Formula_One_season |
| 2010 | http://en.wikipedia.org/wiki/2010_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 1 | Finished |

**Gold result on the witness:** `[['Lewis', 'Hamilton']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `circuits.circuitId`: 72 rows, 0 NULL, 72 distinct values, all non-NULL values unique. Witness values: 15 occurs 1x; 17 occurs 1x.
- `circuits.name`: 72 rows, 0 NULL, 72 distinct values, all non-NULL values unique. Witness values: 'Marina Bay Street Circuit' occurs 1x; 'Shanghai International Circuit' occurs 1x.
- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 9 occurs 1x.
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: 'Lewis' occurs 1x; 'Robert' occurs 5x.
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: 'Hamilton' occurs 2x; 'Kubica' occurs 1x.
- `qualifying.raceId`: 7,397 rows, 0 NULL, 339 distinct values. Witness values: 32 occurs 20x.
- `qualifying.driverId`: 7,397 rows, 0 NULL, 151 distinct values. Witness values: 1 occurs 202x; 9 occurs 76x.
- `qualifying.position`: 7,397 rows, 0 NULL, 28 distinct values. Witness values: 2 occurs 339x; 4 occurs 339x.
- `qualifying.q3`: 7,397 rows, 5,251 NULL, 2,066 distinct values. Witness values: '1:45.465' occurs 1x; '1:45.779' occurs 1x.
- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 32 occurs 1x; 928 occurs 1x; 351 occurs 1x.
- `races.year`: 976 rows, 0 NULL, 68 distinct values. Witness values: 2008 occurs 18x; 2015 occurs 19x; 2010 occurs 19x.
- `races.circuitId`: 976 rows, 0 NULL, 72 distinct values. Witness values: 15 occurs 10x; 17 occurs 14x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-083 (debit_card_specializing)

**Question:** Which country's gas station had the first paid cusomer in 2012/8/25?

**Evidence:** '2012/8/25' can be represented by '2012-08-25'

**Gold SQL:**
```sql
SELECT T2.Country FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T1.Date = '2012-08-25' ORDER BY T1.Time DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T2.Country FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T1.Date = '2012-08-25' ORDER BY T1.Time ASC LIMIT 1
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

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `gasstations.GasStationID`: 5,716 rows, 0 NULL, 5,716 distinct values, all non-NULL values unique. Witness values: 1337 occurs 1x; 1345 occurs 1x.
- `gasstations.Country`: 5,716 rows, 0 NULL, 2 distinct values. Witness values: 'SVK' occurs 880x; 'CZE' occurs 4,836x.
- `transactions_1k.Date`: 1,000 rows, 0 NULL, 4 distinct values. Witness values: '2012-08-25' occurs 425x.
- `transactions_1k.Time`: 1,000 rows, 0 NULL, 599 distinct values. Witness values: '13:52:00' occurs 4x; '08:26:00' occurs 5x.
- `transactions_1k.GasStationID`: 1,000 rows, 0 NULL, 437 distinct values. Witness values: 1337 occurs 1x; 1345 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-109 (thrombosis_prediction)

**Question:** For the patient who was diagnosed SLE on 1997/1/27, what was his/her original diagnose when he/she came to the hospital for the first time?

**Evidence:** 'SLE' AND original diagnose refers to diagnosis; 1997/1/27 refer to `Examination Date` = '1997-01-27'; first came to the hospital refers to patient.`First Date`

**Gold SQL:**
```sql
SELECT T1.Diagnosis FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.ID = ( SELECT ID FROM Examination WHERE `Examination Date` = '1997-01-27' AND Diagnosis = 'SLE' ) AND T2.`Examination Date` = T1.`First Date`
```
**Predicted SQL:**
```sql
SELECT T1.Diagnosis FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T2."Examination Date" = '1997-01-27' AND T2.Diagnosis = 'SLE'
```

**Witness database:**

*Examination* (10 unreferenced columns omitted)

| ID | Examination Date | Diagnosis |
|---|---|---|
| 1 | 1997-01-27 | SLE |

*Patient* (4 unreferenced columns omitted)

| ID | First Date | Diagnosis |
|---|---|---|
| 1 | 1997-01-28 | 2147483648 |

*Laboratory* (40 unreferenced columns omitted)

| ID | Date | GOT | GPT |
|---|---|---|---|
| 1 | 0001-01-01 | 0 | 0 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2147483648']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: 1 occurs 0x.
- `Examination.Examination Date`: 806 rows, 10 NULL, 475 distinct values. Witness values: '1997-01-27' occurs 2x.
- `Examination.Diagnosis`: 806 rows, 331 NULL, 181 distinct values. Witness values: 'SLE' occurs 95x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x.
- `Patient.First Date`: 1,238 rows, 251 NULL, 797 distinct values. Witness values: '1997-01-28' occurs 0x.
- `Patient.Diagnosis`: 1,238 rows, 0 NULL, 220 distinct values. Witness values: '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-032 (toxicology)

**Question:** What is the carcinogenic label for bond TR001_2_4?

**Evidence:** label = '+' mean molecules are carcinogenic

**Gold SQL:**
```sql
SELECT DISTINCT T2.label FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id INNER JOIN bond AS T3 ON T2.molecule_id = T3.molecule_id WHERE T3.bond_id = 'TR001_2_4'
```
**Predicted SQL:**
```sql
SELECT m.label FROM bond b JOIN molecule m ON b.molecule_id = m.molecule_id WHERE b.bond_id = 'TR001_2_4';
```

**Witness database:**

*atom* (2 unreferenced columns omitted)

| molecule_id |
|---|
| 2147483648 |
| 2147483648 |

*bond* (1 unreferenced columns omitted)

| bond_id | molecule_id |
|---|---|
| 7851579254361807365 | 2147483649 |
| TR001_2_4 | 2147483649 |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| 2147483649 | 2147483648 | 7851579254361807365 |
| 2147483648 | 2147483649 | 7851579254361807365 |

*molecule*

| molecule_id | label |
|---|---|
| 2147483648 | - |
| 2147483649 | + |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['+']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.molecule_id`: 12,333 rows, 0 NULL, 444 distinct values. Witness values: '2147483648' occurs 0x.
- `bond.bond_id`: 12,379 rows, 0 NULL, 12,379 distinct values, all non-NULL values unique. Witness values: '7851579254361807365' occurs 0x; 'TR001_2_4' occurs 1x.
- `bond.molecule_id`: 12,379 rows, 0 NULL, 444 distinct values. Witness values: '2147483649' occurs 0x.
- `molecule.molecule_id`: 343 rows, 0 NULL, 343 distinct values, all non-NULL values unique. Witness values: '2147483648' occurs 0x; '2147483649' occurs 0x.
- `molecule.label`: 343 rows, 0 NULL, 2 distinct values. Witness values: '-' occurs 191x; '+' occurs 152x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-048 (financial)

**Question:** For the client who applied the biggest loan, what was his/her first amount of transaction after opened the account?

**Evidence:** -

**Gold SQL:**
```sql
SELECT T3.amount FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id INNER JOIN trans AS T3 ON T2.account_id = T3.account_id ORDER BY T1.amount DESC, T3.date ASC LIMIT 1
```
**Predicted SQL:**
```sql
WITH LargestLoan AS ( SELECT account_id FROM loan ORDER BY amount DESC LIMIT 1 ) SELECT t.amount FROM trans t INNER JOIN LargestLoan ll ON t.account_id = ll.account_id ORDER BY t.date ASC LIMIT 1;
```

**Witness database:**

*account* (3 unreferenced columns omitted)

| account_id |
|---|
| 3 |

*client*

| client_id | gender | birth_date | district_id |
|---|---|---|---|
| 4 | M | 1956-12-01 | 5 |

*disp*

| disp_id | client_id | account_id | type |
|---|---|---|---|
| 4 | 4 | 3 | OWNER |

*district* (12 unreferenced columns omitted)

| district_id | A2 | A3 | A4 |
|---|---|---|---|
| 5 | Kolin | central Bohemia | 95616 |

*loan* (5 unreferenced columns omitted)

| account_id | amount |
|---|---|
| 3 | 45768 |

*trans* (7 unreferenced columns omitted)

| account_id | date | amount |
|---|---|---|
| 3 | 1997-04-30 | 15 |
| 3 | 1997-04-30 | 1 |

**Gold result on the witness:** `[[1]]`  
**Predicted result on the witness:** `[[15]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `account.account_id`: 4,500 rows, 0 NULL, 4,500 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x.
- `loan.account_id`: 682 rows, 0 NULL, 682 distinct values, all non-NULL values unique. Witness values: 3 occurs 0x.
- `loan.amount`: 682 rows, 0 NULL, 645 distinct values. Witness values: 45768 occurs 2x.
- `trans.account_id`: 1,056,320 rows, 0 NULL, 4,500 distinct values. Witness values: 3 occurs 117x.
- `trans.date`: 1,056,320 rows, 0 NULL, 2,191 distinct values. Witness values: '1997-04-30' occurs 7,481x.
- `trans.amount`: 1,056,320 rows, 0 NULL, 35,890 distinct values. Witness values: 15 occurs 144,381x; 1 occurs 368x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-119 (european_football_2)

**Question:** State the name of the most strongest player.

**Evidence:** strongest players refers to player has MAX(overall_rating)

**Gold SQL:**
```sql
SELECT DISTINCT t1.player_name FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t2.overall_rating = (SELECT MAX(overall_rating) FROM Player_Attributes)
```
**Predicted SQL:**
```sql
SELECT `player`.`player_name` FROM `player` INNER JOIN `player_attributes` ON `player`.`player_api_id` = `player_attributes`.`player_api_id` ORDER BY `player_attributes`.`overall_rating` DESC LIMIT 1
```

**Witness database:**

*Player* (5 unreferenced columns omitted)

| player_api_id | player_name |
|---|---|
| 37947 | Sekou Ouattara |
| 317932 | Baptiste Aloe |
| 193226 | Francisco Portillo |
| 174220 | Barak Badash |
| 39200 | Luca Ariatti |
| 428947 | Santi Mina |
| 41704 | Eduardo |
| 37622 | Mane |
| 36412 | Peter Loevenkrands |
| 42645 | Simone Padoin |

*Player_Attributes* (40 unreferenced columns omitted)

| player_api_id | overall_rating |
|---|---|
| 428947 | 75 |
| 41704 | 76 |
| 37622 | 75 |
| 36412 | 71 |
| 42645 | 73 |
| 37947 | 55 |
| 317932 | 66 |
| 193226 | 76 |
| 174220 | 66 |
| 39200 | 63 |

**Gold result on the witness:** `[['Eduardo'], ['Francisco Portillo']]`  
**Predicted result on the witness:** `[['Francisco Portillo']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 37947 occurs 1x; 317932 occurs 1x; 193226 occurs 1x; 174220 occurs 1x; 39200 occurs 1x; 428947 occurs 1x (+4 more).
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'Sekou Ouattara' occurs 1x; 'Baptiste Aloe' occurs 1x; 'Francisco Portillo' occurs 1x; 'Barak Badash' occurs 1x; 'Luca Ariatti' occurs 1x; 'Santi Mina' occurs 1x (+4 more).
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 428947 occurs 19x; 41704 occurs 14x; 37622 occurs 19x; 36412 occurs 19x; 42645 occurs 48x; 37947 occurs 2x (+4 more).
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: 75 occurs 7,359x; 76 occurs 6,150x; 71 occurs 9,354x; 73 occurs 9,044x; 55 occurs 1,418x; 66 occurs 10,112x (+1 more).

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-115 (debit_card_specializing)

**Question:** What is the percentage of "premium" against the overall segment in Country = "SVK"?

**Evidence:** -

**Gold SQL:**
```sql
SELECT CAST(SUM(IIF(Country = 'SVK' AND Segment = 'Premium', 1, 0)) AS FLOAT) * 100 / SUM(IIF(Country = 'SVK', 1, 0)) FROM gasstations
```
**Predicted SQL:**
```sql
SELECT CAST(SUM(CASE WHEN Segment = 'Premium' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(Segment) FROM gasstations WHERE Country = 'SVK'
```

**Witness database:**

*gasstations* (2 unreferenced columns omitted)

| Country | Segment |
|---|---|
| SVK | NULL |
| CZE | Other |
| Premium | Discount |

**Gold result on the witness:** `[[0.0]]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `gasstations.Country`: 5,716 rows, 0 NULL, 2 distinct values. Witness values: 'SVK' occurs 880x; 'CZE' occurs 4,836x; 'Premium' occurs 0x.
- `gasstations.Segment`: 5,716 rows, 0 NULL, 5 distinct values. Witness values: NULL occurs 0x; 'Other' occurs 2,392x; 'Discount' occurs 294x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-098 (formula_1)

**Question:** What is the constructor reference name of the champion in the 2009 Singapore Grand Prix? Please give its website.

**Evidence:** the time of the champion shows in the format of "minutes: seconds.millionsecond" in which Max(time); constructor reference name refers to constructorRef; website refers to url

**Gold SQL:**
```sql
SELECT T3.constructorRef, T3.url FROM results AS T1 INNER JOIN races AS T2 on T1.raceId = T2.raceId INNER JOIN constructors AS T3 on T1.constructorId = T3.constructorId WHERE T2.name = 'Singapore Grand Prix' AND T2.year = 2009 AND T1.time LIKE '_:%:__.___'
```
**Predicted SQL:**
```sql
SELECT T1.constructorRef, T1.url FROM constructors AS T1 INNER JOIN results AS T2 ON T1.constructorId = T2.constructorId INNER JOIN races AS T3 ON T2.raceId = T3.raceId WHERE T3.year = 2009 AND T3.name = 'Singapore Grand Prix' AND T2.position = 1
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 1030 | americas | Circuit of the Americas | Austin |

*constructors* (2 unreferenced columns omitted)

| constructorId | constructorRef | url |
|---|---|---|
| 1031 | fry | http://en.wikipedia.org/wiki/Alfa_Romeo_(Formula_One) |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 1032 | cabianca | NULL | NULL |

*races* (5 unreferenced columns omitted)

| raceId | year | name |
|---|---|---|
| 1033 | 2009 | Singapore Grand Prix |

*results* (14 unreferenced columns omitted)

| raceId | constructorId | position | time |
|---|---|---|---|
| 1033 | 1031 | 2 | 1:34:50.616 |

*seasons*

| year | url |
|---|---|
| 2009 | http://en.wikipedia.org/wiki/2009_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 1 | Finished |

**Gold result on the witness:** `[['fry', 'http://en.wikipedia.org/wiki/Alfa_Romeo_(Formula_One)']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `constructors.constructorId`: 208 rows, 0 NULL, 208 distinct values, all non-NULL values unique. Witness values: 1031 occurs 0x.
- `constructors.constructorRef`: 208 rows, 0 NULL, 208 distinct values, all non-NULL values unique. Witness values: 'fry' occurs 1x.
- `constructors.url`: 208 rows, 0 NULL, 171 distinct values. Witness values: 'http://en.wikipedia.org/wiki/Alfa_Romeo_(Formula_ occurs 1x.
- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 1033 occurs 0x.
- `races.year`: 976 rows, 0 NULL, 68 distinct values. Witness values: 2009 occurs 17x.
- `races.name`: 976 rows, 0 NULL, 42 distinct values. Witness values: 'Singapore Grand Prix' occurs 10x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 1033 occurs 0x.
- `results.constructorId`: 23,657 rows, 0 NULL, 207 distinct values. Witness values: 1031 occurs 0x.
- `results.position`: 23,657 rows, 10,528 NULL, 33 distinct values. Witness values: 2 occurs 978x.
- `results.time`: 23,657 rows, 17,696 NULL, 5,755 distinct values. Witness values: '1:34:50.616' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-026 (debit_card_specializing)

**Question:** What percentage of Slovakian gas stations are premium?

**Evidence:** Percentage of premium gas station = (Total of premium gas station in Slovakia / Total of gas station in Slovakia) * 100%.

**Gold SQL:**
```sql
SELECT CAST(SUM(IIF(Segment = 'Premium', 1, 0)) AS FLOAT) * 100 / COUNT(GasStationID) FROM gasstations WHERE Country = 'SVK'
```
**Predicted SQL:**
```sql
SELECT (CAST(SUM(CASE WHEN Segment = 'Premium' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100 AS percentage_of_premium FROM gasstations WHERE Country = 'SVK';
```

**Witness database:**

*gasstations* (1 unreferenced columns omitted)

| GasStationID | Country | Segment |
|---|---|---|
| 5122 | SVK | Other |
| 1003 | SVK | Premium |
| 1079 | SVK | Other |

**Gold result on the witness:** `[[33.333333333333336]]`  
**Predicted result on the witness:** `[[33.33333333333333]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `gasstations.GasStationID`: 5,716 rows, 0 NULL, 5,716 distinct values, all non-NULL values unique. Witness values: 5122 occurs 1x; 1003 occurs 1x; 1079 occurs 1x.
- `gasstations.Country`: 5,716 rows, 0 NULL, 2 distinct values. Witness values: 'SVK' occurs 880x.
- `gasstations.Segment`: 5,716 rows, 0 NULL, 5 distinct values. Witness values: 'Other' occurs 2,392x; 'Premium' occurs 1,428x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-147 (codebase_community)

**Question:** Identify the number of posts that offer a bounty amount over 30.

**Evidence:** bounty amount over 30 refers to BountyAmount > = 30;

**Gold SQL:**
```sql
SELECT COUNT(id) FROM votes WHERE BountyAmount >= 30
```
**Predicted SQL:**
```sql
SELECT COUNT(PostId) FROM votes WHERE BountyAmount >= 30
```

**Witness database:**

*posts* (17 unreferenced columns omitted)

| Id | PostTypeId | AcceptedAnswerId | CreaionDate |
|---|---|---|---|
| 3 | 7 | 8 | 2000-01-02 00:00:00 |
| 41 | 7 | 8 | 2000-01-02 00:00:00 |
| 1 | 7 | 8 | 2000-01-02 00:00:00 |

*users* (10 unreferenced columns omitted)

| Id | Reputation | CreationDate | DisplayName |
|---|---|---|---|
| 5 | 17 | 2000-01-12 00:00:00 | m |
| 15 | 23 | 2000-01-19 00:00:00 | t |
| 11 | 29 | 2000-01-26 00:00:00 | aa |

*votes* (3 unreferenced columns omitted)

| Id | PostId | BountyAmount |
|---|---|---|
| 2 | 3 | 31 |
| 37 | 3 | 36 |
| 40 | 41 | -1 |
| 44 | 3 | NULL |
| 46 | NULL | 45 |

**Gold result on the witness:** `[[3]]`  
**Predicted result on the witness:** `[[2]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `votes.Id`: 38,930 rows, 0 NULL, 38,930 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 37 occurs 1x; 40 occurs 1x; 44 occurs 1x; 46 occurs 1x.
- `votes.PostId`: 38,930 rows, 0 NULL, 8,584 distinct values. Witness values: 3 occurs 49x; 41 occurs 7x; NULL occurs 0x.
- `votes.BountyAmount`: 38,930 rows, 38,829 NULL, 6 distinct values. Witness values: 31 occurs 0x; 36 occurs 0x; -1 occurs 0x; NULL occurs 38,829x; 45 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-114 (codebase_community)

**Question:** User No.3025 gave a comment at 20:29:39 on 2014/4/23 to a post, how many favorite counts did that post get?

**Evidence:** user no. 3025 refers to UserId = '3025'; comment at 20:29:39 on 2014/4/23 refers to CreationDate = '2014/4/23 20:29:39.0'

**Gold SQL:**
```sql
SELECT T1.FavoriteCount FROM posts AS T1 INNER JOIN comments AS T2 ON T1.Id = T2.PostId WHERE T2.CreationDate = '2014-04-23 20:29:39.0' AND T2.UserId = 3025
```
**Predicted SQL:**
```sql
SELECT T2.FavoriteCount FROM comments AS T1 INNER JOIN posts AS T2 ON T1.PostId = T2.Id WHERE T1.UserId = 3025 AND STRFTIME('%Y-%m-%d %H:%M:%S', T1.CreationDate) = '2014-04-23 20:29:39'
```

**Witness database:**

*comments* (4 unreferenced columns omitted)

| PostId | CreationDate | UserId |
|---|---|---|
| 1002 | 2014-04-23 20:29:39 | 3025 |

*posts* (19 unreferenced columns omitted)

| Id | FavoriteCount |
|---|---|
| 1002 | NULL |

*users* (10 unreferenced columns omitted)

| Id | Reputation | CreationDate | DisplayName |
|---|---|---|---|
| 3025 | 0 | NULL | x1 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `comments.PostId`: 174,285 rows, 0 NULL, 53,416 distinct values. Witness values: 1002 occurs 0x.
- `comments.CreationDate`: 174,285 rows, 0 NULL, 174,100 distinct values. Witness values: '2014-04-23 20:29:39' occurs 0x.
- `comments.UserId`: 174,285 rows, 2,835 NULL, 13,647 distinct values. Witness values: 3025 occurs 14x.
- `posts.Id`: 91,966 rows, 0 NULL, 91,966 distinct values, all non-NULL values unique. Witness values: 1002 occurs 0x.
- `posts.FavoriteCount`: 91,966 rows, 78,723 NULL, 77 distinct values. Witness values: NULL occurs 78,723x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-066 (superhero)

**Question:** Calculate the average attribute value of all neutral superheroes.

**Evidence:** average = AVG(attribute_value); neutral superheroes refers to alignment_id = 3;

**Gold SQL:**
```sql
SELECT AVG(T1.attribute_value) FROM hero_attribute AS T1 INNER JOIN superhero AS T2 ON T1.hero_id = T2.id INNER JOIN alignment AS T3 ON T2.alignment_id = T3.id WHERE T3.alignment = 'Neutral'
```
**Predicted SQL:**
```sql
SELECT AVG(hero_attribute.attribute_value) AS average_attribute_value FROM superhero INNER JOIN hero_attribute ON superhero.id = hero_attribute.hero_id WHERE superhero.alignment_id = 3
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 3 | Bad |
| 2 | Good |

*attribute*

| id | attribute_name |
|---|---|
| 3 | Neutral |

*colour*

| id | colour |
|---|---|
| 3 | 3 |
| 2 | Neutral |
| 1 | Neutral |

*gender*

| id | gender |
|---|---|
| 1 | Female |
| 2 | Male |
| 3 | Neutral |

*hero_attribute* (1 unreferenced columns omitted)

| hero_id | attribute_value |
|---|---|
| 1 | 3 |
| 2 | 100 |
| 2 | NULL |

*publisher*

| id | publisher_name |
|---|---|
| 1 | NULL |

*race*

| id | race |
|---|---|
| 3 | 3 |
| 1 | c |

*superhero* (10 unreferenced columns omitted)

| id | alignment_id |
|---|---|
| 3 | 3 |
| 1 | 2 |
| 2 | 3 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[100.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `alignment.id`: 4 rows, 0 NULL, 4 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x; 2 occurs 1x.
- `alignment.alignment`: 4 rows, 0 NULL, 4 distinct values, all non-NULL values unique. Witness values: 'Bad' occurs 1x; 'Good' occurs 1x.
- Real content of `alignment` (4 rows; referenced columns): (1, 'Good'); (2, 'Bad'); (3, 'Neutral'); (4, 'N/A').
- `hero_attribute.hero_id`: 3,738 rows, 0 NULL, 623 distinct values. Witness values: 1 occurs 6x; 2 occurs 6x.
- `hero_attribute.attribute_value`: 3,738 rows, 0 NULL, 20 distinct values. Witness values: 3 occurs 0x; 100 occurs 279x; NULL occurs 0x.
- `superhero.id`: 750 rows, 0 NULL, 750 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x; 1 occurs 1x; 2 occurs 1x.
- `superhero.alignment_id`: 750 rows, 6 NULL, 3 distinct values. Witness values: 3 occurs 28x; 2 occurs 212x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-082 (european_football_2)

**Question:** Among the players whose preferred foot was the left foot when attacking, how many of them would remain in his position when the team attacked?

**Evidence:** preferred foot when attacking was the left refers to preferred_foot = 'left'; players who would remain in his position when the team attacked refers to attacking_work_rate = 'low';

**Gold SQL:**
```sql
SELECT COUNT(player_api_id) FROM Player_Attributes WHERE preferred_foot = 'left' AND attacking_work_rate = 'low'
```
**Predicted SQL:**
```sql
SELECT COUNT(id) FROM Player_Attributes WHERE preferred_foot = 'left' AND attacking_work_rate = 'low'
```

**Witness database:**

*Player_Attributes* (38 unreferenced columns omitted)

| id | player_api_id | preferred_foot | attacking_work_rate |
|---|---|---|---|
| 1 | 3 | left | low |
| 41 | 3 | left | low |
| 49 | NULL | left | low |
| 58 | NULL | left | low |
| 74 | NULL | right | low |
| 82 | NULL | NULL | low |
| 96 | NULL | left | lowa |
| 102 | NULL | left | NULL |

*Player* (3 unreferenced columns omitted)

| id | player_api_id | player_name | player_fifa_api_id |
|---|---|---|---|
| 37 | 38 | e | 2 |

**Gold result on the witness:** `[[2]]`  
**Predicted result on the witness:** `[[4]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player_Attributes.id`: 183,978 rows, 0 NULL, 183,978 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 41 occurs 1x; 49 occurs 1x; 58 occurs 1x; 74 occurs 1x; 82 occurs 1x (+2 more).
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 3 occurs 0x; NULL occurs 0x.
- `Player_Attributes.preferred_foot`: 183,978 rows, 836 NULL, 2 distinct values. Witness values: 'left' occurs 44,733x; 'right' occurs 138,409x; NULL occurs 836x.
- `Player_Attributes.attacking_work_rate`: 183,978 rows, 3,230 NULL, 8 distinct values. Witness values: 'low' occurs 8,569x; 'lowa' occurs 0x; NULL occurs 3,230x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-085 (codebase_community)

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
| 3 | 1 |
| 16 | 15 |
| 22 | NULL |
| 34 | 32 |

*users* (11 unreferenced columns omitted)

| Id | DisplayName | Views |
|---|---|---|
| 1 | NULL | 201 |
| 15 | NULL | 201 |
| 32 | NULL | 33 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[1.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `badges.Id`: 79,851 rows, 0 NULL, 79,851 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x; 16 occurs 1x; 22 occurs 1x; 34 occurs 1x.
- `badges.UserId`: 79,851 rows, 0 NULL, 25,078 distinct values. Witness values: 1 occurs 0x; 15 occurs 1x; NULL occurs 0x; 32 occurs 0x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 15 occurs 1x; 32 occurs 0x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: NULL occurs 0x.
- `users.Views`: 40,325 rows, 0 NULL, 362 distinct values. Witness values: 201 occurs 1x; 33 occurs 28x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-135 (california_schools)

**Question:** What is the website for the schools under the administrations of Mike Larson and Dante Alvarez?

**Evidence:** -

**Gold SQL:**
```sql
SELECT Website FROM schools WHERE (AdmFName1 = 'Mike' AND AdmLName1 = 'Larson') OR (AdmFName1 = 'Dante' AND AdmLName1 = 'Alvarez')
```
**Predicted SQL:**
```sql
SELECT Website FROM schools WHERE AdmFName1 = 'Mike' AND AdmLName1 = 'Larson' OR AdmFName2 = 'Dante' AND AdmLName2 = 'Alvarez' OR AdmFName3 = 'Mike' AND AdmLName3 = 'Larson' OR AdmFName1 = 'Dante' AND AdmLName1 = 'Alvarez' OR AdmFName2 = 'Mike' AND AdmLName2 = 'Larson' OR AdmFName3 = 'Dante' AND AdmLName3 = 'Alvarez'
```

**Witness database:**

*schools* (42 unreferenced columns omitted)

| Website | AdmFName1 | AdmLName1 | AdmFName2 | AdmLName2 | AdmFName3 | AdmLName3 |
|---|---|---|---|---|---|---|
| www.compton.k12.ca.us | Dante | Larson | Mike | Larson | Eric | Andreasen |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['www.compton.k12.ca.us']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `schools.Website`: 17,686 rows, 10,722 NULL, 4,082 distinct values. Witness values: 'www.compton.k12.ca.us' occurs 41x.
- `schools.AdmFName1`: 17,686 rows, 5,986 NULL, 2,327 distinct values. Witness values: 'Dante' occurs 2x.
- `schools.AdmLName1`: 17,686 rows, 5,986 NULL, 6,394 distinct values. Witness values: 'Larson' occurs 7x.
- `schools.AdmFName2`: 17,686 rows, 17,255 NULL, 285 distinct values. Witness values: 'Mike' occurs 1x.
- `schools.AdmLName2`: 17,686 rows, 17,255 NULL, 363 distinct values. Witness values: 'Larson' occurs 0x.
- `schools.AdmFName3`: 17,686 rows, 17,644 NULL, 40 distinct values. Witness values: 'Eric' occurs 2x.
- `schools.AdmLName3`: 17,686 rows, 17,644 NULL, 42 distinct values, all non-NULL values unique. Witness values: 'Andreasen' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-031 (toxicology)

**Question:** How many double bonds does TR006 have and is it carcinogenic?

**Evidence:** label = '+' mean molecules are carcinogenic; label = '-' means molecules are non-carcinogenic; double bond refers to bond_type = ' = ';

**Gold SQL:**
```sql
SELECT COUNT(T1.bond_id), T2.label FROM bond AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '=' AND T2.molecule_id = 'TR006' GROUP BY T2.label
```
**Predicted SQL:**
```sql
SELECT (SELECT COUNT(*) FROM bond WHERE molecule_id = 'TR006' AND bond_type = '=') AS double_bonds_count, (SELECT label FROM molecule WHERE molecule_id = 'TR006') AS molecule_label
```

**Witness database:**

*atom*

| atom_id | molecule_id | element |
|---|---|---|
| TR409_11 | TR409 | c |
| TR409_15 | TR409 | c |
| TR409_16 | TR409 | c |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
| TR409_15_16 | TR409 | = |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| TR409_16 | TR409_15 | TR409_15_16 |
| TR409_15 | TR409_16 | TR409_15_16 |

*molecule*

| molecule_id | label |
|---|---|
| TR409 | + |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[0, None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `bond.bond_id`: 12,379 rows, 0 NULL, 12,379 distinct values, all non-NULL values unique. Witness values: 'TR409_15_16' occurs 1x.
- `bond.molecule_id`: 12,379 rows, 0 NULL, 444 distinct values. Witness values: 'TR409' occurs 34x.
- `bond.bond_type`: 12,379 rows, 1 NULL, 3 distinct values. Witness values: '=' occurs 1,844x.
- `molecule.molecule_id`: 343 rows, 0 NULL, 343 distinct values, all non-NULL values unique. Witness values: 'TR409' occurs 1x.
- `molecule.label`: 343 rows, 0 NULL, 2 distinct values. Witness values: '+' occurs 152x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-142 (california_schools)

**Question:** What is the free or reduced price meal count for ages 5 to 17 in the Youth Authority School with a mailing street address of PO Box 1040?

**Evidence:** -

**Gold SQL:**
```sql
SELECT T1.`FRPM Count (Ages 5-17)` FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.MailStreet = 'PO Box 1040' AND T2.SOCType = 'Youth Authority Facilities'
```
**Predicted SQL:**
```sql
SELECT T2.`FRPM Count (Ages 5-17)` FROM schools AS T1 INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.EdOpsName = 'Youth Authority School' AND T1.MailStrAbr = 'PO Box 1040'
```

**Witness database:**

*frpm* (27 unreferenced columns omitted)

| CDSCode | FRPM Count (Ages 5-17) |
|---|---|
| 34322760330027 | 5.0 |

*schools* (44 unreferenced columns omitted)

| CDSCode | MailStreet | MailStrAbr | SOCType | EdOpsName |
|---|---|---|---|---|
| 34322760330027 | PO Box 1040 | PO Box 1040 | Juvenile Court Schools | Youth Authority School |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[5.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `frpm.CDSCode`: 9,986 rows, 0 NULL, 9,986 distinct values, all non-NULL values unique. Witness values: '34322760330027' occurs 1x.
- `frpm.FRPM Count (Ages 5-17)`: 9,986 rows, 72 NULL, 1,330 distinct values. Witness values: 5.0 occurs 52x.
- `schools.CDSCode`: 17,686 rows, 0 NULL, 17,686 distinct values, all non-NULL values unique. Witness values: '34322760330027' occurs 1x.
- `schools.MailStreet`: 17,686 rows, 292 NULL, 12,395 distinct values. Witness values: 'PO Box 1040' occurs 1x.
- `schools.MailStrAbr`: 17,686 rows, 292 NULL, 12,429 distinct values. Witness values: 'PO Box 1040' occurs 1x.
- `schools.SOCType`: 17,686 rows, 1,369 NULL, 20 distinct values. Witness values: 'Juvenile Court Schools' occurs 254x.
- `schools.EdOpsName`: 17,686 rows, 5,711 NULL, 13 distinct values. Witness values: 'Youth Authority School' occurs 6x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-015 (european_football_2)

**Question:** Which player is the tallest?

**Evidence:** tallest player refers to MAX(height);

**Gold SQL:**
```sql
SELECT player_name FROM Player ORDER BY height DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT `player_name` FROM `player` WHERE `height` = (SELECT MAX(`height`) FROM `player`)
```

**Witness database:**

*Player* (5 unreferenced columns omitted)

| player_name | height |
|---|---|
| Diego Buonanotte | 160.02 |
| Maxi Moralez | 160.02 |

*Player_Attributes* (38 unreferenced columns omitted)

| id | player_fifa_api_id | player_api_id | date |
|---|---|---|---|
| 43638 | 170719 | 103139 | 2013-06-07 00:00:00 |
| 121211 | 183895 | 29587 | 2013-09-27 00:00:00 |

**Gold result on the witness:** `[['Diego Buonanotte']]`  
**Predicted result on the witness:** `[['Diego Buonanotte'], ['Maxi Moralez']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'Diego Buonanotte' occurs 1x; 'Maxi Moralez' occurs 1x.
- `Player.height`: 11,060 rows, 0 NULL, 20 distinct values. Witness values: 160.02 occurs 2x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-024 (toxicology)

**Question:** Calculate the total atoms with triple-bond molecules containing the element phosphorus or bromine.

**Evidence:** triple bond refers to bond_type = '#'; phosphorus refers to element = 'p'; bromine refers to element = 'br'

**Gold SQL:**
```sql
SELECT COUNT(T1.atom_id) FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id INNER JOIN bond AS T3 ON T2.molecule_id = T3.molecule_id WHERE T3.bond_type = '#' AND T1.element IN ('p', 'br')
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT a.atom_id) FROM atom AS a JOIN connected AS c ON a.atom_id = c.atom_id JOIN bond AS b ON b.bond_id = c.bond_id WHERE b.bond_type = '#' AND a.element IN ('p', 'br')
```

**Witness database:**

*atom*

| atom_id | molecule_id | element |
|---|---|---|
| TR000_1 | TR060 | br |
| TR000_3 | TR338 | i |
| TR000_2 | TR496 | cu |
| TR338_32 | TR338 | c |
| TR338_91 | TR338 | h |
| TR001_13 | TR000 | h |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
| TR000_2_4 | TR496 | # |
| TR001_10_11 | TR060 | NULL |
| TR000_2_5 | TR000 | - |
| TR338_32_91 | TR338 | - |

*connected* (1 unreferenced columns omitted)

| atom_id | bond_id |
|---|---|
| TR000_1 | TR000_2_4 |
| TR000_2 | TR000_2_5 |
| TR000_2 | TR001_10_11 |
| TR338_91 | TR338_32_91 |
| TR000_3 | TR000_2_4 |
| TR000_1 | TR000_2_5 |
| TR000_3 | TR001_10_11 |
| TR338_32 | TR338_32_91 |

*molecule* (1 unreferenced columns omitted)

| molecule_id |
|---|
| TR496 |
| TR338 |
| TR060 |
| TR000 |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.atom_id`: 12,333 rows, 0 NULL, 12,333 distinct values, all non-NULL values unique. Witness values: 'TR000_1' occurs 1x; 'TR000_3' occurs 1x; 'TR000_2' occurs 1x; 'TR338_32' occurs 1x; 'TR338_91' occurs 1x; 'TR001_13' occurs 1x.
- `atom.molecule_id`: 12,333 rows, 0 NULL, 444 distinct values. Witness values: 'TR060' occurs 103x; 'TR338' occurs 174x; 'TR496' occurs 109x; 'TR000' occurs 5x.
- `atom.element`: 12,333 rows, 0 NULL, 21 distinct values. Witness values: 'br' occurs 47x; 'i' occurs 6x; 'cu' occurs 2x; 'c' occurs 4,605x; 'h' occurs 5,518x.
- `bond.bond_id`: 12,379 rows, 0 NULL, 12,379 distinct values, all non-NULL values unique. Witness values: 'TR000_2_4' occurs 1x; 'TR001_10_11' occurs 1x; 'TR000_2_5' occurs 1x; 'TR338_32_91' occurs 1x.
- `bond.molecule_id`: 12,379 rows, 0 NULL, 444 distinct values. Witness values: 'TR496' occurs 108x; 'TR060' occurs 107x; 'TR000' occurs 4x; 'TR338' occurs 175x.
- `bond.bond_type`: 12,379 rows, 1 NULL, 3 distinct values. Witness values: '#' occurs 6x; NULL occurs 1x; '-' occurs 10,528x.
- `connected.atom_id`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'TR000_1' occurs 1x; 'TR000_2' occurs 4x; 'TR338_91' occurs 1x; 'TR000_3' occurs 1x; 'TR338_32' occurs 4x.
- `connected.bond_id`: 24,758 rows, 0 NULL, 12,379 distinct values. Witness values: 'TR000_2_4' occurs 2x; 'TR000_2_5' occurs 2x; 'TR001_10_11' occurs 2x; 'TR338_32_91' occurs 2x.
- `molecule.molecule_id`: 343 rows, 0 NULL, 343 distinct values, all non-NULL values unique. Witness values: 'TR496' occurs 1x; 'TR338' occurs 0x; 'TR060' occurs 1x; 'TR000' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-107 (codebase_community)

**Question:** Identify the latest badge awarded to the user with the display name Emmett.

**Evidence:** the latest badge refers to Name FROM badges where MAX(Date);

**Gold SQL:**
```sql
SELECT T1.Name FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.DisplayName = 'Emmett' ORDER BY T1.Date DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT Name FROM badges WHERE UserId = (SELECT Id FROM users WHERE DisplayName = 'Emmett') ORDER BY Date DESC LIMIT 1;
```

**Witness database:**

*badges*

| Id | UserId | Name | Date |
|---|---|---|---|
| 3 | 3 | Notable Question | 2014-04-20 21:33:45.0 |
| 2 | 3 | Notable Question | 2014-04-18 01:28:55.0 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 1 | Emmett |
| 2 | Tom |
| 3 | Emmett |

**Gold result on the witness:** `[['Notable Question']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `badges.Id`: 79,851 rows, 0 NULL, 79,851 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x; 2 occurs 1x.
- `badges.UserId`: 79,851 rows, 0 NULL, 25,078 distinct values. Witness values: 3 occurs 3x.
- `badges.Name`: 79,851 rows, 0 NULL, 153 distinct values. Witness values: 'Notable Question' occurs 1,725x.
- `badges.Date`: 79,851 rows, 0 NULL, 65,586 distinct values. Witness values: '2014-04-20 21:33:45.0' occurs 1x; '2014-04-18 01:28:55.0' occurs 1x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 2 occurs 1x; 3 occurs 1x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: 'Emmett' occurs 1x; 'Tom' occurs 57x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-096 (european_football_2)

**Question:** Which teams have build up play passing more than 70? Please list their short names.

**Evidence:** build up play passing refers to buildUpPlayPassing; buildUpPlayPassing > 70; short names refers to team_short_name;

**Gold SQL:**
```sql
SELECT DISTINCT t1.team_short_name FROM Team AS t1 INNER JOIN Team_Attributes AS t2 ON t1.team_api_id = t2.team_api_id WHERE t2.buildUpPlayPassing > 70
```
**Predicted SQL:**
```sql
SELECT T1.team_short_name FROM Team AS T1 INNER JOIN Team_Attributes AS T2 ON T1.team_fifa_api_id = T2.team_fifa_api_id WHERE T2.buildUpPlayPassing > 70
```

**Witness database:**

*Match* (111 unreferenced columns omitted)

| id | country_id | league_id | season |
|---|---|---|---|
| 2347 | 1729 | 1729 | 2009/2010 |
| 18199 | 21518 | 21518 | 2008/2009 |

*Team* (2 unreferenced columns omitted)

| team_api_id | team_fifa_api_id | team_short_name |
|---|---|---|
| 8191 | 1796 | BUR |
| 10 | NULL | AMA |

*Team_Attributes* (22 unreferenced columns omitted)

| team_fifa_api_id | team_api_id | buildUpPlayPassing |
|---|---|---|
| 1796 | 10 | 74 |

**Gold result on the witness:** `[['AMA']]`  
**Predicted result on the witness:** `[['BUR']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Team.team_api_id`: 299 rows, 0 NULL, 299 distinct values, all non-NULL values unique. Witness values: 8191 occurs 1x; 10 occurs 0x.
- `Team.team_fifa_api_id`: 299 rows, 11 NULL, 285 distinct values. Witness values: 1796 occurs 1x; NULL occurs 11x.
- `Team.team_short_name`: 299 rows, 0 NULL, 259 distinct values. Witness values: 'BUR' occurs 1x; 'AMA' occurs 2x.
- `Team_Attributes.team_fifa_api_id`: 1,458 rows, 0 NULL, 285 distinct values. Witness values: 1796 occurs 6x.
- `Team_Attributes.team_api_id`: 1,458 rows, 0 NULL, 288 distinct values. Witness values: 10 occurs 0x.
- `Team_Attributes.buildUpPlayPassing`: 1,458 rows, 0 NULL, 58 distinct values. Witness values: 74 occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-068 (european_football_2)

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

*Player* (4 unreferenced columns omitted)

| player_api_id | player_fifa_api_id | birthday |
|---|---|---|
| 2752 | 1 | 1989-11-14 00:00:00 |
| 37622 | 170456 | 1981-12-21 00:00:00 |
| 423223 | 220048 | 1996-05-31 00:00:00 |
| 30615 | 244 | 1975-02-18 00:00:00 |
| 164385 | 191032 | 1992-01-20 00:00:00 |
| 2796 | 198735 | 1987-06-08 00:00:00 |
| 2977 | 134594 | 1978-12-02 00:00:00 |
| 2790 | 110809 | 1974-02-15 00:00:00 |

*Player_Attributes* (39 unreferenced columns omitted)

| player_fifa_api_id | player_api_id | overall_rating |
|---|---|---|
| 170456 | 37622 | 74 |
| 198735 | 2796 | 67 |
| 134594 | 2977 | 63 |
| 110809 | 2790 | 67 |
| 1 | 2752 | 72 |
| 220048 | 423223 | 69 |
| 244 | 30615 | 76 |
| 191032 | 164385 | 80 |
| 1 | 2752 | 80 |

**Gold result on the witness:** `[['1989-11-14 00:00:00']]`  
**Predicted result on the witness:** `[['1992-01-20 00:00:00']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 2752 occurs 1x; 37622 occurs 1x; 423223 occurs 1x; 30615 occurs 1x; 164385 occurs 1x; 2796 occurs 1x (+2 more).
- `Player.player_fifa_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 170456 occurs 1x; 220048 occurs 1x; 244 occurs 1x; 191032 occurs 1x; 198735 occurs 1x (+2 more).
- `Player.birthday`: 11,060 rows, 0 NULL, 5,762 distinct values. Witness values: '1989-11-14 00:00:00' occurs 7x; '1981-12-21 00:00:00' occurs 3x; '1996-05-31 00:00:00' occurs 2x; '1975-02-18 00:00:00' occurs 1x; '1992-01-20 00:00:00' occurs 2x; '1987-06-08 00:00:00' occurs 4x (+2 more).
- `Player_Attributes.player_fifa_api_id`: 183,978 rows, 0 NULL, 11,062 distinct values. Witness values: 170456 occurs 19x; 198735 occurs 15x; 134594 occurs 8x; 110809 occurs 5x; 1 occurs 0x; 220048 occurs 20x (+2 more).
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 37622 occurs 19x; 2796 occurs 15x; 2977 occurs 8x; 2790 occurs 5x; 2752 occurs 21x; 423223 occurs 20x (+2 more).
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: 74 occurs 8,556x; 67 occurs 10,198x; 63 occurs 7,704x; 72 occurs 9,740x; 69 occurs 10,281x; 76 occurs 6,150x (+1 more).

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-029 (thrombosis_prediction)

**Question:** How many male patients who underwent testing between 1995 and 1997 and were subsequently diagnosed with Behcet disease did not stay in the hospital for treatment?

**Evidence:** male refers to SEX = 'M'; underwent testing between 1995 and 1997 refers to `Examination Date` between '1995' and '1997'; Behcet refers to diagnosis; did not stay in the hospital refers to Admission = '-'

**Gold SQL:**
```sql
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T2.Diagnosis = 'Behcet' AND T1.SEX = 'M' AND STRFTIME('%Y', T2.`Examination Date`) BETWEEN '1995' AND '1997' AND T1.Admission = '-'
```
**Predicted SQL:**
```sql
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'M' AND T2."Examination Date" BETWEEN '1995-01-01' AND '1997-12-31' AND T1.Admission = '-' AND T2.Diagnosis LIKE '%Behcet%'
```

**Witness database:**

*Examination* (10 unreferenced columns omitted)

| ID | Examination Date | Diagnosis |
|---|---|---|
| 1 | 1996-03-12 | SLE, SjS susp |
| 2 | NULL | APS |
| 2 | NULL | PM |
| 3 | 1996-03-18 | Behcet, SjS susp |
| 2 | 1996-07-22 | SLE, SjS susp |

*Patient* (4 unreferenced columns omitted)

| ID | SEX | Admission |
|---|---|---|
| 1 | F | - |
| 2 | M | - |
| 3 | M | - |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: 1 occurs 0x; 2 occurs 0x; 3 occurs 0x.
- `Examination.Examination Date`: 806 rows, 10 NULL, 475 distinct values. Witness values: '1996-03-12' occurs 4x; NULL occurs 10x; '1996-03-18' occurs 4x; '1996-07-22' occurs 5x.
- `Examination.Diagnosis`: 806 rows, 331 NULL, 181 distinct values. Witness values: 'SLE, SjS susp' occurs 3x; 'APS' occurs 10x; 'PM' occurs 6x; 'Behcet, SjS susp' occurs 1x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 2 occurs 0x; 3 occurs 0x.
- `Patient.SEX`: 1,238 rows, 0 NULL, 3 distinct values. Witness values: 'F' occurs 1,023x; 'M' occurs 202x.
- `Patient.Admission`: 1,238 rows, 0 NULL, 4 distinct values. Witness values: '-' occurs 713x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-129 (card_games)

**Question:** What's the French name of the set of cards with "Tendo Ice Bridge" is in?

**Evidence:** French refers to language = 'French'; "Tendo Ice Bridge" is a translated name of a card; translated name refers to translation

**Gold SQL:**
```sql
SELECT T2.translation FROM cards AS T1 INNER JOIN set_translations AS T2 ON T2.setCode = T1.setCode WHERE T1.name = 'Tendo Ice Bridge' AND T2.language = 'French' AND T2.translation IS NOT NULL
```
**Predicted SQL:**
```sql
SELECT DISTINCT `set_translations`.`translation` FROM `cards` INNER JOIN `set_translations` ON `cards`.`setCode` = `set_translations`.`setCode` WHERE `cards`.`name` = 'Tendo Ice Bridge' AND `set_translations`.`language` = 'French'
```

**Witness database:**

*cards* (72 unreferenced columns omitted)

| name | setCode |
|---|---|
| Tendo Ice Bridge | BOK |
| Tendo Ice Bridge | BOK |

*set_translations* (1 unreferenced columns omitted)

| language | setCode | translation |
|---|---|---|
| French | BOK | NULL |

*sets* (17 unreferenced columns omitted)

| id | baseSetSize | block | booster |
|---|---|---|---|
| 34 | 165 | Kamigawa | {'default': {'boosters': [{'contents': {'common': 11, 'rare' |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `cards.name`: 56,822 rows, 0 NULL, 21,738 distinct values. Witness values: 'Tendo Ice Bridge' occurs 1x.
- `cards.setCode`: 56,822 rows, 0 NULL, 536 distinct values. Witness values: 'BOK' occurs 170x.
- `set_translations.language`: 1,210 rows, 0 NULL, 10 distinct values. Witness values: 'French' occurs 121x.
- `set_translations.setCode`: 1,210 rows, 0 NULL, 121 distinct values. Witness values: 'BOK' occurs 10x.
- `set_translations.translation`: 1,210 rows, 231 NULL, 504 distinct values. Witness values: NULL occurs 231x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-138 (financial)

**Question:** For the client who applied the biggest loan, what was his/her first amount of transaction after opened the account?

**Evidence:** -

**Gold SQL:**
```sql
SELECT T3.amount FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id INNER JOIN trans AS T3 ON T2.account_id = T3.account_id ORDER BY T1.amount DESC, T3.date ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T3.amount FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id INNER JOIN trans AS T3 ON T2.account_id = T3.account_id WHERE T1.loan_id = ( SELECT loan_id FROM loan ORDER BY amount DESC LIMIT 1 ) ORDER BY T3.date LIMIT 1
```

**Witness database:**

*account* (3 unreferenced columns omitted)

| account_id |
|---|
| 1001 |
| 1017 |

*district* (12 unreferenced columns omitted)

| district_id | A2 | A3 | A4 |
|---|---|---|---|
| 1002 | b | south Moravia | y2 |
| 1018 | A | b | A |

*loan* (4 unreferenced columns omitted)

| loan_id | account_id | amount |
|---|---|---|
| 1003 | 1001 | 2 |
| 1019 | 1017 | 2 |

*trans* (7 unreferenced columns omitted)

| account_id | date | amount |
|---|---|---|
| 1001 | 2015-03-20 | 3 |
| 1017 | 2010-06-15 | 1 |

**Gold result on the witness:** `[[1]]`  
**Predicted result on the witness:** `[[3]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `account.account_id`: 4,500 rows, 0 NULL, 4,500 distinct values, all non-NULL values unique. Witness values: 1001 occurs 0x; 1017 occurs 1x.
- `loan.loan_id`: 682 rows, 0 NULL, 682 distinct values, all non-NULL values unique. Witness values: 1003 occurs 0x; 1019 occurs 0x.
- `loan.account_id`: 682 rows, 0 NULL, 682 distinct values, all non-NULL values unique. Witness values: 1001 occurs 0x; 1017 occurs 0x.
- `loan.amount`: 682 rows, 0 NULL, 645 distinct values. Witness values: 2 occurs 0x.
- `trans.account_id`: 1,056,320 rows, 0 NULL, 4,500 distinct values. Witness values: 1001 occurs 0x; 1017 occurs 351x.
- `trans.date`: 1,056,320 rows, 0 NULL, 2,191 distinct values. Witness values: '2015-03-20' occurs 0x; '2010-06-15' occurs 0x.
- `trans.amount`: 1,056,320 rows, 0 NULL, 35,890 distinct values. Witness values: 3 occurs 293x; 1 occurs 368x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-063 (california_schools)

**Question:** How many schools with an average score in Math greater than 400 in the SAT test are exclusively virtual?

**Evidence:** Exclusively virtual refers to Virtual = 'F'

**Gold SQL:**
```sql
SELECT COUNT(DISTINCT T2.School) FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.Virtual = 'F' AND T1.AvgScrMath > 400
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.Virtual = 'F' AND T1.AvgScrMath > 400
```

**Witness database:**

*satscores* (9 unreferenced columns omitted)

| cds | AvgScrMath |
|---|---|
| 10101080109991 | 518 |
| 10101080111682 | 505 |
| 10101080000000 | 550 |

*schools* (46 unreferenced columns omitted)

| CDSCode | School | Virtual |
|---|---|---|
| 10101080000000 | Jefferson Elementary | F |
| 10101080111682 | NULL | F |
| 10101080109991 | Crescent View West Charter | P |

**Gold result on the witness:** `[[1]]`  
**Predicted result on the witness:** `[[2]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `satscores.cds`: 2,269 rows, 0 NULL, 2,269 distinct values, all non-NULL values unique. Witness values: '10101080109991' occurs 1x; '10101080111682' occurs 1x; '10101080000000' occurs 1x.
- `satscores.AvgScrMath`: 2,269 rows, 596 NULL, 295 distinct values. Witness values: 518 occurs 14x; 505 occurs 18x; 550 occurs 13x.
- `schools.CDSCode`: 17,686 rows, 0 NULL, 17,686 distinct values, all non-NULL values unique. Witness values: '10101080000000' occurs 1x; '10101080111682' occurs 1x; '10101080109991' occurs 1x.
- `schools.School`: 17,686 rows, 1,369 NULL, 13,875 distinct values. Witness values: 'Jefferson Elementary' occurs 33x; NULL occurs 1,369x; 'Crescent View West Charter' occurs 1x.
- `schools.Virtual`: 17,686 rows, 6,868 NULL, 3 distinct values. Witness values: 'F' occurs 69x; 'P' occurs 1,046x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-023 (debit_card_specializing)

**Question:** How much more was customer 7 consuming in April 2013 than customer 5?

**Evidence:** April 2013 refers to 201304 in the yearmonth.date

**Gold SQL:**
```sql
SELECT SUM(IIF(CustomerID = 7, Consumption, 0)) - SUM(IIF(CustomerID = 5, Consumption, 0)) FROM yearmonth WHERE Date = '201304'
```
**Predicted SQL:**
```sql
SELECT ( SELECT Consumption FROM yearmonth WHERE CustomerID = 7 AND `Date` = '201304' ) - ( SELECT Consumption FROM yearmonth WHERE CustomerID = 5 AND `Date` = '201304' ) AS Difference
```

**Witness database:**

*customers*

| CustomerID | Segment | Currency |
|---|---|---|
| 7 | KAM | CZK |

*yearmonth*

| CustomerID | Date | Consumption |
|---|---|---|
| 7 | 201304 | 1.58 |

**Gold result on the witness:** `[[1.58]]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `yearmonth.CustomerID`: 383,282 rows, 0 NULL, 30,566 distinct values. Witness values: 7 occurs 17x.
- `yearmonth.Date`: 383,282 rows, 0 NULL, 21 distinct values. Witness values: '201304' occurs 25,487x.
- `yearmonth.Consumption`: 383,282 rows, 0 NULL, 279,091 distinct values. Witness values: 1.58 occurs 149x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-010 (formula_1)

**Question:** Paul di Resta was in the No. 853 race, what percent faster did he finish in the 853rd race than the next race for the fastest lap speed?

**Evidence:** Paul di Resta refers to the full name of the driver; Full name of the driver refers to drivers.forename ='Paul' and drivers.surname = 'di Resta'; race number refers to raceId; percentage = DIVIDE(SUBTRACT(fastestLapSpeed(raceId = 853), (fastestLapSpeed (raceId = 854)) * 100 , (fastestLapSpeed(raceId = 853))

**Gold SQL:**
```sql
SELECT (SUM(IIF(T2.raceId = 853, T2.fastestLapSpeed, 0)) - SUM(IIF(T2.raceId = 854, T2.fastestLapSpeed, 0))) * 100 / SUM(IIF(T2.raceId = 853, T2.fastestLapSpeed, 0)) FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId WHERE T1.forename = 'Paul' AND T1.surname = 'di Resta'
```
**Predicted SQL:**
```sql
SELECT ((CASE WHEN r1.raceid = 853 THEN CAST(r1.fastestlapspeed AS REAL) ELSE 0 END) - CASE WHEN r2.raceid = 854 THEN CAST(r2.fastestlapspeed AS REAL) ELSE 0 END) / CASE WHEN r1.raceid = 853 THEN CAST(r1.fastestlapspeed AS REAL) ELSE 0 END * 100 AS percentage FROM drivers AS d INNER JOIN results AS r1 ON d.driverid = r1.driverid INNER JOIN results AS r2 ON d.driverid = r2.driverid WHERE d.forename = 'Paul' AND d.surname = 'di Resta' AND r1.raceid = 853 AND r2.raceid = 854
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | 2147483648 |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | 2147483648 |

*drivers* (6 unreferenced columns omitted)

| driverId | forename | surname |
|---|---|---|
| 1 | PAUL | DI RESTA |

*seasons*

| year | url |
|---|---|
| 0 | 2147483648 |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 853 | 0 | 1 | 1 |

*constructorResults* (1 unreferenced columns omitted)

| constructorResultsId | raceId | constructorId | points |
|---|---|---|---|
| 1 | 853 | 1 | 1e+308 |

*constructorStandings* (3 unreferenced columns omitted)

| constructorStandingsId | raceId | constructorId | points |
|---|---|---|---|
| 1 | 853 | 1 | 1e+308 |

*driverStandings* (3 unreferenced columns omitted)

| driverStandingsId | raceId | driverId | points |
|---|---|---|---|
| 1 | 853 | 1 | 1e+308 |

*lapTimes* (2 unreferenced columns omitted)

| raceId | driverId | lap | position |
|---|---|---|---|
| 853 | 1 | 1 | 1 |

*pitStops* (3 unreferenced columns omitted)

| raceId | driverId | stop | lap |
|---|---|---|---|
| 853 | 1 | 1 | 1 |

*qualifying* (5 unreferenced columns omitted)

| qualifyId | raceId | driverId | constructorId |
|---|---|---|---|
| 1 | 853 | 1 | 1 |

*status*

| statusId | status |
|---|---|
| 1 | 2147483648 |

*results* (15 unreferenced columns omitted)

| raceId | driverId | fastestLapSpeed |
|---|---|---|
| 853 | 1 | 2147483648 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x.
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: 'PAUL' occurs 0x.
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: 'DI RESTA' occurs 0x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 853 occurs 24x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 1 occurs 202x.
- `results.fastestLapSpeed`: 23,657 rows, 18,389 NULL, 5,045 distinct values. Witness values: '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-131 (european_football_2)

**Question:** How was the build up play dribbling class for "LEI" on 2015/9/10?

**Evidence:** "LEI" refers to team_short_name = 'LEI'; on 2015/9/10 refers to  date = '2015-09-10 00:00:00'

**Gold SQL:**
```sql
SELECT t2.buildUpPlayDribblingClass FROM Team AS t1 INNER JOIN Team_Attributes AS t2 ON t1.team_api_id = t2.team_api_id WHERE t1.team_short_name = 'LEI' AND SUBSTR(t2.`date`, 1, 10) = '2015-09-10'
```
**Predicted SQL:**
```sql
SELECT T1.buildUpPlayDribblingClass FROM Team_Attributes AS T1 JOIN Team AS T2 ON T1.team_api_id = T2.team_api_id AND T1.team_fifa_api_id = T2.team_fifa_api_id WHERE T2.team_short_name = 'LEI' AND T1.date = '2015-09-10 00:00:00'
```

**Witness database:**

*Team* (2 unreferenced columns omitted)

| team_api_id | team_fifa_api_id | team_short_name |
|---|---|---|
| 1 | 2 | LEI |
| 14 | 19 | l |
| NULL | 30 | LEI |
| 49 | NULL | LEI |
| 63 | 10 | NULL |

*Team_Attributes* (21 unreferenced columns omitted)

| team_fifa_api_id | team_api_id | date | buildUpPlayDribblingClass |
|---|---|---|---|
| 2 | 1 | 2015-09-10 00:00:00 | Little |
| 19 | 1 | 2015-09-10 00:00:00 | Little |
| 2 | 1 | 2015-09-10 00:00:00 | Little |
| 30 | NULL | 2015-09-10 00:00:00 | Little |
| NULL | 1 | 2015-09-10 00:00:00 | NULL |
| NULL | 49 | 2015-09-10 00:00:00 | Little |
| 10 | 63 | 2015-09-10 00:00:00 | Little |
| 19 | 1 | NULL | Little |

**Gold result on the witness:** `[['Little'], ['Little'], ['Little'], [None], ['Little']]`  
**Predicted result on the witness:** `[['Little'], ['Little']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Team.team_api_id`: 299 rows, 0 NULL, 299 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 14 occurs 0x; NULL occurs 0x; 49 occurs 0x; 63 occurs 0x.
- `Team.team_fifa_api_id`: 299 rows, 11 NULL, 285 distinct values. Witness values: 2 occurs 1x; 19 occurs 1x; 30 occurs 0x; NULL occurs 11x; 10 occurs 1x.
- `Team.team_short_name`: 299 rows, 0 NULL, 259 distinct values. Witness values: 'LEI' occurs 2x; 'l' occurs 0x; NULL occurs 0x.
- `Team_Attributes.team_fifa_api_id`: 1,458 rows, 0 NULL, 285 distinct values. Witness values: 2 occurs 6x; 19 occurs 6x; 30 occurs 0x; NULL occurs 0x; 10 occurs 6x.
- `Team_Attributes.team_api_id`: 1,458 rows, 0 NULL, 288 distinct values. Witness values: 1 occurs 0x; NULL occurs 0x; 49 occurs 0x; 63 occurs 0x.
- `Team_Attributes.date`: 1,458 rows, 0 NULL, 6 distinct values. Witness values: '2015-09-10 00:00:00' occurs 245x; NULL occurs 0x.
- `Team_Attributes.buildUpPlayDribblingClass`: 1,458 rows, 0 NULL, 3 distinct values. Witness values: 'Little' occurs 1,004x; NULL occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-091 (thrombosis_prediction)

**Question:** Among the patients whose level of Hematoclit isn't normal, which patient has the highest anti-Cardiolipin antibody concentration? Please list his or her ID.

**Evidence:** Hematoclit is normal refers to 29 < N < 52; highest anti-Cardiolipin antibody concentration refers to MAX(`aCL IgA`);

**Gold SQL:**
```sql
SELECT DISTINCT T1.ID FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID INNER JOIN Laboratory AS T3 on T1.ID = T3.ID WHERE (T3.HCT >= 52 OR T3.HCT <= 29) ORDER BY T2.`aCL IgA` DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT L.ID FROM Laboratory AS L INNER JOIN Examination AS E ON L.ID = E.ID WHERE L.HCT <= 29 OR L.HCT >= 52 ORDER BY E.`aCL IgA` DESC LIMIT 1;
```

**Witness database:**

*Examination* (11 unreferenced columns omitted)

| ID | aCL IgA |
|---|---|
| 29 | 1 |
| 1 | 5 |
| 3 | 29 |
| 1 | 52 |

*Laboratory* (42 unreferenced columns omitted)

| ID | HCT |
|---|---|
| 3 | 1.0 |
| 3 | 29.0 |
| 1 | 1.5 |
| 1 | 1.0 |

*Patient* (6 unreferenced columns omitted)

| ID |
|---|
| 3 |
| 29 |
| 1 |

**Gold result on the witness:** `[[3]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: 29 occurs 0x; 1 occurs 0x; 3 occurs 0x.
- `Examination.aCL IgA`: 806 rows, 0 NULL, 52 distinct values. Witness values: 1 occurs 13x; 5 occurs 37x; 29 occurs 0x; 52 occurs 0x.
- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 3 occurs 0x; 1 occurs 0x.
- `Laboratory.HCT`: 13,908 rows, 1,827 NULL, 363 distinct values. Witness values: 1.0 occurs 0x; 29.0 occurs 16x; 1.5 occurs 0x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 3 occurs 0x; 29 occurs 0x; 1 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-059 (card_games)

**Question:** What's the French name of the set of cards with "Tendo Ice Bridge" is in?

**Evidence:** French refers to language = 'French'; "Tendo Ice Bridge" is a translated name of a card; translated name refers to translation

**Gold SQL:**
```sql
SELECT T2.translation FROM cards AS T1 INNER JOIN set_translations AS T2 ON T2.setCode = T1.setCode WHERE T1.name = 'Tendo Ice Bridge' AND T2.language = 'French' AND T2.translation IS NOT NULL
```
**Predicted SQL:**
```sql
SELECT st.translation FROM cards c INNER JOIN sets s ON c.setCode = s.code INNER JOIN set_translations st ON s.code = st.setCode WHERE c.name = 'Tendo Ice Bridge' AND st.language = 'French';
```

**Witness database:**

*cards* (72 unreferenced columns omitted)

| name | setCode |
|---|---|
| Tendo Ice Bridge | a |
| Tendo Ice Bridge | NULL |
| Tendo Ice Bridge | a |
| Tendo Ice Bridge | a |
| Tendo Ice Bridge | a |

*sets* (20 unreferenced columns omitted)

| code |
|---|
| a |

*set_translations* (1 unreferenced columns omitted)

| language | setCode | translation |
|---|---|---|
| French | a | az |
| French | NULL | cl |
| French | a | cl |
| az | a | eo |
| French | a | NULL |

**Gold result on the witness:** `[['az'], ['cl'], ['az'], ['cl'], ['az'], ['cl'], ['az'], ['cl']]`  
**Predicted result on the witness:** `[[None], ['az'], ['cl'], [None], ['az'], ['cl'], [None], ['az'], ['cl'], [None], ['az'], ['cl']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `cards.name`: 56,822 rows, 0 NULL, 21,738 distinct values. Witness values: 'Tendo Ice Bridge' occurs 1x.
- `cards.setCode`: 56,822 rows, 0 NULL, 536 distinct values. Witness values: 'a' occurs 0x; NULL occurs 0x.
- `sets.code`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 'a' occurs 0x.
- `set_translations.language`: 1,210 rows, 0 NULL, 10 distinct values. Witness values: 'French' occurs 121x; 'az' occurs 0x.
- `set_translations.setCode`: 1,210 rows, 0 NULL, 121 distinct values. Witness values: 'a' occurs 0x; NULL occurs 0x.
- `set_translations.translation`: 1,210 rows, 231 NULL, 504 distinct values. Witness values: 'az' occurs 0x; 'cl' occurs 0x; 'eo' occurs 0x; NULL occurs 231x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-125 (european_football_2)

**Question:** What is the average overall rating of the football player Aaron Doran?

**Evidence:** average overall rating = AVG(overall_rating);

**Gold SQL:**
```sql
SELECT CAST(SUM(t2.overall_rating) AS REAL) / COUNT(t2.id) FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t1.player_name = 'Aaron Doran'
```
**Predicted SQL:**
```sql
SELECT AVG(T1.overall_rating) FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id WHERE T2.player_name = 'Aaron Doran'
```

**Witness database:**

*Player* (5 unreferenced columns omitted)

| player_api_id | player_name |
|---|---|
| 3 | Aaron Doran |
| 1 | Aaron Doran |

*Player_Attributes* (39 unreferenced columns omitted)

| id | player_api_id | overall_rating |
|---|---|---|
| 2 | 3 | 1 |
| 3 | 2 | 3 |
| 1 | 3 | NULL |

**Gold result on the witness:** `[[0.5]]`  
**Predicted result on the witness:** `[[1.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 3 occurs 0x; 1 occurs 0x.
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'Aaron Doran' occurs 1x.
- `Player_Attributes.id`: 183,978 rows, 0 NULL, 183,978 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 3 occurs 1x; 1 occurs 1x.
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 3 occurs 0x; 2 occurs 0x.
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: 1 occurs 0x; 3 occurs 0x; NULL occurs 836x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-043 (codebase_community)

**Question:** What is the average number of badges obtained by a user with over 200 views?

**Evidence:** user with over 200 views refers to Views > 200; average number of badges = Divide (Count(Id), Count(DisplayName))

**Gold SQL:**
```sql
SELECT CAST(COUNT(T1.Id) AS REAL) / COUNT(DISTINCT T2.DisplayName) FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.Views > 200
```
**Predicted SQL:**
```sql
SELECT CAST(COUNT(T2.Id) AS REAL) / COUNT(DISTINCT T1.Id) FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.Views > 200
```

**Witness database:**

*badges* (2 unreferenced columns omitted)

| Id | UserId |
|---|---|
| 0 | 0 |

*comments* (3 unreferenced columns omitted)

| Id | PostId | Score | Text |
|---|---|---|---|
| 0 | 0 | 0 | 2147483648 |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 0 | 0 | 0 | 2147483648 |

*postLinks* (1 unreferenced columns omitted)

| Id | CreationDate | PostId | RelatedPostId |
|---|---|---|---|
| 0 | 1000-01-01 | 0 | 0 |

*posts* (17 unreferenced columns omitted)

| Id | PostTypeId | AcceptedAnswerId | CreaionDate |
|---|---|---|---|
| 0 | 0 | 0 | 1000-01-01 |

*tags* (1 unreferenced columns omitted)

| Id | TagName | Count | ExcerptPostId |
|---|---|---|---|
| 0 | 2147483648 | 0 | 0 |

*users* (11 unreferenced columns omitted)

| Id | DisplayName | Views |
|---|---|---|
| 0 | NULL | 201 |

*votes* (2 unreferenced columns omitted)

| Id | PostId | VoteTypeId | CreationDate |
|---|---|---|---|
| 0 | 0 | 0 | 1000-01-01 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[1.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `badges.Id`: 79,851 rows, 0 NULL, 79,851 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x.
- `badges.UserId`: 79,851 rows, 0 NULL, 25,078 distinct values. Witness values: 0 occurs 0x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: NULL occurs 0x.
- `users.Views`: 40,325 rows, 0 NULL, 362 distinct values. Witness values: 201 occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-088 (codebase_community)

**Question:** What is the display name of the user who acquired the highest amount of badges?

**Evidence:** highest amount of badges refers to MAX(COUNT(Name));

**Gold SQL:**
```sql
SELECT T1.DisplayName FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId GROUP BY T1.DisplayName ORDER BY COUNT(T1.Id) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T2.DisplayName FROM badges AS T1 JOIN users AS T2 ON T1.UserId = T2.Id GROUP BY T2.DisplayName ORDER BY COUNT(T1.Name) DESC LIMIT 1
```

**Witness database:**

*badges* (2 unreferenced columns omitted)

| UserId | Name |
|---|---|
| 0 | NULL |
| 1 | 2147483648 |

*comments* (3 unreferenced columns omitted)

| Id | PostId | Score | Text |
|---|---|---|---|
| -1 | 1 | 0 | 2147483648 |
| 0 | 0 | 0 | 2147483648 |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 1 | 0 | 1 | 2147483648 |
| 0 | 0 | 0 | 2147483648 |

*postLinks* (1 unreferenced columns omitted)

| Id | CreationDate | PostId | RelatedPostId |
|---|---|---|---|
| 0 | 1000-01-01 | 0 | 0 |
| 1 | 1000-01-01 | 0 | 0 |

*posts* (17 unreferenced columns omitted)

| Id | PostTypeId | AcceptedAnswerId | CreaionDate |
|---|---|---|---|
| 1 | 0 | 0 | 1000-01-01 |
| 0 | 0 | 0 | 1000-01-01 |

*tags* (1 unreferenced columns omitted)

| Id | TagName | Count | ExcerptPostId |
|---|---|---|---|
| -1 | 2147483648 | 0 | 1 |
| 0 | 2147483648 | 0 | 0 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 1 | 2147483648 |
| 0 | 2147483649 |

*votes* (2 unreferenced columns omitted)

| Id | PostId | VoteTypeId | CreationDate |
|---|---|---|---|
| 0 | 1 | 0 | 1000-01-01 |
| 1 | 1 | 0 | 1000-01-01 |

**Gold result on the witness:** `[['2147483649']]`  
**Predicted result on the witness:** `[['2147483648']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `badges.UserId`: 79,851 rows, 0 NULL, 25,078 distinct values. Witness values: 0 occurs 0x; 1 occurs 0x.
- `badges.Name`: 79,851 rows, 0 NULL, 153 distinct values. Witness values: NULL occurs 0x; '2147483648' occurs 0x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 0 occurs 0x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: '2147483648' occurs 0x; '2147483649' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-007 (superhero)

**Question:** List down at least five superpowers of male superheroes.

**Evidence:** male refers to gender = 'Male'; superpowers refers to power_name;

**Gold SQL:**
```sql
SELECT T3.power_name FROM superhero AS T1 INNER JOIN hero_power AS T2 ON T1.id = T2.hero_id INNER JOIN superpower AS T3 ON T3.id = T2.power_id INNER JOIN gender AS T4 ON T4.id = T1.gender_id WHERE T4.gender = 'Male' LIMIT 5
```
**Predicted SQL:**
```sql
SELECT DISTINCT sp.power_name FROM superhero sh JOIN gender g ON sh.gender_id = g.id JOIN hero_power hp ON sh.id = hp.hero_id JOIN superpower sp ON hp.power_id = sp.id WHERE g.gender = 'Male' LIMIT 5;
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
| 7 | Blue |
| 23 | Red |
| 13 | Grey |
| 9 | Brown |
| 33 | Yellow |

*gender*

| id | gender |
|---|---|
| 1 | Male |

*hero_power*

| hero_id | power_id |
|---|---|
| 1 | 18 |
| 1 | 31 |
| 2 | 6 |
| 2 | 18 |
| 3 | 1 |
| 3 | 5 |
| 4 | 3 |

*publisher*

| id | publisher_name |
|---|---|
| 13 | Marvel Comics |
| 3 | Dark Horse Comics |
| 4 | DC Comics |

*race*

| id | race |
|---|---|
| 1 | - |
| 24 | Human |
| 33 | Icthyo Sapien |
| 55 | Ungaran |

*superhero* (10 unreferenced columns omitted)

| id | gender_id |
|---|---|
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |

*superpower*

| id | power_name |
|---|---|
| 18 | Super Strength |
| 31 | Super Speed |
| 6 | Durability |
| 1 | Agility |
| 5 | Cold Resistance |
| 3 | Lantern Power Ring |

**Gold result on the witness:** `[['Super Strength'], ['Super Speed'], ['Durability'], ['Super Strength'], ['Agility']]`  
**Predicted result on the witness:** `[['Super Strength'], ['Super Speed'], ['Durability'], ['Agility'], ['Cold Resistance']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `gender.id`: 3 rows, 0 NULL, 3 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x.
- `gender.gender`: 3 rows, 0 NULL, 3 distinct values, all non-NULL values unique. Witness values: 'Male' occurs 1x.
- Real content of `gender` (3 rows; referenced columns): (1, 'Male'); (2, 'Female'); (3, 'N/A').
- `hero_power.hero_id`: 5,825 rows, 0 NULL, 652 distinct values. Witness values: 1 occurs 4x; 2 occurs 7x; 3 occurs 16x; 4 occurs 1x.
- `hero_power.power_id`: 5,825 rows, 0 NULL, 167 distinct values. Witness values: 18 occurs 358x; 31 occurs 249x; 6 occurs 257x; 1 occurs 239x; 5 occurs 48x; 3 occurs 11x.
- `superhero.id`: 750 rows, 0 NULL, 750 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 2 occurs 1x; 3 occurs 1x; 4 occurs 1x.
- `superhero.gender_id`: 750 rows, 0 NULL, 3 distinct values. Witness values: 1 occurs 519x.
- `superpower.id`: 167 rows, 0 NULL, 167 distinct values, all non-NULL values unique. Witness values: 18 occurs 1x; 31 occurs 1x; 6 occurs 1x; 1 occurs 1x; 5 occurs 1x; 3 occurs 1x.
- `superpower.power_name`: 167 rows, 0 NULL, 167 distinct values, all non-NULL values unique. Witness values: 'Super Strength' occurs 1x; 'Super Speed' occurs 1x; 'Durability' occurs 1x; 'Agility' occurs 1x; 'Cold Resistance' occurs 1x; 'Lantern Power Ring' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-105 (codebase_community)

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
| 8 | 8 | 1 | 2020-02-29 23:59:59 |
| 1 | 8 | 1 | 2010-06-15 12:30:00 |
| 2 | 2 | -1 | 2010-06-15 12:30:00 |

*users* (11 unreferenced columns omitted)

| Id | DisplayName | WebsiteUrl |
|---|---|---|
| 1 | 8 | A |
| 8 | 8 | 1 |
| 3 | 1 | b |
| 2 | 1 | 8 |

*votes* (3 unreferenced columns omitted)

| VoteTypeId | UserId | BountyAmount |
|---|---|---|
| 8 | 8 | NULL |
| 1 | 3 | 1 |
| 100 | 3 | 1 |

**Gold result on the witness:** `[['8', '1']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 8 occurs 1x; 3 occurs 1x; 2 occurs 1x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: '8' occurs 0x; '1' occurs 0x.
- `users.WebsiteUrl`: 40,325 rows, 32,204 NULL, 7,787 distinct values. Witness values: 'A' occurs 0x; '1' occurs 0x; 'b' occurs 0x; '8' occurs 0x.
- `votes.VoteTypeId`: 38,930 rows, 0 NULL, 10 distinct values. Witness values: 8 occurs 60x; 1 occurs 1,451x; 100 occurs 0x.
- `votes.UserId`: 38,930 rows, 35,505 NULL, 509 distinct values. Witness values: 8 occurs 13x; 3 occurs 0x.
- `votes.BountyAmount`: 38,930 rows, 38,829 NULL, 6 distinct values. Witness values: NULL occurs 38,829x; 1 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-001 (card_games)

**Question:** Among the Artifact cards, which are black color and comes with foreign languague translation?

**Evidence:** Artifact card refers to originalType = 'Artifact'; black color refers to colors = 'B'; foreign language refers to language in foreign_data

**Gold SQL:**
```sql
SELECT DISTINCT T1.name FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T1.uuid = T2.uuid WHERE T1.originalType = 'Artifact' AND T1.colors = 'B'
```
**Predicted SQL:**
```sql
SELECT DISTINCT cards.name FROM cards INNER JOIN foreign_data ON cards.uuid = foreign_data.uuid WHERE cards.originalType = 'Artifact' AND cards.colors = 'B' AND foreign_data.language IS NOT NULL;
```

**Witness database:**

*cards* (70 unreferenced columns omitted)

| colors | name | originalType | uuid |
|---|---|---|---|
| B | ac | Artifact | a |
| B | ac | Artifact | cr |
| B | cx | Artifact | ab |
| B | cx | Artifact | az |
| B | NULL | Artifact | a1 |
| B | ac | NULL | aa |

*foreign_data* (6 unreferenced columns omitted)

| language | uuid |
|---|---|
| German | a |
| German | cr |
| NULL | ab |
| German | az |
| German | NULL |
| NULL | a1 |
| NULL | aa |

**Gold result on the witness:** `[['ac'], ['cx'], [None]]`  
**Predicted result on the witness:** `[['ac'], ['cx']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `cards.colors`: 56,822 rows, 12,540 NULL, 39 distinct values. Witness values: 'B' occurs 7,807x.
- `cards.name`: 56,822 rows, 0 NULL, 21,738 distinct values. Witness values: 'ac' occurs 0x; 'cx' occurs 0x; NULL occurs 0x.
- `cards.originalType`: 56,822 rows, 14,766 NULL, 2,992 distinct values. Witness values: 'Artifact' occurs 2,093x; NULL occurs 14,766x.
- `cards.uuid`: 56,822 rows, 0 NULL, 56,822 distinct values, all non-NULL values unique. Witness values: 'a' occurs 0x; 'cr' occurs 0x; 'ab' occurs 0x; 'az' occurs 0x; 'a1' occurs 0x; 'aa' occurs 0x.
- `foreign_data.language`: 229,186 rows, 0 NULL, 16 distinct values. Witness values: 'German' occurs 28,891x; NULL occurs 0x.
- `foreign_data.uuid`: 229,186 rows, 0 NULL, 34,056 distinct values. Witness values: 'a' occurs 0x; 'cr' occurs 0x; 'ab' occurs 0x; 'az' occurs 0x; NULL occurs 0x; 'a1' occurs 0x (+1 more).

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-124 (financial)

**Question:** Among the accounts who have loan validity more than 24 months, list out the accounts that have the lowest approved amount and have account opening date before 1997.

**Evidence:** -

**Gold SQL:**
```sql
SELECT T1.account_id FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id WHERE T1.duration > 24 AND STRFTIME('%Y', T2.date) < '1997' ORDER BY T1.amount ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT a.account_id FROM account a JOIN loan l ON a.account_id = l.account_id WHERE l.duration > 24 AND a.date < '1997-01-01' AND l.amount = (SELECT MIN(amount) FROM loan WHERE duration > 24);
```

**Witness database:**

*account* (2 unreferenced columns omitted)

| account_id | date |
|---|---|
| 1004 | 1997-01-01 |
| 1151 | 1997-01-01 |
| 1019 | 1996-12-31 |

*district* (12 unreferenced columns omitted)

| district_id | A2 | A3 | A4 |
|---|---|---|---|
| 1005 | c | south Bohemia | x1 |
| 1020 | b | south Moravia | A |
| 1152 | x1 | south Moravia | c |

*loan* (4 unreferenced columns omitted)

| account_id | amount | duration |
|---|---|---|
| 1004 | 0 | 25 |
| 1019 | 2 | 25 |
| 1019 | 2 | 25 |

**Gold result on the witness:** `[[1019]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `account.account_id`: 4,500 rows, 0 NULL, 4,500 distinct values, all non-NULL values unique. Witness values: 1004 occurs 1x; 1151 occurs 1x; 1019 occurs 1x.
- `account.date`: 4,500 rows, 0 NULL, 1,535 distinct values. Witness values: '1997-01-01' occurs 4x; '1996-12-31' occurs 0x.
- `loan.account_id`: 682 rows, 0 NULL, 682 distinct values, all non-NULL values unique. Witness values: 1004 occurs 1x; 1019 occurs 0x.
- `loan.amount`: 682 rows, 0 NULL, 645 distinct values. Witness values: 0 occurs 0x; 2 occurs 0x.
- `loan.duration`: 682 rows, 0 NULL, 5 distinct values. Witness values: 25 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-052 (thrombosis_prediction)

**Question:** For the patients with an abnormal Ig M level, what is the most common disease they are diagnosed with?

**Evidence:** abnormal Ig M level refers to IGM <=40 OR IGM >= 400; most common disease refers to MAX(COUNT(Diagnosis));

**Gold SQL:**
```sql
SELECT T1.Diagnosis FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.IGM NOT BETWEEN 40 AND 400 GROUP BY T1.Diagnosis ORDER BY COUNT(T1.Diagnosis) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT p.Diagnosis FROM Laboratory l JOIN Patient p ON l.ID = p.ID WHERE l.IGM <= 40 OR l.IGM >= 400 GROUP BY p.Diagnosis ORDER BY COUNT(p.Diagnosis) DESC LIMIT 1
```

**Witness database:**

*Laboratory* (42 unreferenced columns omitted)

| ID | IGM |
|---|---|
| 2 | 400 |

*Patient* (5 unreferenced columns omitted)

| ID | Diagnosis |
|---|---|
| 2 | SLE susp |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['SLE susp']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 2 occurs 0x.
- `Laboratory.IGM`: 13,908 rows, 11,230 NULL, 487 distinct values. Witness values: 400 occurs 0x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 2 occurs 0x.
- `Patient.Diagnosis`: 1,238 rows, 0 NULL, 220 distinct values. Witness values: 'SLE susp' occurs 19x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-072 (codebase_community)

**Question:** What is the id of the youngest user?

**Evidence:** the youngest user refers to MIN(Age);

**Gold SQL:**
```sql
SELECT Id FROM users WHERE Age = ( SELECT MIN(Age) FROM users )
```
**Predicted SQL:**
```sql
SELECT Id FROM users WHERE Age IS NOT NULL ORDER BY Age ASC LIMIT 1
```

**Witness database:**

*badges*

| Id | UserId | Name | Date |
|---|---|---|---|
| 1 | 1 | 2147483648 | 0001-01-01 |
| 2 | 1 | 2147483648 | 0001-01-01 |

*comments* (3 unreferenced columns omitted)

| Id | PostId | Score | Text |
|---|---|---|---|
| 1 | 1 | 0 | 2147483648 |
| 2 | 1 | 0 | 2147483648 |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 1 | 1 | 1 | 2147483648 |
| 2 | 1 | 1 | 2147483648 |

*postLinks* (1 unreferenced columns omitted)

| Id | CreationDate | PostId | RelatedPostId |
|---|---|---|---|
| 1 | 0001-01-01 | 1 | 1 |
| 2 | 0001-01-01 | 1 | 1 |

*posts* (17 unreferenced columns omitted)

| Id | PostTypeId | AcceptedAnswerId | CreaionDate |
|---|---|---|---|
| 2 | 1 | 1 | 0001-01-01 |
| 1 | 1 | 1 | 0001-01-01 |

*tags* (1 unreferenced columns omitted)

| Id | TagName | Count | ExcerptPostId |
|---|---|---|---|
| 1 | 2147483648 | 0 | 1 |
| 2 | 2147483649 | 0 | 2 |

*users* (12 unreferenced columns omitted)

| Id | Age |
|---|---|
| 1 | 0 |
| 2 | 0 |

*votes* (2 unreferenced columns omitted)

| Id | PostId | VoteTypeId | CreationDate |
|---|---|---|---|
| 1 | 2 | 1 | 0001-01-01 |
| 2 | 2 | 1 | 0001-01-01 |

**Gold result on the witness:** `[[1], [2]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 2 occurs 1x.
- `users.Age`: 40,325 rows, 32,007 NULL, 70 distinct values. Witness values: 0 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-033 (thrombosis_prediction)

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
| 1 | 40 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2147483648']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x.
- `Patient.Diagnosis`: 1,238 rows, 0 NULL, 220 distinct values. Witness values: '2147483648' occurs 0x.
- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 1 occurs 0x.
- `Laboratory.IGM`: 13,908 rows, 11,230 NULL, 487 distinct values. Witness values: 40 occurs 4x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-104 (debit_card_specializing)

**Question:** How many transactions were paid in CZK in the morning of 2012/8/26?

**Evidence:** '2012/8/26' can be represented by '2012-08-26'; The morning refers to the time before '13:00:00'

**Gold SQL:**
```sql
SELECT COUNT(T1.TransactionID) FROM transactions_1k AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Date = '2012-08-26' AND T1.Time < '13:00:00' AND T2.Currency = 'CZK'
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM transactions_1k AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.`Date` = '2012-08-26' AND T1.`Time` BETWEEN '00:00:00' AND '13:00:00' AND T2.Currency = 'CZK'
```

**Witness database:**

*customers* (1 unreferenced columns omitted)

| CustomerID | Currency |
|---|---|
| 1 | CZK |
| 2 | EUR |
| 3 | EUR |
| 5476 | CZK |
| 24455 | CZK |

*gasstations*

| GasStationID | ChainID | Country | Segment |
|---|---|---|---|
| 2 | 3 | CZE | Other |
| 3 | 148 | SVK | Other |

*products*

| ProductID | Description |
|---|---|
| 1 | Rucní zadání |
| 3 | Special |
| 2 | Nafta |

*transactions_1k* (5 unreferenced columns omitted)

| TransactionID | Date | Time | CustomerID |
|---|---|---|---|
| 2 | 2012-08-26 | 13:00:00 | 5476 |
| 3 | 2012-08-24 | 13:00:00 | 24455 |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `customers.CustomerID`: 32,461 rows, 0 NULL, 32,461 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 2 occurs 0x; 3 occurs 1x; 5476 occurs 1x; 24455 occurs 1x.
- `customers.Currency`: 32,461 rows, 0 NULL, 2 distinct values. Witness values: 'CZK' occurs 30,459x; 'EUR' occurs 2,002x.
- `transactions_1k.TransactionID`: 1,000 rows, 0 NULL, 1,000 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 3 occurs 1x.
- `transactions_1k.Date`: 1,000 rows, 0 NULL, 4 distinct values. Witness values: '2012-08-26' occurs 73x; '2012-08-24' occurs 492x.
- `transactions_1k.Time`: 1,000 rows, 0 NULL, 599 distinct values. Witness values: '13:00:00' occurs 0x.
- `transactions_1k.CustomerID`: 1,000 rows, 0 NULL, 517 distinct values. Witness values: 5476 occurs 8x; 24455 occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-084 (codebase_community)

**Question:** Under the vote type of 8, provide the display names and websites URLs of the user who got the highest bounty amount.

**Evidence:** vote type of 8 refers to VoteTypeId = 8; the highest bounty amount refers to MAX(BountyAmount);

**Gold SQL:**
```sql
SELECT DisplayName, WebsiteUrl FROM users WHERE Id = ( SELECT UserId FROM votes WHERE VoteTypeId = 8 ORDER BY BountyAmount DESC LIMIT 1 )
```
**Predicted SQL:**
```sql
SELECT users.DisplayName, users.WebsiteUrl FROM votes INNER JOIN users ON votes.UserId = users.Id WHERE votes.VoteTypeId = 8 AND votes.BountyAmount = ( SELECT MAX(BountyAmount) FROM votes WHERE VoteTypeId = 8 );
```

**Witness database:**

*badges*

| Id | UserId | Name | Date |
|---|---|---|---|
| 0 | 0 | 2147483648 | 1000-01-01 |

*comments* (3 unreferenced columns omitted)

| Id | PostId | Score | Text |
|---|---|---|---|
| 0 | 0 | 0 | 2147483648 |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 0 | 0 | 0 | 2147483648 |

*postLinks* (1 unreferenced columns omitted)

| Id | CreationDate | PostId | RelatedPostId |
|---|---|---|---|
| 0 | 1000-01-01 | 0 | 0 |

*posts* (17 unreferenced columns omitted)

| Id | PostTypeId | AcceptedAnswerId | CreaionDate |
|---|---|---|---|
| 0 | 0 | 0 | 1000-01-01 |

*tags* (1 unreferenced columns omitted)

| Id | TagName | Count | ExcerptPostId |
|---|---|---|---|
| 0 | 2147483648 | 0 | 0 |

*users* (11 unreferenced columns omitted)

| Id | DisplayName | WebsiteUrl |
|---|---|---|
| 0 | 2147483648 | 2147483648 |

*votes* (3 unreferenced columns omitted)

| VoteTypeId | UserId | BountyAmount |
|---|---|---|
| 8 | 0 | NULL |

**Gold result on the witness:** `[['2147483648', '2147483648']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: '2147483648' occurs 0x.
- `users.WebsiteUrl`: 40,325 rows, 32,204 NULL, 7,787 distinct values. Witness values: '2147483648' occurs 0x.
- `votes.VoteTypeId`: 38,930 rows, 0 NULL, 10 distinct values. Witness values: 8 occurs 60x.
- `votes.UserId`: 38,930 rows, 35,505 NULL, 509 distinct values. Witness values: 0 occurs 0x.
- `votes.BountyAmount`: 38,930 rows, 38,829 NULL, 6 distinct values. Witness values: NULL occurs 38,829x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-022 (card_games)

**Question:** How many cards with unknown power that can't be found in foil is in duel deck A?

**Evidence:** unknown power refers to power IS NULL or power = '*'; can't be found in foil refers to hasFoil = 0; duel deck A refers to duelDeck = 'a'

**Gold SQL:**
```sql
SELECT SUM(CASE WHEN power = '*' OR power IS NULL THEN 1 ELSE 0 END) FROM cards WHERE hasFoil = 0 AND duelDeck = 'a'
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM cards WHERE (power IS NULL OR power = '*') AND hasfoil = 0 AND dueldeck = 'a'
```

**Witness database:**

*cards* (71 unreferenced columns omitted)

| duelDeck | hasFoil | power |
|---|---|---|
| b | 0 | 2147483648 |

*foreign_data* (4 unreferenced columns omitted)

| id | flavorText | language | multiverseid |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | 0 |

*legalities*

| id | format | status | uuid |
|---|---|---|---|
| 1 | 2147483648 | Restricted | 2147483648 |

*sets* (17 unreferenced columns omitted)

| id | baseSetSize | block | booster |
|---|---|---|---|
| 1 | 0 | 2147483648 | 2147483648 |

*set_translations*

| id | language | setCode | translation |
|---|---|---|---|
| 1 | Japanese | 2147483648 | 2147483648 |

*rulings*

| id | date | text | uuid |
|---|---|---|---|
| 1 | 0001-01-01 | 2147483648 | 2147483648 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `cards.duelDeck`: 56,822 rows, 55,228 NULL, 2 distinct values. Witness values: 'b' occurs 790x.
- `cards.hasFoil`: 56,822 rows, 0 NULL, 2 distinct values. Witness values: 0 occurs 22,204x.
- `cards.power`: 56,822 rows, 30,624 NULL, 28 distinct values. Witness values: '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-038 (european_football_2)

**Question:** What is the preferred foot when attacking of the player with the lowest potential?

**Evidence:** preferred foot when attacking refers to preferred_foot; lowest potential refers to MIN(potential);

**Gold SQL:**
```sql
SELECT preferred_foot FROM Player_Attributes WHERE potential IS NOT NULL ORDER BY potential ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT `preferred_foot` FROM `player_attributes` WHERE `potential` = (SELECT MIN(`potential`) FROM `player_attributes`)
```

**Witness database:**

*Player_Attributes* (40 unreferenced columns omitted)

| potential | preferred_foot |
|---|---|
| 0 | right |
| 0 | left |

*Player* (3 unreferenced columns omitted)

| id | player_api_id | player_name | player_fifa_api_id |
|---|---|---|---|
| 1 | 2625 | 2147483648 | 0 |
| 2 | 2624 | 2147483648 | -1 |

*League*

| id | country_id | name |
|---|---|---|
| 1 | 0 | 2147483648 |
| 0 | 0 | 2147483648 |

*Country*

| id | name |
|---|---|
| 1 | 2147483648 |
| 0 | 2147483648 |

*Team* (1 unreferenced columns omitted)

| id | team_api_id | team_fifa_api_id | team_long_name |
|---|---|---|---|
| 1 | 0 | 0 | 2147483648 |
| 2 | 1 | 1 | 2147483649 |

*Team_Attributes* (21 unreferenced columns omitted)

| id | team_fifa_api_id | team_api_id | date |
|---|---|---|---|
| 1 | 0 | 0 | 2147483648 |
| 2 | 1 | 1 | 2147483648 |

*Match* (111 unreferenced columns omitted)

| id | country_id | league_id | season |
|---|---|---|---|
| 1 | 1 | 1 | 2147483648 |
| 2 | 1 | 1 | 2147483648 |

**Gold result on the witness:** `[['right']]`  
**Predicted result on the witness:** `[['right'], ['left']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player_Attributes.potential`: 183,978 rows, 836 NULL, 56 distinct values. Witness values: 0 occurs 0x.
- `Player_Attributes.preferred_foot`: 183,978 rows, 836 NULL, 2 distinct values. Witness values: 'right' occurs 138,409x; 'left' occurs 44,733x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-046 (toxicology)

**Question:** What are the bond type for atoms with element Tin?

**Evidence:** element Tin refers to element = 'sn'; double bond refers to bond_type = ' = '; single bond refers to bond_type = '-'; triple bond refers to bond_type = '#'

**Gold SQL:**
```sql
SELECT DISTINCT T3.bond_type FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id INNER JOIN bond AS T3 ON T3.bond_id = T2.bond_id WHERE T1.element = 'sn'
```
**Predicted SQL:**
```sql
SELECT DISTINCT `bond`.`bond_type` FROM `atom` INNER JOIN `connected` ON `atom`.`atom_id` = `connected`.`atom_id` OR `atom`.`atom_id` = `connected`.`atom_id2` INNER JOIN `bond` ON `connected`.`bond_id` = `bond`.`bond_id` WHERE `atom`.`element` = 'sn'
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| atom_id | element |
|---|---|
| sn | sn |
| k2 | cl |

*bond* (1 unreferenced columns omitted)

| bond_id | bond_type |
|---|---|
| k3 | = |
| sn | = |
| k2 | NULL |
| k1 | # |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| k2 | sn | k1 |

*molecule*

| molecule_id | label |
|---|---|
| k3 | - |
| sn | - |
| k1 | + |
| k2 | + |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['#']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.atom_id`: 12,333 rows, 0 NULL, 12,333 distinct values, all non-NULL values unique. Witness values: 'sn' occurs 0x; 'k2' occurs 0x.
- `atom.element`: 12,333 rows, 0 NULL, 21 distinct values. Witness values: 'sn' occurs 2x; 'cl' occurs 429x.
- `bond.bond_id`: 12,379 rows, 0 NULL, 12,379 distinct values, all non-NULL values unique. Witness values: 'k3' occurs 0x; 'sn' occurs 0x; 'k2' occurs 0x; 'k1' occurs 0x.
- `bond.bond_type`: 12,379 rows, 1 NULL, 3 distinct values. Witness values: '=' occurs 1,844x; NULL occurs 1x; '#' occurs 6x.
- `connected.atom_id`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'k2' occurs 0x.
- `connected.atom_id2`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'sn' occurs 0x.
- `connected.bond_id`: 24,758 rows, 0 NULL, 12,379 distinct values. Witness values: 'k1' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-025 (codebase_community)

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

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 164181 | 2 | 51463 | 707034dc-8d9c-4398-a415-93d43daa0852 |

*posts* (19 unreferenced columns omitted)

| OwnerUserId | FavoriteCount |
|---|---|
| 7486 | NULL |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 7486 | Robert Long |

**Gold result on the witness:** `[['Robert Long']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `posts.OwnerUserId`: 91,966 rows, 1,392 NULL, 21,979 distinct values. Witness values: 7486 occurs 30x.
- `posts.FavoriteCount`: 91,966 rows, 78,723 NULL, 77 distinct values. Witness values: NULL occurs 78,723x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 7486 occurs 1x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: 'Robert Long' occurs 2x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-058 (formula_1)

**Question:** What is the average lap time for Lewis Hamilton in the 2009 Malaysian Grand Prix?

**Evidence:** average lap time = AVG(milliseconds); 'Lewis Hamilton' refers to the full name of the driver; Full name of the driver refers to drivers.forename and drivers.surname; 'Malaysian Grand Prix' refers to races.name = 'Malaysian Grand Prix'

**Gold SQL:**
```sql
SELECT AVG(T2.milliseconds) FROM races AS T1 INNER JOIN lapTimes AS T2 ON T2.raceId = T1.raceId INNER JOIN drivers AS T3 ON T3.driverId = T2.driverId WHERE T3.forename = 'Lewis' AND T3.surname = 'Hamilton' AND T1.year = 2009 AND T1.name = 'Malaysian Grand Prix'
```
**Predicted SQL:**
```sql
SELECT AVG(laptimes.milliseconds) FROM drivers INNER JOIN results ON drivers.driverId = results.driverId INNER JOIN races ON results.raceId = races.raceId INNER JOIN laptimes ON results.raceId = laptimes.raceId AND results.driverId = laptimes.driverId WHERE drivers.forename = 'Lewis' AND drivers.surname = 'Hamilton' AND races.year = 2009 AND races.name = 'Malaysian Grand Prix'
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 12359 | yeongam | Korean International Circuit | Yeongam County |
| 12371 | zandvoort | Circuit Park Zandvoort | Zandvoort |
| 12389 | valencia | Valencia Street Circuit | Valencia |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 12360 | del_roy | Del Roy | American |
| 12372 | mclaren-alfa_romeo | McLaren-Alfa Romeo | British |

*drivers* (6 unreferenced columns omitted)

| driverId | forename | surname |
|---|---|---|
| 12361 | Lewis | Hamilton |
| 12373 | Lewis | Hamilton |
| 12387 | Lewis | Hamilton |

*lapTimes* (3 unreferenced columns omitted)

| raceId | driverId | milliseconds |
|---|---|---|
| 12362 | 12361 | 77710 |
| 12374 | 12373 | 80450 |

*races* (5 unreferenced columns omitted)

| raceId | year | name |
|---|---|---|
| 12362 | 2009 | Malaysian Grand Prix |
| 12374 | 1999 | Malaysian Grand Prix |
| 12388 | 2008 | Portuguese Grand Prix |

*results* (16 unreferenced columns omitted)

| raceId | driverId |
|---|---|
| 12388 | 12361 |
| 12374 | 12373 |
| 12362 | 12387 |

*seasons*

| year | url |
|---|---|
| 2009 | http://en.wikipedia.org/wiki/2009_Formula_One_season |
| 1999 | http://en.wikipedia.org/wiki/1999_Formula_One_season |
| 2008 | http://en.wikipedia.org/wiki/2008_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 1 | Finished |
| 77 | 107% Rule |

**Gold result on the witness:** `[[77710.0]]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 12361 occurs 0x; 12373 occurs 0x; 12387 occurs 0x.
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: 'Lewis' occurs 1x.
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: 'Hamilton' occurs 2x.
- `lapTimes.raceId`: 420,369 rows, 0 NULL, 389 distinct values. Witness values: 12362 occurs 0x; 12374 occurs 0x.
- `lapTimes.driverId`: 420,369 rows, 0 NULL, 121 distinct values. Witness values: 12361 occurs 0x; 12373 occurs 0x.
- `lapTimes.milliseconds`: 420,369 rows, 0 NULL, 67,578 distinct values. Witness values: 77710 occurs 26x; 80450 occurs 29x.
- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 12362 occurs 0x; 12374 occurs 0x; 12388 occurs 0x.
- `races.year`: 976 rows, 0 NULL, 68 distinct values. Witness values: 2009 occurs 17x; 1999 occurs 16x; 2008 occurs 18x.
- `races.name`: 976 rows, 0 NULL, 42 distinct values. Witness values: 'Malaysian Grand Prix' occurs 19x; 'Portuguese Grand Prix' occurs 16x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 12388 occurs 0x; 12374 occurs 0x; 12362 occurs 0x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 12361 occurs 0x; 12373 occurs 0x; 12387 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-049 (formula_1)

**Question:** Which driver created the fastest lap speed in a Formula_1 race? Please give both his forename and surname.

**Evidence:** -

**Gold SQL:**
```sql
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId WHERE T2.fastestLapTime IS NOT NULL ORDER BY T2.fastestLapSpeed DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.forename, T1.surname FROM drivers AS T1 JOIN results AS T2 ON T1.driverId = T2.driverId ORDER BY T2.fastestLapSpeed DESC LIMIT 1
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

*drivers* (6 unreferenced columns omitted)

| driverId | forename | surname |
|---|---|---|
| 0 | 2147483648 | 2147483648 |

*seasons*

| year | url |
|---|---|
| 0 | 2147483648 |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

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

*results* (15 unreferenced columns omitted)

| driverId | fastestLapTime | fastestLapSpeed |
|---|---|---|
| 0 | NULL | 2147483648 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2147483648', '2147483648']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x.
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: '2147483648' occurs 0x.
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: '2147483648' occurs 0x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 0 occurs 0x.
- `results.fastestLapTime`: 23,657 rows, 18,389 NULL, 4,955 distinct values. Witness values: NULL occurs 18,389x.
- `results.fastestLapSpeed`: 23,657 rows, 18,389 NULL, 5,045 distinct values. Witness values: '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-040 (codebase_community)

**Question:** What is the display name of the user who acquired the highest amount of badges?

**Evidence:** highest amount of badges refers to MAX(COUNT(Name));

**Gold SQL:**
```sql
SELECT T1.DisplayName FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId GROUP BY T1.DisplayName ORDER BY COUNT(T1.Id) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT u.DisplayName FROM users u JOIN badges b ON u.Id = b.UserId GROUP BY u.Id ORDER BY COUNT(b.Name) DESC LIMIT 1;
```

**Witness database:**

*badges* (2 unreferenced columns omitted)

| UserId | Name |
|---|---|
| 1 | f |
| 15 | t |
| 1 | t |
| 25 | f |
| 25 | f |
| NULL | ac |
| 1 | NULL |
| 59 | u |
| 59 | aw |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 1 | NULL |
| 15 | NULL |
| 25 | NULL |
| 59 | ap |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[['ap']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `badges.UserId`: 79,851 rows, 0 NULL, 25,078 distinct values. Witness values: 1 occurs 0x; 15 occurs 1x; 25 occurs 72x; NULL occurs 0x; 59 occurs 20x.
- `badges.Name`: 79,851 rows, 0 NULL, 153 distinct values. Witness values: 'f' occurs 0x; 't' occurs 0x; 'ac' occurs 0x; NULL occurs 0x; 'u' occurs 0x; 'aw' occurs 0x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 15 occurs 1x; 25 occurs 1x; 59 occurs 1x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: NULL occurs 0x; 'ap' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-097 (formula_1)

**Question:** What was the fastest lap speed among all drivers in the 2009 Spanish Grand Prix?

**Evidence:** the fastest lap speed among all refers to max(fastestLapSpeed); Spanish Grand Prix refers to races.name = 'Spanish Grand Prix';

**Gold SQL:**
```sql
SELECT T2.fastestLapSpeed FROM races AS T1 INNER JOIN results AS T2 ON T2.raceId = T1.raceId WHERE T1.name = 'Spanish Grand Prix' AND T1.year = 2009 AND T2.fastestLapSpeed IS NOT NULL ORDER BY T2.fastestLapSpeed DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT MAX(results.fastestlapspeed) AS fastestlapspeed FROM results INNER JOIN races ON results.raceid = races.raceid WHERE races.name = 'Spanish Grand Prix' AND races.year = 2009
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 23 | osterreichring | A1-Ring | Spielburg |
| 21 | imola | Autodromo Enzo e Dino Ferrari | Imola |
| 6 | monaco | Circuit de Monaco | Monte-Carlo |
| 17 | shanghai | Shanghai International Circuit | Shanghai |
| 46 | watkins_glen | Watkins Glen | New York State |
| 18 | interlagos | Autódromo José Carlos Pace | São Paulo |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 65 | martini | Martini | French |
| 4 | renault | Renault | French |
| 78 | amon | Amon | New Zealand |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 163 | arnoux | NULL | NULL |
| 21 | fisichella | NULL | FIS |
| 278 | amon | NULL | NULL |

*races* (5 unreferenced columns omitted)

| raceId | year | name |
|---|---|---|
| 129 | 2002 | Austrian Grand Prix |
| 470 | 1982 | San Marino Grand Prix |
| 278 | 1993 | Monaco Grand Prix |
| 903 | 2014 | Chinese Grand Prix |
| 541 | 1978 | United States Grand Prix |
| 52 | 2007 | Brazilian Grand Prix |
| 595 | 1974 | Monaco Grand Prix |

*results* (16 unreferenced columns omitted)

| raceId | fastestLapSpeed |
|---|---|
| 541 | NULL |
| 52 | 126.446 |
| 595 | NULL |

*seasons*

| year | url |
|---|---|
| 2002 | http://en.wikipedia.org/wiki/2002_Formula_One_season |
| 1982 | http://en.wikipedia.org/wiki/1982_Formula_One_season |
| 1993 | http://en.wikipedia.org/wiki/1993_Formula_One_season |
| 2014 | http://en.wikipedia.org/wiki/2014_Formula_One_season |
| 1978 | http://en.wikipedia.org/wiki/1978_Formula_One_season |
| 2007 | http://en.wikipedia.org/wiki/2007_Formula_One_season |
| 1974 | http://en.wikipedia.org/wiki/1974_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 11 | +1 Lap |
| 4 | Collision |
| 54 | Withdrew |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 129 occurs 1x; 470 occurs 1x; 278 occurs 1x; 903 occurs 1x; 541 occurs 1x; 52 occurs 1x (+1 more).
- `races.year`: 976 rows, 0 NULL, 68 distinct values. Witness values: 2002 occurs 17x; 1982 occurs 16x; 1993 occurs 16x; 2014 occurs 19x; 1978 occurs 16x; 2007 occurs 17x (+1 more).
- `races.name`: 976 rows, 0 NULL, 42 distinct values. Witness values: 'Austrian Grand Prix' occurs 30x; 'San Marino Grand Prix' occurs 26x; 'Monaco Grand Prix' occurs 64x; 'Chinese Grand Prix' occurs 14x; 'United States Grand Prix' occurs 39x; 'Brazilian Grand Prix' occurs 45x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 541 occurs 27x; 52 occurs 22x; 595 occurs 28x.
- `results.fastestLapSpeed`: 23,657 rows, 18,389 NULL, 5,045 distinct values. Witness values: NULL occurs 18,389x; '126.446' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-003 (codebase_community)

**Question:** How many users from India have the teacher badges?

**Evidence:** "India" is the Location; "Teacher" is the Name of badge

**Gold SQL:**
```sql
SELECT COUNT(T1.Id) FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.Location = 'India' AND T1.Name = 'Teacher'
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT b.UserId) FROM badges b JOIN users u ON b.UserId = u.Id WHERE LOWER(u.Location) = 'india' AND b.Name = 'Teacher';
```

**Witness database:**

*badges* (1 unreferenced columns omitted)

| Id | UserId | Name |
|---|---|---|
| 2 | 1 | Teacher |
| 1 | 2 | Scholar |

*users* (12 unreferenced columns omitted)

| Id | Location |
|---|---|
| 2 | India |
| 1 | india |
| 3 | New York, NY |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `badges.Id`: 79,851 rows, 0 NULL, 79,851 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 1 occurs 1x.
- `badges.UserId`: 79,851 rows, 0 NULL, 25,078 distinct values. Witness values: 1 occurs 0x; 2 occurs 3x.
- `badges.Name`: 79,851 rows, 0 NULL, 153 distinct values. Witness values: 'Teacher' occurs 4,679x; 'Scholar' occurs 6,523x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 1 occurs 0x; 3 occurs 1x.
- `users.Location`: 40,325 rows, 28,634 NULL, 2,464 distinct values. Witness values: 'India' occurs 206x; 'india' occurs 1x; 'New York, NY' occurs 116x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-008 (superhero)

**Question:** How many heroes have the highest attribute value in strength?

**Evidence:** highest attribute value in strength refers to MAX(attribute_value) WHERE attribute_name = 'Strength';

**Gold SQL:**
```sql
SELECT COUNT(T1.hero_id) FROM hero_attribute AS T1 INNER JOIN attribute AS T2 ON T1.attribute_id = T2.id WHERE T2.attribute_name = 'Strength' AND T1.attribute_value = ( SELECT MAX(attribute_value) FROM hero_attribute )
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT hero_id) FROM hero_attribute WHERE attribute_id = (SELECT id FROM attribute WHERE attribute_name = 'Strength') AND attribute_value = (SELECT MAX(attribute_value) FROM hero_attribute WHERE attribute_id = (SELECT id FROM attribute WHERE attribute_name = 'Strength'))
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 1 | Good |

*attribute*

| id | attribute_name |
|---|---|
| 1 | Intelligence |
| 2 | Strength |
| 3 | Speed |

*colour*

| id | colour |
|---|---|
| 1 | No Colour |
| 13 | Grey |
| 9 | Brown |
| 33 | Yellow |

*gender*

| id | gender |
|---|---|
| 1 | Male |

*hero_attribute*

| hero_id | attribute_id | attribute_value |
|---|---|---|
| 1 | 3 | 25 |
| 2 | 2 | 10 |

*publisher*

| id | publisher_name |
|---|---|
| 13 | Marvel Comics |

*race*

| id | race |
|---|---|
| 1 | - |
| 24 | Human |

*superhero* (8 unreferenced columns omitted)

| id | superhero_name | full_name | gender_id |
|---|---|---|---|
| 1 | 3-D Man | Charles Chandler | 1 |
| 2 | A-Bomb | Richard Milhouse Jones | 1 |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `attribute.id`: 6 rows, 0 NULL, 6 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 2 occurs 1x; 3 occurs 1x.
- `attribute.attribute_name`: 6 rows, 0 NULL, 6 distinct values, all non-NULL values unique. Witness values: 'Intelligence' occurs 1x; 'Strength' occurs 1x; 'Speed' occurs 1x.
- Real content of `attribute` (6 rows; referenced columns): (1, 'Intelligence'); (2, 'Strength'); (3, 'Speed'); (4, 'Durability'); (5, 'Power'); (6, 'Combat').
- `hero_attribute.hero_id`: 3,738 rows, 0 NULL, 623 distinct values. Witness values: 1 occurs 6x; 2 occurs 6x.
- `hero_attribute.attribute_id`: 3,738 rows, 0 NULL, 6 distinct values. Witness values: 3 occurs 623x; 2 occurs 623x.
- `hero_attribute.attribute_value`: 3,738 rows, 0 NULL, 20 distinct values. Witness values: 25 occurs 400x; 10 occurs 222x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-099 (european_football_2)

**Question:** Calculate the average overall rating of Pietro Marino.

**Evidence:** Pietro Marino refers to player_name = 'Pietro Marino'; average overall rating AVG(T1.overall_rating)

**Gold SQL:**
```sql
SELECT CAST(SUM(t2.overall_rating) AS REAL) / COUNT(t2.id) FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t1.player_name = 'Pietro Marino'
```
**Predicted SQL:**
```sql
SELECT AVG(T1.overall_rating) FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_fifa_api_id = T2.player_fifa_api_id WHERE T2.player_name = 'Pietro Marino'
```

**Witness database:**

*Player* (4 unreferenced columns omitted)

| player_api_id | player_name | player_fifa_api_id |
|---|---|---|
| 2805 | Pietro Marino | 249 |
| 147729 | Luiz Gustavo | 185221 |
| 69637 | Piotr Grzelczak | 180430 |
| 30955 | Andres Iniesta | 41 |
| 24217 | Emre Belozoglu | 80 |
| 3316 | Oscar Sanchez | 146501 |
| 35559 | Jose Saez | 100330 |

*Player_Attributes* (38 unreferenced columns omitted)

| id | player_fifa_api_id | player_api_id | overall_rating |
|---|---|---|---|
| 3 | 249 | 2805 | NULL |
| 1 | 185221 | 147729 | NULL |
| 2 | 80 | 24217 | 67 |
| 136900 | 146501 | 3316 | 64 |
| 89078 | 100330 | 35559 | 64 |
| 154463 | 249 | 2805 | 71 |
| 12774 | 41 | 30955 | 88 |
| 50309 | 80 | 24217 | 81 |
| 1335 | 180430 | 69637 | 83 |
| 1336 | 249 | 2805 | 68 |

**Gold result on the witness:** `[[46.333333333333336]]`  
**Predicted result on the witness:** `[[69.5]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 2805 occurs 1x; 147729 occurs 1x; 69637 occurs 1x; 30955 occurs 1x; 24217 occurs 1x; 3316 occurs 1x (+1 more).
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'Pietro Marino' occurs 1x; 'Luiz Gustavo' occurs 1x; 'Piotr Grzelczak' occurs 1x; 'Andres Iniesta' occurs 1x; 'Emre Belozoglu' occurs 1x; 'Oscar Sanchez' occurs 1x (+1 more).
- `Player.player_fifa_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 249 occurs 1x; 185221 occurs 1x; 180430 occurs 1x; 41 occurs 1x; 80 occurs 1x; 146501 occurs 1x (+1 more).
- `Player_Attributes.id`: 183,978 rows, 0 NULL, 183,978 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x; 1 occurs 1x; 2 occurs 1x; 136900 occurs 1x; 89078 occurs 1x; 154463 occurs 1x (+4 more).
- `Player_Attributes.player_fifa_api_id`: 183,978 rows, 0 NULL, 11,062 distinct values. Witness values: 249 occurs 16x; 185221 occurs 20x; 80 occurs 26x; 146501 occurs 13x; 100330 occurs 15x; 41 occurs 25x (+1 more).
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 2805 occurs 28x; 147729 occurs 20x; 24217 occurs 26x; 3316 occurs 13x; 35559 occurs 15x; 30955 occurs 25x (+1 more).
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: NULL occurs 836x; 67 occurs 10,198x; 64 occurs 9,030x; 71 occurs 9,354x; 88 occurs 151x; 81 occurs 2,174x (+2 more).

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-027 (thrombosis_prediction)

**Question:** Among the patients whose level of Hematoclit isn't normal, which patient has the highest anti-Cardiolipin antibody concentration? Please list his or her ID.

**Evidence:** Hematoclit is normal refers to 29 < N < 52; highest anti-Cardiolipin antibody concentration refers to MAX(`aCL IgA`);

**Gold SQL:**
```sql
SELECT DISTINCT T1.ID FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID INNER JOIN Laboratory AS T3 on T1.ID = T3.ID WHERE (T3.HCT >= 52 OR T3.HCT <= 29) ORDER BY T2.`aCL IgA` DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT E.ID FROM Examination AS E INNER JOIN Patient AS P ON E.ID = P.ID INNER JOIN Laboratory AS L ON P.ID = L.ID WHERE(L.ALB < 29 AND L.ALB > 52) OR(L.ALB IS NULL) GROUP BY E.ID ORDER BY MAX(E.`aCL IgA`) DESC LIMIT 1
```

**Witness database:**

*Examination* (11 unreferenced columns omitted)

| ID | aCL IgA |
|---|---|
| 0 | 0 |

*Patient* (6 unreferenced columns omitted)

| ID |
|---|
| 0 |

*Laboratory* (41 unreferenced columns omitted)

| ID | ALB | HCT |
|---|---|---|
| 0 | 0 | 52 |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: 0 occurs 0x.
- `Examination.aCL IgA`: 806 rows, 0 NULL, 52 distinct values. Witness values: 0 occurs 409x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x.
- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 0 occurs 0x.
- `Laboratory.ALB`: 13,908 rows, 2,840 NULL, 39 distinct values. Witness values: 0 occurs 0x.
- `Laboratory.HCT`: 13,908 rows, 1,827 NULL, 363 distinct values. Witness values: 52 occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-112 (student_club)

**Question:** Among all events hold by the Student_Club in 2019, find the percentage share of events related to 'Community Service'

**Evidence:** DIVIDE(SUM(type = 'Community Service'), COUNT(event_id)) * 100 where event_date BETWEEN' 2019-01-01' and '2019-12-31'

**Gold SQL:**
```sql
SELECT CAST(SUM(CASE WHEN type = 'Community Service' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(type) FROM event WHERE SUBSTR(event_date, 1, 4) = '2019'
```
**Predicted SQL:**
```sql
SELECT CAST(SUM(CASE WHEN type = 'Community Service' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(event_id) AS percentage FROM event WHERE STRFTIME('%Y', event_date) = '2019'
```

**Witness database:**

*event* (4 unreferenced columns omitted)

| event_id | event_date | type |
|---|---|---|
| v1036 | 2019-01-01 | NULL |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[0.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `event.event_id`: 42 rows, 0 NULL, 42 distinct values, all non-NULL values unique. Witness values: 'v1036' occurs 0x.
- `event.event_date`: 42 rows, 0 NULL, 41 distinct values. Witness values: '2019-01-01' occurs 0x.
- `event.type`: 42 rows, 0 NULL, 8 distinct values. Witness values: NULL occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-076 (european_football_2)

**Question:** What is the average overall rating of the football player Aaron Doran?

**Evidence:** average overall rating = AVG(overall_rating);

**Gold SQL:**
```sql
SELECT CAST(SUM(t2.overall_rating) AS REAL) / COUNT(t2.id) FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t1.player_name = 'Aaron Doran'
```
**Predicted SQL:**
```sql
SELECT AVG(T2.overall_rating) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_fifa_api_id = T2.player_fifa_api_id WHERE T1.player_name = 'Aaron Doran'
```

**Witness database:**

*Player* (4 unreferenced columns omitted)

| player_api_id | player_name | player_fifa_api_id |
|---|---|---|
| 2977 | Aaron Doran | 246 |
| 3 | Aaron Doran | 269 |

*Player_Attributes* (38 unreferenced columns omitted)

| id | player_fifa_api_id | player_api_id | overall_rating |
|---|---|---|---|
| 1398 | 246 | 2977 | NULL |
| 1402 | 269 | 3 | 69 |

**Gold result on the witness:** `[[34.5]]`  
**Predicted result on the witness:** `[[69.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 2977 occurs 1x; 3 occurs 0x.
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'Aaron Doran' occurs 1x.
- `Player.player_fifa_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 246 occurs 1x; 269 occurs 1x.
- `Player_Attributes.id`: 183,978 rows, 0 NULL, 183,978 distinct values, all non-NULL values unique. Witness values: 1398 occurs 1x; 1402 occurs 1x.
- `Player_Attributes.player_fifa_api_id`: 183,978 rows, 0 NULL, 11,062 distinct values. Witness values: 246 occurs 13x; 269 occurs 8x.
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 2977 occurs 8x; 3 occurs 0x.
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: NULL occurs 836x; 69 occurs 10,281x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-019 (thrombosis_prediction)

**Question:** Among the patients whose level of Hematoclit isn't normal, which patient has the highest anti-Cardiolipin antibody concentration? Please list his or her ID.

**Evidence:** Hematoclit is normal refers to 29 < N < 52; highest anti-Cardiolipin antibody concentration refers to MAX(`aCL IgA`);

**Gold SQL:**
```sql
SELECT DISTINCT T1.ID FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID INNER JOIN Laboratory AS T3 on T1.ID = T3.ID WHERE (T3.HCT >= 52 OR T3.HCT <= 29) ORDER BY T2.`aCL IgA` DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.ID FROM Examination AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.HCT < 29 OR T2.HCT > 52 ORDER BY T1.`aCL IgA` DESC LIMIT 1
```

**Witness database:**

*Examination* (11 unreferenced columns omitted)

| ID | aCL IgA |
|---|---|
| 1 | 0 |

*Patient* (6 unreferenced columns omitted)

| ID |
|---|
| 1 |

*Laboratory* (42 unreferenced columns omitted)

| ID | HCT |
|---|---|
| 1 | 29 |

**Gold result on the witness:** `[[1]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: 1 occurs 0x.
- `Examination.aCL IgA`: 806 rows, 0 NULL, 52 distinct values. Witness values: 0 occurs 409x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x.
- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 1 occurs 0x.
- `Laboratory.HCT`: 13,908 rows, 1,827 NULL, 363 distinct values. Witness values: 29 occurs 16x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-002 (california_schools)

**Question:** Between 1/1/2000 to 12/31/2005, how many directly funded schools opened in the county of Stanislaus?

**Evidence:** Directly funded schools refers to FundingType = 'Directly Funded'

**Gold SQL:**
```sql
SELECT COUNT(School) FROM schools WHERE strftime('%Y', OpenDate) BETWEEN '2000' AND '2005' AND County = 'Stanislaus' AND FundingType = 'Directly funded'
```
**Predicted SQL:**
```sql
SELECT COUNT(CDSCode) FROM schools WHERE FundingType = 'Directly funded' AND County = 'Stanislaus' AND OpenDate BETWEEN '2000-01-01' AND '2005-12-31'
```

**Witness database:**

*schools* (44 unreferenced columns omitted)

| CDSCode | County | School | OpenDate | FundingType |
|---|---|---|---|---|
| 01100170000000 | Sonoma | Directly funded | 1980-07-01 | Directly funded |
| 01100170112607 | Fresno | Cantua Elementary | 1993-09-01 | NULL |
| 01100170109835 | Stanislaus | NULL | 2003-09-02 | Directly funded |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `schools.CDSCode`: 17,686 rows, 0 NULL, 17,686 distinct values, all non-NULL values unique. Witness values: '01100170000000' occurs 1x; '01100170112607' occurs 1x; '01100170109835' occurs 1x.
- `schools.County`: 17,686 rows, 0 NULL, 58 distinct values. Witness values: 'Sonoma' occurs 331x; 'Fresno' occurs 620x; 'Stanislaus' occurs 319x.
- `schools.School`: 17,686 rows, 1,369 NULL, 13,875 distinct values. Witness values: 'Directly funded' occurs 0x; 'Cantua Elementary' occurs 3x; NULL occurs 1,369x.
- `schools.OpenDate`: 17,686 rows, 1,369 NULL, 1,406 distinct values. Witness values: '1980-07-01' occurs 10,679x; '1993-09-01' occurs 40x; '2003-09-02' occurs 43x.
- `schools.FundingType`: 17,686 rows, 16,044 NULL, 3 distinct values. Witness values: 'Directly funded' occurs 1,176x; NULL occurs 16,044x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-020 (thrombosis_prediction)

**Question:** Which patient is the first patient with an abnormal anti-SSA to come to the hospital? Please give his or her ID.

**Evidence:** first patient refers to ID with MIN(`First Date`); abnormal anti-SSA refers to SSA NOT IN('negative', '0');

**Gold SQL:**
```sql
SELECT T1.ID FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.`First Date` IS NOT NULL AND T2.SSA NOT IN ('negative', '0') ORDER BY T1.`First Date` ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT P.ID FROM Patient AS P INNER JOIN Laboratory AS L ON P.ID = L.ID WHERE L.SSA NOT IN ('negative', '0') ORDER BY P.`First Date` ASC LIMIT 1;
```

**Witness database:**

*Examination* (9 unreferenced columns omitted)

| ID | Examination Date | aCL IgG | aCL IgM |
|---|---|---|---|
| 0 | 1000-01-01 | 0 | 0 |

*Patient* (5 unreferenced columns omitted)

| ID | First Date |
|---|---|
| 0 | NULL |

*Laboratory* (42 unreferenced columns omitted)

| ID | SSA |
|---|---|
| 0 | 1237998919616375306 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x.
- `Patient.First Date`: 1,238 rows, 251 NULL, 797 distinct values. Witness values: NULL occurs 251x.
- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 0 occurs 0x.
- `Laboratory.SSA`: 13,908 rows, 13,809 NULL, 7 distinct values. Witness values: '1237998919616375306' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-089 (student_club)

**Question:** For all the budgets for "November Meeting", how many of them had exceeded the budget?

**Evidence:** 'November Meeting' is an event name; remaining < 0 means the cost had exceeded the budget

**Gold SQL:**
```sql
SELECT COUNT(T2.event_id) FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T2.event_name = 'November Meeting' AND T1.remaining < 0
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM budget WHERE link_to_event = (SELECT event_id FROM event WHERE event_name = 'November Meeting') AND remaining < 0
```

**Witness database:**

*budget* (5 unreferenced columns omitted)

| remaining | link_to_event |
|---|---|
| -24.25 | recAlAwtBZ0Fqbr5K |

*event* (5 unreferenced columns omitted)

| event_id | event_name |
|---|---|
| rec2mJrCofveboaz6 | November Meeting |
| recAlAwtBZ0Fqbr5K | November Meeting |
| recEVTik3MlqbvLFi | October Speaker |

**Gold result on the witness:** `[[1]]`  
**Predicted result on the witness:** `[[0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `budget.remaining`: 52 rows, 0 NULL, 22 distinct values. Witness values: -24.25 occurs 1x.
- `budget.link_to_event`: 52 rows, 0 NULL, 23 distinct values. Witness values: 'recAlAwtBZ0Fqbr5K' occurs 4x.
- `event.event_id`: 42 rows, 0 NULL, 42 distinct values, all non-NULL values unique. Witness values: 'rec2mJrCofveboaz6' occurs 1x; 'recAlAwtBZ0Fqbr5K' occurs 1x; 'recEVTik3MlqbvLFi' occurs 1x.
- `event.event_name`: 42 rows, 0 NULL, 39 distinct values. Witness values: 'November Meeting' occurs 1x; 'October Speaker' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-071 (superhero)

**Question:** Find the average weight of the heroes who are aliens.

**Evidence:** average = AVG(weight_kg); aliens refers to race = 'Alien';

**Gold SQL:**
```sql
SELECT CAST(SUM(T1.weight_kg) AS REAL) / COUNT(T1.id) FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T2.race = 'Alien'
```
**Predicted SQL:**
```sql
SELECT AVG(s.weight_kg) AS average_weight FROM superhero s JOIN race r ON s.race_id = r.id WHERE r.race = 'Alien'
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 8 | Good |

*colour*

| id | colour |
|---|---|
| 4 | f |
| 5 | h |
| 6 | k |

*gender*

| id | gender |
|---|---|
| 3 | Male |

*publisher*

| id | publisher_name |
|---|---|
| 7 | ABC Studios |

*race*

| id | race |
|---|---|
| 1 | Alien |
| 11 | Alien |
| 26 | Aliena |
| 31 | Alien |

*superhero* (9 unreferenced columns omitted)

| id | race_id | weight_kg |
|---|---|---|
| 2 | 1 | 10 |
| 12 | 11 | 10 |
| 17 | NULL | 18 |
| 27 | 26 | 29 |
| 32 | 31 | NULL |

**Gold result on the witness:** `[[6.666666666666667]]`  
**Predicted result on the witness:** `[[10.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `race.id`: 61 rows, 0 NULL, 61 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 11 occurs 1x; 26 occurs 1x; 31 occurs 1x.
- `race.race`: 61 rows, 0 NULL, 61 distinct values, all non-NULL values unique. Witness values: 'Alien' occurs 1x; 'Aliena' occurs 0x.
- `superhero.id`: 750 rows, 0 NULL, 750 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 12 occurs 1x; 17 occurs 1x; 27 occurs 1x; 32 occurs 1x.
- `superhero.race_id`: 750 rows, 4 NULL, 61 distinct values. Witness values: 1 occurs 295x; 11 occurs 1x; NULL occurs 4x; 26 occurs 1x; 31 occurs 1x.
- `superhero.weight_kg`: 750 rows, 64 NULL, 140 distinct values. Witness values: 10 occurs 0x; 18 occurs 2x; 29 occurs 0x; NULL occurs 64x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-116 (formula_1)

**Question:** From race no. 50 to 100, how many finishers have been disqualified?

**Evidence:** disqualified refers to statusID = 2, finisher refers to time! = null; race no. refers to raceId; raceId > 50 and raceId < 100;

**Gold SQL:**
```sql
SELECT SUM(IIF(time IS NOT NULL, 1, 0)) FROM results WHERE statusId = 2 AND raceID < 100 AND raceId > 50
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM results WHERE raceId BETWEEN 50 AND 100 AND statusId = 2 AND time IS NOT NULL
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 20 | nurburgring | Nürburgring | Nürburg |
| 9 | silverstone | Silverstone Circuit | Silverstone |
| 6 | monaco | Circuit de Monaco | Monte-Carlo |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 13 | mf1 | MF1 | Russian |
| 183 | brabham-climax | Brabham-Climax | British |
| 204 | brabham-alfa_romeo | Brabham-Alfa Romeo | British |
| 1 | mclaren | McLaren | British |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 33 | monteiro | NULL | TMO |
| 383 | anderson | NULL | NULL |
| 137 | piquet | NULL | NULL |
| 182 | lauda | NULL | NULL |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 57 | 2006 | 5 | 20 |
| 703 | 1965 | 5 | 9 |
| 518 | 1979 | 7 | 6 |
| 456 | 1983 | 5 | 6 |

*results* (15 unreferenced columns omitted)

| raceId | time | statusId |
|---|---|---|
| 57 | NULL | 11 |
| 703 | NULL | 6 |
| 518 | NULL | 7 |
| 456 | NULL | 81 |

*seasons*

| year | url |
|---|---|
| 2006 | http://en.wikipedia.org/wiki/2006_Formula_One_season |
| 1965 | http://en.wikipedia.org/wiki/1965_Formula_One_season |
| 1979 | http://en.wikipedia.org/wiki/1979_Formula_One_season |
| 1983 | http://en.wikipedia.org/wiki/1983_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 11 | +1 Lap |
| 6 | Gearbox |
| 7 | Transmission |
| 81 | Did not qualify |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 57 occurs 22x; 703 occurs 23x; 518 occurs 25x; 456 occurs 28x.
- `results.time`: 23,657 rows, 17,696 NULL, 5,755 distinct values. Witness values: NULL occurs 17,696x.
- `results.statusId`: 23,657 rows, 0 NULL, 132 distinct values. Witness values: 11 occurs 3,265x; 6 occurs 790x; 7 occurs 318x; 81 occurs 1,025x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-012 (student_club)

**Question:** Calculate the difference in the percentage of members in New Jersey and Vermont.

**Evidence:** SUBTRACT( DIVIDE( SUM(state = 'New Jersey'), COUNT(position = 'Member')), DIVIDE( SUM(state = 'Vermont'), COUNT(position = 'Member')) )

**Gold SQL:**
```sql
SELECT CAST((SUM(CASE WHEN T2.state = 'New Jersey' THEN 1 ELSE 0 END) - SUM(CASE WHEN T2.state = 'Vermont' THEN 1 ELSE 0 END)) AS REAL) * 100 / COUNT(T1.member_id) AS diff FROM member AS T1 INNER JOIN zip_code AS T2 ON T2.zip_code = T1.zip
```
**Predicted SQL:**
```sql
SELECT CAST(SUM(CASE WHEN T1.state = 'New Jersey' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T2.position) - CAST(SUM(CASE WHEN T1.state = 'Vermont' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T2.position) FROM zip_code AS T1 INNER JOIN member AS T2 ON T1.zip_code = T2.zip
```

**Witness database:**

*major*

| major_id | major_name | department | college |
|---|---|---|---|
| recxK3MHQFbR9J5uO | n | o | College of Agriculture and Applied Sciences |

*zip_code* (4 unreferenced columns omitted)

| zip_code | state |
|---|---|
| 1 | Vermont |
| -1 | Vermont |
| 2 | New Jersey |

*member* (6 unreferenced columns omitted)

| member_id | position | zip |
|---|---|---|
| f | Member | 1 |
| w | NULL | -1 |
| aa | Member | 2 |
| bc | NULL | NULL |

**Gold result on the witness:** `[[-33.333333333333336]]`  
**Predicted result on the witness:** `[[-50.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `zip_code.zip_code`: 41,877 rows, 0 NULL, 41,877 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; -1 occurs 0x; 2 occurs 0x.
- `zip_code.state`: 41,877 rows, 0 NULL, 52 distinct values. Witness values: 'Vermont' occurs 309x; 'New Jersey' occurs 732x.
- `member.member_id`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: 'f' occurs 0x; 'w' occurs 0x; 'aa' occurs 0x; 'bc' occurs 0x.
- `member.position`: 33 rows, 0 NULL, 6 distinct values. Witness values: 'Member' occurs 26x; NULL occurs 0x.
- `member.zip`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; -1 occurs 0x; 2 occurs 0x; NULL occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-080 (european_football_2)

**Question:** Among the players born before the year 1986, how many of them would remain in his position and defense while the team attacked?

**Evidence:** players born before the year 1986 refers to strftime('%Y', birthday)<'1986'; players who would remain in his position and defense while the team attacked refers to defensive_work_rate = 'high'; Should consider DISTINCT in the final result;

**Gold SQL:**
```sql
SELECT COUNT(DISTINCT t1.player_name) FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE STRFTIME('%Y',t1.birthday) < '1986' AND t2.defensive_work_rate = 'high'
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT pa.player_fifa_api_id) AS num_players FROM Player_Attributes pa JOIN Player p ON pa.player_fifa_api_id = p.player_fifa_api_id WHERE strftime('%Y', p.birthday) < '1986' AND pa.defensive_work_rate = 'high'
```

**Witness database:**

*Player* (3 unreferenced columns omitted)

| player_api_id | player_name | player_fifa_api_id | birthday |
|---|---|---|---|
| 2862 | Eduardo | 100 | 1980-08-05 00:00:00 |
| 2805 | Eduardo | 244 | 1980-08-05 00:00:00 |

*Player_Attributes* (39 unreferenced columns omitted)

| player_fifa_api_id | player_api_id | defensive_work_rate |
|---|---|---|
| 100 | 2862 | high |
| 244 | 2805 | high |

**Gold result on the witness:** `[[1]]`  
**Predicted result on the witness:** `[[2]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 2862 occurs 1x; 2805 occurs 1x.
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'Eduardo' occurs 3x.
- `Player.player_fifa_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 100 occurs 0x; 244 occurs 1x.
- `Player.birthday`: 11,060 rows, 0 NULL, 5,762 distinct values. Witness values: '1980-08-05 00:00:00' occurs 7x.
- `Player_Attributes.player_fifa_api_id`: 183,978 rows, 0 NULL, 11,062 distinct values. Witness values: 100 occurs 0x; 244 occurs 6x.
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 2862 occurs 34x; 2805 occurs 28x.
- `Player_Attributes.defensive_work_rate`: 183,978 rows, 836 NULL, 19 distinct values. Witness values: 'high' occurs 27,041x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-062 (debit_card_specializing)

**Question:** What is the average total price of the transactions taken place in January, 2012?

**Evidence:** In January, 2012 means Date contains '2012-01'

**Gold SQL:**
```sql
SELECT AVG(Amount) FROM transactions_1k WHERE Date LIKE '2012-01%'
```
**Predicted SQL:**
```sql
SELECT AVG(amount * price) AS averagetotalprice FROM transactions_1k WHERE STRFTIME('%Y-%m', "transactions_1k"."Date") = '2012-01'
```

**Witness database:**

*transactions_1k* (6 unreferenced columns omitted)

| Date | Amount | Price |
|---|---|---|
| 2012-01-01 | NULL | NULL |
| 2012-01-01 | 1014 | 1015.0 |

**Gold result on the witness:** `[[1014.0]]`  
**Predicted result on the witness:** `[[1029210.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `transactions_1k.Date`: 1,000 rows, 0 NULL, 4 distinct values. Witness values: '2012-01-01' occurs 0x.
- `transactions_1k.Amount`: 1,000 rows, 0 NULL, 83 distinct values. Witness values: NULL occurs 0x; 1014 occurs 0x.
- `transactions_1k.Price`: 1,000 rows, 0 NULL, 930 distinct values. Witness values: NULL occurs 0x; 1015.0 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-009 (european_football_2)

**Question:** Among the players born before the year 1986, how many of them would remain in his position and defense while the team attacked?

**Evidence:** players born before the year 1986 refers to strftime('%Y', birthday)<'1986'; players who would remain in his position and defense while the team attacked refers to defensive_work_rate = 'high'; Should consider DISTINCT in the final result;

**Gold SQL:**
```sql
SELECT COUNT(DISTINCT t1.player_name) FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE STRFTIME('%Y',t1.birthday) < '1986' AND t2.defensive_work_rate = 'high'
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT Player.player_api_id) FROM Player_Attributes JOIN Player ON Player_Attributes.player_api_id = Player.player_api_id WHERE strftime('%Y', Player.birthday) < '1986' AND Player_Attributes.defensive_work_rate = 'high';
```

**Witness database:**

*Player* (4 unreferenced columns omitted)

| player_api_id | player_name | birthday |
|---|---|---|
| 3204 | Kiko | 1980-08-05 00:00:00 |
| 2770 | Kiko | 1980-08-05 00:00:00 |

*Player_Attributes* (40 unreferenced columns omitted)

| player_api_id | defensive_work_rate |
|---|---|
| 3204 | high |
| 2770 | high |

**Gold result on the witness:** `[[1]]`  
**Predicted result on the witness:** `[[2]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 3204 occurs 1x; 2770 occurs 1x.
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'Kiko' occurs 3x.
- `Player.birthday`: 11,060 rows, 0 NULL, 5,762 distinct values. Witness values: '1980-08-05 00:00:00' occurs 7x.
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 3204 occurs 29x; 2770 occurs 15x.
- `Player_Attributes.defensive_work_rate`: 183,978 rows, 836 NULL, 19 distinct values. Witness values: 'high' occurs 27,041x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-016 (toxicology)

**Question:** Find the percentage of atoms with single bond.

**Evidence:** single bond refers to bond_type = '-'; percentage = DIVIDE(SUM(bond_type = '-'), COUNT(bond_id)) as percentage

**Gold SQL:**
```sql
SELECT CAST(COUNT(CASE WHEN T.bond_type = '-' THEN T.bond_id ELSE NULL END) AS REAL) * 100 / COUNT(T.bond_id) FROM bond t
```
**Predicted SQL:**
```sql
SELECT CAST(SUM(CASE WHEN b.bond_type = '-' THEN 1 ELSE 0 END) AS REAL) * 100.0 / COUNT(*) AS percentage FROM bond AS b INNER JOIN connected AS c ON b.bond_id = c.bond_id INNER JOIN atom AS a ON c.atom_id = a.atom_id
```

**Witness database:**

*atom* (2 unreferenced columns omitted)

| atom_id |
|---|
| TR000_1 |
| TR000_3 |
| TR000_2 |
| TR496_56 |
| TR496_7 |

*bond* (1 unreferenced columns omitted)

| bond_id | bond_type |
|---|---|
| TR000_2_5 | - |
| TR000_2_3 | = |
| TR000_2_4 | - |
| TR496_7_56 | - |

*connected* (1 unreferenced columns omitted)

| atom_id | bond_id |
|---|---|
| TR000_1 | TR000_2_5 |
| TR000_2 | TR000_2_4 |
| TR000_3 | TR000_2_3 |
| TR496_7 | TR496_7_56 |
| TR000_2 | TR000_2_3 |
| TR496_56 | TR496_7_56 |

*molecule*

| molecule_id | label |
|---|---|
| TR060 | - |
| TR496 | + |
| TR000 | + |
| TR338 | + |

**Gold result on the witness:** `[[75.0]]`  
**Predicted result on the witness:** `[[66.66666666666667]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.atom_id`: 12,333 rows, 0 NULL, 12,333 distinct values, all non-NULL values unique. Witness values: 'TR000_1' occurs 1x; 'TR000_3' occurs 1x; 'TR000_2' occurs 1x; 'TR496_56' occurs 1x; 'TR496_7' occurs 1x.
- `bond.bond_id`: 12,379 rows, 0 NULL, 12,379 distinct values, all non-NULL values unique. Witness values: 'TR000_2_5' occurs 1x; 'TR000_2_3' occurs 1x; 'TR000_2_4' occurs 1x; 'TR496_7_56' occurs 1x.
- `bond.bond_type`: 12,379 rows, 1 NULL, 3 distinct values. Witness values: '-' occurs 10,528x; '=' occurs 1,844x.
- `connected.atom_id`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'TR000_1' occurs 1x; 'TR000_2' occurs 4x; 'TR000_3' occurs 1x; 'TR496_7' occurs 4x; 'TR496_56' occurs 1x.
- `connected.bond_id`: 24,758 rows, 0 NULL, 12,379 distinct values. Witness values: 'TR000_2_5' occurs 2x; 'TR000_2_4' occurs 2x; 'TR000_2_3' occurs 2x; 'TR496_7_56' occurs 2x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-037 (toxicology)

**Question:** What is the molecule of atom id "TR000_2" and atom id 2 "TR000_4"?

**Evidence:** -

**Gold SQL:**
```sql
SELECT T1.molecule_id FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE T2.atom_id = 'TR000_2' AND T2.atom_id2 = 'TR000_4'
```
**Predicted SQL:**
```sql
SELECT molecule_id FROM atom WHERE atom_id IN ('TR000_2', 'TR000_4')
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| atom_id | molecule_id |
|---|---|
| TR000_4 | 2147483648 |

*bond* (1 unreferenced columns omitted)

| bond_id | molecule_id |
|---|---|
| 2147483648 | 2147483648 |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| TR000_4 | TR000_4 | 2147483648 |

*molecule*

| molecule_id | label |
|---|---|
| 2147483648 | 2147483648 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2147483648']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.atom_id`: 12,333 rows, 0 NULL, 12,333 distinct values, all non-NULL values unique. Witness values: 'TR000_4' occurs 1x.
- `atom.molecule_id`: 12,333 rows, 0 NULL, 444 distinct values. Witness values: '2147483648' occurs 0x.
- `bond.bond_id`: 12,379 rows, 0 NULL, 12,379 distinct values, all non-NULL values unique. Witness values: '2147483648' occurs 0x.
- `bond.molecule_id`: 12,379 rows, 0 NULL, 444 distinct values. Witness values: '2147483648' occurs 0x.
- `connected.atom_id`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'TR000_4' occurs 1x.
- `connected.atom_id2`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'TR000_4' occurs 1x.
- `connected.bond_id`: 24,758 rows, 0 NULL, 12,379 distinct values. Witness values: '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-123 (codebase_community)

**Question:** What is the display name of the user who acquired the highest amount of badges?

**Evidence:** highest amount of badges refers to MAX(COUNT(Name));

**Gold SQL:**
```sql
SELECT T1.DisplayName FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId GROUP BY T1.DisplayName ORDER BY COUNT(T1.Id) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT u.DisplayName FROM users u JOIN badges b ON u.Id = b.UserId GROUP BY u.Id ORDER BY COUNT(b.Name) DESC LIMIT 1;
```

**Witness database:**

*badges* (2 unreferenced columns omitted)

| UserId | Name |
|---|---|
| 21730 | Teacher |
| 46283 | Autobiographer |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 21730 | user1915348 |
| 46283 | Paul Jackson |

**Gold result on the witness:** `[['user1915348']]`  
**Predicted result on the witness:** `[['Paul Jackson']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `badges.UserId`: 79,851 rows, 0 NULL, 25,078 distinct values. Witness values: 21730 occurs 1x; 46283 occurs 1x.
- `badges.Name`: 79,851 rows, 0 NULL, 153 distinct values. Witness values: 'Teacher' occurs 4,679x; 'Autobiographer' occurs 4,480x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 21730 occurs 1x; 46283 occurs 1x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: 'user1915348' occurs 1x; 'Paul Jackson' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-079 (superhero)

**Question:** Identify the heaviest superhero in DC Comics.

**Evidence:** heaviest refers to MAX(weight_kg); DC Comics refers to publisher_name = 'DC Comics'; superhero refers to superhero_name;

**Gold SQL:**
```sql
SELECT T1.superhero_name FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id WHERE T2.publisher_name = 'DC Comics' ORDER BY T1.weight_kg DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T2.superhero_name FROM publisher AS T1 INNER JOIN superhero AS T2 ON T1.id = T2.publisher_id WHERE T1.publisher_name = 'DC Comics' AND T2.weight_kg IS NOT NULL ORDER BY T2.weight_kg DESC LIMIT 1
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
| 4 | DC Comics |

*race*

| id | race |
|---|---|
| 1 | - |

*superhero* (9 unreferenced columns omitted)

| superhero_name | publisher_id | weight_kg |
|---|---|---|
| Shrinking Violet | 4 | NULL |

**Gold result on the witness:** `[['Shrinking Violet']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `publisher.id`: 25 rows, 0 NULL, 25 distinct values, all non-NULL values unique. Witness values: 4 occurs 1x.
- `publisher.publisher_name`: 25 rows, 0 NULL, 25 distinct values, all non-NULL values unique. Witness values: 'DC Comics' occurs 1x.
- `superhero.superhero_name`: 750 rows, 0 NULL, 743 distinct values. Witness values: 'Shrinking Violet' occurs 1x.
- `superhero.publisher_id`: 750 rows, 3 NULL, 25 distinct values. Witness values: 4 occurs 224x.
- `superhero.weight_kg`: 750 rows, 64 NULL, 140 distinct values. Witness values: NULL occurs 64x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-137 (california_schools)

**Question:** How many schools with an average score in Math greater than 400 in the SAT test are exclusively virtual?

**Evidence:** Exclusively virtual refers to Virtual = 'F'

**Gold SQL:**
```sql
SELECT COUNT(DISTINCT T2.School) FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.Virtual = 'F' AND T1.AvgScrMath > 400
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode WHERE T2.Virtual = 'F' AND T1.AvgScrMath > 400
```

**Witness database:**

*frpm* (25 unreferenced columns omitted)

| CDSCode | Academic Year | County Code | District Code |
|---|---|---|---|
| 2147483648 | 2147483648 | 2147483648 | 0 |

*satscores* (9 unreferenced columns omitted)

| cds | AvgScrMath |
|---|---|
| 2147483648 | 401 |

*schools* (46 unreferenced columns omitted)

| CDSCode | School | Virtual |
|---|---|---|
| 2147483648 | NULL | F |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `satscores.cds`: 2,269 rows, 0 NULL, 2,269 distinct values, all non-NULL values unique. Witness values: '2147483648' occurs 0x.
- `satscores.AvgScrMath`: 2,269 rows, 596 NULL, 295 distinct values. Witness values: 401 occurs 1x.
- `schools.CDSCode`: 17,686 rows, 0 NULL, 17,686 distinct values, all non-NULL values unique. Witness values: '2147483648' occurs 0x.
- `schools.School`: 17,686 rows, 1,369 NULL, 13,875 distinct values. Witness values: NULL occurs 1,369x.
- `schools.Virtual`: 17,686 rows, 6,868 NULL, 3 distinct values. Witness values: 'F' occurs 69x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-014 (toxicology)

**Question:** Which element is the least numerous in non-carcinogenic molecules?

**Evidence:** label = '-' means molecules are non-carcinogenic; least numerous refers to MIN(COUNT(element));

**Gold SQL:**
```sql
SELECT T.element FROM (SELECT T1.element, COUNT(DISTINCT T1.molecule_id) FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '-' GROUP BY T1.element ORDER BY COUNT(DISTINCT T1.molecule_id) ASC LIMIT 1) t
```
**Predicted SQL:**
```sql
SELECT a.element FROM molecule m INNER JOIN atom a ON m.molecule_id = a.molecule_id WHERE m.label = '-' GROUP BY a.element ORDER BY COUNT(a.element) ASC LIMIT 1;
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| molecule_id | element |
|---|---|
| TR060 | c |
| TR060 | h |
| TR060 | c |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
| TR060_5_49 | TR060 | - |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| TR060_5 | TR060_49 | TR060_5_49 |
| TR060_49 | TR060_5 | TR060_5_49 |

*molecule*

| molecule_id | label |
|---|---|
| TR060 | - |

**Gold result on the witness:** `[['c']]`  
**Predicted result on the witness:** `[['h']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.molecule_id`: 12,333 rows, 0 NULL, 444 distinct values. Witness values: 'TR060' occurs 103x.
- `atom.element`: 12,333 rows, 0 NULL, 21 distinct values. Witness values: 'c' occurs 4,605x; 'h' occurs 5,518x.
- `molecule.molecule_id`: 343 rows, 0 NULL, 343 distinct values, all non-NULL values unique. Witness values: 'TR060' occurs 1x.
- `molecule.label`: 343 rows, 0 NULL, 2 distinct values. Witness values: '-' occurs 191x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-073 (european_football_2)

**Question:** Please name one player whose overall strength is the greatest.

**Evidence:** overall strength is the greatest refers to MAX(overall_rating)

**Gold SQL:**
```sql
SELECT DISTINCT t1.player_name FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t2.overall_rating = ( SELECT MAX(overall_rating) FROM Player_Attributes)
```
**Predicted SQL:**
```sql
SELECT T1.player_name FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T2.overall_rating DESC LIMIT 1
```

**Witness database:**

*Player* (5 unreferenced columns omitted)

| player_api_id | player_name |
|---|---|
| 129915 | Johann Berg Gudmundsson |
| 39638 | Erjon Bogdani |

*Player_Attributes* (40 unreferenced columns omitted)

| player_api_id | overall_rating |
|---|---|
| 129915 | 71 |
| 129915 | 69 |
| 39638 | 71 |

**Gold result on the witness:** `[['Johann Berg Gudmundsson'], ['Erjon Bogdani']]`  
**Predicted result on the witness:** `[['Johann Berg Gudmundsson']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 129915 occurs 1x; 39638 occurs 1x.
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'Johann Berg Gudmundsson' occurs 1x; 'Erjon Bogdani' occurs 1x.
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 129915 occurs 27x; 39638 occurs 12x.
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: 71 occurs 9,354x; 69 occurs 10,281x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-120 (california_schools)

**Question:** Give the names of the schools with the percent eligible for free meals in K-12 is more than 0.1 and test takers whose test score is greater than or equal to 1500?

**Evidence:** Percent eligible for free meals = Free Meal Count (K-12) / Total (Enrollment (K-12)

**Gold SQL:**
```sql
SELECT T2.`School Name` FROM satscores AS T1 INNER JOIN frpm AS T2 ON T1.cds = T2.CDSCode WHERE CAST(T2.`Free Meal Count (K-12)` AS REAL) / T2.`Enrollment (K-12)` > 0.1 AND T1.NumGE1500 > 0
```
**Predicted SQL:**
```sql
SELECT frpm.`School Name` FROM frpm INNER JOIN satscores ON frpm.CDSCode = satscores.cds WHERE frpm.`Percent (%) Eligible Free (K-12)` > 0.1 AND satscores.NumGE1500 > 0;
```

**Witness database:**

*frpm* (24 unreferenced columns omitted)

| CDSCode | School Name | Enrollment (K-12) | Free Meal Count (K-12) | Percent (%) Eligible Free (K-12) |
|---|---|---|---|---|
| 01611436090187 | Garfield Elementary | 427.0 | 16.0 | 0.25 |

*satscores* (9 unreferenced columns omitted)

| cds | NumGE1500 |
|---|---|
| 01611436090187 | 1 |

*schools* (45 unreferenced columns omitted)

| CDSCode | NCESDist | NCESSchool | StatusType |
|---|---|---|---|
| 01611436090187 | 0620880 | 09559 | Active |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['Garfield Elementary']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `frpm.CDSCode`: 9,986 rows, 0 NULL, 9,986 distinct values, all non-NULL values unique. Witness values: '01611436090187' occurs 1x.
- `frpm.School Name`: 9,986 rows, 0 NULL, 8,652 distinct values. Witness values: 'Garfield Elementary' occurs 11x.
- `frpm.Enrollment (K-12)`: 9,986 rows, 0 NULL, 1,882 distinct values. Witness values: 427.0 occurs 20x.
- `frpm.Free Meal Count (K-12)`: 9,986 rows, 56 NULL, 1,216 distinct values. Witness values: 16.0 occurs 39x.
- `frpm.Percent (%) Eligible Free (K-12)`: 9,986 rows, 56 NULL, 8,658 distinct values. Witness values: 0.25 occurs 15x.
- `satscores.cds`: 2,269 rows, 0 NULL, 2,269 distinct values, all non-NULL values unique. Witness values: '01611436090187' occurs 0x.
- `satscores.NumGE1500`: 2,269 rows, 596 NULL, 368 distinct values. Witness values: 1 occurs 19x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-070 (superhero)

**Question:** List the heroes' names whose eyes and hair colours are both black.

**Evidence:** heroes' names refers to superhero_name; eyes and hair colours are both black refers to eye_colour_id AND hair_colour_id WHERE colour.colour = 'Black';

**Gold SQL:**
```sql
SELECT T1.superhero_name FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id AND T1.hair_colour_id = T2.id WHERE T2.colour = 'Black'
```
**Predicted SQL:**
```sql
SELECT s.superhero_name FROM superhero s JOIN colour c_eye ON s.eye_colour_id = c_eye.id JOIN colour c_hair ON s.hair_colour_id = c_hair.id WHERE c_eye.colour = 'Black' AND c_hair.colour = 'Black'
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 8 | Good |

*colour*

| id | colour |
|---|---|
| 1 | Black |
| 2 | Black |
| 5 | j |
| 10 | Black |
| 18 | Black |
| 34 | NULL |

*gender*

| id | gender |
|---|---|
| 4 | Male |

*publisher*

| id | publisher_name |
|---|---|
| 7 | ABC Studios |

*race*

| id | race |
|---|---|
| 6 | i |

*superhero* (9 unreferenced columns omitted)

| superhero_name | eye_colour_id | hair_colour_id |
|---|---|---|
| a | 1 | 2 |
| k | 1 | 10 |
| k | 1 | 2 |
| k | NULL | 18 |
| NULL | 1 | 2 |
| k | 1 | NULL |
| k | 34 | 18 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['a'], ['k'], ['k'], [None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `colour.id`: 35 rows, 0 NULL, 35 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 2 occurs 1x; 5 occurs 1x; 10 occurs 1x; 18 occurs 1x; 34 occurs 1x.
- `colour.colour`: 35 rows, 0 NULL, 35 distinct values, all non-NULL values unique. Witness values: 'Black' occurs 1x; 'j' occurs 0x; NULL occurs 0x.
- `superhero.superhero_name`: 750 rows, 0 NULL, 743 distinct values. Witness values: 'a' occurs 0x; 'k' occurs 0x; NULL occurs 0x.
- `superhero.eye_colour_id`: 750 rows, 0 NULL, 21 distinct values. Witness values: 1 occurs 169x; NULL occurs 0x; 34 occurs 1x.
- `superhero.hair_colour_id`: 750 rows, 0 NULL, 26 distinct values. Witness values: 2 occurs 0x; 10 occurs 1x; 18 occurs 1x; NULL occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-042 (superhero)

**Question:** What is the eye clolour of the heaviest superhero?

**Evidence:** the heaviest superhero refers to MAX(weight_kg); eye colour refers to colour where eye_colour_id = colour.id;

**Gold SQL:**
```sql
SELECT T2.colour FROM superhero AS T1 INNER JOIN colour AS T2 ON T1.eye_colour_id = T2.id ORDER BY T1.weight_kg DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT colour.colour FROM superhero INNER JOIN colour ON superhero.eye_colour_id = colour.id WHERE superhero.weight_kg = (SELECT MAX(weight_kg) FROM superhero);
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 1001 | b |

*colour*

| id | colour |
|---|---|
| 1002 | NULL |

*gender*

| id | gender |
|---|---|
| 1003 | N/A |

*publisher*

| id | publisher_name |
|---|---|
| 1004 | NULL |

*race*

| id | race |
|---|---|
| 1005 | NULL |

*superhero* (10 unreferenced columns omitted)

| eye_colour_id | weight_kg |
|---|---|
| 1002 | NULL |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `colour.id`: 35 rows, 0 NULL, 35 distinct values, all non-NULL values unique. Witness values: 1002 occurs 0x.
- `colour.colour`: 35 rows, 0 NULL, 35 distinct values, all non-NULL values unique. Witness values: NULL occurs 0x.
- `superhero.eye_colour_id`: 750 rows, 0 NULL, 21 distinct values. Witness values: 1002 occurs 0x.
- `superhero.weight_kg`: 750 rows, 64 NULL, 140 distinct values. Witness values: NULL occurs 64x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-021 (debit_card_specializing)

**Question:** How much more was customer 7 consuming in April 2013 than customer 5?

**Evidence:** April 2013 refers to 201304 in the yearmonth.date

**Gold SQL:**
```sql
SELECT SUM(IIF(CustomerID = 7, Consumption, 0)) - SUM(IIF(CustomerID = 5, Consumption, 0)) FROM yearmonth WHERE Date = '201304'
```
**Predicted SQL:**
```sql
SELECT (SELECT `consumption` FROM `yearmonth` WHERE `customerid` = 7 AND `date` = '201304') - (SELECT `consumption` FROM `yearmonth` WHERE `customerid` = 5 AND `date` = '201304') AS consumption_difference
```

**Witness database:**

*customers*

| CustomerID | Segment | Currency |
|---|---|---|
| 7 | KAM | CZK |

*yearmonth*

| CustomerID | Date | Consumption |
|---|---|---|
| 7 | 201304 | 1.58 |

**Gold result on the witness:** `[[1.58]]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `yearmonth.CustomerID`: 383,282 rows, 0 NULL, 30,566 distinct values. Witness values: 7 occurs 17x.
- `yearmonth.Date`: 383,282 rows, 0 NULL, 21 distinct values. Witness values: '201304' occurs 25,487x.
- `yearmonth.Consumption`: 383,282 rows, 0 NULL, 279,091 distinct values. Witness values: 1.58 occurs 149x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-128 (codebase_community)

**Question:** What is the display name of the user who has the most number of views?

**Evidence:** user who has the most number of view refers to Max(Views)

**Gold SQL:**
```sql
SELECT DisplayName FROM users WHERE Views = ( SELECT MAX(Views) FROM users )
```
**Predicted SQL:**
```sql
SELECT DisplayName FROM users ORDER BY Views DESC LIMIT 1;
```

**Witness database:**

*users* (12 unreferenced columns omitted)

| DisplayName | Views |
|---|---|
| Community | 0 |
| user53158 | 0 |

**Gold result on the witness:** `[['Community'], ['user53158']]`  
**Predicted result on the witness:** `[['Community']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: 'Community' occurs 1x; 'user53158' occurs 1x.
- `users.Views`: 40,325 rows, 0 NULL, 362 distinct values. Witness values: 0 occurs 20,198x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-036 (superhero)

**Question:** Which publisher published the slowest superhero?

**Evidence:** the slowest superhero refers to attribute_name = 'Speed' where MIN(attribute_value); publisher refers to publisher_name

**Gold SQL:**
```sql
SELECT T2.publisher_name FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id INNER JOIN hero_attribute AS T3 ON T1.id = T3.hero_id INNER JOIN attribute AS T4 ON T3.attribute_id = T4.id WHERE T4.attribute_name = 'Speed' ORDER BY T3.attribute_value LIMIT 1
```
**Predicted SQL:**
```sql
SELECT p.publisher_name FROM publisher p INNER JOIN superhero s ON p.id = s.publisher_id INNER JOIN hero_attribute ha ON s.id = ha.hero_id INNER JOIN attribute a ON ha.attribute_id = a.id WHERE a.attribute_name = 'Speed' AND ha.attribute_value = ( SELECT MIN(ha2.attribute_value) FROM hero_attribute ha2 INNER JOIN attribute a2 ON ha2.attribute_id = a2.id WHERE a2.attribute_name = 'Speed' );
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 1 | Good |
| 2 | Bad |

*attribute*

| id | attribute_name |
|---|---|
| 3 | Speed |

*colour*

| id | colour |
|---|---|
| 1 | No Colour |
| 9 | Brown |
| 31 | White |
| 4 | Black |
| 23 | Red |

*gender*

| id | gender |
|---|---|
| 1 | Male |

*hero_attribute*

| hero_id | attribute_id | attribute_value |
|---|---|---|
| 107 | 3 | 10 |
| 116 | 3 | 10 |
| 148 | 3 | 10 |
| 194 | 3 | 10 |

*publisher*

| id | publisher_name |
|---|---|
| 13 | Marvel Comics |
| 4 | DC Comics |

*race*

| id | race |
|---|---|
| 24 | Human |
| 2 | Alien |

*superhero* (10 unreferenced columns omitted)

| id | publisher_id |
|---|---|
| 107 | 13 |
| 116 | 13 |
| 148 | 4 |
| 194 | 13 |

**Gold result on the witness:** `[['Marvel Comics']]`  
**Predicted result on the witness:** `[['Marvel Comics'], ['Marvel Comics'], ['DC Comics'], ['Marvel Comics']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `attribute.id`: 6 rows, 0 NULL, 6 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x.
- `attribute.attribute_name`: 6 rows, 0 NULL, 6 distinct values, all non-NULL values unique. Witness values: 'Speed' occurs 1x.
- Real content of `attribute` (6 rows; referenced columns): (1, 'Intelligence'); (2, 'Strength'); (3, 'Speed'); (4, 'Durability'); (5, 'Power'); (6, 'Combat').
- `hero_attribute.hero_id`: 3,738 rows, 0 NULL, 623 distinct values. Witness values: 107 occurs 6x; 116 occurs 6x; 148 occurs 6x; 194 occurs 6x.
- `hero_attribute.attribute_id`: 3,738 rows, 0 NULL, 6 distinct values. Witness values: 3 occurs 623x.
- `hero_attribute.attribute_value`: 3,738 rows, 0 NULL, 20 distinct values. Witness values: 10 occurs 222x.
- `publisher.id`: 25 rows, 0 NULL, 25 distinct values, all non-NULL values unique. Witness values: 13 occurs 1x; 4 occurs 1x.
- `publisher.publisher_name`: 25 rows, 0 NULL, 25 distinct values, all non-NULL values unique. Witness values: 'Marvel Comics' occurs 1x; 'DC Comics' occurs 1x.
- `superhero.id`: 750 rows, 0 NULL, 750 distinct values, all non-NULL values unique. Witness values: 107 occurs 1x; 116 occurs 1x; 148 occurs 1x; 194 occurs 1x.
- `superhero.publisher_id`: 750 rows, 3 NULL, 25 distinct values. Witness values: 13 occurs 387x; 4 occurs 224x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-126 (card_games)

**Question:** What is the status of card "Cloudchaser Eagle"?

**Evidence:** Cloudchaser Eagle is the name of card;

**Gold SQL:**
```sql
SELECT DISTINCT T2.status FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Cloudchaser Eagle'
```
**Predicted SQL:**
```sql
SELECT status FROM legalities WHERE uuid = (SELECT uuid FROM cards WHERE name = 'Cloudchaser Eagle');
```

**Witness database:**

*cards* (72 unreferenced columns omitted)

| name | uuid |
|---|---|
| Cloudchaser Eagle | b |
| Cloudchaser Eagle | y2 |

*legalities* (2 unreferenced columns omitted)

| status | uuid |
|---|---|
| Legal | b |
| Banned | y2 |

**Gold result on the witness:** `[['Legal'], ['Banned']]`  
**Predicted result on the witness:** `[['Legal']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `cards.name`: 56,822 rows, 0 NULL, 21,738 distinct values. Witness values: 'Cloudchaser Eagle' occurs 3x.
- `cards.uuid`: 56,822 rows, 0 NULL, 56,822 distinct values, all non-NULL values unique. Witness values: 'b' occurs 0x; 'y2' occurs 0x.
- `legalities.status`: 427,907 rows, 0 NULL, 3 distinct values. Witness values: 'Legal' occurs 424,958x; 'Banned' occurs 2,313x.
- `legalities.uuid`: 427,907 rows, 0 NULL, 55,608 distinct values. Witness values: 'b' occurs 0x; 'y2' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-044 (codebase_community)

**Question:** What is the display name of the user who has obtained the most number of badges?

**Evidence:** who obtained the most number of badges refers to UserID with Max(Count(Id))

**Gold SQL:**
```sql
SELECT T2.DisplayName FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id GROUP BY T2.DisplayName ORDER BY COUNT(T1.Id) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT u.DisplayName FROM badges b JOIN users u ON b.UserId = u.Id GROUP BY b.UserId ORDER BY COUNT(b.Id) DESC LIMIT 1
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

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `badges.Id`: 79,851 rows, 0 NULL, 79,851 distinct values, all non-NULL values unique. Witness values: 13353 occurs 1x; 81335 occurs 1x; 73258 occurs 1x; 6230 occurs 1x.
- `badges.UserId`: 79,851 rows, 0 NULL, 25,078 distinct values. Witness values: 4673 occurs 17x; 48030 occurs 3x; 44011 occurs 3x; 3443 occurs 10x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 45466 occurs 1x; 13979 occurs 1x; 37654 occurs 1x; 4673 occurs 1x; 48030 occurs 1x; 44011 occurs 1x (+1 more).
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: 'freddyfree' occurs 1x; 'Julian' occurs 11x; 'Just A Name' occurs 1x; 'user4673' occurs 1x; 'NassibBueno' occurs 1x; 'user2448064' occurs 1x (+1 more).

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-030 (european_football_2)

**Question:** When is the birthday of the football player who has the highest overall rating?

**Evidence:** football player who has the highest overall rating refers to MAX(overall_rating);

**Gold SQL:**
```sql
SELECT t1.birthday FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id ORDER BY t2.overall_rating DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT Player.birthday FROM Player INNER JOIN Player_Attributes ON Player.player_fifa_api_id = Player_Attributes.player_fifa_api_id ORDER BY Player_Attributes.overall_rating DESC LIMIT 1
```

**Witness database:**

*Player* (4 unreferenced columns omitted)

| player_api_id | player_fifa_api_id | birthday |
|---|---|---|
| 2752 | 1 | 1989-11-14 00:00:00 |
| 37622 | 170456 | 1981-12-21 00:00:00 |
| 423223 | 220048 | 1996-05-31 00:00:00 |
| 30615 | 244 | 1975-02-18 00:00:00 |
| 164385 | 191032 | 1992-01-20 00:00:00 |
| 2796 | 198735 | 1987-06-08 00:00:00 |
| 2977 | 134594 | 1978-12-02 00:00:00 |
| 2790 | 110809 | 1974-02-15 00:00:00 |

*Player_Attributes* (39 unreferenced columns omitted)

| player_fifa_api_id | player_api_id | overall_rating |
|---|---|---|
| 170456 | 37622 | 74 |
| 198735 | 2796 | 67 |
| 134594 | 2977 | 63 |
| 110809 | 2790 | 67 |
| 1 | 2752 | 72 |
| 220048 | 423223 | 69 |
| 244 | 30615 | 76 |
| 191032 | 164385 | 80 |
| 1 | 2752 | 80 |

**Gold result on the witness:** `[['1989-11-14 00:00:00']]`  
**Predicted result on the witness:** `[['1992-01-20 00:00:00']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 2752 occurs 1x; 37622 occurs 1x; 423223 occurs 1x; 30615 occurs 1x; 164385 occurs 1x; 2796 occurs 1x (+2 more).
- `Player.player_fifa_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 170456 occurs 1x; 220048 occurs 1x; 244 occurs 1x; 191032 occurs 1x; 198735 occurs 1x (+2 more).
- `Player.birthday`: 11,060 rows, 0 NULL, 5,762 distinct values. Witness values: '1989-11-14 00:00:00' occurs 7x; '1981-12-21 00:00:00' occurs 3x; '1996-05-31 00:00:00' occurs 2x; '1975-02-18 00:00:00' occurs 1x; '1992-01-20 00:00:00' occurs 2x; '1987-06-08 00:00:00' occurs 4x (+2 more).
- `Player_Attributes.player_fifa_api_id`: 183,978 rows, 0 NULL, 11,062 distinct values. Witness values: 170456 occurs 19x; 198735 occurs 15x; 134594 occurs 8x; 110809 occurs 5x; 1 occurs 0x; 220048 occurs 20x (+2 more).
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 37622 occurs 19x; 2796 occurs 15x; 2977 occurs 8x; 2790 occurs 5x; 2752 occurs 21x; 423223 occurs 20x (+2 more).
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: 74 occurs 8,556x; 67 occurs 10,198x; 63 occurs 7,704x; 72 occurs 9,740x; 69 occurs 10,281x; 76 occurs 6,150x (+1 more).

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-090 (codebase_community)

**Question:** What is the display name of the user who acquired the highest amount of badges?

**Evidence:** highest amount of badges refers to MAX(COUNT(Name));

**Gold SQL:**
```sql
SELECT T1.DisplayName FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId GROUP BY T1.DisplayName ORDER BY COUNT(T1.Id) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT u.DisplayName FROM users u JOIN badges b ON u.Id = b.UserId GROUP BY u.Id ORDER BY COUNT(b.Name) DESC LIMIT 1;
```

**Witness database:**

*badges* (2 unreferenced columns omitted)

| UserId | Name |
|---|---|
| 0 | NULL |
| 1 | 2147483648 |

*comments* (3 unreferenced columns omitted)

| Id | PostId | Score | Text |
|---|---|---|---|
| -1 | 1 | 0 | 2147483648 |
| 0 | 0 | 0 | 2147483648 |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 1 | 0 | 1 | 2147483648 |
| 0 | 0 | 0 | 2147483648 |

*postLinks* (1 unreferenced columns omitted)

| Id | CreationDate | PostId | RelatedPostId |
|---|---|---|---|
| 0 | 1000-01-01 | 0 | 0 |
| 1 | 1000-01-01 | 0 | 0 |

*posts* (17 unreferenced columns omitted)

| Id | PostTypeId | AcceptedAnswerId | CreaionDate |
|---|---|---|---|
| 1 | 0 | 0 | 1000-01-01 |
| 0 | 0 | 0 | 1000-01-01 |

*tags* (1 unreferenced columns omitted)

| Id | TagName | Count | ExcerptPostId |
|---|---|---|---|
| -1 | 2147483648 | 0 | 1 |
| 0 | 2147483648 | 0 | 0 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 1 | 2147483648 |
| 0 | 2147483649 |

*votes* (2 unreferenced columns omitted)

| Id | PostId | VoteTypeId | CreationDate |
|---|---|---|---|
| 0 | 1 | 0 | 1000-01-01 |
| 1 | 1 | 0 | 1000-01-01 |

**Gold result on the witness:** `[['2147483649']]`  
**Predicted result on the witness:** `[['2147483648']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `badges.UserId`: 79,851 rows, 0 NULL, 25,078 distinct values. Witness values: 0 occurs 0x; 1 occurs 0x.
- `badges.Name`: 79,851 rows, 0 NULL, 153 distinct values. Witness values: NULL occurs 0x; '2147483648' occurs 0x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 0 occurs 0x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: '2147483648' occurs 0x; '2147483649' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-053 (formula_1)

**Question:** Paul di Resta was in the No. 853 race, what percent faster did he finish in the 853rd race than the next race for the fastest lap speed?

**Evidence:** Paul di Resta refers to the full name of the driver; Full name of the driver refers to drivers.forename ='Paul' and drivers.surname = 'di Resta'; race number refers to raceId; percentage = DIVIDE(SUBTRACT(fastestLapSpeed(raceId = 853), (fastestLapSpeed (raceId = 854)) * 100 , (fastestLapSpeed(raceId = 853))

**Gold SQL:**
```sql
SELECT (SUM(IIF(T2.raceId = 853, T2.fastestLapSpeed, 0)) - SUM(IIF(T2.raceId = 854, T2.fastestLapSpeed, 0))) * 100 / SUM(IIF(T2.raceId = 853, T2.fastestLapSpeed, 0)) FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId WHERE T1.forename = 'Paul' AND T1.surname = 'di Resta'
```
**Predicted SQL:**
```sql
SELECT (T1.fastestLapSpeed - T2.fastestLapSpeed) * 100.0 / T1.fastestLapSpeed AS percentage_difference FROM results AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId WHERE T1.raceId = 853 AND T2.raceId = 854 AND T1.driverId = ( SELECT driverId FROM drivers WHERE forename = 'Paul' AND surname = 'di Resta' );
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

*drivers* (6 unreferenced columns omitted)

| driverId | forename | surname |
|---|---|---|
| 0 | PAUL | DI RESTA |

*seasons*

| year | url |
|---|---|
| 0 | 2147483648 |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 853 | 0 | 0 | 0 |

*constructorResults* (1 unreferenced columns omitted)

| constructorResultsId | raceId | constructorId | points |
|---|---|---|---|
| 0 | 853 | 0 | 0 |

*constructorStandings* (3 unreferenced columns omitted)

| constructorStandingsId | raceId | constructorId | points |
|---|---|---|---|
| 0 | 853 | 0 | 0 |

*driverStandings* (3 unreferenced columns omitted)

| driverStandingsId | raceId | driverId | points |
|---|---|---|---|
| 0 | 853 | 0 | 0 |

*lapTimes* (2 unreferenced columns omitted)

| raceId | driverId | lap | position |
|---|---|---|---|
| 853 | 0 | 0 | 0 |

*pitStops* (3 unreferenced columns omitted)

| raceId | driverId | stop | lap |
|---|---|---|---|
| 853 | 0 | 0 | 0 |

*qualifying* (5 unreferenced columns omitted)

| qualifyId | raceId | driverId | constructorId |
|---|---|---|---|
| 0 | 853 | 0 | 0 |

*status*

| statusId | status |
|---|---|
| 0 | 2147483648 |

*results* (15 unreferenced columns omitted)

| raceId | driverId | fastestLapSpeed |
|---|---|---|
| 853 | 0 | 2147483648 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x.
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: 'PAUL' occurs 0x.
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: 'DI RESTA' occurs 0x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 853 occurs 24x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 0 occurs 0x.
- `results.fastestLapSpeed`: 23,657 rows, 18,389 NULL, 5,045 distinct values. Witness values: '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-075 (codebase_community)

**Question:** Among the tags with tag ID below 15, how many of them have 20 count of posts and below?

**Evidence:** ID below 15 refers to Id < 15; have 20 count of posts and below refers to Count < = 20;

**Gold SQL:**
```sql
SELECT COUNT(id) FROM tags WHERE Count <= 20 AND Id < 15
```
**Predicted SQL:**
```sql
SELECT COUNT(Id) FROM tags WHERE Id < 15 AND Count < 20
```

**Witness database:**

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 4 | 2 | 2 | 18bf9150-f1cb-432d-b7b7-26d2f8e33581 |
| 8 | 1 | 3 | 6320bb0f-c792-4a8c-8083-89507c28d375 |

*posts* (17 unreferenced columns omitted)

| Id | PostTypeId | AcceptedAnswerId | CreaionDate |
|---|---|---|---|
| 2 | 1 | 59 | 2010-07-19 19:12:57.0 |
| 3 | 1 | 5 | 2010-07-19 19:13:28.0 |

*tags* (3 unreferenced columns omitted)

| Id | Count |
|---|---|
| 3 | 3 |
| 2 | 20 |

*users* (10 unreferenced columns omitted)

| Id | Reputation | CreationDate | DisplayName |
|---|---|---|---|
| 24 | 344 | 2010-07-19 19:09:32.0 | A Lion |
| 18 | 128 | 2010-07-19 19:08:29.0 | grokus |
| 88 | 14082 | 2010-07-19 19:35:37.0 | mbq |
| 183 | 22625 | 2010-07-20 02:56:34.0 | Jeromy Anglim |

**Gold result on the witness:** `[[2]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `tags.Id`: 1,032 rows, 0 NULL, 1,032 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x; 2 occurs 1x.
- `tags.Count`: 1,032 rows, 0 NULL, 272 distinct values. Witness values: 3 occurs 39x; 20 occurs 11x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-069 (superhero)

**Question:** Count the good female superheroes.

**Evidence:** good refers to alignment.id = 1; female refers to gender.id = 2;

**Gold SQL:**
```sql
SELECT COUNT(T1.id) FROM superhero AS T1 INNER JOIN alignment AS T2 ON T1.alignment_id = T2.id INNER JOIN gender AS T3 ON T1.gender_id = T3.id WHERE T2.alignment = 'Good' AND T3.gender = 'Female'
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM superhero WHERE alignment_id = 1 AND gender_id = 2
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 1 | 2147483648 |

*attribute*

| id | attribute_name |
|---|---|
| 0 | 2147483648 |

*colour*

| id | colour |
|---|---|
| 0 | 2147483648 |

*gender*

| id | gender |
|---|---|
| 2 | 1021719141584888273 |

*publisher*

| id | publisher_name |
|---|---|
| 0 | 2147483648 |

*race*

| id | race |
|---|---|
| 0 | 2147483648 |

*superhero* (9 unreferenced columns omitted)

| id | gender_id | alignment_id |
|---|---|---|
| 0 | 2 | 1 |

*hero_attribute*

| hero_id | attribute_id | attribute_value |
|---|---|---|
| 0 | 0 | 0 |

*superpower*

| id | power_name |
|---|---|
| 0 | 2147483648 |

*hero_power*

| hero_id | power_id |
|---|---|
| 0 | 0 |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `alignment.id`: 4 rows, 0 NULL, 4 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x.
- `alignment.alignment`: 4 rows, 0 NULL, 4 distinct values, all non-NULL values unique. Witness values: '2147483648' occurs 0x.
- Real content of `alignment` (4 rows; referenced columns): (1, 'Good'); (2, 'Bad'); (3, 'Neutral'); (4, 'N/A').
- `gender.id`: 3 rows, 0 NULL, 3 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x.
- `gender.gender`: 3 rows, 0 NULL, 3 distinct values, all non-NULL values unique. Witness values: '1021719141584888273' occurs 0x.
- Real content of `gender` (3 rows; referenced columns): (1, 'Male'); (2, 'Female'); (3, 'N/A').
- `superhero.id`: 750 rows, 0 NULL, 750 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x.
- `superhero.gender_id`: 750 rows, 0 NULL, 3 distinct values. Witness values: 2 occurs 203x.
- `superhero.alignment_id`: 750 rows, 6 NULL, 3 distinct values. Witness values: 1 occurs 504x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-045 (european_football_2)

**Question:** State the name of the most strongest player.

**Evidence:** strongest players refers to player has MAX(overall_rating)

**Gold SQL:**
```sql
SELECT DISTINCT t1.player_name FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t2.overall_rating = (SELECT MAX(overall_rating) FROM Player_Attributes)
```
**Predicted SQL:**
```sql
SELECT T1.player_name FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T2.overall_rating DESC LIMIT 1
```

**Witness database:**

*Player* (5 unreferenced columns omitted)

| player_api_id | player_name |
|---|---|
| -1 | NULL |

*Player_Attributes* (40 unreferenced columns omitted)

| player_api_id | overall_rating |
|---|---|
| -1 | NULL |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: -1 occurs 0x.
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: NULL occurs 0x.
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: -1 occurs 0x.
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: NULL occurs 836x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-110 (codebase_community)

**Question:** What is the average number of badges obtained by a user with over 200 views?

**Evidence:** user with over 200 views refers to Views > 200; average number of badges = Divide (Count(Id), Count(DisplayName))

**Gold SQL:**
```sql
SELECT CAST(COUNT(T1.Id) AS REAL) / COUNT(DISTINCT T2.DisplayName) FROM badges AS T1 INNER JOIN users AS T2 ON T1.UserId = T2.Id WHERE T2.Views > 200
```
**Predicted SQL:**
```sql
SELECT CAST(COUNT(T2.Id) AS REAL) / COUNT(DISTINCT T1.Id) FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.Views > 200
```

**Witness database:**

*badges* (2 unreferenced columns omitted)

| Id | UserId |
|---|---|
| 1001 | 1002 |

*users* (11 unreferenced columns omitted)

| Id | DisplayName | Views |
|---|---|---|
| 1002 | NULL | 201 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[1.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `badges.Id`: 79,851 rows, 0 NULL, 79,851 distinct values, all non-NULL values unique. Witness values: 1001 occurs 1x.
- `badges.UserId`: 79,851 rows, 0 NULL, 25,078 distinct values. Witness values: 1002 occurs 0x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 1002 occurs 0x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: NULL occurs 0x.
- `users.Views`: 40,325 rows, 0 NULL, 362 distinct values. Witness values: 201 occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-117 (financial)

**Question:** For the female client who was born in 1976/1/29, which district did she opened her account?

**Evidence:** Female refers to gender = 'F'; A2 refers to district names

**Gold SQL:**
```sql
SELECT T1.A2 FROM district AS T1 INNER JOIN client AS T2 ON T1.district_id = T2.district_id WHERE T2.birth_date = '1976-01-29' AND T2.gender = 'F'
```
**Predicted SQL:**
```sql
SELECT T4.A2 FROM client AS T1 INNER JOIN disp AS T2 ON T1.client_id = T2.client_id INNER JOIN account AS T3 ON T2.account_id = T3.account_id INNER JOIN district AS T4 ON T3.district_id = T4.district_id WHERE T1.gender = 'F' AND T1.birth_date = '1976-01-29'
```

**Witness database:**

*account* (2 unreferenced columns omitted)

| account_id | district_id |
|---|---|
| 2 | 1 |
| 3 | 5 |
| 1 | 18 |
| 650 | 3 |
| 1082 | 2 |
| 3221 | 5 |
| 3192 | 18 |

*client*

| client_id | gender | birth_date | district_id |
|---|---|---|---|
| 1 | F | 1976-01-29 | 2 |
| 3 | F | 1940-10-09 | 1 |
| 780 | M | 1924-02-26 | 3 |
| 1299 | F | 1920-10-16 | 2 |
| 3896 | M | 1923-10-03 | 5 |
| 3859 | M | 1941-05-03 | 18 |
| 1059 | F | 1951-11-27 | 3 |

*disp* (2 unreferenced columns omitted)

| client_id | account_id |
|---|---|
| 3 | 2 |
| 1 | 3 |
| 780 | 650 |
| 1299 | 1082 |
| 3896 | 3221 |
| 3859 | 3192 |
| 1059 | 1 |

*district* (14 unreferenced columns omitted)

| district_id | A2 |
|---|---|
| 3 | Beroun |
| 2 | Benesov |
| 1 | Hl.m. Praha |
| 5 | Kolin |
| 18 | Pisek |

*trans* (6 unreferenced columns omitted)

| trans_id | account_id | date | type |
|---|---|---|---|
| 3530535 | 2 | 1997-07-31 | PRIJEM |
| 938 | 3 | 1997-12-28 | VYDAJ |
| 3530463 | 1 | 1997-05-31 | PRIJEM |
| 3551957 | 650 | 1995-11-30 | PRIJEM |
| 3566202 | 1082 | 1998-03-31 | PRIJEM |
| 3636851 | 3221 | 1994-06-30 | PRIJEM |
| 935350 | 3192 | 1998-01-31 | VYDAJ |

**Gold result on the witness:** `[['Benesov']]`  
**Predicted result on the witness:** `[['Kolin']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `account.account_id`: 4,500 rows, 0 NULL, 4,500 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 3 occurs 1x; 1 occurs 1x; 650 occurs 1x; 1082 occurs 1x; 3221 occurs 1x (+1 more).
- `account.district_id`: 4,500 rows, 0 NULL, 77 distinct values. Witness values: 1 occurs 554x; 5 occurs 65x; 18 occurs 46x; 3 occurs 50x; 2 occurs 42x.
- `client.client_id`: 5,369 rows, 0 NULL, 5,369 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 3 occurs 1x; 780 occurs 1x; 1299 occurs 1x; 3896 occurs 1x; 3859 occurs 1x (+1 more).
- `client.gender`: 5,369 rows, 0 NULL, 2 distinct values. Witness values: 'F' occurs 2,645x; 'M' occurs 2,724x.
- `client.birth_date`: 5,369 rows, 0 NULL, 4,738 distinct values. Witness values: '1976-01-29' occurs 2x; '1940-10-09' occurs 2x; '1924-02-26' occurs 1x; '1920-10-16' occurs 2x; '1923-10-03' occurs 1x; '1941-05-03' occurs 1x (+1 more).
- `client.district_id`: 5,369 rows, 0 NULL, 77 distinct values. Witness values: 2 occurs 46x; 1 occurs 663x; 3 occurs 63x; 5 occurs 71x; 18 occurs 60x.
- `disp.client_id`: 5,369 rows, 0 NULL, 5,369 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x; 1 occurs 1x; 780 occurs 1x; 1299 occurs 1x; 3896 occurs 1x; 3859 occurs 1x (+1 more).
- `disp.account_id`: 5,369 rows, 0 NULL, 4,500 distinct values. Witness values: 2 occurs 2x; 3 occurs 2x; 650 occurs 1x; 1082 occurs 1x; 3221 occurs 1x; 3192 occurs 2x (+1 more).
- `district.district_id`: 77 rows, 0 NULL, 77 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x; 2 occurs 1x; 1 occurs 1x; 5 occurs 1x; 18 occurs 1x.
- `district.A2`: 77 rows, 0 NULL, 77 distinct values, all non-NULL values unique. Witness values: 'Beroun' occurs 1x; 'Benesov' occurs 1x; 'Hl.m. Praha' occurs 1x; 'Kolin' occurs 1x; 'Pisek' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-065 (thrombosis_prediction)

**Question:** How many of the patients with the most serious thrombosis cases examined in 1997 are women?

**Evidence:** the most serious thrombosis refers to Thrombosis = '1' (the most severe one); women refers to sex = 'F'

**Gold SQL:**
```sql
SELECT  COUNT(*) FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.SEX = 'F' AND STRFTIME('%Y', T2.`Examination Date`) = '1997' AND T2.Thrombosis = 1
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT Patient.ID) AS FemaleThrombosisCount FROM Patient INNER JOIN Examination ON Patient.ID = Examination.ID WHERE Patient.SEX = 'F' AND Examination.Thrombosis = 1 AND Examination.`Examination Date` BETWEEN '1997-01-01' AND '1997-12-31';
```

**Witness database:**

*Examination* (10 unreferenced columns omitted)

| ID | Examination Date | Thrombosis |
|---|---|---|
| -2147483647 | 1997-01-01 | 1 |
| -2147483647 | 1997-01-01 | 1 |

*Patient* (5 unreferenced columns omitted)

| ID | SEX |
|---|---|
| -2147483648 |  |
| -2147483647 | F |

*Laboratory* (40 unreferenced columns omitted)

| ID | Date | GOT | GPT |
|---|---|---|---|
| -2147483648 | 1000-01-01 | -2147483648 | -2147483648 |
| -2147483647 | 1000-01-02 | -2147483648 | -2147483648 |

**Gold result on the witness:** `[[2]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: -2147483647 occurs 0x.
- `Examination.Examination Date`: 806 rows, 10 NULL, 475 distinct values. Witness values: '1997-01-01' occurs 0x.
- `Examination.Thrombosis`: 806 rows, 0 NULL, 4 distinct values. Witness values: 1 occurs 57x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: -2147483648 occurs 0x; -2147483647 occurs 0x.
- `Patient.SEX`: 1,238 rows, 0 NULL, 3 distinct values. Witness values: '' occurs 13x; 'F' occurs 1,023x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-054 (european_football_2)

**Question:** What is the name of players with the highest potential?

**Evidence:** highest potential refers to MAX(potential)

**Gold SQL:**
```sql
SELECT DISTINCT t1.player_name FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id ORDER BY t2.potential DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT DISTINCT player_name FROM Player JOIN Player_Attributes ON Player.player_api_id = Player_Attributes.player_api_id WHERE potential = (SELECT MAX(potential) FROM Player_Attributes);
```

**Witness database:**

*Player* (5 unreferenced columns omitted)

| player_api_id | player_name |
|---|---|
| 2625 | Aaron Cresswell |
| 128455 | Fernando |
| 1 | Daniel Hoeegh |
| 150872 | Wakaso Mubarak |
| 26245 | Andre Luiz |
| 2770 | Ignacio Gonzalez |
| 37194 | Erik Pieters |
| 2983 | Jaime |
| 155782 | Caleb Patterson-Sewell |
| 172768 | Marc Pfertzel |
| 303360 | Antonio Balzano |

*Player_Attributes* (40 unreferenced columns omitted)

| player_api_id | potential |
|---|---|
| 150872 | NULL |
| 26245 | 84 |
| 2625 | 60 |
| 128455 | 62 |
| 1 | 70 |
| 2983 | 73 |
| 37194 | 76 |
| 2625 | 64 |
| 2770 | 69 |
| 155782 | 66 |
| 172768 | 74 |
| 303360 | 68 |
| 2625 | 84 |
| 2625 | 82 |

**Gold result on the witness:** `[['Andre Luiz']]`  
**Predicted result on the witness:** `[['Andre Luiz'], ['Aaron Cresswell']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 2625 occurs 1x; 128455 occurs 1x; 1 occurs 0x; 150872 occurs 1x; 26245 occurs 1x; 2770 occurs 1x (+5 more).
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'Aaron Cresswell' occurs 1x; 'Fernando' occurs 4x; 'Daniel Hoeegh' occurs 1x; 'Wakaso Mubarak' occurs 1x; 'Andre Luiz' occurs 1x; 'Ignacio Gonzalez' occurs 1x (+5 more).
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 150872 occurs 25x; 26245 occurs 14x; 2625 occurs 14x; 128455 occurs 16x; 1 occurs 0x; 2983 occurs 20x (+5 more).
- `Player_Attributes.potential`: 183,978 rows, 836 NULL, 56 distinct values. Witness values: NULL occurs 836x; 84 occurs 3,946x; 60 occurs 1,215x; 62 occurs 2,345x; 70 occurs 9,459x; 73 occurs 10,128x (+7 more).

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-134 (toxicology)

**Question:** Among the molecules with element Calcium, are they mostly carcinogenic or non carcinogenic?

**Evidence:** calcium refers to element = 'ca'; label = '+' mean molecules are carcinogenic; label = '-' means molecules are non-carcinogenic; MAX(label)

**Gold SQL:**
```sql
SELECT T2.label FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'ca' GROUP BY T2.label ORDER BY COUNT(T2.label) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT molecule.label FROM molecule INNER JOIN atom ON molecule.molecule_id = atom.molecule_id WHERE atom.element = 'ca' GROUP BY molecule.label ORDER BY COUNT(*) DESC LIMIT 1
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| molecule_id | element |
|---|---|
| k1 | ca |
| k2 | ca |
| 1 | ca |

*molecule*

| molecule_id | label |
|---|---|
| k2 | NULL |
| k1 | NULL |
| 1 | - |

**Gold result on the witness:** `[['-']]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.molecule_id`: 12,333 rows, 0 NULL, 444 distinct values. Witness values: 'k1' occurs 0x; 'k2' occurs 0x; '1' occurs 0x.
- `atom.element`: 12,333 rows, 0 NULL, 21 distinct values. Witness values: 'ca' occurs 1x.
- `molecule.molecule_id`: 343 rows, 0 NULL, 343 distinct values, all non-NULL values unique. Witness values: 'k2' occurs 0x; 'k1' occurs 0x; '1' occurs 0x.
- `molecule.label`: 343 rows, 0 NULL, 2 distinct values. Witness values: NULL occurs 0x; '-' occurs 191x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-081 (california_schools)

**Question:** What is the administrator's last name that oversees the school with Charter number 40? Indicate the district, the county where the school is situated, and the name of the school.

**Evidence:** -

**Gold SQL:**
```sql
SELECT AdmLName1, District, County, School FROM schools WHERE CharterNum = '0040'
```
**Predicted SQL:**
```sql
SELECT s.AdmLName1, s.District, s.County, s.School FROM schools s JOIN frpm f ON s.CDSCode = f.CDSCode WHERE f."Charter School Number" = '0040';
```

**Witness database:**

*frpm* (27 unreferenced columns omitted)

| CDSCode | Charter School Number |
|---|---|
| 0040 | b |
| k1 | a |

*schools* (43 unreferenced columns omitted)

| CDSCode | County | District | School | CharterNum | AdmLName1 |
|---|---|---|---|---|---|
| 0040 | 0040 | 0040 | y2 | a | 0040 |
| k1 | 0040 | 0040 | NULL | 0040 | NULL |

**Gold result on the witness:** `[[None, '0040', '0040', None]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `frpm.CDSCode`: 9,986 rows, 0 NULL, 9,986 distinct values, all non-NULL values unique. Witness values: '0040' occurs 0x; 'k1' occurs 0x.
- `frpm.Charter School Number`: 9,986 rows, 8,819 NULL, 1,152 distinct values. Witness values: 'b' occurs 0x; 'a' occurs 0x.
- `schools.CDSCode`: 17,686 rows, 0 NULL, 17,686 distinct values, all non-NULL values unique. Witness values: '0040' occurs 0x; 'k1' occurs 0x.
- `schools.County`: 17,686 rows, 0 NULL, 58 distinct values. Witness values: '0040' occurs 0x.
- `schools.District`: 17,686 rows, 0 NULL, 1,411 distinct values. Witness values: '0040' occurs 0x.
- `schools.School`: 17,686 rows, 1,369 NULL, 13,875 distinct values. Witness values: 'y2' occurs 0x; NULL occurs 1,369x.
- `schools.CharterNum`: 17,686 rows, 15,885 NULL, 1,763 distinct values. Witness values: 'a' occurs 0x; '0040' occurs 1x.
- `schools.AdmLName1`: 17,686 rows, 5,986 NULL, 6,394 distinct values. Witness values: '0040' occurs 0x; NULL occurs 5,986x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-056 (financial)

**Question:** List the top nine districts, by descending order, from the highest to the lowest, the number of female account holders.

**Evidence:** A2 refers to districts; Female refers to gender = 'F'

**Gold SQL:**
```sql
SELECT T2.A2, COUNT(T1.client_id) FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.gender = 'F' GROUP BY T2.district_id, T2.A2 ORDER BY COUNT(T1.client_id) DESC LIMIT 9
```
**Predicted SQL:**
```sql
SELECT `district`.`A2`, COUNT(`client`.`client_id`) AS `female_count` FROM `client` INNER JOIN `district` ON `client`.`district_id` = `district`.`district_id` WHERE `client`.`gender` = 'F' GROUP BY `district`.`A2` ORDER BY `female_count` DESC LIMIT 9
```

**Witness database:**

*account*

| account_id | district_id | frequency | date |
|---|---|---|---|
| 1 | -1 | 2147483648 | 1000-01-01 |
| 0 | -1 | 2147483648 | 1000-01-01 |

*card*

| card_id | disp_id | type | issued |
|---|---|---|---|
| 0 | 0 | 2147483648 | 1000-01-01 |
| 1 | 1 | 2147483648 | 1000-01-01 |

*client* (1 unreferenced columns omitted)

| client_id | gender | district_id |
|---|---|---|
| 1 | F | -1 |
| 0 | F | 0 |

*disp*

| disp_id | client_id | account_id | type |
|---|---|---|---|
| 0 | 1 | 1 | 2147483648 |
| 1 | 1 | 0 | 2147483648 |

*district* (14 unreferenced columns omitted)

| district_id | A2 |
|---|---|
| 0 | 2147483648 |
| -1 | 2147483648 |

*loan* (3 unreferenced columns omitted)

| loan_id | account_id | date | amount |
|---|---|---|---|
| 0 | 1 | 1000-01-01 | 0 |
| -1 | 1 | 1000-01-01 | 0 |

*order* (2 unreferenced columns omitted)

| order_id | account_id | bank_to | account_to |
|---|---|---|---|
| 0 | 1 | 2147483648 | 0 |
| -1 | 1 | 2147483648 | 0 |

*trans* (6 unreferenced columns omitted)

| trans_id | account_id | date | type |
|---|---|---|---|
| 0 | 1 | 1000-01-01 | 2147483648 |
| -1 | 0 | 1000-01-01 | 2147483648 |

**Gold result on the witness:** `[['2147483648', 1], ['2147483648', 1]]`  
**Predicted result on the witness:** `[['2147483648', 2]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `client.client_id`: 5,369 rows, 0 NULL, 5,369 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 0 occurs 0x.
- `client.gender`: 5,369 rows, 0 NULL, 2 distinct values. Witness values: 'F' occurs 2,645x.
- `client.district_id`: 5,369 rows, 0 NULL, 77 distinct values. Witness values: -1 occurs 0x; 0 occurs 0x.
- `district.district_id`: 77 rows, 0 NULL, 77 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x; -1 occurs 0x.
- `district.A2`: 77 rows, 0 NULL, 77 distinct values, all non-NULL values unique. Witness values: '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-087 (thrombosis_prediction)

**Question:** Please list a patient's platelet level if it is within the normal range and if he or she is diagnosed with MCTD.

**Evidence:** PLT > 100 and PLT < 400 means platelet level is within the normal range; PLT < 100 and PLT > 400 means platelet level is not within the normal range; diagnosed with MCTD refers to Diagnosis = 'MCTD';

**Gold SQL:**
```sql
SELECT T2.PLT FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'MCTD' AND T2.PLT BETWEEN 100 AND 400
```
**Predicted SQL:**
```sql
SELECT PLT FROM Laboratory WHERE PLT > 100 AND PLT < 400 AND ID IN (SELECT ID FROM Patient WHERE Diagnosis = 'MCTD');
```

**Witness database:**

*Examination* (9 unreferenced columns omitted)

| ID | Examination Date | aCL IgG | aCL IgM |
|---|---|---|---|
| 0 | 1000-01-01 | 0 | 0 |

*Patient* (5 unreferenced columns omitted)

| ID | Diagnosis |
|---|---|
| 0 | MCTD |

*Laboratory* (42 unreferenced columns omitted)

| ID | PLT |
|---|---|
| 0 | 100 |

**Gold result on the witness:** `[[100]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x.
- `Patient.Diagnosis`: 1,238 rows, 0 NULL, 220 distinct values. Witness values: 'MCTD' occurs 35x.
- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 0 occurs 0x.
- `Laboratory.PLT`: 13,908 rows, 2,621 NULL, 657 distinct values. Witness values: 100 occurs 3x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-148 (thrombosis_prediction)

**Question:** Among the patients whose level of Hematoclit isn't normal, which patient has the highest anti-Cardiolipin antibody concentration? Please list his or her ID.

**Evidence:** Hematoclit is normal refers to 29 < N < 52; highest anti-Cardiolipin antibody concentration refers to MAX(`aCL IgA`);

**Gold SQL:**
```sql
SELECT DISTINCT T1.ID FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID INNER JOIN Laboratory AS T3 on T1.ID = T3.ID WHERE (T3.HCT >= 52 OR T3.HCT <= 29) ORDER BY T2.`aCL IgA` DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.ID FROM Laboratory AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.HCT < 29 OR T1.HCT > 52 ORDER BY T2.`aCL IgA` DESC LIMIT 1
```

**Witness database:**

*Examination* (11 unreferenced columns omitted)

| ID | aCL IgA |
|---|---|
| 1074 | 8 |

*Laboratory* (42 unreferenced columns omitted)

| ID | HCT |
|---|---|
| 1074 | 52.0 |

*Patient* (6 unreferenced columns omitted)

| ID |
|---|
| 1074 |

**Gold result on the witness:** `[[1074]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: 1074 occurs 0x.
- `Examination.aCL IgA`: 806 rows, 0 NULL, 52 distinct values. Witness values: 8 occurs 18x.
- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 1074 occurs 0x.
- `Laboratory.HCT`: 13,908 rows, 1,827 NULL, 363 distinct values. Witness values: 52.0 occurs 1x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 1074 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-028 (formula_1)

**Question:** Which driver created the fastest lap speed in a Formula_1 race? Please give both his forename and surname.

**Evidence:** -

**Gold SQL:**
```sql
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId WHERE T2.fastestLapTime IS NOT NULL ORDER BY T2.fastestLapSpeed DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT d.forename, d.surname FROM drivers d JOIN results r ON d.driverId = r.driverId ORDER BY r.fastestLapSpeed DESC LIMIT 1;
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | 2147483648 |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | 2147483648 |

*drivers* (6 unreferenced columns omitted)

| driverId | forename | surname |
|---|---|---|
| 1 | 2147483648 | 2147483648 |

*seasons*

| year | url |
|---|---|
| 0 | 2147483648 |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 1 | 0 | 1 | 1 |

*constructorResults* (1 unreferenced columns omitted)

| constructorResultsId | raceId | constructorId | points |
|---|---|---|---|
| 1 | 1 | 1 | 0 |

*constructorStandings* (3 unreferenced columns omitted)

| constructorStandingsId | raceId | constructorId | points |
|---|---|---|---|
| 1 | 1 | 1 | 0 |

*driverStandings* (3 unreferenced columns omitted)

| driverStandingsId | raceId | driverId | points |
|---|---|---|---|
| 1 | 1 | 1 | 0 |

*lapTimes* (2 unreferenced columns omitted)

| raceId | driverId | lap | position |
|---|---|---|---|
| 1 | 1 | 1 | 1 |

*pitStops* (3 unreferenced columns omitted)

| raceId | driverId | stop | lap |
|---|---|---|---|
| 1 | 1 | 1 | 1 |

*qualifying* (5 unreferenced columns omitted)

| qualifyId | raceId | driverId | constructorId |
|---|---|---|---|
| 1 | 1 | 1 | 1 |

*status*

| statusId | status |
|---|---|
| 1 | 2147483648 |

*results* (15 unreferenced columns omitted)

| driverId | fastestLapTime | fastestLapSpeed |
|---|---|---|
| 1 | NULL | 2147483648 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2147483648', '2147483648']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x.
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: '2147483648' occurs 0x.
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: '2147483648' occurs 0x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 1 occurs 202x.
- `results.fastestLapTime`: 23,657 rows, 18,389 NULL, 4,955 distinct values. Witness values: NULL occurs 18,389x.
- `results.fastestLapSpeed`: 23,657 rows, 18,389 NULL, 5,045 distinct values. Witness values: '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-064 (european_football_2)

**Question:** State the name of the most strongest player.

**Evidence:** strongest players refers to player has MAX(overall_rating)

**Gold SQL:**
```sql
SELECT DISTINCT t1.player_name FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t2.overall_rating = (SELECT MAX(overall_rating) FROM Player_Attributes)
```
**Predicted SQL:**
```sql
SELECT T2.player_name FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_fifa_api_id = T2.player_fifa_api_id ORDER BY T1.overall_rating DESC LIMIT 10
```

**Witness database:**

*Player_Attributes* (39 unreferenced columns omitted)

| player_fifa_api_id | player_api_id | overall_rating |
|---|---|---|
| 8 | 1 | 2 |
| 42 | 43 | 2 |
| 8 | 85 | 86 |
| 42 | 98 | 86 |
| 8 | NULL | 2 |
| 42 | 43 | 2 |
| 8 | 159 | 86 |
| 42 | 98 | 86 |
| 8 | 193 | NULL |
| 42 | 205 | NULL |
| 8 | 85 | 2 |
| 42 | 98 | 2 |

*Player* (4 unreferenced columns omitted)

| player_api_id | player_name | player_fifa_api_id |
|---|---|---|
| 1 | a | 4 |
| 78 | g | 42 |
| 82 | i | 8 |
| 85 | k | 88 |
| NULL | a | 149 |
| 159 | o | NULL |
| 193 | q | 195 |
| 85 | NULL | 249 |

**Gold result on the witness:** `[[None], ['k'], ['o']]`  
**Predicted result on the witness:** `[['i'], ['g'], ['i'], ['g'], ['i'], ['g'], ['i'], ['g'], ['i'], ['g']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player_Attributes.player_fifa_api_id`: 183,978 rows, 0 NULL, 11,062 distinct values. Witness values: 8 occurs 0x; 42 occurs 0x.
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 1 occurs 0x; 43 occurs 0x; 85 occurs 0x; 98 occurs 0x; NULL occurs 0x; 159 occurs 0x (+2 more).
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: 2 occurs 0x; 86 occurs 456x; NULL occurs 836x.
- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 78 occurs 0x; 82 occurs 0x; 85 occurs 0x; NULL occurs 0x; 159 occurs 0x (+1 more).
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'a' occurs 0x; 'g' occurs 0x; 'i' occurs 0x; 'k' occurs 0x; 'o' occurs 0x; 'q' occurs 0x (+1 more).
- `Player.player_fifa_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 4 occurs 0x; 42 occurs 0x; 8 occurs 0x; 88 occurs 0x; 149 occurs 0x; NULL occurs 0x (+2 more).

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-108 (toxicology)

**Question:** Identify whether the molecule that contains atom TR001_1 is carcinogenic.

**Evidence:** label = '+' mean molecules are carcinogenic;

**Gold SQL:**
```sql
SELECT T2.label AS flag_carcinogenic FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.atom_id = 'TR001_1'
```
**Predicted SQL:**
```sql
SELECT label FROM molecule WHERE molecule_id = (SELECT molecule_id FROM atom WHERE atom_id = 'TR001_1') AND label = '+';
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| atom_id | molecule_id |
|---|---|
| TR001_1 | TR001 |
| TR001_12 | TR001 |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
| TR001_1_12 | TR001 | - |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| TR001_12 | TR001_1 | TR001_1_12 |
| TR001_1 | TR001_12 | TR001_1_12 |

*molecule*

| molecule_id | label |
|---|---|
| TR001 | - |

**Gold result on the witness:** `[['-']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.atom_id`: 12,333 rows, 0 NULL, 12,333 distinct values, all non-NULL values unique. Witness values: 'TR001_1' occurs 1x; 'TR001_12' occurs 1x.
- `atom.molecule_id`: 12,333 rows, 0 NULL, 444 distinct values. Witness values: 'TR001' occurs 21x.
- `molecule.molecule_id`: 343 rows, 0 NULL, 343 distinct values, all non-NULL values unique. Witness values: 'TR001' occurs 1x.
- `molecule.label`: 343 rows, 0 NULL, 2 distinct values. Witness values: '-' occurs 191x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-005 (card_games)

**Question:** Among the cards that doesn't have multiple faces on the same card, who is the illustrator of the card art that has the highest cost of converted mana?

**Evidence:** doesn't have multiple faces refers to side IS NULL; illustrator refers to artist

**Gold SQL:**
```sql
SELECT artist FROM cards WHERE side IS NULL ORDER BY convertedManaCost DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT artist FROM cards WHERE side IS NULL AND convertedmanacost = (SELECT MAX(convertedmanacost) FROM cards WHERE side IS NULL)
```

**Witness database:**

*cards* (71 unreferenced columns omitted)

| artist | convertedManaCost | side |
|---|---|---|
| Dan Scott | 0.0 | NULL |
| Dana Knutson | 0.0 | NULL |

**Gold result on the witness:** `[['Dan Scott']]`  
**Predicted result on the witness:** `[['Dan Scott'], ['Dana Knutson']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `cards.artist`: 56,822 rows, 3 NULL, 991 distinct values. Witness values: 'Dan Scott' occurs 540x; 'Dana Knutson' occurs 37x.
- `cards.convertedManaCost`: 56,822 rows, 0 NULL, 19 distinct values. Witness values: 0.0 occurs 7,327x.
- `cards.side`: 56,822 rows, 55,455 NULL, 5 distinct values. Witness values: NULL occurs 55,455x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-013 (formula_1)

**Question:** For the driver who set the fastest lap speed, what is his nationality?

**Evidence:** the fastest lap speed refers to (MAX) fastestLapSpeed;

**Gold SQL:**
```sql
SELECT T1.nationality FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId ORDER BY T2.fastestLapSpeed DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT d.nationality FROM results r INNER JOIN drivers d ON r.driverId = d.driverId WHERE r.fastestLapSpeed = ( SELECT MAX(fastestLapSpeed) FROM results );
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 64 | ain-diab | Ain Diab | Casablanca |
| 58 | aintree | Aintree | Liverpool |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 66 | brm | BRM | British |

*drivers* (7 unreferenced columns omitted)

| driverId | nationality |
|---|---|
| 541 | British |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 775 | 1958 | 11 | 64 |
| 760 | 1959 | 5 | 58 |

*results* (16 unreferenced columns omitted)

| driverId | fastestLapSpeed |
|---|---|
| 541 | NULL |
| 541 | NULL |

*seasons*

| year | url |
|---|---|
| 1958 | http://en.wikipedia.org/wiki/1958_Formula_One_season |
| 1959 | http://en.wikipedia.org/wiki/1959_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 5 | Engine |
| 20 | Spun off |

**Gold result on the witness:** `[['British']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 541 occurs 1x.
- `drivers.nationality`: 840 rows, 0 NULL, 41 distinct values. Witness values: 'British' occurs 162x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 541 occurs 15x.
- `results.fastestLapSpeed`: 23,657 rows, 18,389 NULL, 5,045 distinct values. Witness values: NULL occurs 18,389x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-047 (codebase_community)

**Question:** What is the total score of the posts edited by Yevgeny and include the user's website URL.

**Evidence:** "Yevgeny" is the DisplayName; edited refers to LastEditorUserId

**Gold SQL:**
```sql
SELECT SUM(T1.Score), T2.WebsiteUrl FROM posts AS T1 INNER JOIN users AS T2 ON T1.LastEditorUserId = T2.Id WHERE T2.DisplayName = 'Yevgeny' GROUP BY T2.WebsiteUrl
```
**Predicted SQL:**
```sql
SELECT COALESCE(SUM(posts.Score), 0) AS TotalScore, users.WebsiteUrl FROM users JOIN posts ON users.Id = posts.LastEditorUserId WHERE users.DisplayName = 'Yevgeny';
```

**Witness database:**

*badges*

| Id | UserId | Name | Date |
|---|---|---|---|
| 0 | 0 | 2147483648 | 1000-01-01 |

*comments* (3 unreferenced columns omitted)

| Id | PostId | Score | Text |
|---|---|---|---|
| 0 | 0 | 0 | 2147483648 |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 0 | 0 | 0 | 2147483648 |

*postLinks* (1 unreferenced columns omitted)

| Id | CreationDate | PostId | RelatedPostId |
|---|---|---|---|
| 0 | 1000-01-01 | 0 | 0 |

*posts* (19 unreferenced columns omitted)

| Score | LastEditorUserId |
|---|---|
| 0 | 0 |

*tags* (1 unreferenced columns omitted)

| Id | TagName | Count | ExcerptPostId |
|---|---|---|---|
| 0 | 2147483648 | 0 | 0 |

*users* (11 unreferenced columns omitted)

| Id | DisplayName | WebsiteUrl |
|---|---|---|
| 0 | 1803838093158530456 | 2147483648 |

*votes* (2 unreferenced columns omitted)

| Id | PostId | VoteTypeId | CreationDate |
|---|---|---|---|
| 0 | 0 | 0 | 1000-01-01 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[0, None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `posts.Score`: 91,966 rows, 0 NULL, 130 distinct values. Witness values: 0 occurs 20,194x.
- `posts.LastEditorUserId`: 91,966 rows, 47,361 NULL, 6,578 distinct values. Witness values: 0 occurs 0x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: '1803838093158530456' occurs 0x.
- `users.WebsiteUrl`: 40,325 rows, 32,204 NULL, 7,787 distinct values. Witness values: '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-018 (thrombosis_prediction)

**Question:** What was the gender of the first AORTITIS diagnosed patient?

**Evidence:** gender means SEX; 'AORTITIS' refers to Diagnosis;

**Gold SQL:**
```sql
SELECT SEX FROM Patient WHERE Diagnosis = 'AORTITIS' AND `First Date` IS NOT NULL ORDER BY `First Date` ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT SEX FROM Patient WHERE Diagnosis = 'AORTITIS' ORDER BY Description ASC LIMIT 1
```

**Witness database:**

*Patient* (3 unreferenced columns omitted)

| SEX | Description | First Date | Diagnosis |
|---|---|---|---|
| F | 1994-02-19 | NULL | AORTITIS |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['F']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Patient.SEX`: 1,238 rows, 0 NULL, 3 distinct values. Witness values: 'F' occurs 1,023x.
- `Patient.Description`: 1,238 rows, 216 NULL, 97 distinct values. Witness values: '1994-02-19' occurs 24x.
- `Patient.First Date`: 1,238 rows, 251 NULL, 797 distinct values. Witness values: NULL occurs 251x.
- `Patient.Diagnosis`: 1,238 rows, 0 NULL, 220 distinct values. Witness values: 'AORTITIS' occurs 13x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-057 (formula_1)

**Question:** What's the fastest lap time ever in a race for Lewis Hamilton?

**Evidence:** fastest lap time ever refers to min(fastestLapTime)

**Gold SQL:**
```sql
SELECT T2.fastestLapTime FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId WHERE T1.forename = 'Lewis' AND T1.surname = 'Hamilton' AND T2.fastestLapTime IS NOT NULL ORDER BY T2.fastestLapTime ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT MIN(results.fastestLapTime) AS fastest_lap_time FROM results INNER JOIN drivers ON results.driverId = drivers.driverId WHERE drivers.forename = 'Lewis' AND drivers.surname = 'Hamilton';
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 46 | watkins_glen | Watkins Glen | New York State |
| 18 | interlagos | Autódromo José Carlos Pace | São Paulo |
| 6 | monaco | Circuit de Monaco | Monte-Carlo |
| 38 | brands_hatch | Brands Hatch | Kent |
| 26 | jerez | Circuito de Jerez | Jerez de la Frontera |
| 14 | monza | Autodromo Nazionale di Monza | Monza |
| 20 | nurburgring | Nürburgring | Nürburg |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 65 | martini | Martini | French |
| 4 | renault | Renault | French |
| 78 | amon | Amon | New Zealand |
| 167 | cooper-maserati | Cooper-Maserati | British |
| 42 | coloni | Coloni | Italian |
| 6 | ferrari | Ferrari | Italian |
| 128 | gordini | Gordini | French |

*drivers* (6 unreferenced columns omitted)

| driverId | forename | surname |
|---|---|---|
| 389 | Guy | Ligier |
| 134 | Enrico | Bertaggia |
| 791 | Clemente | Biondetti |
| 639 | André | Milhoux |
| 163 | René | Arnoux |
| 21 | Giancarlo | Fisichella |
| 278 | Chris | Amon |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 541 | 1978 | 15 | 46 |
| 52 | 2007 | 17 | 18 |
| 595 | 1974 | 6 | 6 |
| 693 | 1966 | 4 | 38 |
| 369 | 1989 | 14 | 26 |
| 839 | 1950 | 7 | 14 |
| 790 | 1956 | 7 | 20 |

*results* (16 unreferenced columns omitted)

| driverId | fastestLapTime |
|---|---|
| 163 | NULL |
| 21 | 2:02.680 |
| 278 | NULL |
| 389 | NULL |
| 134 | NULL |
| 791 | NULL |
| 639 | NULL |

*seasons*

| year | url |
|---|---|
| 1978 | http://en.wikipedia.org/wiki/1978_Formula_One_season |
| 2007 | http://en.wikipedia.org/wiki/2007_Formula_One_season |
| 1974 | http://en.wikipedia.org/wiki/1974_Formula_One_season |
| 1966 | http://en.wikipedia.org/wiki/1966_Formula_One_season |
| 1989 | http://en.wikipedia.org/wiki/1989_Formula_One_season |
| 1950 | http://en.wikipedia.org/wiki/1950_Formula_One_season |
| 1956 | http://en.wikipedia.org/wiki/1956_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 11 | +1 Lap |
| 4 | Collision |
| 54 | Withdrew |
| 15 | +5 Laps |
| 97 | Did not prequalify |
| 5 | Engine |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 389 occurs 1x; 134 occurs 1x; 791 occurs 1x; 639 occurs 1x; 163 occurs 1x; 21 occurs 1x (+1 more).
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: 'Guy' occurs 4x; 'Enrico' occurs 1x; 'Clemente' occurs 1x; 'André' occurs 6x; 'René' occurs 1x; 'Giancarlo' occurs 2x (+1 more).
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: 'Ligier' occurs 1x; 'Bertaggia' occurs 1x; 'Biondetti' occurs 1x; 'Milhoux' occurs 1x; 'Arnoux' occurs 1x; 'Fisichella' occurs 1x (+1 more).
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 163 occurs 164x; 21 occurs 231x; 278 occurs 106x; 389 occurs 13x; 134 occurs 6x; 791 occurs 1x (+1 more).
- `results.fastestLapTime`: 23,657 rows, 18,389 NULL, 4,955 distinct values. Witness values: NULL occurs 18,389x; '2:02.680' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-074 (codebase_community)

**Question:** What is the display name of the user who is the owner of the most valuable post?

**Evidence:** most valuable post refers to Max(FavoriteCount)

**Gold SQL:**
```sql
SELECT T2.DisplayName FROM posts AS T1 INNER JOIN users AS T2 ON T1.OwnerUserId = T2.Id ORDER BY T1.FavoriteCount DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT users.displayname FROM users INNER JOIN posts ON users.id = posts.owneruserid WHERE posts.favoritecount = (SELECT MAX(favoritecount) FROM posts)
```

**Witness database:**

*posts* (19 unreferenced columns omitted)

| OwnerUserId | FavoriteCount |
|---|---|
| 1 | 9 |
| 30 | 37 |
| NULL | 37 |
| 71 | 37 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 1 | l |
| 10 | s |
| 30 | ao |
| 71 | NULL |

**Gold result on the witness:** `[['ao']]`  
**Predicted result on the witness:** `[['ao'], [None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `posts.OwnerUserId`: 91,966 rows, 1,392 NULL, 21,979 distinct values. Witness values: 1 occurs 0x; 30 occurs 39x; NULL occurs 1,392x; 71 occurs 40x.
- `posts.FavoriteCount`: 91,966 rows, 78,723 NULL, 77 distinct values. Witness values: 9 occurs 84x; 37 occurs 3x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 10 occurs 1x; 30 occurs 1x; 71 occurs 1x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: 'l' occurs 0x; 's' occurs 0x; 'ao' occurs 0x; NULL occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-103 (debit_card_specializing)

**Question:** There's one customer spent 214582.17 in the June of 2013, which currency did he/she use?

**Evidence:** June of 2013 means Date contains '201306' in the yearmonth.date of the database

**Gold SQL:**
```sql
SELECT T2.Currency FROM yearmonth AS T1 INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Date = '201306' AND T1.Consumption = 214582.17
```
**Predicted SQL:**
```sql
SELECT c.Currency FROM yearmonth AS y JOIN customers AS c ON y.CustomerID = c.CustomerID WHERE y.`Date` LIKE '201306%' GROUP BY y.CustomerID HAVING SUM(y.Consumption) > 214582.17
```

**Witness database:**

*customers* (1 unreferenced columns omitted)

| CustomerID | Currency |
|---|---|
| 33810 | CZK |

*yearmonth*

| CustomerID | Date | Consumption |
|---|---|---|
| 33810 | 201306 | 214582.17 |

**Gold result on the witness:** `[['CZK']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `customers.CustomerID`: 32,461 rows, 0 NULL, 32,461 distinct values, all non-NULL values unique. Witness values: 33810 occurs 1x.
- `customers.Currency`: 32,461 rows, 0 NULL, 2 distinct values. Witness values: 'CZK' occurs 30,459x.
- `yearmonth.CustomerID`: 383,282 rows, 0 NULL, 30,566 distinct values. Witness values: 33810 occurs 18x.
- `yearmonth.Date`: 383,282 rows, 0 NULL, 21 distinct values. Witness values: '201306' occurs 25,378x.
- `yearmonth.Consumption`: 383,282 rows, 0 NULL, 279,091 distinct values. Witness values: 214582.17 occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-094 (student_club)

**Question:** For all the budgets for "November Meeting", how many of them had exceeded the budget?

**Evidence:** 'November Meeting' is an event name; remaining < 0 means the cost had exceeded the budget

**Gold SQL:**
```sql
SELECT COUNT(T2.event_id) FROM budget AS T1 INNER JOIN event AS T2 ON T1.link_to_event = T2.event_id WHERE T2.event_name = 'November Meeting' AND T1.remaining < 0
```
**Predicted SQL:**
```sql
SELECT SUM(CASE WHEN b.remaining < 0 THEN 1 ELSE 0 END) AS total_burden FROM event AS e INNER JOIN budget AS b ON e.event_id = b.link_to_event WHERE e.event_name = 'November Meeting'
```

**Witness database:**

*event* (5 unreferenced columns omitted)

| event_id | event_name |
|---|---|
| 2147483648 | 281070425175486376 |

*major*

| major_id | major_name | department | college |
|---|---|---|---|
| 2147483648 | 2147483648 | 2147483648 | 2147483648 |

*zip_code* (2 unreferenced columns omitted)

| zip_code | type | city | county |
|---|---|---|---|
| 0 | Standard | 2147483648 | 2147483648 |

*attendance*

| link_to_event | link_to_member |
|---|---|
| 2147483648 | 2147483648 |

*budget* (5 unreferenced columns omitted)

| remaining | link_to_event |
|---|---|
| 0 | 2147483648 |

*expense* (3 unreferenced columns omitted)

| expense_id | expense_description | expense_date | cost |
|---|---|---|---|
| 2147483648 | 2147483648 | 2147483648 | 0 |

*income* (2 unreferenced columns omitted)

| income_id | date_received | amount | source |
|---|---|---|---|
| 2147483648 | 2147483648 | 0 | 2147483648 |

*member* (5 unreferenced columns omitted)

| member_id | first_name | last_name | email |
|---|---|---|---|
| 2147483648 | 2147483648 | 2147483648 | 2147483648 |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `event.event_id`: 42 rows, 0 NULL, 42 distinct values, all non-NULL values unique. Witness values: '2147483648' occurs 0x.
- `event.event_name`: 42 rows, 0 NULL, 39 distinct values. Witness values: '281070425175486376' occurs 0x.
- `budget.remaining`: 52 rows, 0 NULL, 22 distinct values. Witness values: 0 occurs 0x.
- `budget.link_to_event`: 52 rows, 0 NULL, 23 distinct values. Witness values: '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-051 (card_games)

**Question:** How many cards in the set Coldsnap have a black border color?

**Evidence:** card set Coldsnap refers to name = 'Coldsnap'; black border color refers to borderColor = 'black'

**Gold SQL:**
```sql
SELECT SUM(CASE WHEN T1.borderColor = 'black' THEN 1 ELSE 0 END) FROM cards AS T1 INNER JOIN sets AS T2 ON T2.code = T1.setCode WHERE T2.name = 'Coldsnap'
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM sets s JOIN cards c ON s.code = c.setCode WHERE s.name = 'Coldsnap' AND c.borderColor = 'black'
```

**Witness database:**

*cards* (72 unreferenced columns omitted)

| borderColor | setCode |
|---|---|
| silver | UNH |
| black | MBS |
| black | M20 |
| black | PFRF |

*sets* (19 unreferenced columns omitted)

| code | name |
|---|---|
| CM1 | Commander's Arsenal |
| NEM | Nemesis |
| P10 | Magic Player Rewards 2010 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `cards.borderColor`: 56,822 rows, 0 NULL, 5 distinct values. Witness values: 'silver' occurs 591x; 'black' occurs 49,729x.
- `cards.setCode`: 56,822 rows, 0 NULL, 536 distinct values. Witness values: 'UNH' occurs 173x; 'MBS' occurs 155x; 'M20' occurs 345x; 'PFRF' occurs 42x.
- `sets.code`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 'CM1' occurs 1x; 'NEM' occurs 1x; 'P10' occurs 1x.
- `sets.name`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: "Commander's Arsenal" occurs 1x; 'Nemesis' occurs 1x; 'Magic Player Rewards 2010' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-055 (codebase_community)

**Question:** Give the only one comment text of the post with parent id 107829.

**Evidence:** one comment refers to CommentCount = '1'

**Gold SQL:**
```sql
SELECT T2.Text FROM posts AS T1 INNER JOIN comments AS T2 ON T1.Id = T2.PostId WHERE T1.ParentId = 107829 AND T1.CommentCount = 1
```
**Predicted SQL:**
```sql
SELECT comments.Text FROM posts INNER JOIN comments ON posts.Id = comments.PostId WHERE posts.ParentId = 107829 AND posts.CommentCount = 1 LIMIT 1;
```

**Witness database:**

*badges*

| Id | UserId | Name | Date |
|---|---|---|---|
| 1 | 1 | 2147483648 | 0001-01-01 |
| 2 | 1 | 2147483648 | 0001-01-01 |

*comments* (5 unreferenced columns omitted)

| PostId | Text |
|---|---|
| 1 | 2147483649 |
| 2 | 2147483648 |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 2 | 1 | 1 | 2147483648 |
| 1 | 3 | 1 | 2147483648 |

*postLinks* (1 unreferenced columns omitted)

| Id | CreationDate | PostId | RelatedPostId |
|---|---|---|---|
| 1 | 0001-01-01 | 1 | 1 |
| 2 | 0001-01-01 | 1 | 1 |

*posts* (18 unreferenced columns omitted)

| Id | CommentCount | ParentId |
|---|---|---|
| 2 | 1 | 107829 |
| 1 | 1 | 107829 |

*tags* (1 unreferenced columns omitted)

| Id | TagName | Count | ExcerptPostId |
|---|---|---|---|
| 1 | 2147483648 | 0 | 1 |
| 2 | 2147483649 | 0 | 2 |

*users* (10 unreferenced columns omitted)

| Id | Reputation | CreationDate | DisplayName |
|---|---|---|---|
| 2 | 1 | 0001-01-01 | 2147483648 |
| 1 | 1 | 0001-01-01 | 2147483648 |

*votes* (2 unreferenced columns omitted)

| Id | PostId | VoteTypeId | CreationDate |
|---|---|---|---|
| 1 | 2 | 1 | 0001-01-01 |
| 2 | 2 | 1 | 0001-01-01 |

**Gold result on the witness:** `[['2147483649'], ['2147483648']]`  
**Predicted result on the witness:** `[['2147483649']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `comments.PostId`: 174,285 rows, 0 NULL, 53,416 distinct values. Witness values: 1 occurs 1x; 2 occurs 1x.
- `comments.Text`: 174,285 rows, 0 NULL, 173,644 distinct values. Witness values: '2147483649' occurs 0x; '2147483648' occurs 0x.
- `posts.Id`: 91,966 rows, 0 NULL, 91,966 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 1 occurs 1x.
- `posts.CommentCount`: 91,966 rows, 0 NULL, 39 distinct values. Witness values: 1 occurs 15,091x.
- `posts.ParentId`: 91,966 rows, 44,211 NULL, 29,006 distinct values. Witness values: 107829 occurs 4x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-101 (codebase_community)

**Question:** What is the total score of the posts edited by Yevgeny and include the user's website URL.

**Evidence:** "Yevgeny" is the DisplayName; edited refers to LastEditorUserId

**Gold SQL:**
```sql
SELECT SUM(T1.Score), T2.WebsiteUrl FROM posts AS T1 INNER JOIN users AS T2 ON T1.LastEditorUserId = T2.Id WHERE T2.DisplayName = 'Yevgeny' GROUP BY T2.WebsiteUrl
```
**Predicted SQL:**
```sql
SELECT SUM(CAST(posts.Score AS FLOAT)) AS total_score, users.WebsiteUrl FROM posts JOIN users ON posts.LastEditorUserId = users.Id WHERE users.DisplayName = 'Yevgeny';
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
| 2 | 1 | 0 | 2147483648 |
| 1 | 1 | 0 | 2147483648 |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 2 | 10 | 1 | 2147483648 |
| 1 | 1 | 1 | 2147483648 |

*postLinks* (1 unreferenced columns omitted)

| Id | CreationDate | PostId | RelatedPostId |
|---|---|---|---|
| 1 | 0001-01-01 | 1 | 2 |
| 2 | 0001-01-01 | 1 | 1 |

*posts* (19 unreferenced columns omitted)

| Score | LastEditorUserId |
|---|---|
| -2147459906 | 2 |
| 0 | 1 |

*tags* (1 unreferenced columns omitted)

| Id | TagName | Count | ExcerptPostId |
|---|---|---|---|
| 1 | 2147483648 | 0 | 1 |
| 2 | 2147483649 | 0 | 2 |

*users* (11 unreferenced columns omitted)

| Id | DisplayName | WebsiteUrl |
|---|---|---|
| 2 | YEVGENY | 2147483649 |
| 1 | YEVGENY | 2147483648 |

*votes* (2 unreferenced columns omitted)

| Id | PostId | VoteTypeId | CreationDate |
|---|---|---|---|
| 1 | 2 | 1 | 0001-01-01 |
| 2 | 2 | 2 | 0001-01-01 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None, None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `posts.Score`: 91,966 rows, 0 NULL, 130 distinct values. Witness values: -2147459906 occurs 0x; 0 occurs 20,194x.
- `posts.LastEditorUserId`: 91,966 rows, 47,361 NULL, 6,578 distinct values. Witness values: 2 occurs 0x; 1 occurs 0x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 1 occurs 0x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: 'YEVGENY' occurs 0x.
- `users.WebsiteUrl`: 40,325 rows, 32,204 NULL, 7,787 distinct values. Witness values: '2147483649' occurs 0x; '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-092 (toxicology)

**Question:** What is the average number of bonds the atoms with the element iodine have?

**Evidence:** atoms with the element iodine refers to element = 'i'; average = DIVIDE(COUND(bond_id), COUNT(atom_id)) where element = 'i'

**Gold SQL:**
```sql
SELECT CAST(COUNT(T2.bond_id) AS REAL) / COUNT(T1.atom_id) FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id WHERE T1.element = 'i'
```
**Predicted SQL:**
```sql
SELECT CAST(COUNT(c.bond_id) AS REAL) / COUNT(DISTINCT a.atom_id) AS average_bonds FROM atom AS a INNER JOIN connected AS c ON a.atom_id = c.atom_id WHERE a.element = 'i'
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| atom_id | element |
|---|---|
| k1 | s |
| k3 | c |
| k2 | i |
| i | cl |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
| i | k1 | NULL |
| k1 | k3 | = |

*connected* (1 unreferenced columns omitted)

| atom_id | bond_id |
|---|---|
| i | i |
| k2 | k1 |
| k2 | k1 |

*molecule*

| molecule_id | label |
|---|---|
| k1 | - |
| k2 | - |
| i | + |
| k3 | + |

**Gold result on the witness:** `[[1.0]]`  
**Predicted result on the witness:** `[[2.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.atom_id`: 12,333 rows, 0 NULL, 12,333 distinct values, all non-NULL values unique. Witness values: 'k1' occurs 0x; 'k3' occurs 0x; 'k2' occurs 0x; 'i' occurs 0x.
- `atom.element`: 12,333 rows, 0 NULL, 21 distinct values. Witness values: 's' occurs 113x; 'c' occurs 4,605x; 'i' occurs 6x; 'cl' occurs 429x.
- `connected.atom_id`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'i' occurs 0x; 'k2' occurs 0x.
- `connected.bond_id`: 24,758 rows, 0 NULL, 12,379 distinct values. Witness values: 'i' occurs 0x; 'k1' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-149 (student_club)

**Question:** Calculate the difference in the percentage of members in New Jersey and Vermont.

**Evidence:** SUBTRACT( DIVIDE( SUM(state = 'New Jersey'), COUNT(position = 'Member')), DIVIDE( SUM(state = 'Vermont'), COUNT(position = 'Member')) )

**Gold SQL:**
```sql
SELECT CAST((SUM(CASE WHEN T2.state = 'New Jersey' THEN 1 ELSE 0 END) - SUM(CASE WHEN T2.state = 'Vermont' THEN 1 ELSE 0 END)) AS REAL) * 100 / COUNT(T1.member_id) AS diff FROM member AS T1 INNER JOIN zip_code AS T2 ON T2.zip_code = T1.zip
```
**Predicted SQL:**
```sql
SELECT(SUM(CASE WHEN z.state = 'New Jersey' THEN 1 ELSE 0 END) * 100.0) /(COUNT(*) * 1.0) -(SUM(CASE WHEN z.state = 'Vermont' THEN 1 ELSE 0 END) * 100.0) FROM member m INNER JOIN zip_code z ON m.zip = z.zip_code
```

**Witness database:**

*major*

| major_id | major_name | department | college |
|---|---|---|---|
| rec1SiX2nFrkbTleH | Biological Engineering | Biological Engineering Department | College of Engineering |
| rec09LedkREyskCNv | Agricultural Communication | School of Applied Sciences, Technology and Education | College of Agriculture and Applied Sciences |

*member* (7 unreferenced columns omitted)

| member_id | zip |
|---|---|
| rec280Sk7o31iG0Tx | 3 |
| rec28ORZgcm1dtqBZ | 2 |

*zip_code* (4 unreferenced columns omitted)

| zip_code | state |
|---|---|
| 3 | New York |
| 2 | Vermont |

**Gold result on the witness:** `[[-50.0]]`  
**Predicted result on the witness:** `[[-100.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `member.member_id`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: 'rec280Sk7o31iG0Tx' occurs 1x; 'rec28ORZgcm1dtqBZ' occurs 1x.
- `member.zip`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: 3 occurs 0x; 2 occurs 0x.
- `zip_code.zip_code`: 41,877 rows, 0 NULL, 41,877 distinct values, all non-NULL values unique. Witness values: 3 occurs 0x; 2 occurs 0x.
- `zip_code.state`: 41,877 rows, 0 NULL, 52 distinct values. Witness values: 'New York' occurs 2,208x; 'Vermont' occurs 309x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-113 (codebase_community)

**Question:** Identify the total views on the post 'Computer Game Datasets'. Name the user who posted it last time.

**Evidence:** total views refer to ViewCount; Name the user refers to DisplayName; post 'Computer Game Datasets' refers to Text = 'Computer Game Datasets';

**Gold SQL:**
```sql
SELECT T2.ViewCount, T3.DisplayName FROM postHistory AS T1 INNER JOIN posts AS T2 ON T1.PostId = T2.Id INNER JOIN users AS T3 ON T2.LastEditorUserId = T3.Id WHERE T1.Text = 'Computer Game Datasets'
```
**Predicted SQL:**
```sql
SELECT p.ViewCount, u.DisplayName FROM posts p JOIN users u ON p.LastEditorUserId = u.Id WHERE p.Title = 'Computer game datasets'
```

**Witness database:**

*postHistory* (7 unreferenced columns omitted)

| PostId | Text |
|---|---|
| 8222 | I have been looking for computer game datasets, but so far I |
| 8222 | <data-mining><dataset><games> |

*posts* (17 unreferenced columns omitted)

| Id | ViewCount | Title | LastEditorUserId |
|---|---|---|---|
| 8222 | 1708 | Computer game datasets | 88 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 88 | mbq |
| 37 | Menno |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[1708, 'mbq']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `postHistory.PostId`: 303,155 rows, 0 NULL, 91,976 distinct values. Witness values: 8222 occurs 7x.
- `postHistory.Text`: 303,155 rows, 0 NULL, 254,564 distinct values. Witness values: "I have been looking for computer game datasets, b occurs 1x; '<data-mining><dataset><games>' occurs 1x.
- `posts.Id`: 91,966 rows, 0 NULL, 91,966 distinct values, all non-NULL values unique. Witness values: 8222 occurs 1x.
- `posts.ViewCount`: 91,966 rows, 49,054 NULL, 3,714 distinct values. Witness values: 1708 occurs 1x.
- `posts.Title`: 91,966 rows, 49,054 NULL, 42,877 distinct values. Witness values: 'Computer game datasets' occurs 1x.
- `posts.LastEditorUserId`: 91,966 rows, 47,361 NULL, 6,578 distinct values. Witness values: 88 occurs 2,663x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 88 occurs 1x; 37 occurs 1x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: 'mbq' occurs 1x; 'Menno' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-118 (superhero)

**Question:** How many heroes have the highest attribute value in strength?

**Evidence:** highest attribute value in strength refers to MAX(attribute_value) WHERE attribute_name = 'Strength';

**Gold SQL:**
```sql
SELECT COUNT(T1.hero_id) FROM hero_attribute AS T1 INNER JOIN attribute AS T2 ON T1.attribute_id = T2.id WHERE T2.attribute_name = 'Strength' AND T1.attribute_value = ( SELECT MAX(attribute_value) FROM hero_attribute )
```
**Predicted SQL:**
```sql
SELECT COUNT(hero_id) FROM hero_attribute AS ha INNER JOIN attribute AS a ON ha.attribute_id = a.id WHERE a.attribute_name = 'Strength' AND ha.attribute_value = ( SELECT MAX(attribute_value) FROM hero_attribute AS ha2 INNER JOIN attribute AS a2 ON ha2.attribute_id = a2.id WHERE a2.attribute_name = 'Strength' );
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 1077 | b |
| 1084 | N/A |

*attribute*

| id | attribute_name |
|---|---|
| 1002 | STRENGTH |
| 1065 | Strength |
| 1401 | Speed |
| 2413 | Durability |

*colour*

| id | colour |
|---|---|
| 1074 | NULL |
| 1081 | NULL |
| 1073 | NULL |
| 1080 | NULL |
| 1072 | NULL |
| 1079 | NULL |

*gender*

| id | gender |
|---|---|
| 1071 | Male |
| 1078 | Female |

*hero_attribute*

| hero_id | attribute_id | attribute_value |
|---|---|---|
| 1005 | 2413 | 3 |
| 1068 | 1065 | 1 |

*publisher*

| id | publisher_name |
|---|---|
| 1076 | Dark Horse Comics |
| 1083 | a |

*race*

| id | race |
|---|---|
| 1075 | NULL |
| 1082 | NULL |

*superhero* (8 unreferenced columns omitted)

| id | superhero_name | full_name | gender_id |
|---|---|---|---|
| 1005 | NULL | NULL | 1071 |
| 1068 | a | NULL | 1078 |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `attribute.id`: 6 rows, 0 NULL, 6 distinct values, all non-NULL values unique. Witness values: 1002 occurs 0x; 1065 occurs 0x; 1401 occurs 0x; 2413 occurs 0x.
- `attribute.attribute_name`: 6 rows, 0 NULL, 6 distinct values, all non-NULL values unique. Witness values: 'STRENGTH' occurs 0x; 'Strength' occurs 1x; 'Speed' occurs 1x; 'Durability' occurs 1x.
- Real content of `attribute` (6 rows; referenced columns): (1, 'Intelligence'); (2, 'Strength'); (3, 'Speed'); (4, 'Durability'); (5, 'Power'); (6, 'Combat').
- `hero_attribute.hero_id`: 3,738 rows, 0 NULL, 623 distinct values. Witness values: 1005 occurs 0x; 1068 occurs 0x.
- `hero_attribute.attribute_id`: 3,738 rows, 0 NULL, 6 distinct values. Witness values: 2413 occurs 0x; 1065 occurs 0x.
- `hero_attribute.attribute_value`: 3,738 rows, 0 NULL, 20 distinct values. Witness values: 3 occurs 0x; 1 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-093 (formula_1)

**Question:** How many drivers don't have a code?

**Evidence:** don't have a code refers to code is null

**Gold SQL:**
```sql
SELECT COUNT(driverId) - COUNT(CASE WHEN code IS NOT NULL THEN code END) FROM drivers
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM drivers WHERE code IS NULL OR code = ''
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

*drivers* (7 unreferenced columns omitted)

| driverId | code |
|---|---|
| 0 |  |

*seasons*

| year | url |
|---|---|
| 0 | 2147483648 |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

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

| resultId | raceId | driverId | constructorId |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x.
- `drivers.code`: 840 rows, 757 NULL, 80 distinct values. Witness values: '' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-077 (formula_1)

**Question:** For the driver who set the fastest lap speed in race No.933, where does he come from?

**Evidence:** fastest lap speed refers to MAX(fastestLapSpeed);

**Gold SQL:**
```sql
SELECT T1.nationality FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId WHERE T2.raceId = 933 AND T2.fastestLapTime IS NOT NULL ORDER BY T2.fastestLapSpeed DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T2.nationality FROM results AS T1 INNER JOIN drivers AS T2 ON T1.driverId = T2.driverId WHERE T1.raceId = 933 ORDER BY T1.fastestLapSpeed DESC LIMIT 1
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | 2147483648 |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | 2147483648 |

*drivers* (7 unreferenced columns omitted)

| driverId | nationality |
|---|---|
| 1 | 2147483648 |

*seasons*

| year | url |
|---|---|
| 0 | 2147483648 |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 933 | 0 | 1 | 1 |

*constructorResults* (1 unreferenced columns omitted)

| constructorResultsId | raceId | constructorId | points |
|---|---|---|---|
| 1 | 933 | 1 | 0 |

*constructorStandings* (3 unreferenced columns omitted)

| constructorStandingsId | raceId | constructorId | points |
|---|---|---|---|
| 1 | 933 | 1 | 0 |

*driverStandings* (3 unreferenced columns omitted)

| driverStandingsId | raceId | driverId | points |
|---|---|---|---|
| 1 | 933 | 1 | 0 |

*lapTimes* (2 unreferenced columns omitted)

| raceId | driverId | lap | position |
|---|---|---|---|
| 933 | 1 | 1 | 1 |

*pitStops* (3 unreferenced columns omitted)

| raceId | driverId | stop | lap |
|---|---|---|---|
| 933 | 1 | 1 | 1 |

*qualifying* (5 unreferenced columns omitted)

| qualifyId | raceId | driverId | constructorId |
|---|---|---|---|
| 1 | 933 | 1 | 1 |

*status*

| statusId | status |
|---|---|
| 1 | 2147483648 |

*results* (14 unreferenced columns omitted)

| raceId | driverId | fastestLapTime | fastestLapSpeed |
|---|---|---|---|
| 933 | 1 | NULL | 2147483648 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2147483648']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x.
- `drivers.nationality`: 840 rows, 0 NULL, 41 distinct values. Witness values: '2147483648' occurs 0x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 933 occurs 20x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 1 occurs 202x.
- `results.fastestLapTime`: 23,657 rows, 18,389 NULL, 4,955 distinct values. Witness values: NULL occurs 18,389x.
- `results.fastestLapSpeed`: 23,657 rows, 18,389 NULL, 5,045 distinct values. Witness values: '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-150 (formula_1)

**Question:** How many drivers don't have a code?

**Evidence:** don't have a code refers to code is null

**Gold SQL:**
```sql
SELECT COUNT(driverId) - COUNT(CASE WHEN code IS NOT NULL THEN code END) FROM drivers
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM drivers WHERE code IS NULL OR code = ''
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | 2147483648 |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | 2147483648 |

*drivers* (7 unreferenced columns omitted)

| driverId | code |
|---|---|
| 1 |  |

*seasons*

| year | url |
|---|---|
| 0 | 2147483648 |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 1 | 0 | 1 | 1 |

*constructorResults* (1 unreferenced columns omitted)

| constructorResultsId | raceId | constructorId | points |
|---|---|---|---|
| 1 | 1 | 1 | 0 |

*constructorStandings* (3 unreferenced columns omitted)

| constructorStandingsId | raceId | constructorId | points |
|---|---|---|---|
| 1 | 1 | 1 | 0 |

*driverStandings* (3 unreferenced columns omitted)

| driverStandingsId | raceId | driverId | points |
|---|---|---|---|
| 1 | 1 | 1 | 0 |

*lapTimes* (2 unreferenced columns omitted)

| raceId | driverId | lap | position |
|---|---|---|---|
| 1 | 1 | 1 | 1 |

*pitStops* (3 unreferenced columns omitted)

| raceId | driverId | stop | lap |
|---|---|---|---|
| 1 | 1 | 1 | 1 |

*qualifying* (5 unreferenced columns omitted)

| qualifyId | raceId | driverId | constructorId |
|---|---|---|---|
| 1 | 1 | 1 | 1 |

*status*

| statusId | status |
|---|---|
| 1 | 2147483648 |

*results* (14 unreferenced columns omitted)

| resultId | raceId | driverId | constructorId |
|---|---|---|---|
| 1 | 1 | 1 | 1 |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x.
- `drivers.code`: 840 rows, 757 NULL, 80 distinct values. Witness values: '' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-035 (codebase_community)

**Question:** State all the tags used by Mark Meckes in his posts that doesn't have comments.

**Evidence:** used by Mark Meckes refers to DisplayName = 'Mark Meckes'; Doen't have comments refers to CommentCount = 0;

**Gold SQL:**
```sql
SELECT T3.Tags FROM users AS T1 INNER JOIN postHistory AS T2 ON T1.Id = T2.UserId INNER JOIN posts AS T3 ON T3.Id = T2.PostId WHERE T1.DisplayName = 'Mark Meckes' AND T3.CommentCount = 0
```
**Predicted SQL:**
```sql
SELECT DISTINCT p.Tags FROM posts p JOIN users u ON p.OwnerUserId = u.Id WHERE u.DisplayName = 'Mark Meckes' AND p.CommentCount = 0
```

**Witness database:**

*postHistory* (7 unreferenced columns omitted)

| PostId | UserId |
|---|---|
| 1230 | 1612 |
| 1050 | 1051 |
| 1609 | 1231 |

*posts* (17 unreferenced columns omitted)

| Id | OwnerUserId | Tags | CommentCount |
|---|---|---|---|
| 1230 | 1231 | <r> | 0 |
| 1050 | 1051 | <sampling> | 0 |
| 1609 | 1610 | <anova> | 20 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 1231 | Mark Meckes |
| 1051 | Mark Meckes |
| 1612 | Chris |
| 1610 | Will |
| 1611 | Eric |

**Gold result on the witness:** `[['<sampling>']]`  
**Predicted result on the witness:** `[['<sampling>'], ['<r>']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `postHistory.PostId`: 303,155 rows, 0 NULL, 91,976 distinct values. Witness values: 1230 occurs 2x; 1050 occurs 2x; 1609 occurs 2x.
- `postHistory.UserId`: 303,155 rows, 21,326 NULL, 22,107 distinct values. Witness values: 1612 occurs 0x; 1051 occurs 0x; 1231 occurs 0x.
- `posts.Id`: 91,966 rows, 0 NULL, 91,966 distinct values, all non-NULL values unique. Witness values: 1230 occurs 1x; 1050 occurs 1x; 1609 occurs 1x.
- `posts.OwnerUserId`: 91,966 rows, 1,392 NULL, 21,979 distinct values. Witness values: 1231 occurs 0x; 1051 occurs 0x; 1610 occurs 0x.
- `posts.Tags`: 91,966 rows, 49,054 NULL, 28,528 distinct values. Witness values: '<r>' occurs 301x; '<sampling>' occurs 83x; '<anova>' occurs 94x.
- `posts.CommentCount`: 91,966 rows, 0 NULL, 39 distinct values. Witness values: 0 occurs 38,553x; 20 occurs 14x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 1231 occurs 0x; 1051 occurs 0x; 1612 occurs 1x; 1610 occurs 0x; 1611 occurs 1x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: 'Mark Meckes' occurs 1x; 'Chris' occurs 80x; 'Will' occurs 24x; 'Eric' occurs 27x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-111 (thrombosis_prediction)

**Question:** For the patient who first came to the hospital on 1991/6/13 who was diagnosed with SJS, what is the total number of his/her Laboratory tests in 1995?

**Evidence:** 1991/6/13 refers to `First Date` = '1991-06-13'; 'SJS' refers to Diagnosis; total number of his/her Laboratory tests refers to COUNT(ID); 1995 refers to Date

**Gold SQL:**
```sql
SELECT COUNT(*) FROM Laboratory WHERE ID = ( SELECT ID FROM Patient WHERE `First Date` = '1991-06-13' AND Diagnosis = 'SJS' ) AND STRFTIME('%Y', Date) = '1995'
```
**Predicted SQL:**
```sql
SELECT COUNT(ID) FROM Laboratory WHERE ID IN (SELECT ID FROM Patient WHERE `First Date` = '1991-06-13' AND Diagnosis = 'SJS') AND `Date` LIKE '1995%'
```

**Witness database:**

*Laboratory* (43 unreferenced columns omitted)

| Date |
|---|
| 1995-02-02 |
| 1995-03-30 |
| 1995-02-02 |
| 1995-03-30 |

*Patient* (4 unreferenced columns omitted)

| ID | First Date | Diagnosis |
|---|---|---|
| 4634342 | 1991-06-13 | SJS |
| 1006 | 1991-06-13 | SJS |

**Gold result on the witness:** `[[2]]`  
**Predicted result on the witness:** `[[4]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Laboratory.Date`: 13,908 rows, 0 NULL, 3,723 distinct values. Witness values: '1995-02-02' occurs 4x; '1995-03-30' occurs 4x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 4634342 occurs 1x; 1006 occurs 0x.
- `Patient.First Date`: 1,238 rows, 251 NULL, 797 distinct values. Witness values: '1991-06-13' occurs 1x.
- `Patient.Diagnosis`: 1,238 rows, 0 NULL, 220 distinct values. Witness values: 'SJS' occurs 160x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-106 (card_games)

**Question:** How many cards with original type of "Summon - Angel" have subtype other than "Angel"?

**Evidence:** subtype other than Angel refers to subtypes is not 'Angel';

**Gold SQL:**
```sql
SELECT COUNT(id) FROM cards WHERE originalType = 'Summon - Angel' AND subtypes != 'Angel'
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM cards WHERE originalType = 'Summon - Angel' AND (subtypes IS NULL OR subtypes != 'Angel');
```

**Witness database:**

*cards* (71 unreferenced columns omitted)

| id | originalType | subtypes |
|---|---|---|
| 2 | NULL | Forest |
| 1 | Summon - Angel | NULL |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `cards.id`: 56,822 rows, 0 NULL, 56,822 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 1 occurs 1x.
- `cards.originalType`: 56,822 rows, 14,766 NULL, 2,992 distinct values. Witness values: NULL occurs 14,766x; 'Summon - Angel' occurs 20x.
- `cards.subtypes`: 56,822 rows, 22,228 NULL, 1,505 distinct values. Witness values: 'Forest' occurs 707x; NULL occurs 22,228x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-132 (student_club)

**Question:** With the biggest budget for the "Food", what was the remaining of it?

**Evidence:** remaining of budget refers to remaining, biggest budget for 'Food' refers to MAX(budget.amount) where category = 'Food'

**Gold SQL:**
```sql
SELECT remaining FROM budget WHERE category = 'Food' AND amount = ( SELECT MAX(amount) FROM budget WHERE category = 'Food' )
```
**Predicted SQL:**
```sql
SELECT remaining FROM budget WHERE category = 'Food' ORDER BY amount DESC LIMIT 1
```

**Witness database:**

*budget* (4 unreferenced columns omitted)

| category | remaining | amount |
|---|---|---|
| Food | 28.86 | 150 |
| Food | 150.0 | 150 |

*event* (3 unreferenced columns omitted)

| event_id | event_name | event_date | type |
|---|---|---|---|
| recggMW2eyCYceNcy | October Meeting | 2019-10-08T12:00:00 | Meeting |
| recY3Yesu24bRK7tr | January Meeting | 2020-01-14T12:00:00 | Meeting |

**Gold result on the witness:** `[[28.86], [150.0]]`  
**Predicted result on the witness:** `[[28.86]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `budget.category`: 52 rows, 0 NULL, 5 distinct values. Witness values: 'Food' occurs 22x.
- `budget.remaining`: 52 rows, 0 NULL, 22 distinct values. Witness values: 28.86 occurs 1x; 150.0 occurs 8x.
- `budget.amount`: 52 rows, 0 NULL, 9 distinct values. Witness values: 150 occurs 14x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-133 (student_club)

**Question:** Which college do most of the members go to?

**Evidence:** college most members go refers to MAX(COUNT(major.college))

**Gold SQL:**
```sql
SELECT T2.college FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id GROUP BY T2.major_id ORDER BY COUNT(T2.college) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT major.college FROM member INNER JOIN major ON member.link_to_major = major.major_id GROUP BY major.college ORDER BY COUNT(member.member_id) DESC LIMIT 1
```

**Witness database:**

*major* (2 unreferenced columns omitted)

| major_id | college |
|---|---|
| rec1N0upiVLy5esTO | College of Natural Resources |
| rec3pZhvStMoNbVgy | College of Humanities and Social Sciences |
| recdem96jNnpiXfsH | School of Business |
| recGvuGMS6k5vjnst | College of Humanities and Social Sciences |
| recKJHO1P6ZC5m567 | College of Education & Human Services |
| recRA9IxLl6eKPsJX | College of Humanities and Social Sciences |
| recaJdSK83k6ekRJL | College of Agriculture and Applied Sciences |

*member* (7 unreferenced columns omitted)

| member_id | link_to_major |
|---|---|
| reccSUPwy30AeZLEb | recKJHO1P6ZC5m567 |
| recT92PyyZCGq1R68 | recRA9IxLl6eKPsJX |
| rec3pH4DxMcWHMRB7 | recaJdSK83k6ekRJL |

*zip_code* (2 unreferenced columns omitted)

| zip_code | type | city | county |
|---|---|---|---|
| 35640 | Standard | Hartselle | Morgan County |
| 79106 | Standard | Amarillo | Potter County |
| 48236 | Standard | Grosse Pointe | Wayne County |

**Gold result on the witness:** `[['College of Agriculture and Applied Sciences']]`  
**Predicted result on the witness:** `[['College of Humanities and Social Sciences']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `major.major_id`: 113 rows, 0 NULL, 113 distinct values, all non-NULL values unique. Witness values: 'rec1N0upiVLy5esTO' occurs 1x; 'rec3pZhvStMoNbVgy' occurs 1x; 'recdem96jNnpiXfsH' occurs 1x; 'recGvuGMS6k5vjnst' occurs 1x; 'recKJHO1P6ZC5m567' occurs 1x; 'recRA9IxLl6eKPsJX' occurs 1x (+1 more).
- `major.college`: 113 rows, 0 NULL, 8 distinct values. Witness values: 'College of Natural Resources' occurs 9x; 'College of Humanities and Social Sciences' occurs 24x; 'School of Business' occurs 7x; 'College of Education & Human Services' occurs 13x; 'College of Agriculture and Applied Sciences' occurs 36x.
- `member.member_id`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: 'reccSUPwy30AeZLEb' occurs 1x; 'recT92PyyZCGq1R68' occurs 1x; 'rec3pH4DxMcWHMRB7' occurs 1x.
- `member.link_to_major`: 33 rows, 1 NULL, 26 distinct values. Witness values: 'recKJHO1P6ZC5m567' occurs 3x; 'recRA9IxLl6eKPsJX' occurs 1x; 'recaJdSK83k6ekRJL' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-078 (california_schools)

**Question:** Which different county has the most number of closed schools? Please provide the name of each school as well as the closure date.

**Evidence:** Closure date and closed date are synonyms; 'Closed' was mentioned in schools.StatusType.

**Gold SQL:**
```sql
SELECT DISTINCT County, School, ClosedDate FROM schools WHERE County = ( SELECT County FROM schools WHERE StatusType = 'Closed' GROUP BY County ORDER BY COUNT(School) DESC LIMIT 1 ) AND StatusType = 'Closed' AND school IS NOT NULL
```
**Predicted SQL:**
```sql
SELECT County, School, ClosedDate FROM schools WHERE StatusType = 'Closed' AND School IS NOT NULL AND ClosedDate IS NOT NULL AND County = (SELECT County FROM schools WHERE StatusType = 'Closed' GROUP BY County ORDER BY COUNT(CDSCode) DESC LIMIT 1) ORDER BY School;
```

**Witness database:**

*schools* (44 unreferenced columns omitted)

| CDSCode | StatusType | County | School | ClosedDate |
|---|---|---|---|---|
| 17640226109706 | Active | Lake | Pomo | NULL |
| 39686766116032 | Closed | San Joaquin | Golden Valley Elementary Community Day | NULL |
| 01100176098586 | Active | Lake | NULL | NULL |

**Gold result on the witness:** `[['San Joaquin', 'Golden Valley Elementary Community Day', None]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `schools.CDSCode`: 17,686 rows, 0 NULL, 17,686 distinct values, all non-NULL values unique. Witness values: '17640226109706' occurs 1x; '39686766116032' occurs 1x; '01100176098586' occurs 1x.
- `schools.StatusType`: 17,686 rows, 0 NULL, 4 distinct values. Witness values: 'Active' occurs 11,708x; 'Closed' occurs 4,518x.
- `schools.County`: 17,686 rows, 0 NULL, 58 distinct values. Witness values: 'Lake' occurs 76x; 'San Joaquin' occurs 427x.
- `schools.School`: 17,686 rows, 1,369 NULL, 13,875 distinct values. Witness values: 'Pomo' occurs 1x; 'Golden Valley Elementary Community Day' occurs 1x; NULL occurs 1,369x.
- `schools.ClosedDate`: 17,686 rows, 11,992 NULL, 899 distinct values. Witness values: NULL occurs 11,992x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-011 (thrombosis_prediction)

**Question:** How many male patients who underwent testing between 1995 and 1997 and were subsequently diagnosed with Behcet disease did not stay in the hospital for treatment?

**Evidence:** male refers to SEX = 'M'; underwent testing between 1995 and 1997 refers to `Examination Date` between '1995' and '1997'; Behcet refers to diagnosis; did not stay in the hospital refers to Admission = '-'

**Gold SQL:**
```sql
SELECT COUNT(T1.ID) FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T2.Diagnosis = 'Behcet' AND T1.SEX = 'M' AND STRFTIME('%Y', T2.`Examination Date`) BETWEEN '1995' AND '1997' AND T1.Admission = '-'
```
**Predicted SQL:**
```sql
SELECT COUNT(T1.ID) FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T2.SEX = 'M' AND T1.`Examination Date` BETWEEN '1995-01-01' AND '1997-12-31' AND T2.Diagnosis = 'BEHCET' AND T2.Admission = '-'
```

**Witness database:**

*Examination* (10 unreferenced columns omitted)

| ID | Examination Date | Diagnosis |
|---|---|---|
| 1 | 1995-08-21 | collagen susp |
| 1 | 1997-05-13 | RA susp |
| 1 | 1995-08-28 | PSS |
| 1 | 1995-06-26 | Adult Still |

*Patient* (3 unreferenced columns omitted)

| ID | SEX | Admission | Diagnosis |
|---|---|---|---|
| 1 | M | - | BEHCET |
| 3 | F | - | PNc |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[4]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: 1 occurs 0x.
- `Examination.Examination Date`: 806 rows, 10 NULL, 475 distinct values. Witness values: '1995-08-21' occurs 4x; '1997-05-13' occurs 4x; '1995-08-28' occurs 4x; '1995-06-26' occurs 4x.
- `Examination.Diagnosis`: 806 rows, 331 NULL, 181 distinct values. Witness values: 'collagen susp' occurs 2x; 'RA susp' occurs 8x; 'PSS' occurs 10x; 'Adult Still' occurs 2x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 3 occurs 0x.
- `Patient.SEX`: 1,238 rows, 0 NULL, 3 distinct values. Witness values: 'M' occurs 202x; 'F' occurs 1,023x.
- `Patient.Admission`: 1,238 rows, 0 NULL, 4 distinct values. Witness values: '-' occurs 713x.
- `Patient.Diagnosis`: 1,238 rows, 0 NULL, 220 distinct values. Witness values: 'BEHCET' occurs 90x; 'PNc' occurs 5x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-041 (european_football_2)

**Question:** Give the name of the league had the most goals in the 2016 season?

**Evidence:** league that had the most goals refers to MAX(SUM(home_team_goal, away_team_goal)); 2016 season refers to season = '2015/2016';

**Gold SQL:**
```sql
SELECT t2.name FROM Match AS t1 INNER JOIN League AS t2 ON t1.league_id = t2.id WHERE t1.season = '2015/2016' GROUP BY t2.name ORDER BY SUM(t1.home_team_goal + t1.away_team_goal) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT L.name FROM Match AS M INNER JOIN League AS L ON M.league_id = L.id WHERE M.season = '2015/2016' GROUP BY L.id ORDER BY SUM(M.home_team_goal + M.away_team_goal) DESC LIMIT 1
```

**Witness database:**

*Country*

| id | name |
|---|---|
| 1 | Germany |

*League* (1 unreferenced columns omitted)

| id | name |
|---|---|
| 2 | Portugal Liga ZON Sagres |
| 3 | England Premier League |
| 1 | Italy Serie A |

*Match* (111 unreferenced columns omitted)

| league_id | season | home_team_goal | away_team_goal |
|---|---|---|---|
| 1 | 2015/2016 | 3 | -1 |
| 3 | 2015/2016 | 1 | 1 |

*Team* (1 unreferenced columns omitted)

| id | team_api_id | team_fifa_api_id | team_long_name |
|---|---|---|---|
| 1 | 1 | -1 | c |

**Gold result on the witness:** `[['Italy Serie A']]`  
**Predicted result on the witness:** `[['England Premier League']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `League.id`: 11 rows, 0 NULL, 11 distinct values, all non-NULL values unique. Witness values: 2 occurs 0x; 3 occurs 0x; 1 occurs 1x.
- `League.name`: 11 rows, 0 NULL, 11 distinct values, all non-NULL values unique. Witness values: 'Portugal Liga ZON Sagres' occurs 1x; 'England Premier League' occurs 1x; 'Italy Serie A' occurs 1x.
- Real content of `League` (11 rows; referenced columns): (1, 'Belgium Jupiler League'); (1729, 'England Premier League'); (4769, 'France Ligue 1'); (7809, 'Germany 1. Bundesliga'); (10257, 'Italy Serie A'); (13274, 'Netherlands Eredivisie'); (15722, 'Poland Ekstraklasa'); (17642, 'Portugal Liga ZON Sagres'); (19694, 'Scotland Premier League'); (21518, 'Spain LIGA BBVA'); (24558, 'Switzerland Super League').
- `Match.league_id`: 25,979 rows, 0 NULL, 11 distinct values. Witness values: 1 occurs 1,728x; 3 occurs 0x.
- `Match.season`: 25,979 rows, 0 NULL, 8 distinct values. Witness values: '2015/2016' occurs 3,326x.
- `Match.home_team_goal`: 25,979 rows, 0 NULL, 11 distinct values. Witness values: 3 occurs 3,288x; 1 occurs 8,400x.
- `Match.away_team_goal`: 25,979 rows, 0 NULL, 10 distinct values. Witness values: -1 occurs 0x; 1 occurs 8,989x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-145 (superhero)

**Question:** List down at least five full name of Demi-God superheroes.

**Evidence:** Demi-God superheroes refers to race = 'Demi-God'

**Gold SQL:**
```sql
SELECT T1.full_name FROM superhero AS T1 INNER JOIN race AS T2 ON T1.race_id = T2.id WHERE T2.race = 'Demi-God'
```
**Predicted SQL:**
```sql
SELECT superhero.full_name FROM superhero INNER JOIN race ON superhero.race_id = race.id WHERE race.race = 'Demi-God' LIMIT 5;
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 1 | Good |
| 4 | N/A |

*colour*

| id | colour |
|---|---|
| 1 | No Colour |
| 9 | Brown |
| 7 | Blue |

*gender*

| id | gender |
|---|---|
| 1 | Male |
| 2 | Female |

*publisher*

| id | publisher_name |
|---|---|
| 25 | Wildstorm |
| 13 | Marvel Comics |

*race*

| id | race |
|---|---|
| 16 | Demi-God |
| 1 | - |

*superhero* (10 unreferenced columns omitted)

| full_name | race_id |
|---|---|
| - | 16 |
| Heracles | 16 |
| Heracles | 16 |
| - | 16 |
| Heracles | 16 |
| Angel Salvadore Bohusk | 16 |

**Gold result on the witness:** `[['Heracles'], ['-'], ['Heracles'], ['-'], ['Heracles'], ['Angel Salvadore Bohusk']]`  
**Predicted result on the witness:** `[['Heracles'], ['-'], ['Heracles'], ['-'], ['Heracles']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `race.id`: 61 rows, 0 NULL, 61 distinct values, all non-NULL values unique. Witness values: 16 occurs 1x; 1 occurs 1x.
- `race.race`: 61 rows, 0 NULL, 61 distinct values, all non-NULL values unique. Witness values: 'Demi-God' occurs 1x; '-' occurs 1x.
- `superhero.full_name`: 750 rows, 122 NULL, 483 distinct values. Witness values: '-' occurs 125x; 'Heracles' occurs 1x; 'Angel Salvadore Bohusk' occurs 2x.
- `superhero.race_id`: 750 rows, 4 NULL, 61 distinct values. Witness values: 16 occurs 3x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-144 (financial)

**Question:** The average unemployment ratio of 1995 and 1996, which one has higher percentage?

**Evidence:** A12 refers to unemploymant rate 1995; A13 refers to unemploymant rate 1996

**Gold SQL:**
```sql
SELECT DISTINCT IIF(AVG(A13) > AVG(A12), '1996', '1995') FROM district
```
**Predicted SQL:**
```sql
SELECT CASE WHEN AVG(a12) > AVG(a13) THEN '1995' ELSE '1996' END AS higher_unemployment_year FROM district
```

**Witness database:**

*district* (14 unreferenced columns omitted)

| A12 | A13 |
|---|---|
| 1996.0 | 1996.0 |
| 1995.0 | 1.5 |
| 1.5 | 1995.0 |
| 1996.0 | 1996.0 |

**Gold result on the witness:** `[['1995']]`  
**Predicted result on the witness:** `[['1996']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `district.A12`: 77 rows, 1 NULL, 41 distinct values. Witness values: 1996.0 occurs 0x; 1995.0 occurs 0x; 1.5 occurs 2x.
- `district.A13`: 77 rows, 0 NULL, 73 distinct values. Witness values: 1996.0 occurs 0x; 1.5 occurs 0x; 1995.0 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-100 (toxicology)

**Question:** Among all the atoms from 21 to 25, list all the molecules that are carcinogenic.

**Evidence:** atoms from 21 to 25 refers to SUBSTR(atom_id, 7, 2) between '21' and '25'; label = '+' mean molecules are carcinogenic

**Gold SQL:**
```sql
SELECT DISTINCT T2.molecule_id FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE SUBSTR(T1.atom_id, -2) BETWEEN '21' AND '25' AND T2.label = '+'
```
**Predicted SQL:**
```sql
SELECT DISTINCT T1.molecule_id FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T2.label = '+' AND CAST(SUBSTR(T1.atom_id, 7, 2) AS INTEGER) BETWEEN 21 AND 25;
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| atom_id | molecule_id |
|---|---|
| ABCDE21 | G |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
|  | G |  |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| ABCDE21 | ABCDE21 |  |

*molecule*

| molecule_id | label |
|---|---|
| G | + |

**Gold result on the witness:** `[['G']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.atom_id`: 12,333 rows, 0 NULL, 12,333 distinct values, all non-NULL values unique. Witness values: 'ABCDE21' occurs 0x.
- `atom.molecule_id`: 12,333 rows, 0 NULL, 444 distinct values. Witness values: 'G' occurs 0x.
- `molecule.molecule_id`: 343 rows, 0 NULL, 343 distinct values, all non-NULL values unique. Witness values: 'G' occurs 0x.
- `molecule.label`: 343 rows, 0 NULL, 2 distinct values. Witness values: '+' occurs 152x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-136 (european_football_2)

**Question:** List all the football player with the highest balance score and potential score of 61.

**Evidence:** balance score refers to balance; highest balance score refers to MAX(balance); potential score refers to potential; potential = 61;

**Gold SQL:**
```sql
SELECT t1.player_name FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t2.potential = '61' ORDER BY t2.balance DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T2.player_name FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_fifa_api_id = T2.player_fifa_api_id WHERE T1.balance = (SELECT MAX(balance) FROM Player_Attributes WHERE potential = 61) AND T1.potential = 61
```

**Witness database:**

*Player* (4 unreferenced columns omitted)

| player_api_id | player_name | player_fifa_api_id |
|---|---|---|
| 2625 | Rafael | 10899 |
| 38607 | Domingos Alexandre Martins da Costa Alex | 201 |
| 24217 | Emre Belozoglu | 80 |
| 26785 | Atiba Hutchinson | 134744 |
| 30373 | Paul Scholes | 246 |
| 361316 | Fabris Fokobo | 213360 |
| 3264 | Abdelmalek Cherrad | 51868 |
| 2790 | Alberto Rey | 110809 |
| 23728 | Uros Korun | 229666 |
| 25930 | Patrick Paauwe | 7391 |

*Player_Attributes* (38 unreferenced columns omitted)

| player_fifa_api_id | player_api_id | potential | balance |
|---|---|---|---|
| 80 | 24217 | NULL | 61 |
| 134744 | 26785 | 61 | NULL |
| 10899 | 2625 | 81 | 69 |
| 201 | 38607 | 75 | 64 |
| 213360 | 361316 | 75 | 67 |
| 51868 | 3264 | 73 | 62 |
| 110809 | 2790 | 77 | 67 |
| 10899 | 2625 | 64 | 49 |
| 201 | 38607 | 68 | 74 |
| 80 | 24217 | 81 | 89 |
| 246 | 30373 | 81 | 82 |
| 229666 | 23728 | 82 | 86 |
| 7391 | 25930 | 73 | NULL |

**Gold result on the witness:** `[['Atiba Hutchinson']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 2625 occurs 1x; 38607 occurs 1x; 24217 occurs 1x; 26785 occurs 1x; 30373 occurs 1x; 361316 occurs 1x (+4 more).
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'Rafael' occurs 4x; 'Domingos Alexandre Martins da Costa Alex' occurs 1x; 'Emre Belozoglu' occurs 1x; 'Atiba Hutchinson' occurs 1x; 'Paul Scholes' occurs 1x; 'Fabris Fokobo' occurs 1x (+4 more).
- `Player.player_fifa_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 10899 occurs 1x; 201 occurs 1x; 80 occurs 1x; 134744 occurs 1x; 246 occurs 1x; 213360 occurs 1x (+4 more).
- `Player_Attributes.player_fifa_api_id`: 183,978 rows, 0 NULL, 11,062 distinct values. Witness values: 80 occurs 26x; 134744 occurs 28x; 10899 occurs 27x; 201 occurs 12x; 213360 occurs 16x; 51868 occurs 5x (+4 more).
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 24217 occurs 26x; 26785 occurs 28x; 2625 occurs 14x; 38607 occurs 13x; 361316 occurs 16x; 3264 occurs 5x (+4 more).
- `Player_Attributes.potential`: 183,978 rows, 836 NULL, 56 distinct values. Witness values: NULL occurs 836x; 61 occurs 1,629x; 81 occurs 5,143x; 75 occurs 11,270x; 73 occurs 10,128x; 77 occurs 8,947x (+3 more).
- `Player_Attributes.balance`: 183,978 rows, 2,713 NULL, 81 distinct values. Witness values: 61 occurs 4,628x; NULL occurs 2,713x; 69 occurs 4,939x; 64 occurs 5,244x; 67 occurs 5,001x; 62 occurs 5,656x (+5 more).

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-141 (toxicology)

**Question:** Name the elements that comprise the atoms of bond TR001_2_4.

**Evidence:** element = 'cl' means Chlorine; element = 'c' means Carbon; element = 'h' means Hydrogen; element = 'o' means Oxygen, element = 's' means Sulfur; element = 'n' means Nitrogen, element = 'p' means Phosphorus, element = 'na' means Sodium, element = 'br' means Bromine, element = 'f' means Fluorine; element = 'i' means Iodine; element = 'sn' means Tin; element = 'pb' means Lead; element = 'te' means Tellurium; element = 'ca' means Calcium

**Gold SQL:**
```sql
SELECT DISTINCT T1.element FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id WHERE T2.bond_id = 'TR001_2_4'
```
**Predicted SQL:**
```sql
SELECT DISTINCT COALESCE(T2.element, T4.element) AS element FROM connected AS T1 LEFT JOIN atom AS T2 ON T1.atom_id = T2.atom_id LEFT JOIN atom AS T4 ON T1.atom_id2 = T4.atom_id WHERE T1.bond_id = 'TR001_2_4';
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| atom_id | element |
|---|---|
| 2147483648 | NULL |
| 2147483649 | 2147483648 |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
| TR001_2_4 | 2147483648 | 2147483648 |
| 1071112397389843872 | 2147483648 | 2147483648 |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| 2147483648 | 2147483649 | TR001_2_4 |
| 2147483649 | 2147483648 | 1071112397389843872 |

*molecule*

| molecule_id | label |
|---|---|
| 2147483648 | 2147483648 |
| 2147483649 | 2147483648 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[['2147483648']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.atom_id`: 12,333 rows, 0 NULL, 12,333 distinct values, all non-NULL values unique. Witness values: '2147483648' occurs 0x; '2147483649' occurs 0x.
- `atom.element`: 12,333 rows, 0 NULL, 21 distinct values. Witness values: NULL occurs 0x; '2147483648' occurs 0x.
- `connected.atom_id`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: '2147483648' occurs 0x; '2147483649' occurs 0x.
- `connected.atom_id2`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: '2147483649' occurs 0x; '2147483648' occurs 0x.
- `connected.bond_id`: 24,758 rows, 0 NULL, 12,379 distinct values. Witness values: 'TR001_2_4' occurs 2x; '1071112397389843872' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-039 (formula_1)

**Question:** Which year was the first Singapore Grand Prix?

**Evidence:** the first race refers to race happened in min(year);

**Gold SQL:**
```sql
SELECT year FROM races WHERE name = 'Singapore Grand Prix' ORDER BY year ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT MIN(year) AS first_singapore_gp_year FROM races WHERE name = 'Singapore Grand Prix';
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 23 | osterreichring | A1-Ring | Spielburg |
| 21 | imola | Autodromo Enzo e Dino Ferrari | Imola |
| 6 | monaco | Circuit de Monaco | Monte-Carlo |
| 17 | shanghai | Shanghai International Circuit | Shanghai |

*races* (6 unreferenced columns omitted)

| year | name |
|---|---|
| 2002 | Austrian Grand Prix |
| 1982 | San Marino Grand Prix |
| 1993 | Monaco Grand Prix |
| 2014 | Chinese Grand Prix |

*seasons*

| year | url |
|---|---|
| 2002 | http://en.wikipedia.org/wiki/2002_Formula_One_season |
| 1982 | http://en.wikipedia.org/wiki/1982_Formula_One_season |
| 1993 | http://en.wikipedia.org/wiki/1993_Formula_One_season |
| 2014 | http://en.wikipedia.org/wiki/2014_Formula_One_season |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `races.year`: 976 rows, 0 NULL, 68 distinct values. Witness values: 2002 occurs 17x; 1982 occurs 16x; 1993 occurs 16x; 2014 occurs 19x.
- `races.name`: 976 rows, 0 NULL, 42 distinct values. Witness values: 'Austrian Grand Prix' occurs 30x; 'San Marino Grand Prix' occurs 26x; 'Monaco Grand Prix' occurs 64x; 'Chinese Grand Prix' occurs 14x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-102 (formula_1)

**Question:** What's the fastest lap time ever in a race for Lewis Hamilton?

**Evidence:** fastest lap time ever refers to min(fastestLapTime)

**Gold SQL:**
```sql
SELECT T2.fastestLapTime FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId WHERE T1.forename = 'Lewis' AND T1.surname = 'Hamilton' AND T2.fastestLapTime IS NOT NULL ORDER BY T2.fastestLapTime ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT MIN(T2.fastestLapTime) FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId WHERE T1.forename = 'Lewis' AND T1.surname = 'Hamilton'
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

*drivers* (6 unreferenced columns omitted)

| driverId | forename | surname |
|---|---|---|
| 69 | Luca | Badoer |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 178 | 1999 | 4 | 6 |

*results* (16 unreferenced columns omitted)

| driverId | fastestLapTime |
|---|---|
| 69 | NULL |

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

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 69 occurs 1x.
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: 'Luca' occurs 1x.
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: 'Badoer' occurs 1x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 69 occurs 58x.
- `results.fastestLapTime`: 23,657 rows, 18,389 NULL, 4,955 distinct values. Witness values: NULL occurs 18,389x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-146 (toxicology)

**Question:** What type of bond is there between the atoms TR004_8 and TR004_20?

**Evidence:** type of bond refers to bond_type; between the atoms TR004_8 and TR004_20 refers to atom_id = 'TR004_8' AND atom_id2 = 'TR004_20' OR another way around

**Gold SQL:**
```sql
SELECT T1.bond_type FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE T2.atom_id = 'TR004_8' AND T2.atom_id2 = 'TR004_20' OR T2.atom_id2 = 'TR004_8' AND T2.atom_id = 'TR004_20'
```
**Predicted SQL:**
```sql
SELECT T1.bond_type FROM bond AS T1 INNER JOIN connected AS T2 ON T1.bond_id = T2.bond_id WHERE T2.atom_id = 'TR004_8' AND T2.atom_id2 = 'TR004_20'
```

**Witness database:**

*atom*

| atom_id | molecule_id | element |
|---|---|---|
| TR004_20 | TR004 | h |
| TR004_8 | TR004 | c |
| PH755_4 | FE515 | c |

*bond* (1 unreferenced columns omitted)

| bond_id | bond_type |
|---|---|
| TR004_8_20 | - |
| FL868_3_0 | = |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| TR004_8 | TR004_20 | TR004_8_20 |
| TR004_20 | TR004_8 | FL868_3_0 |

*molecule*

| molecule_id | label |
|---|---|
| TR004 | - |
| FE515 | - |

**Gold result on the witness:** `[['-'], ['=']]`  
**Predicted result on the witness:** `[['-']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `bond.bond_id`: 12,379 rows, 0 NULL, 12,379 distinct values, all non-NULL values unique. Witness values: 'TR004_8_20' occurs 1x; 'FL868_3_0' occurs 0x.
- `bond.bond_type`: 12,379 rows, 1 NULL, 3 distinct values. Witness values: '-' occurs 10,528x; '=' occurs 1,844x.
- `connected.atom_id`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'TR004_8' occurs 4x; 'TR004_20' occurs 1x.
- `connected.atom_id2`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'TR004_20' occurs 1x; 'TR004_8' occurs 4x.
- `connected.bond_id`: 24,758 rows, 0 NULL, 12,379 distinct values. Witness values: 'TR004_8_20' occurs 2x; 'FL868_3_0' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-143 (formula_1)

**Question:** From race no. 50 to 100, how many finishers have been disqualified?

**Evidence:** disqualified refers to statusID = 2, finisher refers to time! = null; race no. refers to raceId; raceId > 50 and raceId < 100;

**Gold SQL:**
```sql
SELECT SUM(IIF(time IS NOT NULL, 1, 0)) FROM results WHERE statusId = 2 AND raceID < 100 AND raceId > 50
```
**Predicted SQL:**
```sql
SELECT COUNT(driverId) FROM results WHERE raceId > 50 AND raceId < 100 AND time IS NOT NULL AND statusId = 2
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 1328 | y2 | a | NULL |
| 1330 | A | b | y2 |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 1310 | y2 | c | German |
| 1321 | x1 | b | NULL |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 1311 | A | 2 | NULL |
| 1322 | c | NULL | NULL |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 99 | 1327 | 3 | 1328 |
| 1323 | 1329 | 10 | 1330 |

*results* (14 unreferenced columns omitted)

| raceId | driverId | time | statusId |
|---|---|---|---|
| 99 | 1311 | NULL | 1314 |
| 1323 | 1322 | 2000-01-01 | 1326 |

*seasons*

| year | url |
|---|---|
| 1327 | b |
| 1329 | y2 |

*status*

| statusId | status |
|---|---|
| 1314 | x1 |
| 1326 | b |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 99 occurs 20x; 1323 occurs 0x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 1311 occurs 0x; 1322 occurs 0x.
- `results.time`: 23,657 rows, 17,696 NULL, 5,755 distinct values. Witness values: NULL occurs 17,696x; '2000-01-01' occurs 0x.
- `results.statusId`: 23,657 rows, 0 NULL, 132 distinct values. Witness values: 1314 occurs 0x; 1326 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-050 (card_games)

**Question:** How many cards with unknown power that can't be found in foil is in duel deck A?

**Evidence:** unknown power refers to power IS NULL or power = '*'; can't be found in foil refers to hasFoil = 0; duel deck A refers to duelDeck = 'a'

**Gold SQL:**
```sql
SELECT SUM(CASE WHEN power = '*' OR power IS NULL THEN 1 ELSE 0 END) FROM cards WHERE hasFoil = 0 AND duelDeck = 'a'
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM cards WHERE (power IS NULL OR power = '*') AND hasfoil = 0 AND dueldeck = 'a'
```

**Witness database:**

*cards* (71 unreferenced columns omitted)

| duelDeck | hasFoil | power |
|---|---|---|
| NULL | 1 | 3 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `cards.duelDeck`: 56,822 rows, 55,228 NULL, 2 distinct values. Witness values: NULL occurs 55,228x.
- `cards.hasFoil`: 56,822 rows, 0 NULL, 2 distinct values. Witness values: 1 occurs 34,618x.
- `cards.power`: 56,822 rows, 30,624 NULL, 28 distinct values. Witness values: '3' occurs 4,414x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-060 (formula_1)

**Question:** List down top 3 German drivers who has the shortest average pit stop duration and were born between 1980-1985.

**Evidence:** Full name of the driver refers to drivers.forename and drivers.surname; born between 1980-1985 refers to 1980< year(dob)>1985; Average pitstop duration refers to Divide(SUM(duration),COUNT(duration)); shortest average refers to Min(avg(duration));

**Gold SQL:**
```sql
SELECT T2.forename, T2.surname FROM pitStops AS T1 INNER JOIN drivers AS T2 on T1.driverId = T2.driverId WHERE T2.nationality = 'German' AND STRFTIME('%Y', T2.dob) BETWEEN '1980' AND '1985' GROUP BY T2.forename, T2.surname ORDER BY AVG(T1.duration) LIMIT 3
```
**Predicted SQL:**
```sql
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN pitStops AS T2 ON T1.driverId = T2.driverId WHERE T1.nationality = 'German' AND STRFTIME('%Y', T1.dob) BETWEEN '1980' AND '1985' GROUP BY T1.driverId ORDER BY AVG(STRFTIME('%s', T2.duration)) LIMIT 3
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 1272 | monaco | Circuit de Monaco | Monte-Carlo |
| 1273 | avus | AVUS | Berlin |
| 1274 | reims | Reims-Gueux | Reims |
| 1275 | zandvoort | Circuit Park Zandvoort | Zandvoort |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 34 | brabham | Brabham | British |
| 51 | alfa | Alfa Romeo | American |
| 5 | toro_rosso | Toro Rosso | Italian |

*drivers* (4 unreferenced columns omitted)

| driverId | forename | surname | dob | nationality |
|---|---|---|---|---|
| 1071 | Hans | Bianchi | 1980-01-01 | German |
| 1255 | Bill | Brown | 1980-01-01 | German |
| 1261 | Tony | Fittipaldi | 1980-01-01 | German |
| 1267 | Bob | Hill | 1980-01-01 | German |

*pitStops* (5 unreferenced columns omitted)

| driverId | duration |
|---|---|
| 1071 | 20.567 |
| 1255 | 20.567 |
| 1261 | 20.567 |
| 1267 | 20.567 |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 1072 | 1950 | 20 | 1272 |
| 1256 | 1958 | 1 | 1273 |
| 1262 | 2004 | 4 | 1274 |
| 1268 | 1978 | 17 | 1275 |

*results* (14 unreferenced columns omitted)

| resultId | raceId | driverId | constructorId |
|---|---|---|---|
| 1276 | 1072 | 1071 | 34 |
| 1277 | 1072 | 1255 | 51 |
| 1278 | 1072 | 1261 | 34 |
| 1279 | 1072 | 1267 | 5 |

*seasons*

| year | url |
|---|---|
| 1950 | http://en.wikipedia.org/wiki/1950_Formula_One_season |
| 1958 | http://en.wikipedia.org/wiki/1958_Formula_One_season |
| 2004 | http://en.wikipedia.org/wiki/2004_Formula_One_season |
| 1978 | http://en.wikipedia.org/wiki/1978_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 12 | +2 Laps |
| 4 | Collision |
| 11 | +1 Lap |

**Gold result on the witness:** `[['Bill', 'Brown'], ['Bob', 'Hill'], ['Hans', 'Bianchi']]`  
**Predicted result on the witness:** `[['Hans', 'Bianchi'], ['Bill', 'Brown'], ['Tony', 'Fittipaldi']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 1071 occurs 0x; 1255 occurs 0x; 1261 occurs 0x; 1267 occurs 0x.
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: 'Hans' occurs 5x; 'Bill' occurs 11x; 'Tony' occurs 11x; 'Bob' occurs 10x.
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: 'Bianchi' occurs 2x; 'Brown' occurs 3x; 'Fittipaldi' occurs 3x; 'Hill' occurs 3x.
- `drivers.dob`: 840 rows, 1 NULL, 821 distinct values. Witness values: '1980-01-01' occurs 0x.
- `drivers.nationality`: 840 rows, 0 NULL, 41 distinct values. Witness values: 'German' occurs 49x.
- `pitStops.driverId`: 6,070 rows, 0 NULL, 54 distinct values. Witness values: 1071 occurs 0x; 1255 occurs 0x; 1261 occurs 0x; 1267 occurs 0x.
- `pitStops.duration`: 6,070 rows, 0 NULL, 4,713 distinct values. Witness values: '20.567' occurs 4x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-067 (student_club)

**Question:** Which college do most of the members go to?

**Evidence:** college most members go refers to MAX(COUNT(major.college))

**Gold SQL:**
```sql
SELECT T2.college FROM member AS T1 INNER JOIN major AS T2 ON T1.link_to_major = T2.major_id GROUP BY T2.major_id ORDER BY COUNT(T2.college) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT college FROM major AS T1 INNER JOIN member AS T2 ON T1.major_id = T2.link_to_major GROUP BY T1.college ORDER BY COUNT(T2.member_id) DESC LIMIT 1
```

**Witness database:**

*event* (3 unreferenced columns omitted)

| event_id | event_name | event_date | type |
|---|---|---|---|
| 2147483648 | 2147483648 | 2147483648 | 2147483648 |
| 2147483649 | 2147483648 | 2147483648 | 2147483648 |

*major* (2 unreferenced columns omitted)

| major_id | college |
|---|---|
| 2147483649 | 2147483648 |
| 2147483648 | 2147483649 |

*zip_code* (2 unreferenced columns omitted)

| zip_code | type | city | county |
|---|---|---|---|
| 0 | Unique | 2147483648 | 2147483648 |
| 1 | Unique | 2147483648 | 2147483648 |

*attendance*

| link_to_event | link_to_member |
|---|---|
| 2147483648 | 2147483649 |
| 2147483649 | 2147483649 |

*budget* (3 unreferenced columns omitted)

| budget_id | category | spent | remaining |
|---|---|---|---|
| 2147483648 | 2147483648 | 0 | 0 |
| 2147483649 | 2147483648 | 0 | 0 |

*expense* (3 unreferenced columns omitted)

| expense_id | expense_description | expense_date | cost |
|---|---|---|---|
| 2147483648 | 2147483648 | 2147483648 | 0 |
| 2147483649 | 2147483648 | 2147483648 | 0 |

*income* (2 unreferenced columns omitted)

| income_id | date_received | amount | source |
|---|---|---|---|
| 2147483649 | 2147483648 | 0 | 2147483648 |
| 2147483648 | 2147483648 | 0 | 2147483648 |

*member* (7 unreferenced columns omitted)

| member_id | link_to_major |
|---|---|
| 2147483648 | 2147483648 |
| 2147483649 | 2147483649 |

**Gold result on the witness:** `[['2147483648']]`  
**Predicted result on the witness:** `[['2147483649']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `major.major_id`: 113 rows, 0 NULL, 113 distinct values, all non-NULL values unique. Witness values: '2147483649' occurs 0x; '2147483648' occurs 0x.
- `major.college`: 113 rows, 0 NULL, 8 distinct values. Witness values: '2147483648' occurs 0x; '2147483649' occurs 0x.
- `member.member_id`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: '2147483648' occurs 0x; '2147483649' occurs 0x.
- `member.link_to_major`: 33 rows, 1 NULL, 26 distinct values. Witness values: '2147483648' occurs 0x; '2147483649' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-121 (card_games)

**Question:** For all the set of cards that has Brazil Portuguese translation, what is the percentage of them are only available online?

**Evidence:** Brazil Portuguese translation refers to language = 'Portuguese (Brazil)'; only available online refers to isOnlineOnly = 1; percentage of online only Brazil Portuguese in all Brazil Portuguese cards refers to DIVIDE(SUM(isOnlineOnly = 1), SUM(language = 'Portuguese (Brazil)))*100

**Gold SQL:**
```sql
SELECT CAST(SUM(CASE WHEN isOnlineOnly = 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(id) FROM sets WHERE code IN ( SELECT setCode FROM set_translations WHERE language = 'Portuguese (Brazil)' )
```
**Predicted SQL:**
```sql
SELECT CAST(SUM(CASE WHEN T1.isOnlineOnly = 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) FROM sets AS T1 INNER JOIN set_translations AS T2 ON T1.code = T2.setCode WHERE T2.language = 'Portuguese (Brazil)'
```

**Witness database:**

*set_translations* (2 unreferenced columns omitted)

| language | setCode |
|---|---|
| Portuguese (Brazil) | k2 |
| Portuguese (Brazil) | k1 |
| Portuguese (Brazil) | k1 |

*sets* (18 unreferenced columns omitted)

| id | code | isOnlineOnly |
|---|---|---|
| 100 | k1 | 3 |
| 0 | 0 | 0 |
| 1 | k2 | 1 |

**Gold result on the witness:** `[[50.0]]`  
**Predicted result on the witness:** `[[33.333333333333336]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `set_translations.language`: 1,210 rows, 0 NULL, 10 distinct values. Witness values: 'Portuguese (Brazil)' occurs 121x.
- `set_translations.setCode`: 1,210 rows, 0 NULL, 121 distinct values. Witness values: 'k2' occurs 0x; 'k1' occurs 0x.
- `sets.id`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 100 occurs 1x; 0 occurs 0x; 1 occurs 1x.
- `sets.code`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 'k1' occurs 0x; '0' occurs 0x; 'k2' occurs 0x.
- `sets.isOnlineOnly`: 551 rows, 0 NULL, 2 distinct values. Witness values: 3 occurs 0x; 0 occurs 525x; 1 occurs 26x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-004 (toxicology)

**Question:** Name chemical elements that form a bond TR001_10_11.

**Evidence:** element = 'cl' means Chlorine; element = 'c' means Carbon; element = 'h' means Hydrogen; element = 'o' means Oxygen, element = 's' means Sulfur; element = 'n' means Nitrogen, element = 'p' means Phosphorus, element = 'na' means Sodium, element = 'br' means Bromine, element = 'f' means Fluorine; element = 'i' means Iodine; element = 'sn' means Tin; element = 'pb' means Lead; element = 'te' means Tellurium; element = 'ca' means Calcium; TR001_10_11 is the bond id; molecule id refers to SUBSTR(bond_id, 1, 5); atom 1 refers to SUBSTR(bond_id, 7, 2); atom 2 refers to SUBSTR(bond_id, 10, 2)

**Gold SQL:**
```sql
SELECT T1.element FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id INNER JOIN bond AS T3 ON T2.bond_id = T3.bond_id WHERE T3.bond_id = 'TR001_10_11'
```
**Predicted SQL:**
```sql
SELECT DISTINCT a.element FROM atom a JOIN connected c ON a.atom_id IN (c.atom_id, c.atom_id2) WHERE c.bond_id = 'TR001_10_11';
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| atom_id | element |
|---|---|
| v1001 | A |
| v1044 | a |

*bond* (2 unreferenced columns omitted)

| bond_id |
|---|
| TR001_10_11 |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| v1001 | v1001 | TR001_10_11 |
| v1001 | v1044 | TR001_10_11 |

*molecule*

| molecule_id | label |
|---|---|
| v1002 | + |
| v1045 | + |

**Gold result on the witness:** `[['A'], ['A']]`  
**Predicted result on the witness:** `[['A'], ['a']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.atom_id`: 12,333 rows, 0 NULL, 12,333 distinct values, all non-NULL values unique. Witness values: 'v1001' occurs 0x; 'v1044' occurs 0x.
- `atom.element`: 12,333 rows, 0 NULL, 21 distinct values. Witness values: 'A' occurs 0x; 'a' occurs 0x.
- `bond.bond_id`: 12,379 rows, 0 NULL, 12,379 distinct values, all non-NULL values unique. Witness values: 'TR001_10_11' occurs 1x.
- `connected.atom_id`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'v1001' occurs 0x.
- `connected.atom_id2`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'v1001' occurs 0x; 'v1044' occurs 0x.
- `connected.bond_id`: 24,758 rows, 0 NULL, 12,379 distinct values. Witness values: 'TR001_10_11' occurs 2x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-017 (formula_1)

**Question:** How much faster in percentage is the champion than the driver who finished the race last in the 2008 Australian Grand Prix?

**Evidence:** how much faster in percentage = divide(subtract(incremental time, champion time), last_driver time) * 100; last driver finished time = incremental time + champion time; only champion's finished time is represented by 'HH:MM:SS.mmm'; finished the game refers to time is not null

**Gold SQL:**
```sql
WITH time_in_seconds AS ( SELECT T1.positionOrder, CASE WHEN T1.positionOrder = 1 THEN (CAST(SUBSTR(T1.time, 1, 1) AS REAL) * 3600) + (CAST(SUBSTR(T1.time, 3, 2) AS REAL) * 60) + CAST(SUBSTR(T1.time, 6) AS REAL) ELSE CAST(SUBSTR(T1.time, 2) AS REAL) END AS time_seconds FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T2.name = 'Australian Grand Prix' AND T1.time IS NOT NULL AND T2.year = 2008 ), champion_time AS ( SELECT time_seconds FROM time_in_seconds WHERE positionOrder = 1), last_driver_incremental AS ( SELECT time_seconds FROM time_in_seconds WHERE positionOrder = (SELECT MAX(positionOrder) FROM time_in_seconds) ) SELECT (CAST((SELECT time_seconds FROM last_driver_incremental) AS REAL) * 100) / (SELECT time_seconds + (SELECT time_seconds FROM last_driver_incremental) FROM champion_time)
```
**Predicted SQL:**
```sql
SELECT CAST((MAX(r1.milliseconds) - (SUBSTRING(r2.time, 1, INSTR(r2.time, ':') - 1) * 3600000 + SUBSTRING(r2.time, INSTR(r2.time, ':') + 1, INSTR(r2.time, '.') - INSTR(r2.time, ':') - 1) * 60000 + SUBSTRING(r2.time, INSTR(r2.time, '.') - 2, 3) * 1000 + SUBSTRING(r2.time, INSTR(r2.time, '.') + 1))) AS REAL) * 100 / MAX(r1.milliseconds) AS percentage_difference FROM results AS r1 INNER JOIN races ON r1.raceid = races.raceid INNER JOIN results AS r2 ON r1.raceid = r2.raceid WHERE races.name = 'Australian Grand Prix' AND races.year = 2008 AND r2.time LIKE '%:%'
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 3 | 3600000 | a | NULL |
| 1 | 6 | %:% | b |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 1 | 100 | : | French |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 2 | Australian Grand Prix | 1 | a |
| 3 | c | 3600000 | 1 |
| 60000 | x1 | NULL | 2008 |

*races* (5 unreferenced columns omitted)

| raceId | year | name |
|---|---|---|
| 6 | 100 | x1 |
| 2 | 2008 | Australian Grand Prix |
| 1 | 60 | 3600 |
| 3 | 100 | 6 |

*results* (14 unreferenced columns omitted)

| raceId | positionOrder | time | milliseconds |
|---|---|---|---|
| 3 | 1000 | 2000-01-01 | 5 |
| 2 | 10 | 2010-06-15 00:00:00 | 10 |
| 1 | 2008 | 2012-02-22 00:00:00 | 3 |

*seasons*

| year | url |
|---|---|
| 100 | 60 |
| 2008 | 2008 |
| 60 | y2 |

*status*

| statusId | status |
|---|---|
| 2 | 2008 |
| 1 | b |
| 3 | x1 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[-73566020000.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 6 occurs 1x; 2 occurs 1x; 1 occurs 1x; 3 occurs 1x.
- `races.year`: 976 rows, 0 NULL, 68 distinct values. Witness values: 100 occurs 0x; 2008 occurs 18x; 60 occurs 0x.
- `races.name`: 976 rows, 0 NULL, 42 distinct values. Witness values: 'x1' occurs 0x; 'Australian Grand Prix' occurs 33x; '3600' occurs 0x; '6' occurs 0x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 3 occurs 20x; 2 occurs 20x; 1 occurs 20x.
- `results.positionOrder`: 23,657 rows, 0 NULL, 39 distinct values. Witness values: 1000 occurs 0x; 10 occurs 975x; 2008 occurs 0x.
- `results.time`: 23,657 rows, 17,696 NULL, 5,755 distinct values. Witness values: '2000-01-01' occurs 0x; '2010-06-15 00:00:00' occurs 0x; '2012-02-22 00:00:00' occurs 0x.
- `results.milliseconds`: 23,657 rows, 17,697 NULL, 5,923 distinct values. Witness values: 5 occurs 0x; 10 occurs 0x; 3 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-122 (financial)

**Question:** Among the accounts who have loan validity more than 24 months, list out the accounts that have the lowest approved amount and have account opening date before 1997.

**Evidence:** -

**Gold SQL:**
```sql
SELECT T1.account_id FROM loan AS T1 INNER JOIN account AS T2 ON T1.account_id = T2.account_id WHERE T1.duration > 24 AND STRFTIME('%Y', T2.date) < '1997' ORDER BY T1.amount ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT t1.account_id FROM account AS t1 INNER JOIN loan AS t2 ON t1.account_id = t2.account_id WHERE t2.duration > 24 AND STRFTIME('%Y', t1.date) < '1997' AND t2.amount = (SELECT MIN(amount) FROM loan WHERE duration > 24 AND account_id IN (SELECT account_id FROM account WHERE STRFTIME('%Y', date) < '1997'))
```

**Witness database:**

*account* (2 unreferenced columns omitted)

| account_id | date |
|---|---|
| 2 | 2010-06-15 |
| 1 | 1995-12-31 |
| 3 | 2015-03-20 |
| 24 | 1995-12-31 |

*district* (12 unreferenced columns omitted)

| district_id | A2 | A3 | A4 |
|---|---|---|---|
| 1 | %Y | north Bohemia | %Y |
| 2 | a | south Bohemia | %Y |

*loan* (4 unreferenced columns omitted)

| account_id | amount | duration |
|---|---|---|
| 3 | 1 | 10 |
| 1 | 1 | 1997 |
| 24 | 1 | 1997 |

**Gold result on the witness:** `[[24]]`  
**Predicted result on the witness:** `[[24], [1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `account.account_id`: 4,500 rows, 0 NULL, 4,500 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 1 occurs 1x; 3 occurs 1x; 24 occurs 1x.
- `account.date`: 4,500 rows, 0 NULL, 1,535 distinct values. Witness values: '2010-06-15' occurs 0x; '1995-12-31' occurs 0x; '2015-03-20' occurs 0x.
- `loan.account_id`: 682 rows, 0 NULL, 682 distinct values, all non-NULL values unique. Witness values: 3 occurs 0x; 1 occurs 0x; 24 occurs 0x.
- `loan.amount`: 682 rows, 0 NULL, 645 distinct values. Witness values: 1 occurs 0x.
- `loan.duration`: 682 rows, 0 NULL, 5 distinct values. Witness values: 10 occurs 0x; 1997 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-095 (thrombosis_prediction)

**Question:** For the patient who first came to the hospital on 1991/6/13 who was diagnosed with SJS, what is the total number of his/her Laboratory tests in 1995?

**Evidence:** 1991/6/13 refers to `First Date` = '1991-06-13'; 'SJS' refers to Diagnosis; total number of his/her Laboratory tests refers to COUNT(ID); 1995 refers to Date

**Gold SQL:**
```sql
SELECT COUNT(*) FROM Laboratory WHERE ID = ( SELECT ID FROM Patient WHERE `First Date` = '1991-06-13' AND Diagnosis = 'SJS' ) AND STRFTIME('%Y', Date) = '1995'
```
**Predicted SQL:**
```sql
SELECT COUNT(`laboratory`.`id`) FROM `patient` INNER JOIN `laboratory` ON `patient`.`id` = `laboratory`.`id` WHERE `patient`.`first date` = '1991-06-13' AND `patient`.`diagnosis` = 'SJS' AND strftime('%Y', `laboratory`.`date`) = '1995'
```

**Witness database:**

*Laboratory* (42 unreferenced columns omitted)

| ID | Date |
|---|---|
| 4634342 | 1995-02-02 |
| 4634342 | 1995-03-30 |
| 1006 | 1995-02-02 |
| 1006 | 1995-03-30 |

*Patient* (4 unreferenced columns omitted)

| ID | First Date | Diagnosis |
|---|---|---|
| 4634342 | 1991-06-13 | SJS |
| 1006 | 1991-06-13 | SJS |

**Gold result on the witness:** `[[2]]`  
**Predicted result on the witness:** `[[4]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 4634342 occurs 96x; 1006 occurs 0x.
- `Laboratory.Date`: 13,908 rows, 0 NULL, 3,723 distinct values. Witness values: '1995-02-02' occurs 4x; '1995-03-30' occurs 4x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 4634342 occurs 1x; 1006 occurs 0x.
- `Patient.First Date`: 1,238 rows, 251 NULL, 797 distinct values. Witness values: '1991-06-13' occurs 1x.
- `Patient.Diagnosis`: 1,238 rows, 0 NULL, 220 distinct values. Witness values: 'SJS' occurs 160x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-034 (superhero)

**Question:** Calculate the average attribute value of all neutral superheroes.

**Evidence:** average = AVG(attribute_value); neutral superheroes refers to alignment_id = 3;

**Gold SQL:**
```sql
SELECT AVG(T1.attribute_value) FROM hero_attribute AS T1 INNER JOIN superhero AS T2 ON T1.hero_id = T2.id INNER JOIN alignment AS T3 ON T2.alignment_id = T3.id WHERE T3.alignment = 'Neutral'
```
**Predicted SQL:**
```sql
SELECT AVG(hero_attribute.attribute_value) FROM superhero INNER JOIN hero_attribute ON superhero.id = hero_attribute.hero_id WHERE superhero.alignment_id = 3
```

**Witness database:**

*alignment*

| id | alignment |
|---|---|
| 3 | N/A |

*attribute*

| id | attribute_name |
|---|---|
| 1 | Speed |

*colour*

| id | colour |
|---|---|
| 1 | 2147483648 |

*gender*

| id | gender |
|---|---|
| 1 | Male |

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

*hero_attribute* (1 unreferenced columns omitted)

| hero_id | attribute_value |
|---|---|
| 1 | 0 |

*superpower*

| id | power_name |
|---|---|
| 1 | 2147483648 |

*hero_power*

| hero_id | power_id |
|---|---|
| 1 | 1 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[0.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `alignment.id`: 4 rows, 0 NULL, 4 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x.
- `alignment.alignment`: 4 rows, 0 NULL, 4 distinct values, all non-NULL values unique. Witness values: 'N/A' occurs 1x.
- Real content of `alignment` (4 rows; referenced columns): (1, 'Good'); (2, 'Bad'); (3, 'Neutral'); (4, 'N/A').
- `superhero.id`: 750 rows, 0 NULL, 750 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x.
- `superhero.alignment_id`: 750 rows, 6 NULL, 3 distinct values. Witness values: 3 occurs 28x.
- `hero_attribute.hero_id`: 3,738 rows, 0 NULL, 623 distinct values. Witness values: 1 occurs 6x.
- `hero_attribute.attribute_value`: 3,738 rows, 0 NULL, 20 distinct values. Witness values: 0 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-140 (european_football_2)

**Question:** Please name one player whose overall strength is the greatest.

**Evidence:** overall strength is the greatest refers to MAX(overall_rating)

**Gold SQL:**
```sql
SELECT DISTINCT t1.player_name FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t2.overall_rating = ( SELECT MAX(overall_rating) FROM Player_Attributes)
```
**Predicted SQL:**
```sql
SELECT T2.player_name FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_fifa_api_id = T2.player_fifa_api_id ORDER BY T1.overall_rating DESC LIMIT 1
```

**Witness database:**

*Player* (4 unreferenced columns omitted)

| player_api_id | player_name | player_fifa_api_id |
|---|---|---|
| 1 | Kiko | 185 |
| 2805 | Jorginho | 61 |
| 24852 | Luis Garcia | 16 |
| 38880 | Ross Wallace | 140497 |
| 26332 | Moussa Sow | 172124 |
| 102719 | Stefan Nijland | 184635 |
| 100 | Paulinho | 1 |
| 36286 | Uros Korun | 229666 |
| 38243 | Sekou Ouattara | 164430 |

*Player_Attributes* (39 unreferenced columns omitted)

| player_fifa_api_id | player_api_id | overall_rating |
|---|---|---|
| 1 | 100 | 78 |
| 16 | 24852 | 58 |
| 140497 | 38880 | 78 |
| 185 | 1 | 65 |
| 61 | 2805 | 66 |
| 172124 | 26332 | 78 |
| 184635 | 102719 | 69 |
| 16 | 24852 | 69 |
| 140497 | 38880 | 69 |
| 229666 | 36286 | 75 |
| 164430 | 38243 | 73 |
| 185 | 1 | 76 |

**Gold result on the witness:** `[['Paulinho'], ['Ross Wallace'], ['Moussa Sow']]`  
**Predicted result on the witness:** `[['Paulinho']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 2805 occurs 1x; 24852 occurs 1x; 38880 occurs 1x; 26332 occurs 1x; 102719 occurs 1x (+3 more).
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'Kiko' occurs 3x; 'Jorginho' occurs 3x; 'Luis Garcia' occurs 2x; 'Ross Wallace' occurs 1x; 'Moussa Sow' occurs 1x; 'Stefan Nijland' occurs 1x (+3 more).
- `Player.player_fifa_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 185 occurs 1x; 61 occurs 1x; 16 occurs 1x; 140497 occurs 1x; 172124 occurs 1x; 184635 occurs 1x (+3 more).
- `Player_Attributes.player_fifa_api_id`: 183,978 rows, 0 NULL, 11,062 distinct values. Witness values: 1 occurs 0x; 16 occurs 16x; 140497 occurs 24x; 185 occurs 11x; 61 occurs 9x; 172124 occurs 18x (+3 more).
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 100 occurs 0x; 24852 occurs 16x; 38880 occurs 24x; 1 occurs 0x; 2805 occurs 28x; 26332 occurs 18x (+3 more).
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: 78 occurs 4,064x; 58 occurs 2,950x; 65 occurs 9,336x; 66 occurs 10,112x; 69 occurs 10,281x; 75 occurs 7,359x (+2 more).

**Verdict:** ____  
**Reason (one sentence):** 

---

## Item R3-061 (financial)

**Question:** In the branch where the second-highest number of crimes were committed in 1995 occurred, how many male clients are there?

**Evidence:** Male refers to gender = 'M'; A15 stands for no. of commited crimes 1995

**Gold SQL:**
```sql
SELECT COUNT(T1.client_id) FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.gender = 'M' AND T2.A15 = (SELECT T3.A15 FROM district AS T3 ORDER BY T3.A15 DESC LIMIT 1, 1)
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM client c JOIN district d ON c.district_id = d.district_id WHERE c.gender = 'M' AND d.district_id IN ( SELECT district_id FROM district ORDER BY A15 DESC LIMIT 1 OFFSET 1 )
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

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `client.client_id`: 5,369 rows, 0 NULL, 5,369 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 2 occurs 1x; 3931 occurs 1x; 780 occurs 1x; 1299 occurs 1x; 1968 occurs 1x (+1 more).
- `client.gender`: 5,369 rows, 0 NULL, 2 distinct values. Witness values: 'F' occurs 2,645x; 'M' occurs 2,724x.
- `client.district_id`: 5,369 rows, 0 NULL, 77 distinct values. Witness values: 3 occurs 63x; 2 occurs 46x; 1 occurs 663x; 18 occurs 60x.
- `district.district_id`: 77 rows, 0 NULL, 77 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x; 2 occurs 1x; 1 occurs 1x; 18 occurs 1x.
- `district.A15`: 77 rows, 1 NULL, 75 distinct values. Witness values: 1845 occurs 1x; 1740 occurs 1x; 1003 occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 
