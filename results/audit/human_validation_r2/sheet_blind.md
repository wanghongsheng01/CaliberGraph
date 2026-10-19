# Human attribution sheet, round 2 (blind)

For each item, read the question, evidence, both queries, the witness database, the two results and the facts from the real database, then replace `____` after **Verdict:** with exactly one of: `pred_wrong`, `gold_wrong`, `both_wrong`, `ambiguous`, `implausible_data`. See INSTRUCTIONS.md. Do not consult any other file of the repository while annotating.


---

## Item 1 (card_games)

**Question:** How many cards did Volkan BaÇµa illustrated whose foreign language is in French?

**Evidence:** Volkan BaÇµa refers to artist = 'Volkan Baǵa'; foreign language is in French refers to language = 'French'

**Gold SQL:**
```sql
SELECT COUNT(T3.id) FROM ( SELECT T1.id FROM cards AS T1 INNER JOIN foreign_data AS T2 ON T2.uuid = T1.uuid WHERE T1.artist = 'Volkan Baǵa' AND T2.language = 'French' GROUP BY T1.id ) AS T3
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM cards INNER JOIN foreign_data ON cards.uuid = foreign_data.uuid WHERE cards.artist = 'Volkan Baǵa' AND foreign_data.language = 'French';
```

**Witness database:**

*cards* (71 unreferenced columns omitted)

| id | artist | uuid |
|---|---|---|
| 1 | Volkan Baǵa | a |
| 47 | Volkan Baǵa | aa |
| 84 | Volkan Baǵa | gd |

*foreign_data* (6 unreferenced columns omitted)

| language | uuid |
|---|---|
| French | a |
| French | a |
| French | a |
| French | aa |
| French | NULL |
| German | gd |
| NULL | a |

**Gold result on the witness:** `[[2]]`  
**Predicted result on the witness:** `[[4]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `cards.id`: 56,822 rows, 0 NULL, 56,822 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 47 occurs 1x; 84 occurs 1x.
- `cards.artist`: 56,822 rows, 3 NULL, 991 distinct values. Witness values: 'Volkan Baǵa' occurs 350x.
- `cards.uuid`: 56,822 rows, 0 NULL, 56,822 distinct values, all non-NULL values unique. Witness values: 'a' occurs 0x; 'aa' occurs 0x; 'gd' occurs 0x.
- `foreign_data.language`: 229,186 rows, 0 NULL, 16 distinct values. Witness values: 'French' occurs 29,301x; 'German' occurs 28,891x; NULL occurs 0x.
- `foreign_data.uuid`: 229,186 rows, 0 NULL, 34,056 distinct values. Witness values: 'a' occurs 0x; 'aa' occurs 0x; NULL occurs 0x; 'gd' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 2 (financial)

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
| 3 | 1993-02-27 |
| 2 | 1997-08-08 |
| 1 | 1995-09-05 |
| 8628 | 1996-10-15 |
| 269 | 1996-08-30 |
| 3250 | 1995-01-06 |
| 2345 | 1993-10-25 |
| 1049 | 1997-12-04 |
| 5735 | 1995-01-25 |

*client*

| client_id | gender | birth_date | district_id |
|---|---|---|---|
| 10639 | M | 1954-01-29 | 2 |
| 325 | M | 1960-02-21 | 3 |
| 3931 | F | 1921-10-15 | 1 |
| 4 | M | 1956-12-01 | 5 |
| 2 | M | 1945-02-04 | 1 |
| 1 | F | 1970-12-13 | 18 |
| 2834 | M | 1949-05-23 | 52 |
| 1259 | M | 1966-09-29 | 18 |
| 6936 | F | 1959-02-27 | 52 |

*disp*

| disp_id | client_id | account_id | type |
|---|---|---|---|
| 10331 | 10639 | 8628 | OWNER |
| 325 | 325 | 269 | OWNER |
| 3931 | 3931 | 3250 | DISPONENT |
| 4 | 4 | 3 | OWNER |
| 2 | 2 | 2 | OWNER |
| 1 | 1 | 1 | OWNER |
| 2834 | 2834 | 2345 | OWNER |
| 1259 | 1259 | 1049 | OWNER |
| 6936 | 6936 | 5735 | OWNER |

*district* (12 unreferenced columns omitted)

| district_id | A2 | A3 | A4 |
|---|---|---|---|
| 2 | Benesov | central Bohemia | 88884 |
| 3 | Beroun | central Bohemia | 75232 |
| 1 | Hl.m. Praha | Prague | 1204953 |
| 5 | Kolin | central Bohemia | 95616 |
| 18 | Pisek | south Bohemia | 70699 |
| 52 | Usti nad Orlici | east Bohemia | 139012 |

*loan* (4 unreferenced columns omitted)

| account_id | amount | duration |
|---|---|---|
| 1 | 230220 | 60 |
| 3 | 230220 | 36 |
| 2 | 192744 | 12 |

*trans* (6 unreferenced columns omitted)

| trans_id | account_id | date | type |
|---|---|---|---|
| 938 | 3 | 1997-12-28 | VYDAJ |
| 3530535 | 2 | 1997-07-31 | PRIJEM |
| 3530463 | 1 | 1997-05-31 | PRIJEM |
| 2611775 | 8628 | 1997-01-05 | VYDAJ |
| 80278 | 269 | 1998-03-06 | VYDAJ |
| 3638005 | 3250 | 1997-04-30 | PRIJEM |
| 687051 | 2345 | 1997-07-06 | VYDAJ |
| 307733 | 1049 | 1998-09-30 | VYDAJ |
| 1692040 | 5735 | 1998-12-01 | VYDAJ |

**Gold result on the witness:** `[[3]]`  
**Predicted result on the witness:** `[[3], [1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `account.account_id`: 4,500 rows, 0 NULL, 4,500 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x; 2 occurs 1x; 1 occurs 1x; 8628 occurs 1x; 269 occurs 1x; 3250 occurs 1x (+3 more).
- `account.date`: 4,500 rows, 0 NULL, 1,535 distinct values. Witness values: '1993-02-27' occurs 10x; '1997-08-08' occurs 10x; '1995-09-05' occurs 4x; '1996-10-15' occurs 5x; '1996-08-30' occurs 8x; '1995-01-06' occurs 4x (+3 more).
- `loan.account_id`: 682 rows, 0 NULL, 682 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 3 occurs 0x; 2 occurs 1x.
- `loan.amount`: 682 rows, 0 NULL, 645 distinct values. Witness values: 230220 occurs 2x; 192744 occurs 2x.
- `loan.duration`: 682 rows, 0 NULL, 5 distinct values. Witness values: 60 occurs 145x; 36 occurs 130x; 12 occurs 131x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 3 (european_football_2)

**Question:** State the name of the most strongest player.

**Evidence:** strongest players refers to player has MAX(overall_rating)

**Gold SQL:**
```sql
SELECT DISTINCT t1.player_name FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t2.overall_rating = (SELECT MAX(overall_rating) FROM Player_Attributes)
```
**Predicted SQL:**
```sql
SELECT p.player_name FROM Player p JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id WHERE pa.overall_rating = (SELECT MAX(overall_rating) FROM Player_Attributes) LIMIT 1;
```

**Witness database:**

*Player_Attributes* (40 unreferenced columns omitted)

| player_api_id | overall_rating |
|---|---|
| 1 | 2 |
| 43 | 2 |
| 85 | 86 |
| 98 | 86 |
| NULL | 2 |
| 43 | 2 |
| 159 | 86 |
| 98 | 86 |
| 193 | NULL |
| 205 | NULL |
| 85 | 2 |
| 98 | 2 |

*Player* (5 unreferenced columns omitted)

| player_api_id | player_name |
|---|---|
| 1 | a |
| 78 | g |
| 82 | i |
| 85 | k |
| NULL | a |
| 159 | o |
| 193 | q |
| 85 | NULL |

**Gold result on the witness:** `[[None], ['k'], ['o']]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 1 occurs 0x; 43 occurs 0x; 85 occurs 0x; 98 occurs 0x; NULL occurs 0x; 159 occurs 0x (+2 more).
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: 2 occurs 0x; 86 occurs 456x; NULL occurs 836x.
- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 78 occurs 0x; 82 occurs 0x; 85 occurs 0x; NULL occurs 0x; 159 occurs 0x (+1 more).
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'a' occurs 0x; 'g' occurs 0x; 'i' occurs 0x; 'k' occurs 0x; 'o' occurs 0x; 'q' occurs 0x (+1 more).

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 4 (formula_1)

**Question:** Name the driver with the most winning. Mention his nationality and what is his maximum point scores.

**Evidence:** Full name of the driver refers to drivers.forename and drivers.surname; the most winning refers to MAX(COUNT(wins)); average point scores refers to MAX(points);

**Gold SQL:**
```sql
SELECT T1.forename, T1.surname, T1.nationality, MAX(T2.points) FROM drivers AS T1 INNER JOIN driverStandings AS T2 ON T2.driverId = T1.driverId WHERE T2.wins >= 1 GROUP BY T1.forename, T1.surname, T1.nationality ORDER BY COUNT(T2.wins) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.forename, T1.surname, T1.nationality, MAX(T2.points) FROM drivers AS T1 JOIN driverStandings AS T2 ON T1.driverid = T2.driverid GROUP BY T1.driverid ORDER BY SUM(T2.wins) DESC LIMIT 1
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

*drivers* (5 unreferenced columns omitted)

| driverId | forename | surname | nationality |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | 2147483648 |

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

*driverStandings* (4 unreferenced columns omitted)

| driverId | points | wins |
|---|---|---|
| 1 | 0 | 0 |

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

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2147483648', '2147483648', '2147483648', 0.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x.
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: '2147483648' occurs 0x.
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: '2147483648' occurs 0x.
- `drivers.nationality`: 840 rows, 0 NULL, 41 distinct values. Witness values: '2147483648' occurs 0x.
- `driverStandings.driverId`: 31,578 rows, 0 NULL, 833 distinct values. Witness values: 1 occurs 201x.
- `driverStandings.points`: 31,578 rows, 0 NULL, 337 distinct values. Witness values: 0 occurs 16,007x.
- `driverStandings.wins`: 31,578 rows, 0 NULL, 14 distinct values. Witness values: 0 occurs 27,946x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 5 (european_football_2)

**Question:** Among the players whose preferred foot was the left foot when attacking, how many of them would remain in his position when the team attacked?

**Evidence:** preferred foot when attacking was the left refers to preferred_foot = 'left'; players who would remain in his position when the team attacked refers to attacking_work_rate = 'low';

**Gold SQL:**
```sql
SELECT COUNT(player_api_id) FROM Player_Attributes WHERE preferred_foot = 'left' AND attacking_work_rate = 'low'
```
**Predicted SQL:**
```sql
SELECT COUNT(id) FROM player_attributes WHERE preferred_foot = 'left' AND attacking_work_rate = 'low'
```

**Witness database:**

*Player* (3 unreferenced columns omitted)

| id | player_api_id | player_name | player_fifa_api_id |
|---|---|---|---|
| 1003 | NULL | NULL | 100 |

*Player_Attributes* (38 unreferenced columns omitted)

| id | player_api_id | preferred_foot | attacking_work_rate |
|---|---|---|---|
| 1002 | NULL | left | low |

**Gold result on the witness:** `[[0]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player_Attributes.id`: 183,978 rows, 0 NULL, 183,978 distinct values, all non-NULL values unique. Witness values: 1002 occurs 1x.
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: NULL occurs 0x.
- `Player_Attributes.preferred_foot`: 183,978 rows, 836 NULL, 2 distinct values. Witness values: 'left' occurs 44,733x.
- `Player_Attributes.attacking_work_rate`: 183,978 rows, 3,230 NULL, 8 distinct values. Witness values: 'low' occurs 8,569x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 6 (codebase_community)

**Question:** When did 'chl' cast its first vote in a post?

**Evidence:** DisplayName = 'chl'; cast its first vote refers to MIN(CreationDate);

**Gold SQL:**
```sql
SELECT T2.CreationDate FROM users AS T1 INNER JOIN votes AS T2 ON T1.Id = T2.UserId WHERE T1.DisplayName = 'chl' ORDER BY T2.CreationDate LIMIT 1
```
**Predicted SQL:**
```sql
SELECT MIN(votes.CreationDate) AS FirstVoteDate FROM users INNER JOIN votes ON users.Id = votes.UserId WHERE users.DisplayName = 'chl';
```

**Witness database:**

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 1775 | 5 | 732 | 353bc74d-64f3-458c-84b0-452cdcdb0646 |

*posts* (17 unreferenced columns omitted)

| Id | PostTypeId | AcceptedAnswerId | CreaionDate |
|---|---|---|---|
| 732 | 2 | NULL | 2010-07-27 06:51:24.0 |

*users* (12 unreferenced columns omitted)

| Id | DisplayName |
|---|---|
| 223 | robin girard |
| 251 | ars |
| 380 | Jonik |

*votes* (4 unreferenced columns omitted)

| CreationDate | UserId |
|---|---|
| 2011-01-14 | NULL |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 223 occurs 1x; 251 occurs 1x; 380 occurs 1x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: 'robin girard' occurs 1x; 'ars' occurs 1x; 'Jonik' occurs 1x.
- `votes.CreationDate`: 38,930 rows, 0 NULL, 287 distinct values. Witness values: '2011-01-14' occurs 121x.
- `votes.UserId`: 38,930 rows, 35,505 NULL, 509 distinct values. Witness values: NULL occurs 35,505x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 7 (thrombosis_prediction)

**Question:** Which is the youngest patient with an abnormal anti-ribonuclear protein level? Please list his or her date of birth.

**Evidence:** youngest patient refers to MAX(Birthday); abnormal anti-ribonuclear protein level refers to RNP NOT IN('-', '+-'); date of birth refers to Birthday;

**Gold SQL:**
```sql
SELECT T1.Birthday FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.RNP != '-' OR '+-' ORDER BY T1.Birthday DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT P.Birthday FROM Patient AS P INNER JOIN Laboratory AS L ON P.ID = L.ID WHERE L.RNP NOT IN ('-', '+-') ORDER BY P.Birthday DESC LIMIT 1;
```

**Witness database:**

*Examination* (9 unreferenced columns omitted)

| ID | Examination Date | aCL IgG | aCL IgM |
|---|---|---|---|
| 0 | 1000-01-01 | 0 | 0 |

*Patient* (5 unreferenced columns omitted)

| ID | Birthday |
|---|---|
| 0 | 1000-01-01 |

*Laboratory* (42 unreferenced columns omitted)

| ID | RNP |
|---|---|
| 0 | +- |

**Gold result on the witness:** `[['1000-01-01']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x.
- `Patient.Birthday`: 1,238 rows, 1 NULL, 1,193 distinct values. Witness values: '1000-01-01' occurs 0x.
- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 0 occurs 0x.
- `Laboratory.RNP`: 13,908 rows, 13,765 NULL, 8 distinct values. Witness values: '+-' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 8 (formula_1)

**Question:** As of the present, what is the full name of the youngest racer? Indicate her nationality and the name of the race to which he/she first joined.

**Evidence:** full name refers to forename+surname; Youngest racer = MAX(dob)

**Gold SQL:**
```sql
SELECT T1.forename, T1.surname, T1.nationality, T3.name FROM drivers AS T1 INNER JOIN driverStandings AS T2 on T1.driverId = T2.driverId INNER JOIN races AS T3 on T2.raceId = T3.raceId ORDER BY JULIANDAY(T1.dob) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.forename, T1.surname, T1.nationality, T3.name FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T2.raceId = T3.raceId WHERE T1.dob = ( SELECT MAX(dob) FROM drivers ) LIMIT 1
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 30 | kyalami | Kyalami | Midrand |
| 45 | jarama | Jarama | Madrid |
| 20 | nurburgring | Nürburgring | Nürburg |
| 22 | suzuka | Suzuka Circuit | Suzuka |
| 26 | jerez | Circuito de Jerez | Jerez de la Frontera |
| 7 | villeneuve | Circuit Gilles Villeneuve | Montreal |
| 23 | osterreichring | A1-Ring | Spielburg |
| 19 | indianapolis | Indianapolis Motor Speedway | Indianapolis |
| 13 | spa | Circuit de Spa-Francorchamps | Spa |
| 53 | essarts | Rouen-Les-Essarts | Rouen |
| 21 | imola | Autodromo Enzo e Dino Ferrari | Imola |
| 10 | hockenheimring | Hockenheimring | Hockenheim |
| 43 | long_beach | Long Beach | California |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 51 | alfa | Alfa Romeo | Italian |
| 113 | kurtis_kraft | Kurtis Kraft | American |
| 59 | wolf | Wolf | Canadian |
| 133 | hwm | HWM | British |
| 66 | brm | BRM | British |
| 6 | ferrari | Ferrari | Italian |
| 35 | dallara | Dallara | Italian |
| 45 | osella | Osella | Italian |
| 3 | williams | Williams | British |

*driverStandings* (5 unreferenced columns omitted)

| raceId | driverId |
|---|---|
| 205 | 56 |
| 271 | 110 |
| 400 | 160 |
| 496 | 214 |

*drivers* (4 unreferenced columns omitted)

| driverId | forename | surname | dob | nationality |
|---|---|---|---|---|
| 249 | Bobby | Rahal | 1953-01-10 | American |
| 632 | Paul | Frère | 1917-01-30 | Belgian |
| 618 | Herbert | MacKay-Fraser | 1927-06-23 | American |
| 56 | Eddie | Irvine | 1965-11-10 | British |
| 110 | Andrea | de Cesaris | 1959-05-31 | Italian |
| 160 | Piercarlo | Ghinzani | 1952-01-16 | Italian |
| 214 | Kevin | Cogan | 1956-03-31 | American |
| 152 | Bruno | Giacomelli | 1952-09-10 | Italian |
| 516 | Bob | Christie | 1924-04-04 | American |

*races* (6 unreferenced columns omitted)

| raceId | name |
|---|---|
| 667 | South African Grand Prix |
| 622 | Spanish Grand Prix |
| 205 | Luxembourg Grand Prix |
| 271 | Japanese Grand Prix |
| 400 | Spanish Grand Prix |
| 496 | Canadian Grand Prix |
| 479 | Austrian Grand Prix |
| 786 | Indianapolis 500 |
| 542 | Canadian Grand Prix |
| 819 | Belgian Grand Prix |
| 779 | French Grand Prix |
| 228 | San Marino Grand Prix |
| 329 | German Grand Prix |
| 453 | United States Grand Prix West |
| 510 | Canadian Grand Prix |

*results* (16 unreferenced columns omitted)

| raceId | driverId |
|---|---|
| 479 | 152 |
| 786 | 516 |
| 542 | 249 |
| 819 | 632 |
| 779 | 618 |
| 228 | 56 |
| 329 | 110 |
| 453 | 160 |
| 510 | 214 |

*seasons*

| year | url |
|---|---|
| 1968 | http://en.wikipedia.org/wiki/1968_Formula_One_season |
| 1972 | http://en.wikipedia.org/wiki/1972_Formula_One_season |
| 1998 | http://en.wikipedia.org/wiki/1998_Formula_One_season |
| 1994 | http://en.wikipedia.org/wiki/1994_Formula_One_season |
| 1987 | http://en.wikipedia.org/wiki/1987_Formula_One_season |
| 1981 | http://en.wikipedia.org/wiki/1981_Formula_One_season |
| 1982 | http://en.wikipedia.org/wiki/1982_Formula_One_season |
| 1956 | http://en.wikipedia.org/wiki/1956_Formula_One_season |
| 1978 | http://en.wikipedia.org/wiki/1978_Formula_One_season |
| 1952 | http://en.wikipedia.org/wiki/1952_Formula_One_season |
| 1957 | http://en.wikipedia.org/wiki/1957_Formula_One_season |
| 1996 | http://en.wikipedia.org/wiki/1996_Formula_One_season |
| 1990 | http://en.wikipedia.org/wiki/1990_Formula_One_season |
| 1983 | http://en.wikipedia.org/wiki/1983_Formula_One_season |
| 1980 | http://en.wikipedia.org/wiki/1980_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 4 | Collision |
| 14 | +4 Laps |
| 69 | Fuel system |
| 12 | +2 Laps |
| 7 | Transmission |
| 1 | Finished |
| 81 | Did not qualify |

**Gold result on the witness:** `[['Eddie', 'Irvine', 'British', 'Luxembourg Grand Prix']]`  
**Predicted result on the witness:** `[['Eddie', 'Irvine', 'British', 'San Marino Grand Prix']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `driverStandings.raceId`: 31,578 rows, 0 NULL, 970 distinct values. Witness values: 205 occurs 23x; 271 occurs 45x; 400 occurs 29x; 496 occurs 39x.
- `driverStandings.driverId`: 31,578 rows, 0 NULL, 833 distinct values. Witness values: 56 occurs 146x; 110 occurs 216x; 160 occurs 121x; 214 occurs 17x.
- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 249 occurs 1x; 632 occurs 1x; 618 occurs 1x; 56 occurs 1x; 110 occurs 1x; 160 occurs 1x (+3 more).
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: 'Bobby' occurs 4x; 'Paul' occurs 9x; 'Herbert' occurs 1x; 'Eddie' occurs 6x; 'Andrea' occurs 4x; 'Piercarlo' occurs 1x (+3 more).
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: 'Rahal' occurs 1x; 'Frère' occurs 1x; 'MacKay-Fraser' occurs 1x; 'Irvine' occurs 1x; 'de Cesaris' occurs 1x; 'Ghinzani' occurs 1x (+3 more).
- `drivers.dob`: 840 rows, 1 NULL, 821 distinct values. Witness values: '1953-01-10' occurs 1x; '1917-01-30' occurs 1x; '1927-06-23' occurs 1x; '1965-11-10' occurs 1x; '1959-05-31' occurs 1x; '1952-01-16' occurs 1x (+3 more).
- `drivers.nationality`: 840 rows, 0 NULL, 41 distinct values. Witness values: 'American' occurs 157x; 'Belgian' occurs 23x; 'British' occurs 162x; 'Italian' occurs 99x.
- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 667 occurs 1x; 622 occurs 1x; 205 occurs 1x; 271 occurs 1x; 400 occurs 1x; 496 occurs 1x (+9 more).
- `races.name`: 976 rows, 0 NULL, 42 distinct values. Witness values: 'South African Grand Prix' occurs 23x; 'Spanish Grand Prix' occurs 47x; 'Luxembourg Grand Prix' occurs 2x; 'Japanese Grand Prix' occurs 33x; 'Canadian Grand Prix' occurs 48x; 'Austrian Grand Prix' occurs 30x (+6 more).
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 479 occurs 29x; 786 occurs 34x; 542 occurs 28x; 819 occurs 22x; 779 occurs 16x; 228 occurs 22x (+3 more).
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 152 occurs 82x; 516 occurs 5x; 249 occurs 2x; 632 occurs 11x; 618 occurs 1x; 56 occurs 147x (+3 more).

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 9 (formula_1)

**Question:** For the race happened in 2015/11/29, how many drivers did not finish the game?

**Evidence:** game and race are synonyms; drivers who didn't finish the race should have record in time;

**Gold SQL:**
```sql
SELECT COUNT(T2.driverId) FROM races AS T1 INNER JOIN results AS T2 ON T2.raceId = T1.raceId WHERE T1.date = '2015-11-29' AND T2.time IS NULL
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT T2.driverId) FROM races AS T1 INNER JOIN results AS T2 ON T1.raceId = T2.raceId WHERE T1.date = '2015-11-29' AND T2.time IS NULL
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 24 | yas_marina | Yas Marina Circuit | Abu Dhabi |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 3 | williams | Williams | British |
| 15 | sauber | Sauber | Swiss |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 822 | bottas | 77 | BOT |
| 831 | nasr | 12 | NAS |

*races* (6 unreferenced columns omitted)

| raceId | date |
|---|---|
| 945 | 2015-11-29 |

*results* (15 unreferenced columns omitted)

| raceId | driverId | time |
|---|---|---|
| 945 | 822 | NULL |
| 945 | 831 | NULL |
| 945 | 822 | NULL |

*seasons*

| year | url |
|---|---|
| 2015 | http://en.wikipedia.org/wiki/2015_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 11 | +1 Lap |

**Gold result on the witness:** `[[3]]`  
**Predicted result on the witness:** `[[2]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 945 occurs 1x.
- `races.date`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: '2015-11-29' occurs 1x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 945 occurs 20x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 822 occurs 92x; 831 occurs 40x.
- `results.time`: 23,657 rows, 17,696 NULL, 5,755 distinct values. Witness values: NULL occurs 17,696x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 10 (student_club)

**Question:** Provide the number of events attended by Luisa Guidi. What is her major?

**Evidence:** major refers to major_name;

**Gold SQL:**
```sql
SELECT COUNT(T3.link_to_event), T1.major_name FROM major AS T1 INNER JOIN member AS T2 ON T1.major_id = T2.link_to_major INNER JOIN attendance AS T3 ON T2.member_id = T3.link_to_member WHERE T2.first_name = 'Luisa' AND T2.last_name = 'Guidi'
```
**Predicted SQL:**
```sql
SELECT COUNT(T1.link_to_event), T3.major_name FROM attendance AS T1 INNER JOIN member AS T2 ON T1.link_to_member = T2.member_id INNER JOIN major AS T3 ON T2.link_to_major = T3.major_id WHERE T2.first_name = 'Luisa' AND T2.last_name = 'Guidi' GROUP BY T3.major_name
```

**Witness database:**

*attendance*

| link_to_event | link_to_member |
|---|---|
| recykdvf4LgsyA3wZ | recZ4PkGERzl9ziHO |
| rec5XDvJLyxDsGZWc | recZ4PkGERzl9ziHO |
| reciRZdAqNIKuMC96 | recD078PnS3x2doBe |
| recmbOVHSyzXQZpQr | recTjHY5xXhvkCdVT |

*event* (3 unreferenced columns omitted)

| event_id | event_name | event_date | type |
|---|---|---|---|
| recykdvf4LgsyA3wZ | Yearly Kickoff | 2019-09-03T12:00:00 | Meeting |
| rec5XDvJLyxDsGZWc | Laugh Out Loud | 2019-10-24T13:00:00 | Social |
| reciRZdAqNIKuMC96 | November Speaker | 2019-11-19T12:00:00 | Guest Speaker |
| recmbOVHSyzXQZpQr | November Meeting | 2019-11-05T12:00:00 | Meeting |

*major* (2 unreferenced columns omitted)

| major_id | major_name |
|---|---|
| recdIBgeU38UbV2sy | Civil Engineering |
| recd4JTuI0ssyoz07 | Dietetics |
| recr0WVEPZ08hl4Wt | Welding Technology |
| recIzqYuV3wMONTgB | Interior Design |
| recVYIFAwjT91pnv7 | Physics Teaching |
| reclQ8BVvj2w4cQ4V | Environmental Engineering |
| rec9CqGCGV8Y8rOSY | Communication Studies |
| rec09LedkREyskCNv | Agricultural Communication |

*member* (5 unreferenced columns omitted)

| member_id | first_name | last_name | link_to_major |
|---|---|---|---|
| recUdRhbhcEO1Hk5r | Amy | Firth | recIzqYuV3wMONTgB |
| recxBj3tjKTGHqucS | Sherri | Ramsey | recVYIFAwjT91pnv7 |
| recZ4PkGERzl9ziHO | Maya | Mclean | reclQ8BVvj2w4cQ4V |
| recD078PnS3x2doBe | Phillip | Cullen | rec9CqGCGV8Y8rOSY |
| recTjHY5xXhvkCdVT | Edwardo | Ing | rec09LedkREyskCNv |

*zip_code* (2 unreferenced columns omitted)

| zip_code | type | city | county |
|---|---|---|---|
| 21042 | Standard | Ellicott City | Howard County |
| 8861 | Standard | Perth Amboy | Middlesex County |
| 11554 | Standard | East Meadow | Nassau County |
| 1020 | Standard | Chicopee | Hampden County |
| 47711 | Standard | Evansville | Vanderburgh County |

**Gold result on the witness:** `[[0, None]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `attendance.link_to_event`: 326 rows, 0 NULL, 17 distinct values. Witness values: 'recykdvf4LgsyA3wZ' occurs 30x; 'rec5XDvJLyxDsGZWc' occurs 20x; 'reciRZdAqNIKuMC96' occurs 27x; 'recmbOVHSyzXQZpQr' occurs 25x.
- `attendance.link_to_member`: 326 rows, 0 NULL, 30 distinct values. Witness values: 'recZ4PkGERzl9ziHO' occurs 14x; 'recD078PnS3x2doBe' occurs 16x; 'recTjHY5xXhvkCdVT' occurs 14x.
- `major.major_id`: 113 rows, 0 NULL, 113 distinct values, all non-NULL values unique. Witness values: 'recdIBgeU38UbV2sy' occurs 1x; 'recd4JTuI0ssyoz07' occurs 1x; 'recr0WVEPZ08hl4Wt' occurs 1x; 'recIzqYuV3wMONTgB' occurs 1x; 'recVYIFAwjT91pnv7' occurs 1x; 'reclQ8BVvj2w4cQ4V' occurs 1x (+2 more).
- `major.major_name`: 113 rows, 0 NULL, 113 distinct values, all non-NULL values unique. Witness values: 'Civil Engineering' occurs 1x; 'Dietetics' occurs 1x; 'Welding Technology' occurs 1x; 'Interior Design' occurs 1x; 'Physics Teaching' occurs 1x; 'Environmental Engineering' occurs 1x (+2 more).
- `member.member_id`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: 'recUdRhbhcEO1Hk5r' occurs 1x; 'recxBj3tjKTGHqucS' occurs 1x; 'recZ4PkGERzl9ziHO' occurs 1x; 'recD078PnS3x2doBe' occurs 1x; 'recTjHY5xXhvkCdVT' occurs 1x.
- `member.first_name`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: 'Amy' occurs 1x; 'Sherri' occurs 1x; 'Maya' occurs 1x; 'Phillip' occurs 1x; 'Edwardo' occurs 1x.
- `member.last_name`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: 'Firth' occurs 1x; 'Ramsey' occurs 1x; 'Mclean' occurs 1x; 'Cullen' occurs 1x; 'Ing' occurs 1x.
- `member.link_to_major`: 33 rows, 1 NULL, 26 distinct values. Witness values: 'recIzqYuV3wMONTgB' occurs 1x; 'recVYIFAwjT91pnv7' occurs 1x; 'reclQ8BVvj2w4cQ4V' occurs 2x; 'rec9CqGCGV8Y8rOSY' occurs 1x; 'rec09LedkREyskCNv' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 11 (european_football_2)

**Question:** State the name of the most strongest player.

**Evidence:** strongest players refers to player has MAX(overall_rating)

**Gold SQL:**
```sql
SELECT DISTINCT t1.player_name FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE t2.overall_rating = (SELECT MAX(overall_rating) FROM Player_Attributes)
```
**Predicted SQL:**
```sql
SELECT Player.player_name FROM Player INNER JOIN Player_Attributes ON Player.player_fifa_api_id = Player_Attributes.player_fifa_api_id ORDER BY Player_Attributes.overall_rating DESC LIMIT 1
```

**Witness database:**

*Player_Attributes* (39 unreferenced columns omitted)

| player_fifa_api_id | player_api_id | overall_rating |
|---|---|---|
| 0 | 2625 | 0 |
| 0 | 2625 | 1 |

*Player* (4 unreferenced columns omitted)

| player_api_id | player_name | player_fifa_api_id |
|---|---|---|
| 2624 | 2147483649 | 0 |
| 2625 | 2147483648 | 1 |

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
| 2 | -1 | 1 | 2147483648 |
| 1 | 0 | 0 | 2147483649 |

*Team_Attributes* (21 unreferenced columns omitted)

| id | team_fifa_api_id | team_api_id | date |
|---|---|---|---|
| 1 | 1 | -1 | 2147483648 |
| 2 | 0 | 0 | 2147483648 |

*Match* (111 unreferenced columns omitted)

| id | country_id | league_id | season |
|---|---|---|---|
| 2 | 1 | 1 | 2147483648 |
| 1 | 1 | 1 | 2147483648 |

**Gold result on the witness:** `[['2147483648']]`  
**Predicted result on the witness:** `[['2147483649']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player_Attributes.player_fifa_api_id`: 183,978 rows, 0 NULL, 11,062 distinct values. Witness values: 0 occurs 0x.
- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 2625 occurs 14x.
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: 0 occurs 0x; 1 occurs 0x.
- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 2624 occurs 0x; 2625 occurs 1x.
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: '2147483649' occurs 0x; '2147483648' occurs 0x.
- `Player.player_fifa_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x; 1 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 12 (formula_1)

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

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 50 | 0 | 0 | 0 |

*constructorResults* (1 unreferenced columns omitted)

| constructorResultsId | raceId | constructorId | points |
|---|---|---|---|
| 0 | 50 | 0 | 0 |

*constructorStandings* (3 unreferenced columns omitted)

| constructorStandingsId | raceId | constructorId | points |
|---|---|---|---|
| 0 | 50 | 0 | 0 |

*driverStandings* (3 unreferenced columns omitted)

| driverStandingsId | raceId | driverId | points |
|---|---|---|---|
| 0 | 50 | 0 | 0 |

*lapTimes* (2 unreferenced columns omitted)

| raceId | driverId | lap | position |
|---|---|---|---|
| 50 | 0 | 0 | 0 |

*pitStops* (3 unreferenced columns omitted)

| raceId | driverId | stop | lap |
|---|---|---|---|
| 50 | 0 | 0 | 0 |

*qualifying* (5 unreferenced columns omitted)

| qualifyId | raceId | driverId | constructorId |
|---|---|---|---|
| 0 | 50 | 0 | 0 |

*status*

| statusId | status |
|---|---|
| 2 | 2147483648 |

*results* (15 unreferenced columns omitted)

| raceId | time | statusId |
|---|---|---|
| 50 | 2147483648 | 2 |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 50 occurs 22x.
- `results.time`: 23,657 rows, 17,696 NULL, 5,755 distinct values. Witness values: '2147483648' occurs 0x.
- `results.statusId`: 23,657 rows, 0 NULL, 132 distinct values. Witness values: 2 occurs 137x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 13 (california_schools)

**Question:** What is the total amount of Community College District closure in 1989 in the city of San Francisco?

**Evidence:** -

**Gold SQL:**
```sql
SELECT COUNT(School) FROM schools WHERE strftime('%Y', ClosedDate) = '1989' AND City = 'San Francisco' AND DOCType = 'Community College District'
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM schools WHERE schools.city = 'San Francisco' AND schools.doctype = 'Community College District' AND STRFTIME('%Y', schools.closeddate) = '1989'
```

**Witness database:**

*schools* (45 unreferenced columns omitted)

| School | City | ClosedDate | DOCType |
|---|---|---|---|
| Pacific Heights Adult High Sch | San Francisco | 1989-06-30 | Community College District |
| NULL | San Francisco | 1989-06-30 | Community College District |

**Gold result on the witness:** `[[1]]`  
**Predicted result on the witness:** `[[2]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `schools.School`: 17,686 rows, 1,369 NULL, 13,875 distinct values. Witness values: 'Pacific Heights Adult High Sch' occurs 1x; NULL occurs 1,369x.
- `schools.City`: 17,686 rows, 293 NULL, 1,165 distinct values. Witness values: 'San Francisco' occurs 253x.
- `schools.ClosedDate`: 17,686 rows, 11,992 NULL, 899 distinct values. Witness values: '1989-06-30' occurs 2,009x.
- `schools.DOCType`: 17,686 rows, 0 NULL, 12 distinct values. Witness values: 'Community College District' occurs 33x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 14 (toxicology)

**Question:** How many double bonds does TR006 have and is it carcinogenic?

**Evidence:** label = '+' mean molecules are carcinogenic; label = '-' means molecules are non-carcinogenic; double bond refers to bond_type = ' = ';

**Gold SQL:**
```sql
SELECT COUNT(T1.bond_id), T2.label FROM bond AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.bond_type = '=' AND T2.molecule_id = 'TR006' GROUP BY T2.label
```
**Predicted SQL:**
```sql
SELECT COUNT(b.bond_id) AS double_bond_count, m.label FROM bond b JOIN molecule m ON b.molecule_id = m.molecule_id WHERE b.bond_type = '=' AND m.molecule_id = 'TR006';
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

## Item 15 (thrombosis_prediction)

**Question:** Was the patient a man or a women whose ALT glutamic pylvic transaminase status got 9 on 1992-6-12?

**Evidence:** man refers to SEX = 'M'; women refers to SEX = 'F'; ALT glutamic pylvic transaminase status got 9 GPT = '9'; 1992/6/12 refers to Date = '1992-06-12'

**Gold SQL:**
```sql
SELECT T1.SEX FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.GPT = 9.0 AND T2.Date = '1992-06-12'
```
**Predicted SQL:**
```sql
SELECT Patient.SEX FROM Patient INNER JOIN Laboratory ON Patient.ID = Laboratory.ID WHERE Laboratory.Date = '1992-06-12' AND Laboratory.GPT = 9 AND(Patient.SEX = 'M' OR Patient.SEX = 'F')
```

**Witness database:**

*Patient* (5 unreferenced columns omitted)

| ID | SEX |
|---|---|
| 1 | F |
| 38 | F |
| 47 | F |
| 60 | F |
| 78 | NULL |

*Laboratory* (41 unreferenced columns omitted)

| ID | Date | GPT |
|---|---|---|
| 1 | 1992-06-12 | 9 |
| 38 | 1992-06-12 | 9 |
| 47 | 2000-01-30 | 9 |
| 60 | 1992-06-12 | NULL |
| 78 | 1992-06-12 | 9 |

**Gold result on the witness:** `[['F'], ['F'], [None]]`  
**Predicted result on the witness:** `[['F'], ['F']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 38 occurs 0x; 47 occurs 0x; 60 occurs 0x; 78 occurs 0x.
- `Patient.SEX`: 1,238 rows, 0 NULL, 3 distinct values. Witness values: 'F' occurs 1,023x; NULL occurs 0x.
- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 1 occurs 0x; 38 occurs 0x; 47 occurs 0x; 60 occurs 0x; 78 occurs 0x.
- `Laboratory.Date`: 13,908 rows, 0 NULL, 3,723 distinct values. Witness values: '1992-06-12' occurs 2x; '2000-01-30' occurs 0x.
- `Laboratory.GPT`: 13,908 rows, 2,634 NULL, 302 distinct values. Witness values: 9 occurs 441x; NULL occurs 2,634x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 16 (codebase_community)

**Question:** How many elders obtained the "Supporter" badge?

**Evidence:** "Supporter" is the Name of badge;  elders refers to Age > 65

**Gold SQL:**
```sql
SELECT COUNT(T1.Id) FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId WHERE T1.Age > 65 AND T2.Name = 'Supporter'
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT users.id) FROM users INNER JOIN badges ON users.id = badges.userid WHERE users.age > 65 AND badges.name = 'Supporter'
```

**Witness database:**

*badges* (2 unreferenced columns omitted)

| UserId | Name |
|---|---|
| 1 | Supporter |
| 16 | Supporter |
| 1 | Supporter |
| 1 | Supporter |
| NULL | Supporter |
| 2 | Supporter |
| 41 | Supporter |
| 1 | aSupporter |
| 1 | NULL |

*users* (12 unreferenced columns omitted)

| Id | Age |
|---|---|
| 1 | 66 |
| 16 | 66 |
| 2 | -1 |
| 41 | NULL |

**Gold result on the witness:** `[[4]]`  
**Predicted result on the witness:** `[[2]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `badges.UserId`: 79,851 rows, 0 NULL, 25,078 distinct values. Witness values: 1 occurs 0x; 16 occurs 2x; NULL occurs 0x; 2 occurs 3x; 41 occurs 9x.
- `badges.Name`: 79,851 rows, 0 NULL, 153 distinct values. Witness values: 'Supporter' occurs 8,828x; 'aSupporter' occurs 0x; NULL occurs 0x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 16 occurs 1x; 2 occurs 1x; 41 occurs 1x.
- `users.Age`: 40,325 rows, 32,007 NULL, 70 distinct values. Witness values: 66 occurs 5x; -1 occurs 0x; NULL occurs 32,007x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 17 (card_games)

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

*sets* (18 unreferenced columns omitted)

| id | code | isOnlineOnly |
|---|---|---|
| 1 | a | 6 |
| 31 | af | 2 |
| 42 | b | 1 |

*set_translations* (2 unreferenced columns omitted)

| language | setCode |
|---|---|
| Portuguese (Brazil) | a |
| Portuguese (Brazil) | a |
| Portuguese (Brazil) | af |
| Portuguese (Brazil) | NULL |
| Chinese Simplified | a |
| NULL | a |
| Portuguese (Brazil) | b |

**Gold result on the witness:** `[[33.333333333333336]]`  
**Predicted result on the witness:** `[[25.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `sets.id`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 31 occurs 1x; 42 occurs 1x.
- `sets.code`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 'a' occurs 0x; 'af' occurs 0x; 'b' occurs 0x.
- `sets.isOnlineOnly`: 551 rows, 0 NULL, 2 distinct values. Witness values: 6 occurs 0x; 2 occurs 0x; 1 occurs 26x.
- `set_translations.language`: 1,210 rows, 0 NULL, 10 distinct values. Witness values: 'Portuguese (Brazil)' occurs 121x; 'Chinese Simplified' occurs 121x; NULL occurs 0x.
- `set_translations.setCode`: 1,210 rows, 0 NULL, 121 distinct values. Witness values: 'a' occurs 0x; 'af' occurs 0x; NULL occurs 0x; 'b' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 18 (formula_1)

**Question:** What was the fastest lap speed among all drivers in the 2009 Spanish Grand Prix?

**Evidence:** the fastest lap speed among all refers to max(fastestLapSpeed); Spanish Grand Prix refers to races.name = 'Spanish Grand Prix';

**Gold SQL:**
```sql
SELECT T2.fastestLapSpeed FROM races AS T1 INNER JOIN results AS T2 ON T2.raceId = T1.raceId WHERE T1.name = 'Spanish Grand Prix' AND T1.year = 2009 AND T2.fastestLapSpeed IS NOT NULL ORDER BY T2.fastestLapSpeed DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT results.fastestLapSpeed FROM races INNER JOIN results ON races.raceId = results.raceId WHERE races.name = 'Spanish Grand Prix' AND races.year = 2009 ORDER BY results.fastestLapSpeed DESC LIMIT 1
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 1135 | mosport | Mosport International Raceway | Ontario |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 1136 | derrington | Derrington | British |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 1137 | birger | NULL | NULL |

*races* (5 unreferenced columns omitted)

| raceId | year | name |
|---|---|---|
| 1138 | 2009 | Spanish Grand Prix |

*results* (16 unreferenced columns omitted)

| raceId | fastestLapSpeed |
|---|---|
| 1138 | NULL |

*seasons*

| year | url |
|---|---|
| 2009 | http://en.wikipedia.org/wiki/2009_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 1 | Finished |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 1138 occurs 0x.
- `races.year`: 976 rows, 0 NULL, 68 distinct values. Witness values: 2009 occurs 17x.
- `races.name`: 976 rows, 0 NULL, 42 distinct values. Witness values: 'Spanish Grand Prix' occurs 47x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 1138 occurs 0x.
- `results.fastestLapSpeed`: 23,657 rows, 18,389 NULL, 5,045 distinct values. Witness values: NULL occurs 18,389x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 19 (codebase_community)

**Question:** What is the total score of the posts edited by Yevgeny and include the user's website URL.

**Evidence:** "Yevgeny" is the DisplayName; edited refers to LastEditorUserId

**Gold SQL:**
```sql
SELECT SUM(T1.Score), T2.WebsiteUrl FROM posts AS T1 INNER JOIN users AS T2 ON T1.LastEditorUserId = T2.Id WHERE T2.DisplayName = 'Yevgeny' GROUP BY T2.WebsiteUrl
```
**Predicted SQL:**
```sql
SELECT SUM(posts.score) AS totalscore, users.websiteurl FROM posts INNER JOIN users ON posts.lasteditoruserid = users.id WHERE users.displayname = 'Yevgeny'
```

**Witness database:**

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 164181 | 2 | 51463 | 707034dc-8d9c-4398-a415-93d43daa0852 |

*posts* (19 unreferenced columns omitted)

| Score | LastEditorUserId |
|---|---|
| 3 | NULL |

*users* (11 unreferenced columns omitted)

| Id | DisplayName | WebsiteUrl |
|---|---|---|
| 7486 | Robert Long | NULL |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None, None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `posts.Score`: 91,966 rows, 0 NULL, 130 distinct values. Witness values: 3 occurs 10,067x.
- `posts.LastEditorUserId`: 91,966 rows, 47,361 NULL, 6,578 distinct values. Witness values: NULL occurs 47,361x.
- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 7486 occurs 1x.
- `users.DisplayName`: 40,325 rows, 0 NULL, 35,644 distinct values. Witness values: 'Robert Long' occurs 2x.
- `users.WebsiteUrl`: 40,325 rows, 32,204 NULL, 7,787 distinct values. Witness values: NULL occurs 32,204x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 20 (card_games)

**Question:** Please provide top three sets that don't appear in Magic: The Gathering Online, along with their names in in alphabetical order.

**Evidence:** don't appear in Magic: The Gathering Online refers to mtgoCode is NULL or mtgoCode = ''

**Gold SQL:**
```sql
SELECT name FROM sets WHERE mtgoCode IS NULL ORDER BY name LIMIT 3
```
**Predicted SQL:**
```sql
SELECT name FROM sets WHERE mtgoCode IS NULL OR mtgoCode = '' ORDER BY name LIMIT 3
```

**Witness database:**

*cards* (70 unreferenced columns omitted)

| id | artist | asciiName | availability |
|---|---|---|---|
| 1 | 2147483648 | 2147483648 | mtgo |

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
| 1 | Japanese | 2147483648 | 2147483648 |

*rulings*

| id | date | text | uuid |
|---|---|---|---|
| 1 | 0001-01-01 | 2147483648 | 2147483648 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2147483648']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `sets.mtgoCode`: 551 rows, 391 NULL, 160 distinct values, all non-NULL values unique. Witness values: '' occurs 0x.
- `sets.name`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: '2147483648' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 21 (toxicology)

**Question:** What is the molecule id of bond id TR001_1_7?

**Evidence:** -

**Gold SQL:**
```sql
SELECT DISTINCT T1.molecule_id FROM atom AS T1 INNER JOIN connected AS T2 ON T1.atom_id = T2.atom_id WHERE T2.bond_id = 'TR001_1_7'
```
**Predicted SQL:**
```sql
SELECT molecule_id FROM bond WHERE bond_id = 'TR001_1_7';
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| atom_id | molecule_id |
|---|---|
| 2147483649 | 2147483649 |
| 2147483648 | 2147483648 |

*bond* (1 unreferenced columns omitted)

| bond_id | molecule_id |
|---|---|
| TR001_1_7 | 2147483648 |
| 2147483648 | 2147483648 |

*connected* (1 unreferenced columns omitted)

| atom_id | bond_id |
|---|---|
| 2147483649 | TR001_1_7 |
| 2147483649 | TR001_1_7 |

*molecule*

| molecule_id | label |
|---|---|
| 2147483648 | + |
| 2147483649 | + |

**Gold result on the witness:** `[['2147483649']]`  
**Predicted result on the witness:** `[['2147483648']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.atom_id`: 12,333 rows, 0 NULL, 12,333 distinct values, all non-NULL values unique. Witness values: '2147483649' occurs 0x; '2147483648' occurs 0x.
- `atom.molecule_id`: 12,333 rows, 0 NULL, 444 distinct values. Witness values: '2147483649' occurs 0x; '2147483648' occurs 0x.
- `bond.bond_id`: 12,379 rows, 0 NULL, 12,379 distinct values, all non-NULL values unique. Witness values: 'TR001_1_7' occurs 1x; '2147483648' occurs 0x.
- `bond.molecule_id`: 12,379 rows, 0 NULL, 444 distinct values. Witness values: '2147483648' occurs 0x.
- `connected.atom_id`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: '2147483649' occurs 0x.
- `connected.bond_id`: 24,758 rows, 0 NULL, 12,379 distinct values. Witness values: 'TR001_1_7' occurs 2x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 22 (european_football_2)

**Question:** How much is the average build up play speed of the Heart of Midlothian team?

**Evidence:** Heart of Midlothian refers to team_long_name = 'Heart of Midlothian'; average build up play speed refers to  AVG(buildUpPlaySpeed)

**Gold SQL:**
```sql
SELECT CAST(SUM(t2.buildUpPlaySpeed) AS REAL) / COUNT(t2.id) FROM Team AS t1 INNER JOIN Team_Attributes AS t2 ON t1.team_api_id = t2.team_api_id WHERE t1.team_long_name = 'Heart of Midlothian'
```
**Predicted SQL:**
```sql
SELECT AVG(TA.buildUpPlaySpeed) AS average_buildUpPlaySpeed FROM Team AS T INNER JOIN Team_Attributes AS TA ON T.team_fifa_api_id = TA.team_fifa_api_id WHERE T.team_long_name = 'Heart of Midlothian';
```

**Witness database:**

*Match* (111 unreferenced columns omitted)

| id | country_id | league_id | season |
|---|---|---|---|
| 20809 | 19694 | 19694 | 2012/2013 |
| 1495 | 19694 | 19694 | 2008/2009 |

*Team* (2 unreferenced columns omitted)

| team_api_id | team_fifa_api_id | team_long_name |
|---|---|---|
| 5 | 80 | Heart of Midlothian |
| 9860 | NULL | Amadora |

*Team_Attributes* (21 unreferenced columns omitted)

| id | team_fifa_api_id | team_api_id | buildUpPlaySpeed |
|---|---|---|---|
| 565 | 80 | 5 | 66 |
| 567 | 80 | 9860 | 52 |
| 1493 | 80 | 9860 | 66 |

**Gold result on the witness:** `[[66.0]]`  
**Predicted result on the witness:** `[[61.333333333333336]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Team.team_api_id`: 299 rows, 0 NULL, 299 distinct values, all non-NULL values unique. Witness values: 5 occurs 0x; 9860 occurs 1x.
- `Team.team_fifa_api_id`: 299 rows, 11 NULL, 285 distinct values. Witness values: 80 occurs 1x; NULL occurs 11x.
- `Team.team_long_name`: 299 rows, 0 NULL, 296 distinct values. Witness values: 'Heart of Midlothian' occurs 1x; 'Amadora' occurs 1x.
- `Team_Attributes.id`: 1,458 rows, 0 NULL, 1,458 distinct values, all non-NULL values unique. Witness values: 565 occurs 1x; 567 occurs 1x; 1493 occurs 0x.
- `Team_Attributes.team_fifa_api_id`: 1,458 rows, 0 NULL, 285 distinct values. Witness values: 80 occurs 5x.
- `Team_Attributes.team_api_id`: 1,458 rows, 0 NULL, 288 distinct values. Witness values: 5 occurs 0x; 9860 occurs 5x.
- `Team_Attributes.buildUpPlaySpeed`: 1,458 rows, 0 NULL, 57 distinct values. Witness values: 66 occurs 38x; 52 occurs 62x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 23 (thrombosis_prediction)

**Question:** For the patients with an abnormal Ig M level, what is the most common disease they are diagnosed with?

**Evidence:** abnormal Ig M level refers to IGM <=40 OR IGM >= 400; most common disease refers to MAX(COUNT(Diagnosis));

**Gold SQL:**
```sql
SELECT T1.Diagnosis FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.IGM NOT BETWEEN 40 AND 400 GROUP BY T1.Diagnosis ORDER BY COUNT(T1.Diagnosis) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT patient.diagnosis FROM laboratory INNER JOIN patient ON laboratory.id = patient.id WHERE laboratory.igm <= 40 OR laboratory.igm >= 400 GROUP BY patient.diagnosis ORDER BY COUNT(patient.diagnosis) DESC LIMIT 1
```

**Witness database:**

*Patient* (5 unreferenced columns omitted)

| ID | Diagnosis |
|---|---|
| 1 | l |
| 21 | NULL |
| 41 | l |
| 66 | NULL |

*Laboratory* (42 unreferenced columns omitted)

| ID | IGM |
|---|---|
| 1 | 400 |
| 21 | 400 |
| 41 | 400 |
| 21 | 39 |
| 66 | NULL |

**Gold result on the witness:** `[[None]]`  
**Predicted result on the witness:** `[['l']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 21 occurs 0x; 41 occurs 0x; 66 occurs 0x.
- `Patient.Diagnosis`: 1,238 rows, 0 NULL, 220 distinct values. Witness values: 'l' occurs 0x; NULL occurs 0x.
- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 1 occurs 0x; 21 occurs 0x; 41 occurs 0x; 66 occurs 0x.
- `Laboratory.IGM`: 13,908 rows, 11,230 NULL, 487 distinct values. Witness values: 400 occurs 0x; 39 occurs 6x; NULL occurs 11,230x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 24 (card_games)

**Question:** For all the set of cards that has Japanese translation, what is the percentage of them are only available in non-foil?

**Evidence:** Japanese translation refers to language = 'Japanese'; in non-foil refers to isNonFoilOnly = 1; percentage of Japanese non foil in Japanese cards refers to DIVIDE(SUM(isNonFoilOnly = 1), SUM(language = 'Japanese'))*100

**Gold SQL:**
```sql
SELECT CAST(SUM(CASE WHEN isNonFoilOnly = 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(id) FROM sets WHERE code IN ( SELECT setCode FROM set_translations WHERE language = 'Japanese' )
```
**Predicted SQL:**
```sql
SELECT (SUM(CASE WHEN s.isNonFoilOnly = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS percentage FROM sets s JOIN set_translations st ON s.code = st.setCode WHERE st.language = 'Japanese';
```

**Witness database:**

*set_translations* (2 unreferenced columns omitted)

| language | setCode |
|---|---|
| Japanese | k2 |
| Japanese | k2 |
| Italian | k3 |
| German | k1 |
| Japanese | 100.0 |

*sets* (18 unreferenced columns omitted)

| id | code | isNonFoilOnly |
|---|---|---|
| 0 | k2 | 100 |
| 2 | k3 | 100 |
| 1 | k1 | 100 |
| 100 | 100.0 | 1 |

**Gold result on the witness:** `[[50.0]]`  
**Predicted result on the witness:** `[[33.333333333333336]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `set_translations.language`: 1,210 rows, 0 NULL, 10 distinct values. Witness values: 'Japanese' occurs 121x; 'Italian' occurs 121x; 'German' occurs 121x.
- `set_translations.setCode`: 1,210 rows, 0 NULL, 121 distinct values. Witness values: 'k2' occurs 0x; 'k3' occurs 0x; 'k1' occurs 0x; '100.0' occurs 0x.
- `sets.id`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x; 2 occurs 1x; 1 occurs 1x; 100 occurs 1x.
- `sets.code`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 'k2' occurs 0x; 'k3' occurs 0x; 'k1' occurs 0x; '100.0' occurs 0x.
- `sets.isNonFoilOnly`: 551 rows, 0 NULL, 2 distinct values. Witness values: 100 occurs 0x; 1 occurs 106x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 25 (codebase_community)

**Question:** How many users received commentator badges in 2014?

**Evidence:** Commentator is the name of the badge; year(Date) = 2014;

**Gold SQL:**
```sql
SELECT COUNT(Id) FROM badges WHERE Name = 'Commentator' AND STRFTIME('%Y', Date) = '2014'
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT b.UserId) FROM badges AS b WHERE b.Name = 'Commentator' AND strftime('%Y', b.Date) = '2014'
```

**Witness database:**

*badges*

| Id | UserId | Name | Date |
|---|---|---|---|
| 83055 | 48766 | Commentator | 2014-06-28 08:54:03.0 |
| 1001 | 48766 | Commentator | 2014-06-28 08:54:03.0 |

*users* (10 unreferenced columns omitted)

| Id | Reputation | CreationDate | DisplayName |
|---|---|---|---|
| 48766 | 1148 | 2014-06-21 09:46:59.0 | javlacalle |

**Gold result on the witness:** `[[2]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `badges.Id`: 79,851 rows, 0 NULL, 79,851 distinct values, all non-NULL values unique. Witness values: 83055 occurs 1x; 1001 occurs 1x.
- `badges.UserId`: 79,851 rows, 0 NULL, 25,078 distinct values. Witness values: 48766 occurs 9x.
- `badges.Name`: 79,851 rows, 0 NULL, 153 distinct values. Witness values: 'Commentator' occurs 2,047x.
- `badges.Date`: 79,851 rows, 0 NULL, 65,586 distinct values. Witness values: '2014-06-28 08:54:03.0' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 26 (formula_1)

**Question:** What was the fastest lap speed among all drivers in the 2009 Spanish Grand Prix?

**Evidence:** the fastest lap speed among all refers to max(fastestLapSpeed); Spanish Grand Prix refers to races.name = 'Spanish Grand Prix';

**Gold SQL:**
```sql
SELECT T2.fastestLapSpeed FROM races AS T1 INNER JOIN results AS T2 ON T2.raceId = T1.raceId WHERE T1.name = 'Spanish Grand Prix' AND T1.year = 2009 AND T2.fastestLapSpeed IS NOT NULL ORDER BY T2.fastestLapSpeed DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.fastestLapSpeed FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T2.year = 2009 AND T2.name = 'Spanish Grand Prix' ORDER BY T1.fastestLapSpeed DESC LIMIT 1
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 3 | Spanish Grand Prix | 2009 | 2009 |
| 1 | c | A | 1 |
| 2 | y2 | b | c |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 1 | 2009 | 1 | Japanese |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 3 | a | 5 | A |
| 1 | 2009 | 0 | NULL |

*races* (5 unreferenced columns omitted)

| raceId | year | name |
|---|---|---|
| 1 | 3 | 2009 |
| 2009 | 1 | 1 |
| 2 | 2009 | Spanish Grand Prix |
| 3 | 1 | 1 |

*results* (16 unreferenced columns omitted)

| raceId | fastestLapSpeed |
|---|---|
| 2 | NULL |
| 3 | 2009 |

*seasons*

| year | url |
|---|---|
| 3 | b |
| 1 | Spanish Grand Prix |
| 2009 | 1 |

*status*

| statusId | status |
|---|---|
| 2 | x1 |
| 3 | y2 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 2009 occurs 0x; 2 occurs 1x; 3 occurs 1x.
- `races.year`: 976 rows, 0 NULL, 68 distinct values. Witness values: 3 occurs 0x; 1 occurs 0x; 2009 occurs 17x.
- `races.name`: 976 rows, 0 NULL, 42 distinct values. Witness values: '2009' occurs 0x; '1' occurs 0x; 'Spanish Grand Prix' occurs 47x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 2 occurs 20x; 3 occurs 20x.
- `results.fastestLapSpeed`: 23,657 rows, 18,389 NULL, 5,045 distinct values. Witness values: NULL occurs 18,389x; '2009' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 27 (thrombosis_prediction)

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
| 1 | SLE | d |
| 1 | SLE | l |
| 1 | SLE | l |
| 1 | ab | d |
| 1 | NULL | d |
| 1 | SLE | NULL |

*Patient* (5 unreferenced columns omitted)

| ID | Diagnosis |
|---|---|
| 1 | k |

**Gold result on the witness:** `[['l']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: 1 occurs 0x.
- `Examination.Diagnosis`: 806 rows, 331 NULL, 181 distinct values. Witness values: 'SLE' occurs 95x; 'ab' occurs 0x; NULL occurs 331x.
- `Examination.Symptoms`: 806 rows, 726 NULL, 39 distinct values. Witness values: 'd' occurs 0x; 'l' occurs 0x; NULL occurs 726x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x.
- `Patient.Diagnosis`: 1,238 rows, 0 NULL, 220 distinct values. Witness values: 'k' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 28 (formula_1)

**Question:** Which of the Italian constructor got the highest point to date? Give its introduction website?

**Evidence:** introduction website refers to url; Italian is a nationality

**Gold SQL:**
```sql
SELECT T1.url FROM constructors AS T1 INNER JOIN constructorStandings AS T2 on T1.constructorId = T2.constructorId WHERE T1.nationality = 'Italian' ORDER BY T2.points DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT t1.url FROM constructors AS t1 INNER JOIN (SELECT constructorid, SUM(points) AS total_points FROM constructorstandings GROUP BY constructorid ORDER BY total_points DESC LIMIT 1) AS t2 ON t1.constructorid = t2.constructorid WHERE t1.nationality = 'Italian'
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 2 | sepang | Sepang International Circuit | Kuala Lumpur |

*constructorStandings* (5 unreferenced columns omitted)

| constructorId | points |
|---|---|
| 2 | 53.0 |
| 1 | 11.0 |

*constructors* (2 unreferenced columns omitted)

| constructorId | nationality | url |
|---|---|---|
| 1 | Italian | http://en.wikipedia.org/wiki/Apollon_(Formula_One) |
| 2 | German | http://en.wikipedia.org/wiki/BMW_Sauber |

*races* (4 unreferenced columns omitted)

| raceId | year | round | circuitId |
|---|---|---|---|
| 2 | 2009 | 2 | 2 |

*seasons*

| year | url |
|---|---|
| 2009 | http://en.wikipedia.org/wiki/2009_Formula_One_season |

**Gold result on the witness:** `[['http://en.wikipedia.org/wiki/Apollon_(Formula_One)']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `constructorStandings.constructorId`: 11,836 rows, 0 NULL, 156 distinct values. Witness values: 2 occurs 70x; 1 occurs 774x.
- `constructorStandings.points`: 11,836 rows, 0 NULL, 436 distinct values. Witness values: 53.0 occurs 28x; 11.0 occurs 164x.
- `constructors.constructorId`: 208 rows, 0 NULL, 208 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 2 occurs 1x.
- `constructors.nationality`: 208 rows, 0 NULL, 24 distinct values. Witness values: 'Italian' occurs 29x; 'German' occurs 10x.
- `constructors.url`: 208 rows, 0 NULL, 171 distinct values. Witness values: 'http://en.wikipedia.org/wiki/Apollon_(Formula_One occurs 1x; 'http://en.wikipedia.org/wiki/BMW_Sauber' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 29 (toxicology)

**Question:** Among all the atoms from 21 to 25, list all the molecules that are carcinogenic.

**Evidence:** atoms from 21 to 25 refers to SUBSTR(atom_id, 7, 2) between '21' and '25'; label = '+' mean molecules are carcinogenic

**Gold SQL:**
```sql
SELECT DISTINCT T2.molecule_id FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE SUBSTR(T1.atom_id, -2) BETWEEN '21' AND '25' AND T2.label = '+'
```
**Predicted SQL:**
```sql
SELECT T2.molecule_id FROM atom AS T1 INNER JOIN molecule AS T2 ON T1.molecule_id = T2.molecule_id WHERE CAST(SUBSTR(T1.atom_id, 7, 2) AS INTEGER) BETWEEN 21 AND 25 AND T2.label = '+'
```

**Witness database:**

*atom* (1 unreferenced columns omitted)

| atom_id | molecule_id |
|---|---|
| DAEBC22 |  |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
| F |  |  |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| DAEBC22 | DAEBC22 | F |

*molecule*

| molecule_id | label |
|---|---|
|  | + |

**Gold result on the witness:** `[['']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.atom_id`: 12,333 rows, 0 NULL, 12,333 distinct values, all non-NULL values unique. Witness values: 'DAEBC22' occurs 0x.
- `atom.molecule_id`: 12,333 rows, 0 NULL, 444 distinct values. Witness values: '' occurs 0x.
- `molecule.molecule_id`: 343 rows, 0 NULL, 343 distinct values, all non-NULL values unique. Witness values: '' occurs 0x.
- `molecule.label`: 343 rows, 0 NULL, 2 distinct values. Witness values: '+' occurs 152x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 30 (student_club)

**Question:** What is the amount of the funds that the Vice President received?

**Evidence:** 'Vice President' is a position of Student Club; funds received refers to amount.

**Gold SQL:**
```sql
SELECT T2.amount FROM member AS T1 INNER JOIN income AS T2 ON T1.member_id = T2.link_to_member WHERE T1.position = 'Vice President'
```
**Predicted SQL:**
```sql
SELECT SUM(T1.amount) FROM income AS T1 INNER JOIN member AS T2 ON T1.link_to_member = T2.member_id WHERE T2.position = 'Vice President'
```

**Witness database:**

*income* (4 unreferenced columns omitted)

| amount | link_to_member |
|---|---|
| 3000 | NULL |
| 50 | recf4UKTfipCzgcSA |
| 50 | rec28ORZgcm1dtqBZ |
| 50 | recTjHY5xXhvkCdVT |

*major*

| major_id | major_name | department | college |
|---|---|---|---|
| recKJHO1P6ZC5m567 | Human Development and Family Studies | Human Development and Family Studies Department | College of Education & Human Services |
| recRA9IxLl6eKPsJX | International Studies | Political Science Department | College of Humanities and Social Sciences |
| recaJdSK83k6ekRJL | Nutrition Science | Nutrition, Dietetics, and Food Sciences Department | College of Agriculture and Applied Sciences |
| recdIBgeU38UbV2sy | Civil Engineering | Civil and Environmental Engineering Department | College of Engineering |
| rec09LedkREyskCNv | Agricultural Communication | School of Applied Sciences, Technology and Education | College of Agriculture and Applied Sciences |

*member* (7 unreferenced columns omitted)

| member_id | position |
|---|---|
| reccSUPwy30AeZLEb | Inactive |
| recT92PyyZCGq1R68 | Member |
| rec3pH4DxMcWHMRB7 | Member |
| recf4UKTfipCzgcSA | Member |
| rec28ORZgcm1dtqBZ | Member |
| recTjHY5xXhvkCdVT | Member |

*zip_code* (2 unreferenced columns omitted)

| zip_code | type | city | county |
|---|---|---|---|
| 35640 | Standard | Hartselle | Morgan County |
| 79106 | Standard | Amarillo | Potter County |
| 48236 | Standard | Grosse Pointe | Wayne County |
| 21801 | Standard | Salisbury | Wicomico County |
| 10002 | Standard | New York | New York County |
| 47711 | Standard | Evansville | Vanderburgh County |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `income.amount`: 36 rows, 0 NULL, 4 distinct values. Witness values: 3000 occurs 1x; 50 occurs 33x.
- `income.link_to_member`: 36 rows, 3 NULL, 31 distinct values. Witness values: NULL occurs 3x; 'recf4UKTfipCzgcSA' occurs 1x; 'rec28ORZgcm1dtqBZ' occurs 1x; 'recTjHY5xXhvkCdVT' occurs 1x.
- `member.member_id`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: 'reccSUPwy30AeZLEb' occurs 1x; 'recT92PyyZCGq1R68' occurs 1x; 'rec3pH4DxMcWHMRB7' occurs 1x; 'recf4UKTfipCzgcSA' occurs 1x; 'rec28ORZgcm1dtqBZ' occurs 1x; 'recTjHY5xXhvkCdVT' occurs 1x.
- `member.position`: 33 rows, 0 NULL, 6 distinct values. Witness values: 'Inactive' occurs 3x; 'Member' occurs 26x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 31 (codebase_community)

**Question:** Give the only one comment text of the post with parent id 107829.

**Evidence:** one comment refers to CommentCount = '1'

**Gold SQL:**
```sql
SELECT T2.Text FROM posts AS T1 INNER JOIN comments AS T2 ON T1.Id = T2.PostId WHERE T1.ParentId = 107829 AND T1.CommentCount = 1
```
**Predicted SQL:**
```sql
SELECT T1.Text FROM comments AS T1 INNER JOIN posts AS T2 ON T1.PostId = T2.Id WHERE T2.ParentId = 107829 AND T2.CommentCount = 1 LIMIT 1
```

**Witness database:**

*comments* (5 unreferenced columns omitted)

| PostId | Text |
|---|---|
| 2 | Welcome to our site! |
| 2 | That is correct. |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 4 | 2 | 2 | 18bf9150-f1cb-432d-b7b7-26d2f8e33581 |

*posts* (18 unreferenced columns omitted)

| Id | CommentCount | ParentId |
|---|---|---|
| 2 | 1 | 107829 |

*users* (10 unreferenced columns omitted)

| Id | Reputation | CreationDate | DisplayName |
|---|---|---|---|
| 3 | 101 | 2010-07-19 15:34:50.0 | Jarrod Dixon |
| 24 | 344 | 2010-07-19 19:09:32.0 | A Lion |

**Gold result on the witness:** `[['Welcome to our site!'], ['That is correct.']]`  
**Predicted result on the witness:** `[['Welcome to our site!']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `comments.PostId`: 174,285 rows, 0 NULL, 53,416 distinct values. Witness values: 2 occurs 1x.
- `comments.Text`: 174,285 rows, 0 NULL, 173,644 distinct values. Witness values: 'Welcome to our site!' occurs 12x; 'That is correct.' occurs 5x.
- `posts.Id`: 91,966 rows, 0 NULL, 91,966 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x.
- `posts.CommentCount`: 91,966 rows, 0 NULL, 39 distinct values. Witness values: 1 occurs 15,091x.
- `posts.ParentId`: 91,966 rows, 44,211 NULL, 29,006 distinct values. Witness values: 107829 occurs 4x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 32 (formula_1)

**Question:** Who is the champion of the Canadian Grand Prix in 2008? Indicate his finish time.

**Evidence:** Only the time of the champion shows in the format of "hour: minutes: seconds.millionsecond";

**Gold SQL:**
```sql
SELECT T1.time FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId WHERE T2.name = 'Canadian Grand Prix' AND T2.year = 2008 AND T1.time LIKE '_:%:__.___'
```
**Predicted SQL:**
```sql
SELECT T2.time FROM races AS T1 INNER JOIN results AS T2 ON T1.raceId = T2.raceId INNER JOIN drivers AS T3 ON T2.driverId = T3.driverId WHERE T1.year = 2008 AND T1.name = 'Canadian Grand Prix' ORDER BY T2.points DESC LIMIT 1
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 3 | 1 | _:%:__.___ | 2008 |
| 2 | 2008 | Canadian Grand Prix | 2008 |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 2 | _:%:__.___ | _:%:__.___ | German |
| 1 | 2008 | a | NULL |

*drivers* (8 unreferenced columns omitted)

| driverId |
|---|
| 1 |
| 2008 |
| 2 |

*races* (5 unreferenced columns omitted)

| raceId | year | name |
|---|---|---|
| 1 | 1 | Canadian Grand Prix |
| 2 | 2008 | Canadian Grand Prix |

*results* (14 unreferenced columns omitted)

| raceId | driverId | points | time |
|---|---|---|---|
| 2 | 2008 | -1.5 | 2012-02-22 00:00:00 |
| 1 | 2 | 2008.0 | 2015-03-20 |

*seasons*

| year | url |
|---|---|
| 1 | Canadian Grand Prix |
| 2008 | 2008 |

*status*

| statusId | status |
|---|---|
| 2 | y2 |
| 1 | 1 |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2012-02-22 00:00:00']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 2008 occurs 0x; 2 occurs 1x.
- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 1 occurs 1x; 2 occurs 1x.
- `races.year`: 976 rows, 0 NULL, 68 distinct values. Witness values: 1 occurs 0x; 2008 occurs 18x.
- `races.name`: 976 rows, 0 NULL, 42 distinct values. Witness values: 'Canadian Grand Prix' occurs 48x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 2 occurs 20x; 1 occurs 20x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 2008 occurs 0x; 2 occurs 184x.
- `results.points`: 23,657 rows, 0 NULL, 33 distinct values. Witness values: -1.5 occurs 0x; 2008.0 occurs 0x.
- `results.time`: 23,657 rows, 17,696 NULL, 5,755 distinct values. Witness values: '2012-02-22 00:00:00' occurs 0x; '2015-03-20' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 33 (thrombosis_prediction)

**Question:** For the patient who was diagnosed SLE on 1997/1/27, what was his/her original diagnose when he/she came to the hospital for the first time?

**Evidence:** 'SLE' AND original diagnose refers to diagnosis; 1997/1/27 refer to `Examination Date` = '1997-01-27'; first came to the hospital refers to patient.`First Date`

**Gold SQL:**
```sql
SELECT T1.Diagnosis FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.ID = ( SELECT ID FROM Examination WHERE `Examination Date` = '1997-01-27' AND Diagnosis = 'SLE' ) AND T2.`Examination Date` = T1.`First Date`
```
**Predicted SQL:**
```sql
SELECT `patient`.`diagnosis` FROM `patient` INNER JOIN `examination` ON `patient`.`id` = `examination`.`id` WHERE `examination`.`diagnosis` = 'SLE' AND `examination`.`examination date` = '1997-01-27'
```

**Witness database:**

*Examination* (10 unreferenced columns omitted)

| ID | Examination Date | Diagnosis |
|---|---|---|
| 1 | 1996-04-25 | PSS |
| 1 | 1995-08-28 | MRA |
| 1 | 1997-01-27 | SLE |
| 3 | 1996-09-30 | SjS |

*Patient* (4 unreferenced columns omitted)

| ID | First Date | Diagnosis |
|---|---|---|
| 1 | 1991-06-11 | PM/DM |
| 3 | 1995-02-03 | PM |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['PM/DM']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: 1 occurs 0x; 3 occurs 0x.
- `Examination.Examination Date`: 806 rows, 10 NULL, 475 distinct values. Witness values: '1996-04-25' occurs 4x; '1995-08-28' occurs 4x; '1997-01-27' occurs 2x; '1996-09-30' occurs 4x.
- `Examination.Diagnosis`: 806 rows, 331 NULL, 181 distinct values. Witness values: 'PSS' occurs 10x; 'MRA' occurs 3x; 'SLE' occurs 95x; 'SjS' occurs 41x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 3 occurs 0x.
- `Patient.First Date`: 1,238 rows, 251 NULL, 797 distinct values. Witness values: '1991-06-11' occurs 3x; '1995-02-03' occurs 3x.
- `Patient.Diagnosis`: 1,238 rows, 0 NULL, 220 distinct values. Witness values: 'PM/DM' occurs 8x; 'PM' occurs 12x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 34 (formula_1)

**Question:** What's the fastest lap time ever in a race for Lewis Hamilton?

**Evidence:** fastest lap time ever refers to min(fastestLapTime)

**Gold SQL:**
```sql
SELECT T2.fastestLapTime FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId WHERE T1.forename = 'Lewis' AND T1.surname = 'Hamilton' AND T2.fastestLapTime IS NOT NULL ORDER BY T2.fastestLapTime ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT MIN(`results`.`fastestlaptime`) FROM `drivers` INNER JOIN `results` ON `drivers`.`driverid` = `results`.`driverid` WHERE `drivers`.`forename` = 'Lewis' AND `drivers`.`surname` = 'Hamilton'
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

## Item 35 (student_club)

**Question:** Calculate the difference of the total amount spent in all events by the Student_Club in year 2019 and 2020.

**Evidence:** The first 4 strings of the event_date values in the event table can represent year; The difference of the total amount spent = SUBTRACT(spent where YEAR(event_date) = 2019, spent where YEAR(event_date) = 2020)

**Gold SQL:**
```sql
SELECT SUM(CASE WHEN SUBSTR(T1.event_date, 1, 4) = '2019' THEN T2.spent ELSE 0 END) - SUM(CASE WHEN SUBSTR(T1.event_date, 1, 4) = '2020' THEN T2.spent ELSE 0 END) AS num FROM event AS T1 INNER JOIN budget AS T2 ON T1.event_id = T2.link_to_event
```
**Predicted SQL:**
```sql
SELECT (SELECT SUM(`spent`) FROM `budget` INNER JOIN `event` ON `budget`.`link_to_event` = `event`.`event_id` WHERE `event`.`event_date` LIKE '2019%') - (SELECT SUM(`spent`) FROM `budget` INNER JOIN `event` ON `budget`.`link_to_event` = `event`.`event_id` WHERE `event`.`event_date` LIKE '2020%')
```

**Witness database:**

*budget* (5 unreferenced columns omitted)

| spent | link_to_event |
|---|---|
| 13.45 | recAlAwtBZ0Fqbr5K |

*event* (5 unreferenced columns omitted)

| event_id | event_date |
|---|---|
| recEVTik3MlqbvLFi | 2020-02-11T09:30:00 |
| recAlAwtBZ0Fqbr5K | 2020-03-24T12:00:00 |

**Gold result on the witness:** `[[-13.45]]`  
**Predicted result on the witness:** `[[None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `budget.spent`: 52 rows, 0 NULL, 17 distinct values. Witness values: 13.45 occurs 2x.
- `budget.link_to_event`: 52 rows, 0 NULL, 23 distinct values. Witness values: 'recAlAwtBZ0Fqbr5K' occurs 4x.
- `event.event_id`: 42 rows, 0 NULL, 42 distinct values, all non-NULL values unique. Witness values: 'recEVTik3MlqbvLFi' occurs 1x; 'recAlAwtBZ0Fqbr5K' occurs 1x.
- `event.event_date`: 42 rows, 0 NULL, 41 distinct values. Witness values: '2020-02-11T09:30:00' occurs 1x; '2020-03-24T12:00:00' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 36 (thrombosis_prediction)

**Question:** Among the patients whose level of Hematoclit isn't normal, which patient has the highest anti-Cardiolipin antibody concentration? Please list his or her ID.

**Evidence:** Hematoclit is normal refers to 29 < N < 52; highest anti-Cardiolipin antibody concentration refers to MAX(`aCL IgA`);

**Gold SQL:**
```sql
SELECT DISTINCT T1.ID FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID INNER JOIN Laboratory AS T3 on T1.ID = T3.ID WHERE (T3.HCT >= 52 OR T3.HCT <= 29) ORDER BY T2.`aCL IgA` DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.ID FROM Examination AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.HCT < 29 OR T2.HCT > 52 ORDER BY T1."aCL IgA" DESC LIMIT 1
```

**Witness database:**

*Examination* (11 unreferenced columns omitted)

| ID | aCL IgA |
|---|---|
| 1 | 3 |
| 21 | 23 |
| 1 | 23 |
| NULL | NULL |
| 1 | NULL |
| 77 | NULL |
| 89 | 23 |

*Patient* (6 unreferenced columns omitted)

| ID |
|---|
| 1 |
| 21 |
| 77 |
| 89 |

*Laboratory* (42 unreferenced columns omitted)

| ID | HCT |
|---|---|
| 1 | 29.0 |
| 21 | 29.0 |
| 1 | 53.0 |
| 77 | 51.0 |
| 89 | NULL |

**Gold result on the witness:** `[[21]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: 1 occurs 0x; 21 occurs 0x; NULL occurs 36x; 77 occurs 0x; 89 occurs 0x.
- `Examination.aCL IgA`: 806 rows, 0 NULL, 52 distinct values. Witness values: 3 occurs 64x; 23 occurs 1x; NULL occurs 0x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 21 occurs 0x; 77 occurs 0x; 89 occurs 0x.
- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 1 occurs 0x; 21 occurs 0x; 77 occurs 0x; 89 occurs 0x.
- `Laboratory.HCT`: 13,908 rows, 1,827 NULL, 363 distinct values. Witness values: 29.0 occurs 16x; 53.0 occurs 1x; 51.0 occurs 0x; NULL occurs 1,827x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 37 (financial)

**Question:** How many accounts have an owner disposition and request for a statement to be generated upon a transaction?

**Evidence:** Frequency = 'POPLATEK PO OBRATU' stands for issuance after transaction

**Gold SQL:**
```sql
SELECT COUNT(T1.account_id) FROM account AS T1 INNER JOIN disp AS T2 ON T1.account_id = T2.account_id WHERE T2.type = 'OWNER' AND T1.frequency = 'POPLATEK PO OBRATU'
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT account.account_id) FROM account JOIN disp ON account.account_id = disp.account_id WHERE disp.type = 'OWNER' AND account.frequency = 'POPLATEK PO OBRATU';
```

**Witness database:**

*account* (2 unreferenced columns omitted)

| account_id | frequency |
|---|---|
| 0 | POPLATEK PO OBRATU |
| -1 | POPLATEK PO OBRATU |

*card*

| card_id | disp_id | type | issued |
|---|---|---|---|
| -1 | 0 | 2147483648 | 1000-01-01 |
| 0 | 0 | 2147483648 | 1000-01-01 |

*client*

| client_id | gender | birth_date | district_id |
|---|---|---|---|
| 0 | 2147483648 | 1000-01-01 | 0 |
| 1 | 2147483648 | 1000-01-01 | 0 |

*disp* (2 unreferenced columns omitted)

| account_id | type |
|---|---|
| 0 | OWNER |
| 0 | OWNER |

*district* (12 unreferenced columns omitted)

| district_id | A2 | A3 | A4 |
|---|---|---|---|
| 0 | 2147483648 | 2147483648 | 2147483648 |
| 1 | 2147483648 | 2147483648 | 2147483648 |

*loan* (3 unreferenced columns omitted)

| loan_id | account_id | date | amount |
|---|---|---|---|
| -1 | 0 | 1000-01-01 | 0 |
| 0 | 0 | 1000-01-01 | 0 |

*order* (2 unreferenced columns omitted)

| order_id | account_id | bank_to | account_to |
|---|---|---|---|
| -1 | 0 | 2147483648 | 0 |
| 0 | 0 | 2147483648 | 0 |

*trans* (6 unreferenced columns omitted)

| trans_id | account_id | date | type |
|---|---|---|---|
| -1 | 0 | 1000-01-01 | 2147483648 |
| 0 | 0 | 1000-01-01 | 2147483648 |

**Gold result on the witness:** `[[2]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `account.account_id`: 4,500 rows, 0 NULL, 4,500 distinct values, all non-NULL values unique. Witness values: 0 occurs 0x; -1 occurs 0x.
- `account.frequency`: 4,500 rows, 0 NULL, 3 distinct values. Witness values: 'POPLATEK PO OBRATU' occurs 93x.
- `disp.account_id`: 5,369 rows, 0 NULL, 4,500 distinct values. Witness values: 0 occurs 0x.
- `disp.type`: 5,369 rows, 0 NULL, 2 distinct values. Witness values: 'OWNER' occurs 4,500x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 38 (superhero)

**Question:** Which publisher created more superheroes: DC or Marvel Comics? Find the difference in the number of superheroes.

**Evidence:** DC refers to publisher_name = 'DC Comics'; Marvel Comics refers to publisher_name = 'Marvel Comics'; difference = SUBTRACT(SUM(publisher_name = 'DC Comics'), SUM(publisher_name = 'Marvel Comics'));

**Gold SQL:**
```sql
SELECT SUM(CASE WHEN T2.publisher_name = 'DC Comics' THEN 1 ELSE 0 END) - SUM(CASE WHEN T2.publisher_name = 'Marvel Comics' THEN 1 ELSE 0 END) FROM superhero AS T1 INNER JOIN publisher AS T2 ON T1.publisher_id = T2.id
```
**Predicted SQL:**
```sql
SELECT COUNT(CASE WHEN `publisher`.`publisher_name` = 'DC Comics' THEN `superhero`.`id` ELSE NULL END) - COUNT(CASE WHEN `publisher`.`publisher_name` = 'Marvel Comics' THEN `superhero`.`id` ELSE NULL END) AS difference FROM `superhero` INNER JOIN `publisher` ON `superhero`.`publisher_id` = `publisher`.`id`
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
| 22 | Team Epic TV |

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

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `publisher.id`: 25 rows, 0 NULL, 25 distinct values, all non-NULL values unique. Witness values: 22 occurs 1x.
- `publisher.publisher_name`: 25 rows, 0 NULL, 25 distinct values, all non-NULL values unique. Witness values: 'Team Epic TV' occurs 1x.
- `superhero.id`: 750 rows, 0 NULL, 750 distinct values, all non-NULL values unique. Witness values: 613 occurs 1x.
- `superhero.publisher_id`: 750 rows, 3 NULL, 25 distinct values. Witness values: NULL occurs 3x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 39 (toxicology)

**Question:** Determine the bond type that is formed in the chemical compound containing element Carbon.

**Evidence:** Carbon refers to element = 'c'; double bond refers to bond_type = ' = '; single bond refers to bond_type = '-'; triple bond refers to bond_type = '#';

**Gold SQL:**
```sql
SELECT DISTINCT T2.bond_type FROM atom AS T1 INNER JOIN bond AS T2 ON T1.molecule_id = T2.molecule_id WHERE T1.element = 'c'
```
**Predicted SQL:**
```sql
SELECT DISTINCT `bond`.`bond_type` FROM `bond` INNER JOIN `connected` ON `bond`.`bond_id` = `connected`.`bond_id` INNER JOIN `atom` ON `connected`.`atom_id` = `atom`.`atom_id` OR `connected`.`atom_id2` = `atom`.`atom_id` WHERE `atom`.`element` = 'c'
```

**Witness database:**

*atom*

| atom_id | molecule_id | element |
|---|---|---|
| TR000_3 | TR496 | c |
| TR000_2 | TR000 | c |
| TR000_1 | TR000 | cl |
| TR001_19 | TR060 | h |

*bond*

| bond_id | molecule_id | bond_type |
|---|---|---|
| TR000_2_4 | TR496 | = |
| TR000_2_5 | TR060 | # |
| TR000_2_3 | TR000 | - |

*connected*

| atom_id | atom_id2 | bond_id |
|---|---|---|
| TR000_3 | TR000_2 | TR000_2_4 |
| TR000_2 | TR000_3 | TR000_2_3 |
| TR000_1 | TR000_3 | TR000_2_5 |
| TR000_3 | TR000_1 | TR000_2_5 |

*molecule*

| molecule_id | label |
|---|---|
| TR496 | + |
| TR060 | - |
| TR000 | + |

**Gold result on the witness:** `[['='], ['-']]`  
**Predicted result on the witness:** `[['='], ['-'], ['#']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `atom.atom_id`: 12,333 rows, 0 NULL, 12,333 distinct values, all non-NULL values unique. Witness values: 'TR000_3' occurs 1x; 'TR000_2' occurs 1x; 'TR000_1' occurs 1x; 'TR001_19' occurs 1x.
- `atom.molecule_id`: 12,333 rows, 0 NULL, 444 distinct values. Witness values: 'TR496' occurs 109x; 'TR000' occurs 5x; 'TR060' occurs 103x.
- `atom.element`: 12,333 rows, 0 NULL, 21 distinct values. Witness values: 'c' occurs 4,605x; 'cl' occurs 429x; 'h' occurs 5,518x.
- `bond.bond_id`: 12,379 rows, 0 NULL, 12,379 distinct values, all non-NULL values unique. Witness values: 'TR000_2_4' occurs 1x; 'TR000_2_5' occurs 1x; 'TR000_2_3' occurs 1x.
- `bond.molecule_id`: 12,379 rows, 0 NULL, 444 distinct values. Witness values: 'TR496' occurs 108x; 'TR060' occurs 107x; 'TR000' occurs 4x.
- `bond.bond_type`: 12,379 rows, 1 NULL, 3 distinct values. Witness values: '=' occurs 1,844x; '#' occurs 6x; '-' occurs 10,528x.
- `connected.atom_id`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'TR000_3' occurs 1x; 'TR000_2' occurs 4x; 'TR000_1' occurs 1x.
- `connected.atom_id2`: 24,758 rows, 0 NULL, 12,284 distinct values. Witness values: 'TR000_2' occurs 4x; 'TR000_3' occurs 1x; 'TR000_1' occurs 1x.
- `connected.bond_id`: 24,758 rows, 0 NULL, 12,379 distinct values. Witness values: 'TR000_2_4' occurs 2x; 'TR000_2_3' occurs 2x; 'TR000_2_5' occurs 2x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 40 (california_schools)

**Question:** Which county reported the most number of school closure in the 1980s with school wonership code belonging to Youth Authority Facilities (CEA)?

**Evidence:** Youth Authority Facilities (CEA) refers to SOC = 11; 1980s = years between 1980 and 1989

**Gold SQL:**
```sql
SELECT County FROM schools WHERE strftime('%Y', ClosedDate) BETWEEN '1980' AND '1989' AND StatusType = 'Closed' AND SOC = 11 GROUP BY County ORDER BY COUNT(School) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT County FROM schools WHERE SOC = 11 AND ClosedDate BETWEEN '1980-01-01' AND '1989-12-31' GROUP BY County ORDER BY COUNT(*) DESC LIMIT 1;
```

**Witness database:**

*schools* (44 unreferenced columns omitted)

| StatusType | County | School | ClosedDate | SOC |
|---|---|---|---|---|
| Closed | A | c | 1980-01-01 | 11 |
| Closed | a | NULL | 1980-01-01 | 11 |

**Gold result on the witness:** `[['A']]`  
**Predicted result on the witness:** `[['a']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `schools.StatusType`: 17,686 rows, 0 NULL, 4 distinct values. Witness values: 'Closed' occurs 4,518x.
- `schools.County`: 17,686 rows, 0 NULL, 58 distinct values. Witness values: 'A' occurs 0x; 'a' occurs 0x.
- `schools.School`: 17,686 rows, 1,369 NULL, 13,875 distinct values. Witness values: 'c' occurs 0x; NULL occurs 1,369x.
- `schools.ClosedDate`: 17,686 rows, 11,992 NULL, 899 distinct values. Witness values: '1980-01-01' occurs 0x.
- `schools.SOC`: 17,686 rows, 1,369 NULL, 20 distinct values. Witness values: '11' occurs 43x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 41 (codebase_community)

**Question:** How many comments and answers were left by the users on the post with the title 'Clustering 1D data'?

**Evidence:** -

**Gold SQL:**
```sql
SELECT CommentCount, AnswerCount FROM posts WHERE Title = 'Clustering 1D data'
```
**Predicted SQL:**
```sql
SELECT COUNT(T1.Id), T2.AnswerCount FROM comments AS T1 INNER JOIN posts AS T2 ON T1.PostId = T2.Id WHERE T2.Title = 'Clustering 1D data'
```

**Witness database:**

*comments* (5 unreferenced columns omitted)

| Id | PostId |
|---|---|
| 179273 | 91513 |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 307543 | 2 | 91513 | 83eb0b31-12ca-443d-9cbd-3820041aed2f |

*posts* (17 unreferenced columns omitted)

| Id | Title | AnswerCount | CommentCount |
|---|---|---|---|
| 91513 | NULL | NULL | 8 |

*users* (10 unreferenced columns omitted)

| Id | Reputation | CreationDate | DisplayName |
|---|---|---|---|
| 805 | 65272 | 2010-08-07 08:40:07.0 | Glen_b |
| 32036 | 7227 | 2013-10-29 12:42:40.0 | Nick Stauner |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[[0, None]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `comments.Id`: 174,285 rows, 0 NULL, 174,285 distinct values, all non-NULL values unique. Witness values: 179273 occurs 1x.
- `comments.PostId`: 174,285 rows, 0 NULL, 53,416 distinct values. Witness values: 91513 occurs 8x.
- `posts.Id`: 91,966 rows, 0 NULL, 91,966 distinct values, all non-NULL values unique. Witness values: 91513 occurs 1x.
- `posts.Title`: 91,966 rows, 49,054 NULL, 42,877 distinct values. Witness values: NULL occurs 49,054x.
- `posts.AnswerCount`: 91,966 rows, 49,054 NULL, 31 distinct values. Witness values: NULL occurs 49,054x.
- `posts.CommentCount`: 91,966 rows, 0 NULL, 39 distinct values. Witness values: 8 occurs 1,210x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 42 (formula_1)

**Question:** What is the average lap time in milliseconds of all the lap records set on the various circuits in Italy?

**Evidence:** average = AVG(milliseconds)

**Gold SQL:**
```sql
SELECT CAST(SUM(T1.milliseconds) AS REAL) / COUNT(T1.lap) FROM lapTimes AS T1 INNER JOIN races AS T2 on T1.raceId = T2.raceId INNER JOIN circuits AS T3 on T2.circuitId = T3.circuitId WHERE T3.country = 'Italy'
```
**Predicted SQL:**
```sql
SELECT AVG(`laptimes`.`milliseconds`) FROM `laptimes` INNER JOIN `races` ON `laptimes`.`raceid` = `races`.`raceid` INNER JOIN `circuits` ON `races`.`circuitid` = `circuits`.`circuitid` WHERE `circuits`.`country` = 'Italy'
```

**Witness database:**

*circuits* (7 unreferenced columns omitted)

| circuitId | country |
|---|---|
| 1001 | Italy |
| 1026 | Italy |

*drivers* (5 unreferenced columns omitted)

| driverId | driverRef | number | code |
|---|---|---|---|
| 1002 | y2 | NULL | NULL |
| 1027 | c | 1 | A |

*lapTimes* (3 unreferenced columns omitted)

| raceId | lap | milliseconds |
|---|---|---|
| 1003 | 1004 | NULL |
| 1028 | 1029 | 2 |

*races* (6 unreferenced columns omitted)

| raceId | circuitId |
|---|---|
| 1003 | 1001 |
| 1028 | 1026 |

*seasons*

| year | url |
|---|---|
| 1005 | b |
| 1030 | a |

**Gold result on the witness:** `[[1.0]]`  
**Predicted result on the witness:** `[[2.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `circuits.circuitId`: 72 rows, 0 NULL, 72 distinct values, all non-NULL values unique. Witness values: 1001 occurs 0x; 1026 occurs 0x.
- `circuits.country`: 72 rows, 0 NULL, 32 distinct values. Witness values: 'Italy' occurs 3x.
- `lapTimes.raceId`: 420,369 rows, 0 NULL, 389 distinct values. Witness values: 1003 occurs 0x; 1028 occurs 0x.
- `lapTimes.lap`: 420,369 rows, 0 NULL, 78 distinct values. Witness values: 1004 occurs 0x; 1029 occurs 0x.
- `lapTimes.milliseconds`: 420,369 rows, 0 NULL, 67,578 distinct values. Witness values: NULL occurs 0x; 2 occurs 0x.
- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 1003 occurs 0x; 1028 occurs 0x.
- `races.circuitId`: 976 rows, 0 NULL, 72 distinct values. Witness values: 1001 occurs 0x; 1026 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 43 (codebase_community)

**Question:** What is the id of the youngest user?

**Evidence:** the youngest user refers to MIN(Age);

**Gold SQL:**
```sql
SELECT Id FROM users WHERE Age = ( SELECT MIN(Age) FROM users )
```
**Predicted SQL:**
```sql
SELECT Id FROM users WHERE Age IS NOT NULL ORDER BY Age ASC LIMIT 1;
```

**Witness database:**

*users* (12 unreferenced columns omitted)

| Id | Age |
|---|---|
| 1 | 25 |
| 2 | 28 |
| 3 | 25 |

**Gold result on the witness:** `[[1], [3]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `users.Id`: 40,325 rows, 0 NULL, 40,325 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 2 occurs 1x; 3 occurs 1x.
- `users.Age`: 40,325 rows, 32,007 NULL, 70 distinct values. Witness values: 25 occurs 536x; 28 occurs 557x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 44 (thrombosis_prediction)

**Question:** For the year that concluded on December 31, 1998, how many male patients on average were tested in the lab each month?

**Evidence:** the year that concluded on December 31, 1998 refers to Date BETWEEN '1998-01-01' AND '1998-12-31'; male refers to SEX = 'M'; calculation = DIVIDE(COUNT(ID), 12)

**Gold SQL:**
```sql
SELECT CAST(COUNT(T1.ID) AS REAL) / 12 FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE STRFTIME('%Y', T2.Date) = '1998' AND T1.SEX = 'M'
```
**Predicted SQL:**
```sql
SELECT AVG(total_patients_per_month) AS average_patients_per_month FROM(SELECT STRFTIME('%m', L.`Date`) AS month, COUNT(P.ID) AS total_patients_per_month FROM Laboratory AS L INNER JOIN Patient AS P ON L.ID = P.ID WHERE P.SEX = 'M' AND L.`Date` BETWEEN '1998-01-01' AND '1998-12-31' GROUP BY STRFTIME('%m', L.`Date`) ) AS subquery
```

**Witness database:**

*Laboratory* (42 unreferenced columns omitted)

| ID | Date |
|---|---|
| 1998 | 2015-03-20 |
| 3 | 1995-12-31 |
| 3 | 1998-01-01 |
| 12 | 1998-12-31 |

*Patient* (5 unreferenced columns omitted)

| ID | SEX |
|---|---|
| 2 | F |
| 1998 | F |
| 3 | F |
| 12 | M |

**Gold result on the witness:** `[[0.08333333333333333]]`  
**Predicted result on the witness:** `[[1.0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Laboratory.ID`: 13,908 rows, 0 NULL, 302 distinct values. Witness values: 1998 occurs 0x; 3 occurs 0x; 12 occurs 0x.
- `Laboratory.Date`: 13,908 rows, 0 NULL, 3,723 distinct values. Witness values: '2015-03-20' occurs 0x; '1995-12-31' occurs 0x; '1998-01-01' occurs 0x; '1998-12-31' occurs 0x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 2 occurs 0x; 1998 occurs 0x; 3 occurs 0x; 12 occurs 0x.
- `Patient.SEX`: 1,238 rows, 0 NULL, 3 distinct values. Witness values: 'F' occurs 1,023x; 'M' occurs 202x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 45 (codebase_community)

**Question:** Write down the related posts titles and link type IDs of the post "What are principal component scores?".

**Evidence:** Title = 'What are principal component scores?';

**Gold SQL:**
```sql
SELECT T3.Title, T2.LinkTypeId FROM posts AS T1 INNER JOIN postLinks AS T2 ON T1.Id = T2.PostId INNER JOIN posts AS T3 ON T2.RelatedPostId = T3.Id WHERE T1.Title = 'What are principal component scores?'
```
**Predicted SQL:**
```sql
SELECT p.Title, pl.LinkTypeId FROM postLinks AS pl INNER JOIN posts AS p ON pl.RelatedPostId = p.Id WHERE pl.PostId = (SELECT Id FROM posts WHERE Title = 'What are principal component scores?');
```

**Witness database:**

*postLinks* (1 unreferenced columns omitted)

| Id | PostId | RelatedPostId | LinkTypeId |
|---|---|---|---|
| 2 | 3 | 2 | 5 |
| 3 | 2 | 1 | 10 |

*posts* (19 unreferenced columns omitted)

| Id | Title |
|---|---|
| 2 | What are principal component scores? |
| 1 | What are principal component scores? |
| 3 | y2 |

*users* (10 unreferenced columns omitted)

| Id | Reputation | CreationDate | DisplayName |
|---|---|---|---|
| 1 | 3 | 2015-03-20 08:00:00 | What are principal component scores? |
| 3 | 3 | 2020-02-29 23:59:59 | y2 |

**Gold result on the witness:** `[['What are principal component scores?', 10]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `postLinks.Id`: 11,102 rows, 0 NULL, 11,102 distinct values, all non-NULL values unique. Witness values: 2 occurs 0x; 3 occurs 0x.
- `postLinks.PostId`: 11,102 rows, 0 NULL, 7,604 distinct values. Witness values: 3 occurs 0x; 2 occurs 0x.
- `postLinks.RelatedPostId`: 11,102 rows, 0 NULL, 5,177 distinct values. Witness values: 2 occurs 2x; 1 occurs 4x.
- `postLinks.LinkTypeId`: 11,102 rows, 0 NULL, 2 distinct values. Witness values: 5 occurs 0x; 10 occurs 0x.
- `posts.Id`: 91,966 rows, 0 NULL, 91,966 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 1 occurs 1x; 3 occurs 1x.
- `posts.Title`: 91,966 rows, 49,054 NULL, 42,877 distinct values. Witness values: 'What are principal component scores?' occurs 1x; 'y2' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 46 (european_football_2)

**Question:** Among the players born before the year 1986, how many of them would remain in his position and defense while the team attacked?

**Evidence:** players born before the year 1986 refers to strftime('%Y', birthday)<'1986'; players who would remain in his position and defense while the team attacked refers to defensive_work_rate = 'high'; Should consider DISTINCT in the final result;

**Gold SQL:**
```sql
SELECT COUNT(DISTINCT t1.player_name) FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id WHERE STRFTIME('%Y',t1.birthday) < '1986' AND t2.defensive_work_rate = 'high'
```
**Predicted SQL:**
```sql
SELECT COUNT(DISTINCT T1.player_api_id) FROM Player AS T1 INNER JOIN Player_Attributes AS T2 ON T1.player_api_id = T2.player_api_id WHERE SUBSTR(T1.birthday, 1, 4) < '1986' AND T2.defensive_work_rate = 'high'
```

**Witness database:**

*Player_Attributes* (40 unreferenced columns omitted)

| player_api_id | defensive_work_rate |
|---|---|
| 1 | high |
| 1 | high |
| 1 | high |
| NULL | high |
| 2 | high |
| 127 | high |
| 1 | medium |
| 1 | NULL |

*Player* (4 unreferenced columns omitted)

| player_api_id | player_name | birthday |
|---|---|---|
| 1 | b | 1985-01-01 00:00:00 |
| 42 | h | 2000-01-09 |
| 1 | NULL | 1985-01-01 00:00:00 |
| 1 | NULL | 1985-01-01 00:00:00 |
| NULL | NULL | 1985-01-01 00:00:00 |
| 2 | NULL | 1986-01-01 00:00:00 |
| 127 | q | NULL |
| 1 | NULL | 1985-01-01 00:00:00 |
| 1 | q | 1985-01-01 00:00:00 |

**Gold result on the witness:** `[[2]]`  
**Predicted result on the witness:** `[[1]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 1 occurs 0x; NULL occurs 0x; 2 occurs 0x; 127 occurs 0x.
- `Player_Attributes.defensive_work_rate`: 183,978 rows, 836 NULL, 19 distinct values. Witness values: 'high' occurs 27,041x; 'medium' occurs 130,846x; NULL occurs 836x.
- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 42 occurs 0x; NULL occurs 0x; 2 occurs 0x; 127 occurs 0x.
- `Player.player_name`: 11,060 rows, 0 NULL, 10,848 distinct values. Witness values: 'b' occurs 0x; 'h' occurs 0x; NULL occurs 0x; 'q' occurs 0x.
- `Player.birthday`: 11,060 rows, 0 NULL, 5,762 distinct values. Witness values: '1985-01-01 00:00:00' occurs 4x; '2000-01-09' occurs 0x; '1986-01-01 00:00:00' occurs 3x; NULL occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 47 (formula_1)

**Question:** What is full name of the racer who ranked 1st in the 3rd qualifying race held in the Marina Bay Street Circuit in 2008?

**Evidence:** Ranked 1st in the 3rd qualifying race refer to MIN(q3); 2008 is the year of race; full name of racer = forename, surname

**Gold SQL:**
```sql
SELECT T2.forename, T2.surname FROM qualifying AS T1 INNER JOIN drivers AS T2 on T1.driverId = T2.driverId INNER JOIN races AS T3 ON T1.raceid = T3.raceid WHERE q3 IS NOT NULL AND T3.year = 2008 AND T3.circuitId IN ( SELECT circuitId FROM circuits WHERE name = 'Marina Bay Street Circuit' ) ORDER BY CAST(SUBSTR(q3, 1, INSTR(q3, ':') - 1) AS INTEGER) * 60 + CAST(SUBSTR(q3, INSTR(q3, ':') + 1, INSTR(q3, '.') - INSTR(q3, ':') - 1) AS REAL) + CAST(SUBSTR(q3, INSTR(q3, '.') + 1) AS REAL) / 1000 ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T1.forename, T1.surname FROM drivers AS T1 INNER JOIN qualifying AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T2.raceId = T3.raceId WHERE T2.position = 1 AND T3.year = 2008 AND T3.circuitId IN (SELECT circuitId FROM circuits WHERE name = 'Marina Bay Street Circuit')
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

## Item 48 (formula_1)

**Question:** Which was Lewis Hamilton first race? What was his points recorded for his first race event?

**Evidence:** first race refers to min(Year); Lewis Hamiltonrefers to the full name of the driver; Full name of the driver refers to drivers.forename and drivers.surname;

**Gold SQL:**
```sql
SELECT T1.name, T2.points FROM races AS T1 INNER JOIN driverStandings AS T2 ON T2.raceId = T1.raceId INNER JOIN drivers AS T3 ON T3.driverId = T2.driverId WHERE T3.forename = 'Lewis' AND T3.surname = 'Hamilton' ORDER BY T1.year ASC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T2.name, T1.points FROM results AS T1 INNER JOIN races AS T2 ON T1.raceId = T2.raceId INNER JOIN drivers AS T3 ON T3.driverId = T1.driverId WHERE T3.forename = 'Lewis' AND T3.surname = 'Hamilton' ORDER BY T2.year ASC LIMIT 1
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

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `driverStandings.raceId`: 31,578 rows, 0 NULL, 970 distinct values. Witness values: 1 occurs 15x; 3 occurs 20x.
- `driverStandings.driverId`: 31,578 rows, 0 NULL, 833 distinct values. Witness values: 3 occurs 206x; 1 occurs 201x.
- `driverStandings.points`: 31,578 rows, 0 NULL, 337 distinct values. Witness values: 14.0 occurs 230x; 18.0 occurs 228x.
- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 3 occurs 1x; 1 occurs 1x.
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: 'Johnny' occurs 9x; 'Nico' occurs 2x; 'Lewis' occurs 1x.
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: 'Lewis' occurs 1x; 'Rosberg' occurs 2x; 'Hamilton' occurs 2x.
- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 1 occurs 1x; 3 occurs 1x; 172 occurs 1x.
- `races.year`: 976 rows, 0 NULL, 68 distinct values. Witness values: 1952 occurs 8x; 2009 occurs 17x; 2000 occurs 17x.
- `races.name`: 976 rows, 0 NULL, 42 distinct values. Witness values: 'South African Grand Prix' occurs 23x; 'Australian Grand Prix' occurs 33x; 'Chinese Grand Prix' occurs 14x; 'United States Grand Prix' occurs 39x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 2 occurs 20x; 172 occurs 22x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 3 occurs 206x; 1 occurs 202x; 2 occurs 184x.
- `results.points`: 23,657 rows, 0 NULL, 33 distinct values. Witness values: 0.0 occurs 17,037x; 1.0 occurs 913x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 49 (student_club)

**Question:** List out the full name and total cost that member id "rec4BLdZHS2Blfp4v" incurred?

**Evidence:** full name refers to first_name, last name

**Gold SQL:**
```sql
SELECT T1.first_name, T1.last_name, SUM(T2.cost) FROM member AS T1 INNER JOIN expense AS T2 ON T1.member_id = T2.link_to_member WHERE T1.member_id = 'rec4BLdZHS2Blfp4v'
```
**Predicted SQL:**
```sql
SELECT member.first_name, member.last_name, SUM(expense.cost) AS total_cost FROM member INNER JOIN expense ON member.member_id = expense.link_to_member WHERE member.member_id = 'rec4BLdZHS2Blfp4v' GROUP BY member.first_name, member.last_name
```

**Witness database:**

*budget* (3 unreferenced columns omitted)

| budget_id | category | spent | remaining |
|---|---|---|---|
| rec1bG6HSft7XIvTP | Food | 121.14 | 28.86 |

*event* (3 unreferenced columns omitted)

| event_id | event_name | event_date | type |
|---|---|---|---|
| recggMW2eyCYceNcy | October Meeting | 2019-10-08T12:00:00 | Meeting |

*expense* (5 unreferenced columns omitted)

| cost | link_to_member |
|---|---|
| 54.25 | recro8T1MPMwRadVH |
| 20.2 | recro8T1MPMwRadVH |

*major*

| major_id | major_name | department | college |
|---|---|---|---|
| rec1N0upiVLy5esTO | Forest Ecology and Management | Wildland Resources Department | College of Natural Resources |
| rec1SiX2nFrkbTleH | Biological Engineering | Biological Engineering Department | College of Engineering |
| rec09LedkREyskCNv | Agricultural Communication | School of Applied Sciences, Technology and Education | College of Agriculture and Applied Sciences |

*member* (6 unreferenced columns omitted)

| member_id | first_name | last_name |
|---|---|---|
| rec4BLdZHS2Blfp4v | Sacha | Harrison |
| recro8T1MPMwRadVH | Elijah | Allen |

*zip_code* (2 unreferenced columns omitted)

| zip_code | type | city | county |
|---|---|---|---|
| 3 | Standard | Vernon Center | Blue Earth County |
| 1 | Standard | Norwich | Windsor County |

**Gold result on the witness:** `[[None, None, None]]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `expense.cost`: 32 rows, 0 NULL, 21 distinct values. Witness values: 54.25 occurs 3x; 20.2 occurs 3x.
- `expense.link_to_member`: 32 rows, 0 NULL, 3 distinct values. Witness values: 'recro8T1MPMwRadVH' occurs 9x.
- `member.member_id`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: 'rec4BLdZHS2Blfp4v' occurs 1x; 'recro8T1MPMwRadVH' occurs 1x.
- `member.first_name`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: 'Sacha' occurs 1x; 'Elijah' occurs 1x.
- `member.last_name`: 33 rows, 0 NULL, 33 distinct values, all non-NULL values unique. Witness values: 'Harrison' occurs 1x; 'Allen' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 50 (formula_1)

**Question:** Who was the champion of 2008's Australian Grand Prix and where can I know more about him?

**Evidence:** only champion's finished time is represented by 'HH:MM:SS.mmm'; where can I know more refers to url

**Gold SQL:**
```sql
SELECT T1.forename, T1.surname, T1.url FROM drivers AS T1 INNER JOIN results AS T2 ON T1.driverId = T2.driverId INNER JOIN races AS T3 ON T3.raceId = T2.raceId WHERE T3.name = 'Australian Grand Prix' AND T2.time LIKE '_:%:__.___' AND T3.year = 2008
```
**Predicted SQL:**
```sql
SELECT T3.forename, T3.surname, T3.url FROM races AS T1 INNER JOIN results AS T2 ON T1.raceid = T2.raceid INNER JOIN drivers AS T3 ON T2.driverid = T3.driverid WHERE T1.name = 'Australian Grand Prix' AND T1.year = 2008 AND T2.position = 1
```

**Witness database:**

*circuits* (5 unreferenced columns omitted)

| circuitId | circuitRef | name | location |
|---|---|---|---|
| 1030 | reims | Reims-Gueux | Reims |

*constructors* (1 unreferenced columns omitted)

| constructorId | constructorRef | name | nationality |
|---|---|---|---|
| 1031 | osca | OSCA | Italian |

*drivers* (5 unreferenced columns omitted)

| driverId | forename | surname | url |
|---|---|---|---|
| 1032 | Jacques | Taylor | http://en.wikipedia.org/wiki/Alexander_Rossi_%28racing_drive |

*races* (5 unreferenced columns omitted)

| raceId | year | name |
|---|---|---|
| 1033 | 2008 | Australian Grand Prix |

*results* (14 unreferenced columns omitted)

| raceId | driverId | position | time |
|---|---|---|---|
| 1033 | 1032 | 19 | 1:34:50.616 |

*seasons*

| year | url |
|---|---|
| 2008 | http://en.wikipedia.org/wiki/2008_Formula_One_season |

*status*

| statusId | status |
|---|---|
| 1 | Finished |

**Gold result on the witness:** `[['Jacques', 'Taylor', 'http://en.wikipedia.org/wiki/Alexander_Rossi_%28racing_driver%29']]`  
**Predicted result on the witness:** `[]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `drivers.driverId`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 1032 occurs 0x.
- `drivers.forename`: 840 rows, 0 NULL, 465 distinct values. Witness values: 'Jacques' occurs 5x.
- `drivers.surname`: 840 rows, 0 NULL, 784 distinct values. Witness values: 'Taylor' occurs 5x.
- `drivers.url`: 840 rows, 0 NULL, 840 distinct values, all non-NULL values unique. Witness values: 'http://en.wikipedia.org/wiki/Alexander_Rossi_%28r occurs 1x.
- `races.raceId`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: 1033 occurs 0x.
- `races.year`: 976 rows, 0 NULL, 68 distinct values. Witness values: 2008 occurs 18x.
- `races.name`: 976 rows, 0 NULL, 42 distinct values. Witness values: 'Australian Grand Prix' occurs 33x.
- `results.raceId`: 23,657 rows, 0 NULL, 970 distinct values. Witness values: 1033 occurs 0x.
- `results.driverId`: 23,657 rows, 0 NULL, 840 distinct values. Witness values: 1032 occurs 0x.
- `results.position`: 23,657 rows, 10,528 NULL, 33 distinct values. Witness values: 19 occurs 101x.
- `results.time`: 23,657 rows, 17,696 NULL, 5,755 distinct values. Witness values: '1:34:50.616' occurs 1x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 51 (thrombosis_prediction)

**Question:** For the patient who was diagnosed SLE on 1997/1/27, what was his/her original diagnose when he/she came to the hospital for the first time?

**Evidence:** 'SLE' AND original diagnose refers to diagnosis; 1997/1/27 refer to `Examination Date` = '1997-01-27'; first came to the hospital refers to patient.`First Date`

**Gold SQL:**
```sql
SELECT T1.Diagnosis FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T1.ID = ( SELECT ID FROM Examination WHERE `Examination Date` = '1997-01-27' AND Diagnosis = 'SLE' ) AND T2.`Examination Date` = T1.`First Date`
```
**Predicted SQL:**
```sql
SELECT T2.Diagnosis FROM Examination AS T1 INNER JOIN Patient AS T2 ON T1.ID = T2.ID WHERE T1.Diagnosis = 'SLE' AND T1.`Examination Date` = '1997-01-27'
```

**Witness database:**

*Examination* (10 unreferenced columns omitted)

| ID | Examination Date | Diagnosis |
|---|---|---|
| 3 | 2020-02-29 | SLE |
| 1 | 1997-01-27 | SLE |
| 3 | 2015-03-20 | a |

*Patient* (4 unreferenced columns omitted)

| ID | First Date | Diagnosis |
|---|---|---|
| 2 | 1997-01-27 | b |
| 3 | 1997-01-27 | 1997-01-27 |
| 1 | 2015-03-20 | b |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['b']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: 3 occurs 0x; 1 occurs 0x.
- `Examination.Examination Date`: 806 rows, 10 NULL, 475 distinct values. Witness values: '2020-02-29' occurs 0x; '1997-01-27' occurs 2x; '2015-03-20' occurs 0x.
- `Examination.Diagnosis`: 806 rows, 331 NULL, 181 distinct values. Witness values: 'SLE' occurs 95x; 'a' occurs 0x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 2 occurs 0x; 3 occurs 0x; 1 occurs 0x.
- `Patient.First Date`: 1,238 rows, 251 NULL, 797 distinct values. Witness values: '1997-01-27' occurs 1x; '2015-03-20' occurs 0x.
- `Patient.Diagnosis`: 1,238 rows, 0 NULL, 220 distinct values. Witness values: 'b' occurs 0x; '1997-01-27' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 52 (thrombosis_prediction)

**Question:** For the patient who first came to the hospital on 1991/6/13 who was diagnosed with SJS, what is the total number of his/her Laboratory tests in 1995?

**Evidence:** 1991/6/13 refers to `First Date` = '1991-06-13'; 'SJS' refers to Diagnosis; total number of his/her Laboratory tests refers to COUNT(ID); 1995 refers to Date

**Gold SQL:**
```sql
SELECT COUNT(*) FROM Laboratory WHERE ID = ( SELECT ID FROM Patient WHERE `First Date` = '1991-06-13' AND Diagnosis = 'SJS' ) AND STRFTIME('%Y', Date) = '1995'
```
**Predicted SQL:**
```sql
SELECT COUNT(*) AS count_lab_tests_1995 FROM Laboratory AS lab JOIN Patient AS p ON lab.ID = p.ID WHERE p.`First Date` = '1991-06-13' AND p.Diagnosis = 'SJS' AND lab.`Date` BETWEEN '1995-01-01' AND '1995-12-31'
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

## Item 53 (california_schools)

**Question:** What is the educational level name for the schools with Breakfast Provision 2 in county code 37? Indicate the name of the school.

**Evidence:** -

**Gold SQL:**
```sql
SELECT T2.EILName, T2.School FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`NSLP Provision Status` = 'Breakfast Provision 2' AND T1.`County Code` = 37
```
**Predicted SQL:**
```sql
SELECT T1.EILName, T2."School Name" 
FROM schools AS T1 
INNER JOIN frpm AS T2 ON T1.CDSCode = T2.CDSCode 
WHERE T2."County Code" = '37' AND T2."NSLP Provision Status" = 'Breakfast Provision 2';
```

**Witness database:**

*frpm* (25 unreferenced columns omitted)

| CDSCode | County Code | School Name | NSLP Provision Status |
|---|---|---|---|
| 37682056038608 | 37 | Lemon Grove Academy for the Sciences and Humanities | Breakfast Provision 2 |
| 37682056038624 | 37 | Monterey Heights Elementary | Breakfast Provision 2 |
| 37682056038632 | 37 | Mt. Vernon Elementary | Breakfast Provision 2 |
| 37682056038657 | 37 | San Altos Elementary | Breakfast Provision 2 |
| 01611430122689 | 37 | Monterey Heights Elementary | Breakfast Provision 2 |

*schools* (46 unreferenced columns omitted)

| CDSCode | School | EILName |
|---|---|---|
| 37682056038608 | Lemon Grove Academy for the Sciences and Humanities | Elementary |
| 37682056038624 | Roosevelt Elementary | Elementary |
| 37682056038632 | Mt. Vernon Elementary | Elementary |
| 37682056038657 | San Altos Elementary | Elementary |
| 01611430122689 | Monterey Heights Elementary | Elementary |

**Gold result on the witness:** `[['Elementary', 'Lemon Grove Academy for the Sciences and Humanities'], ['Elementary', 'Roosevelt Elementary'], ['Elementary', 'Mt. Vernon Elementary'], ['Elementary', 'San Altos Elementary'], ['Elementary', 'Monterey Heights Elementary']]`  
**Predicted result on the witness:** `[['Elementary', 'Lemon Grove Academy for the Sciences and Humanities'], ['Elementary', 'Monterey Heights Elementary'], ['Elementary', 'Mt. Vernon Elementary'], ['Elementary', 'San Altos Elementary'], ['Elementary', 'Monterey Heights Elementary']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `frpm.CDSCode`: 9,986 rows, 0 NULL, 9,986 distinct values, all non-NULL values unique. Witness values: '37682056038608' occurs 1x; '37682056038624' occurs 1x; '37682056038632' occurs 1x; '37682056038657' occurs 1x; '01611430122689' occurs 1x.
- `frpm.County Code`: 9,986 rows, 0 NULL, 58 distinct values. Witness values: '37' occurs 755x.
- `frpm.School Name`: 9,986 rows, 0 NULL, 8,652 distinct values. Witness values: 'Lemon Grove Academy for the Sciences and Humaniti occurs 1x; 'Monterey Heights Elementary' occurs 1x; 'Mt. Vernon Elementary' occurs 3x; 'San Altos Elementary' occurs 1x.
- `frpm.NSLP Provision Status`: 9,986 rows, 8,139 NULL, 7 distinct values. Witness values: 'Breakfast Provision 2' occurs 285x.
- `schools.CDSCode`: 17,686 rows, 0 NULL, 17,686 distinct values, all non-NULL values unique. Witness values: '37682056038608' occurs 1x; '37682056038624' occurs 1x; '37682056038632' occurs 1x; '37682056038657' occurs 1x; '01611430122689' occurs 1x.
- `schools.School`: 17,686 rows, 1,369 NULL, 13,875 distinct values. Witness values: 'Lemon Grove Academy for the Sciences and Humaniti occurs 1x; 'Roosevelt Elementary' occurs 25x; 'Mt. Vernon Elementary' occurs 3x; 'San Altos Elementary' occurs 1x; 'Monterey Heights Elementary' occurs 1x.
- `schools.EILName`: 17,686 rows, 1,369 NULL, 7 distinct values. Witness values: 'Elementary' occurs 7,298x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 54 (codebase_community)

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
| 24094 | 13781 |
| 24087 | 13781 |

*postHistory* (5 unreferenced columns omitted)

| Id | PostHistoryTypeId | PostId | RevisionGUID |
|---|---|---|---|
| 39997 | 1 | 13781 | 6e2baa0b-ae07-4b55-a70b-75d32823b6a0 |

*posts* (16 unreferenced columns omitted)

| PostTypeId | Title | AnswerCount | CommentCount | ParentId |
|---|---|---|---|---|
| 1 | Clustering 1D data | 4 | 6 | NULL |

*users* (10 unreferenced columns omitted)

| Id | Reputation | CreationDate | DisplayName |
|---|---|---|---|
| 603 | 10647 | 2010-07-29 15:38:09.0 | user603 |
| 5666 | 21 | 2011-08-03 02:36:19.0 | Ali |
| 88 | 14082 | 2010-07-19 19:35:37.0 | mbq |

**Gold result on the witness:** `[[6, 4]]`  
**Predicted result on the witness:** `[[2, 0]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `comments.Id`: 174,285 rows, 0 NULL, 174,285 distinct values, all non-NULL values unique. Witness values: 24094 occurs 1x; 24087 occurs 1x.
- `comments.PostId`: 174,285 rows, 0 NULL, 53,416 distinct values. Witness values: 13781 occurs 6x.
- `posts.PostTypeId`: 91,966 rows, 0 NULL, 7 distinct values. Witness values: 1 occurs 42,912x.
- `posts.Title`: 91,966 rows, 49,054 NULL, 42,877 distinct values. Witness values: 'Clustering 1D data' occurs 1x.
- `posts.AnswerCount`: 91,966 rows, 49,054 NULL, 31 distinct values. Witness values: 4 occurs 818x.
- `posts.CommentCount`: 91,966 rows, 0 NULL, 39 distinct values. Witness values: 6 occurs 2,636x.
- `posts.ParentId`: 91,966 rows, 44,211 NULL, 29,006 distinct values. Witness values: NULL occurs 44,211x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 55 (european_football_2)

**Question:** When is the birthday of the football player who has the highest overall rating?

**Evidence:** football player who has the highest overall rating refers to MAX(overall_rating);

**Gold SQL:**
```sql
SELECT t1.birthday FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id ORDER BY t2.overall_rating DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T2.birthday FROM Player_Attributes AS T1 INNER JOIN Player AS T2 ON T1.player_api_id = T2.player_api_id ORDER BY T1.overall_rating DESC LIMIT 1
```

**Witness database:**

*Player_Attributes* (40 unreferenced columns omitted)

| player_api_id | overall_rating |
|---|---|
| 0 | 0 |
| -1 | 0 |

*Player* (5 unreferenced columns omitted)

| player_api_id | birthday |
|---|---|
| -1 | 2147483648 |
| 0 | 2147483649 |

*League*

| id | country_id | name |
|---|---|---|
| 0 | -1 | 2147483648 |
| 1 | 0 | 2147483648 |

*Country*

| id | name |
|---|---|
| -1 | 2147483648 |
| 0 | 2147483648 |

*Team* (1 unreferenced columns omitted)

| id | team_api_id | team_fifa_api_id | team_long_name |
|---|---|---|---|
| 1 | -1 | 0 | 2147483648 |
| 0 | 0 | -1 | 2147483648 |

*Team_Attributes* (21 unreferenced columns omitted)

| id | team_fifa_api_id | team_api_id | date |
|---|---|---|---|
| 0 | -1 | -1 | 2147483648 |
| 1 | -1 | -1 | 2147483648 |

*Match* (111 unreferenced columns omitted)

| id | country_id | league_id | season |
|---|---|---|---|
| -1 | 0 | 0 | 2147483648 |
| 0 | 0 | 0 | 2147483648 |

**Gold result on the witness:** `[['2147483648']]`  
**Predicted result on the witness:** `[['2147483649']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Player_Attributes.player_api_id`: 183,978 rows, 0 NULL, 11,060 distinct values. Witness values: 0 occurs 0x; -1 occurs 0x.
- `Player_Attributes.overall_rating`: 183,978 rows, 836 NULL, 61 distinct values. Witness values: 0 occurs 0x.
- `Player.player_api_id`: 11,060 rows, 0 NULL, 11,060 distinct values, all non-NULL values unique. Witness values: -1 occurs 0x; 0 occurs 0x.
- `Player.birthday`: 11,060 rows, 0 NULL, 5,762 distinct values. Witness values: '2147483648' occurs 0x; '2147483649' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 56 (card_games)

**Question:** For all the set of cards that has Japanese translation, what is the percentage of them are only available in non-foil?

**Evidence:** Japanese translation refers to language = 'Japanese'; in non-foil refers to isNonFoilOnly = 1; percentage of Japanese non foil in Japanese cards refers to DIVIDE(SUM(isNonFoilOnly = 1), SUM(language = 'Japanese'))*100

**Gold SQL:**
```sql
SELECT CAST(SUM(CASE WHEN isNonFoilOnly = 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(id) FROM sets WHERE code IN ( SELECT setCode FROM set_translations WHERE language = 'Japanese' )
```
**Predicted SQL:**
```sql
SELECT CAST(SUM(CASE WHEN T2.isNonFoilOnly = 1 THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(T1.setCode) AS percentage FROM set_translations AS T1 INNER JOIN sets AS T2 ON T1.setCode = T2.code WHERE T1.language = 'Japanese'
```

**Witness database:**

*set_translations* (2 unreferenced columns omitted)

| language | setCode |
|---|---|
| Italian | 100 |
| Japanese | k2 |
| Japanese | k3 |
| Japanese | k2 |

*sets* (18 unreferenced columns omitted)

| id | code | isNonFoilOnly |
|---|---|---|
| 2 | k2 | 100 |
| 3 | 100 | 1 |
| 1 | k3 | 1 |

**Gold result on the witness:** `[[50.0]]`  
**Predicted result on the witness:** `[[33.333333333333336]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `set_translations.language`: 1,210 rows, 0 NULL, 10 distinct values. Witness values: 'Italian' occurs 121x; 'Japanese' occurs 121x.
- `set_translations.setCode`: 1,210 rows, 0 NULL, 121 distinct values. Witness values: '100' occurs 0x; 'k2' occurs 0x; 'k3' occurs 0x.
- `sets.id`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 2 occurs 1x; 3 occurs 1x; 1 occurs 1x.
- `sets.code`: 551 rows, 0 NULL, 551 distinct values, all non-NULL values unique. Witness values: 'k2' occurs 0x; '100' occurs 0x; 'k3' occurs 0x.
- `sets.isNonFoilOnly`: 551 rows, 0 NULL, 2 distinct values. Witness values: 100 occurs 0x; 1 occurs 106x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 57 (formula_1)

**Question:** Please list the exact dates on which a Formula_1 race took place on the Barcelona-Catalunya circuit.

**Evidence:** -

**Gold SQL:**
```sql
SELECT T2.date FROM circuits AS T1 INNER JOIN races AS T2 ON T2.circuitID = T1.circuitId WHERE T1.name = 'Circuit de Barcelona-Catalunya'
```
**Predicted SQL:**
```sql
SELECT races.date FROM circuits INNER JOIN races ON circuits.circuitId = races.circuitId WHERE circuits.name = 'Barcelona-Catalunya' OR circuits.circuitRef = 'catalunya';
```

**Witness database:**

*circuits* (6 unreferenced columns omitted)

| circuitId | circuitRef | name |
|---|---|---|
| 3 | Barcelona-Catalunya | Barcelona-Catalunya |
| 1 | a | c |

*races* (6 unreferenced columns omitted)

| circuitId | date |
|---|---|
| 3 | 2015-03-20 |
| 3 | 2000-01-01 |

*seasons*

| year | url |
|---|---|
| 1 | catalunya |

**Gold result on the witness:** `[]`  
**Predicted result on the witness:** `[['2000-01-01'], ['2015-03-20']]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `circuits.circuitId`: 72 rows, 0 NULL, 72 distinct values, all non-NULL values unique. Witness values: 3 occurs 1x; 1 occurs 0x.
- `circuits.circuitRef`: 72 rows, 0 NULL, 72 distinct values, all non-NULL values unique. Witness values: 'Barcelona-Catalunya' occurs 0x; 'a' occurs 0x.
- `circuits.name`: 72 rows, 0 NULL, 72 distinct values, all non-NULL values unique. Witness values: 'Barcelona-Catalunya' occurs 0x; 'c' occurs 0x.
- `races.circuitId`: 976 rows, 0 NULL, 72 distinct values. Witness values: 3 occurs 13x.
- `races.date`: 976 rows, 0 NULL, 976 distinct values, all non-NULL values unique. Witness values: '2015-03-20' occurs 0x; '2000-01-01' occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 58 (codebase_community)

**Question:** What is the display name of the user who acquired the highest amount of badges?

**Evidence:** highest amount of badges refers to MAX(COUNT(Name));

**Gold SQL:**
```sql
SELECT T1.DisplayName FROM users AS T1 INNER JOIN badges AS T2 ON T1.Id = T2.UserId GROUP BY T1.DisplayName ORDER BY COUNT(T1.Id) DESC LIMIT 1
```
**Predicted SQL:**
```sql
SELECT T2.DisplayName FROM badges AS T1 JOIN users AS T2 ON T1.UserId = T2.Id GROUP BY T1.UserId ORDER BY COUNT(T1.Name) DESC LIMIT 1
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

## Item 59 (european_football_2)

**Question:** List the top 5 leagues in ascending order of the number of goals made in all seasons combined.

**Evidence:** number of goals made in all seasons combine = SUM(home_team_goal, away_team_goal);

**Gold SQL:**
```sql
SELECT t1.name, SUM(t2.home_team_goal) + SUM(t2.away_team_goal) FROM League AS t1 INNER JOIN Match AS t2 ON t1.id = t2.league_id GROUP BY t1.name ORDER BY SUM(t2.home_team_goal) + SUM(t2.away_team_goal) ASC LIMIT 5
```
**Predicted SQL:**
```sql
SELECT league.name, SUM(match.home_team_goal + match.away_team_goal) AS total_goals FROM match INNER JOIN league ON match.league_id = league.id GROUP BY league.name ORDER BY total_goals ASC LIMIT 5
```

**Witness database:**

*Country*

| id | name |
|---|---|
| 1177 | Poland |
| 1185 | c |

*League* (1 unreferenced columns omitted)

| id | name |
|---|---|
| 1178 | NULL |
| 1186 | Netherlands Eredivisie |

*Match* (112 unreferenced columns omitted)

| league_id | home_team_goal | away_team_goal |
|---|---|---|
| 1178 | NULL | NULL |
| 1186 | 3 | 10 |
| 1186 | NULL | 10 |

**Gold result on the witness:** `[[None, None], ['Netherlands Eredivisie', 23]]`  
**Predicted result on the witness:** `[[None, None], ['Netherlands Eredivisie', 13]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `League.id`: 11 rows, 0 NULL, 11 distinct values, all non-NULL values unique. Witness values: 1178 occurs 0x; 1186 occurs 0x.
- `League.name`: 11 rows, 0 NULL, 11 distinct values, all non-NULL values unique. Witness values: NULL occurs 0x; 'Netherlands Eredivisie' occurs 1x.
- Real content of `League` (11 rows; referenced columns): (1, 'Belgium Jupiler League'); (1729, 'England Premier League'); (4769, 'France Ligue 1'); (7809, 'Germany 1. Bundesliga'); (10257, 'Italy Serie A'); (13274, 'Netherlands Eredivisie'); (15722, 'Poland Ekstraklasa'); (17642, 'Portugal Liga ZON Sagres'); (19694, 'Scotland Premier League'); (21518, 'Spain LIGA BBVA'); (24558, 'Switzerland Super League').
- `Match.league_id`: 25,979 rows, 0 NULL, 11 distinct values. Witness values: 1178 occurs 0x; 1186 occurs 0x.
- `Match.home_team_goal`: 25,979 rows, 0 NULL, 11 distinct values. Witness values: NULL occurs 0x; 3 occurs 3,288x.
- `Match.away_team_goal`: 25,979 rows, 0 NULL, 10 distinct values. Witness values: NULL occurs 0x; 10 occurs 0x.

**Verdict:** ____  
**Reason (one sentence):** 


---

## Item 60 (thrombosis_prediction)

**Question:** Excluding all P only ANA Pattern patients, how many of the remainder are women born between 1980 and 1989?

**Evidence:** Excluding all P only ANA Pattern refers to `ANA Pattern`! = 'P'; women refers to SEX = 'F'; born between 1980 and 1989 refers to BIRTHDAY

**Gold SQL:**
```sql
SELECT COUNT(DISTINCT T1.ID) FROM Patient AS T1 INNER JOIN Examination AS T2 ON T1.ID = T2.ID WHERE T2.`ANA Pattern` != 'P' AND STRFTIME('%Y', T1.Birthday) BETWEEN '1980' AND '1989' AND T1.SEX = 'F'
```
**Predicted SQL:**
```sql
SELECT COUNT(*) FROM patient INNER JOIN examination ON patient.id = examination.id WHERE patient.sex = 'F' AND STRFTIME('%Y', patient.birthday) BETWEEN '1980' AND '1989' AND examination."ANA Pattern" <> 'P'
```

**Witness database:**

*Examination* (11 unreferenced columns omitted)

| ID | ANA Pattern |
|---|---|
| 1 | P,S |
| 1 | S,P |
| 1 | S |
| 3 | NULL |

*Patient* (4 unreferenced columns omitted)

| ID | SEX | Birthday |
|---|---|---|
| 1 | F | 1988-12-31 |
| 3 | M | 1938-01-05 |

**Gold result on the witness:** `[[1]]`  
**Predicted result on the witness:** `[[3]]`

**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):

- `Examination.ID`: 806 rows, 36 NULL, 763 distinct values. Witness values: 1 occurs 0x; 3 occurs 0x.
- `Examination.ANA Pattern`: 806 rows, 261 NULL, 15 distinct values. Witness values: 'P,S' occurs 89x; 'S,P' occurs 11x; 'S' occurs 252x; NULL occurs 261x.
- `Patient.ID`: 1,238 rows, 0 NULL, 1,238 distinct values, all non-NULL values unique. Witness values: 1 occurs 0x; 3 occurs 0x.
- `Patient.SEX`: 1,238 rows, 0 NULL, 3 distinct values. Witness values: 'F' occurs 1,023x; 'M' occurs 202x.
- `Patient.Birthday`: 1,238 rows, 1 NULL, 1,193 distinct values. Witness values: '1988-12-31' occurs 0x; '1938-01-05' occurs 2x.

**Verdict:** ____  
**Reason (one sentence):** 
