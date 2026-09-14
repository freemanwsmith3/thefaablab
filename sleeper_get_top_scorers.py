import json
import requests
from collections import defaultdict

# ---------------------------
# 1) Your pasted SQL results (TOP-5 per week)
# ---------------------------

#TOPN top 10
TOPN_PER_WEEK = [
    (29, 88, "Isaiah Likely", 10819, 29.52),
    (29, 60, "Jordan Mason", 6320, 31.25),
    (29, 106, "Alexander Mattison", 5155, 14.06),
    (29, 271, "J.K. Dobbins", 4817, 28.19),
    (29, 370, "Tank Bigsby", 4156, 12.52),
    (29, 360, "Allen Lazard", 3809, 14.50),
    (29, 915, "Bucky Irving", 2507, 11.34),
    (29, 586, "Colby Parkinson", 2423, 9.92),
    (29, 785, "Tyler Johnson", 2122, 10.65),
    (29, 225, "Demarcus Robinson", 2040, 10.76),
    (29, 439, "Baker Mayfield", 1625, 13.00),
    (29, 347, "Brandin Cooks", 1287, 10.92),
    (29, 558, "Justice Hill", 1230, 10.07),
    (29, 432, "Los Angeles Chargers", 863, 5.74),
    (29, 171, "Wan'Dale Robinson", 862, 8.81),
    (29, 154, "Alec Pierce", 794, 10.63),
    (29, 99, "Greg Dortch", 687, 9.16),
    (29, 708, "Jaleel McLaughlin", 646, 11.50),
    (29, 127, "Jameson Williams", 594, 28.21),
    (29, 134, "Justin Fields", 436, 12.67),
    (30, 976, "Carson Steele", 15656, 23.84),
    (30, 348, "Quentin Johnston", 11021, 17.78),
    (30, 234, "Samaje Perine", 7030, 14.33),
    (30, 917, "Braelon Allen", 6538, 13.76),
    (30, 136, "Hunter Henry", 4038, 11.94),
    (30, 974, "Jordan Whittington", 3438, 10.99),
    (30, 233, "Cam Akers", 3384, 12.22),
    (30, 98, "Derek Carr", 3309, 14.80),
    (30, 225, "Demarcus Robinson", 2514, 15.03),
    (30, 154, "Alec Pierce", 2364, 14.76),
    (30, 416, "Kareem Hunt", 1919, 12.52),
    (30, 915, "Bucky Irving", 1586, 13.39),
    (30, 166, "Mike Gesicki", 1488, 11.21),
    (30, 180, "D'Onta Foreman", 1165, 10.88),
    (30, 458, "Ty Chandler", 860, 11.94),
    (30, 785, "Tyler Johnson", 823, 10.05),
    (30, 910, "Jaylen Wright", 721, 10.16),
    (30, 412, "Josh Downs", 655, 12.22),
    (30, 588, "Rico Dowdle", 646, 13.19),
    (30, 378, "Clyde Edwards-Helaire", 549, 7.95),
    (31, 501, "Jauan Jennings", 3303, 20.44),
    (31, 915, "Bucky Irving", 2774, 18.70),
    (31, 917, "Braelon Allen", 2160, 16.70),
    (31, 373, "Roschon Johnson", 1872, 9.73),
    (31, 113, "Cole Kmet", 1576, 10.95),
    (31, 191, "Darnell Mooney", 949, 11.44),
    (31, 724, "Emanuel Wilson", 885, 8.97),
    (31, 416, "Kareem Hunt", 590, 9.07),
    (31, 83, "Tyler Conklin", 586, 7.80),
    (31, 496, "Sam Darnold", 516, 11.81),
    (31, 171, "Wan'Dale Robinson", 414, 8.90),
    (31, 379, "Cordarrelle Patterson", 385, 7.29),
    (31, 406, "Zach Ertz", 314, 7.93),
    (31, 192, "Andy Dalton", 313, 10.36),
    (31, 134, "Justin Fields", 300, 10.67),
    (31, 588, "Rico Dowdle", 295, 11.75),
    (31, 378, "Clyde Edwards-Helaire", 281, 7.68),
    (31, 348, "Quentin Johnston", 218, 11.94),
    (31, 607, "Tyler Badie", 215, 6.04),
    (31, 646, "Jalen Nailor", 196, 9.49),
    (32, 573, "Dontayvion Wicks", 5608, 20.67),
    (32, 560, "Trey Sermon", 4075, 14.83),
    (32, 416, "Kareem Hunt", 3219, 21.79),
    (32, 505, "Tucker Kraft", 2006, 10.49),
    (32, 906, "Xavier Legette", 1830, 12.20),
    (32, 412, "Josh Downs", 1281, 11.80),
    (32, 370, "Tank Bigsby", 1126, 10.08),
    (32, 171, "Wan'Dale Robinson", 1076, 12.79),
    (32, 134, "Justin Fields", 728, 13.17),
    (32, 422, "Chase Brown", 656, 17.11),
    (32, 58, "Tyler Allgeier", 574, 11.70),
    (32, 558, "Justice Hill", 564, 10.18),
    (32, 614, "Tre Tucker", 521, 8.95),
    (32, 409, "Denver Broncos", 412, 6.76),
    (32, 78, "Romeo Doubs", 329, 10.29),
    (32, 974, "Jordan Whittington", 275, 7.38),
    (32, 106, "Alexander Mattison", 274, 9.78),
    (32, 280, "Nick Chubb", 238, 24.64),
    (32, 267, "Tutu Atwell", 194, 8.94),
    (32, 588, "Rico Dowdle", 185, 16.93),
    (33, 353, "JuJu Smith-Schuster", 2811, 17.29),
    (33, 370, "Tank Bigsby", 2643, 22.53),
    (33, 524, "Jalen Tolbert", 1681, 13.30),
    (33, 924, "Tyrone Tracy Jr.", 1354, 14.66),
    (33, 191, "Darnell Mooney", 866, 22.42),
    (33, 412, "Josh Downs", 467, 13.82),
    (33, 910, "Jaylen Wright", 440, 8.25),
    (33, 378, "Clyde Edwards-Helaire", 369, 5.87),
    (33, 458, "Ty Chandler", 342, 11.40),
    (33, 373, "Roschon Johnson", 266, 10.62),
    (33, 397, "Philadelphia Eagles", 264, 5.33),
    (33, 896, "Blake Corum", 248, 6.13),
    (33, 917, "Braelon Allen", 187, 12.18),
    (33, 505, "Tucker Kraft", 176, 16.88),
    (33, 233, "Cam Akers", 148, 6.39),
    (33, 348, "Quentin Johnston", 135, 5.87),
    (33, 83, "Tyler Conklin", 122, 6.50),
    (33, 154, "Alec Pierce", 99, 8.35),
    (33, 144, "Daniel Jones", 94, 7.01),
    (33, 142, "Christian Watson", 84, 8.74),

    (34, 460, "Sean Tucker", 2072, 16.12),
    (34, 933, "Isaac Guerendo", 1591, 10.28),
    (34, 748, "DeMario Douglas", 1399, 11.22),
    (34, 900, "Ray Davis", 1321, 13.00),
    (34, 918, "Kimani Vidal", 904, 8.92),
    (34, 353, "JuJu Smith-Schuster", 890, 15.43),
    (34, 924, "Tyrone Tracy Jr.", 836, 19.85),
    (34, 142, "Christian Watson", 517, 11.08),
    (34, 445, "D'Ernest Johnson", 402, 7.62),
    (34, 58, "Tyler Allgeier", 365, 12.58),
    (34, 412, "Josh Downs", 332, 18.05),
    (34, 458, "Ty Chandler", 299, 8.72),
    (34, 919, "Drake Maye", 253, 8.25),
    (34, 78, "Romeo Doubs", 225, 10.14),
    (34, 896, "Blake Corum", 208, 6.42),
    (34, 910, "Jaylen Wright", 172, 7.64),
    (34, 895, "Trey Benson", 169, 6.93),
    (34, 360, "Allen Lazard", 133, 9.50),
    (34, 42, "Jaylen Warren", 104, 7.76),
    (34, 906, "Xavier Legette", 86, 6.50),

    # Week 35
    (35, 501, "Jauan Jennings", 2879, 22.66),
    (35, 928, "Jalen McMillan", 2557, 14.49),
    (35, 912, "Ricky Pearsall", 1564, 11.41),
    (35, 159, "Cade Otton", 936, 12.99),
    (35, 457, "Cedric Tillman", 883, 9.65),
    (35, 73, "Sterling Shepard", 542, 9.21),
    (35, 897, "Keon Coleman", 520, 11.31),
    (35, 351, "Rashod Bateman", 442, 9.40),
    (35, 78, "Romeo Doubs", 400, 12.89),
    (35, 136, "Hunter Henry", 312, 10.20),
    (35, 42, "Jaylen Warren", 288, 10.54),
    (35, 268, "Russell Wilson", 251, 8.67),
    (35, 92, "Tua Tagovailoa", 213, 9.21),
    (35, 573, "Dontayvion Wicks", 196, 10.40),
    (35, 900, "Ray Davis", 173, 10.13),
    (35, 524, "Jalen Tolbert", 163, 9.29),
    (35, 742, "Tyler Goodson", 128, 7.73),
    (35, 1, "Jameis Winston", 125, 15.34),
    (35, 919, "Drake Maye", 91, 8.70),
    (35, 913, "Troy Franklin", 83, 8.60),

    # Week 36
    (36, 457, "Cedric Tillman", 2059, 22.26),
    (36, 933, "Isaac Guerendo", 896, 10.49),
    (36, 182, "Elijah Moore", 811, 9.21),
    (36, 412, "Josh Downs", 786, 19.63),
    (36, 897, "Keon Coleman", 516, 12.55),
    (36, 922, "Bo Nix", 379, 10.17),
    (36, 535, "Parker Washington", 351, 7.31),
    (36, 1, "Jameis Winston", 243, 14.07),
    (36, 369, "Matthew Stafford", 195, 9.12),
    (36, 928, "Jalen McMillan", 169, 9.22),
    (36, 912, "Ricky Pearsall", 152, 9.80),
    (36, 42, "Jaylen Warren", 111, 8.09),
    (36, 315, "Jerry Jeudy", 107, 9.86),
    (36, 406, "Zach Ertz", 78, 6.73),
    (36, 384, "John Metchie III", 61, 9.21),
    (36, 41, "Taysom Hill", 57, 6.70),
    (36, 896, "Blake Corum", 56, 7.79),
    (36, 58, "Tyler Allgeier", 44, 7.32),
    (36, 748, "DeMario Douglas", 41, 7.73),
    (36, 917, "Braelon Allen", 37, 7.95),

    # Week 37
    (37, 104, "Khalil Herbert", 909, 12.56),
    (37, 166, "Mike Gesicki", 448, 11.08),
    (37, 348, "Quentin Johnston", 380, 9.63),
    (37, 42, "Jaylen Warren", 235, 10.25),
    (37, 41, "Taysom Hill", 220, 7.76),
    (37, 225, "Demarcus Robinson", 148, 7.07),
    (37, 900, "Ray Davis", 128, 7.77),
    (37, 933, "Isaac Guerendo", 117, 6.99),
    (37, 912, "Ricky Pearsall", 90, 7.13),
    (37, 323, "Justin Herbert", 72, 8.29),
    (37, 136, "Hunter Henry", 67, 6.15),
    (37, 906, "Xavier Legette", 65, 8.48),
    (37, 58, "Tyler Allgeier", 44, 5.43),
    (37, 268, "Russell Wilson", 43, 15.07),
    (37, 486, "Jonnu Smith", 43, 11.91),
    (37, 748, "DeMario Douglas", 40, 6.30),
    (37, 132, "Chris Boswell", 38, 13.79),
    (37, 558, "Justice Hill", 28, 9.32),
    (37, 182, "Elijah Moore", 25, 9.96),
    (37, 455, "Detroit Lions", 23, 8.43),

    # Week 38
    (38, 921, "Audric Estime", 1663, 18.86),
    (38, 912, "Ricky Pearsall", 355, 12.87),
    (38, 181, "Gus Edwards", 317, 7.48),
    (38, 110, "Marquez Valdes-Scantling", 250, 9.89),
    (38, 910, "Jaylen Wright", 194, 7.51),
    (38, 415, "Tyjae Spears", 158, 9.90),
    (38, 899, "Adonai Mitchell", 138, 5.26),
    (38, 922, "Bo Nix", 132, 11.47),
    (38, 268, "Russell Wilson", 123, 8.30),
    (38, 895, "Trey Benson", 100, 8.50),
    (38, 511, "Houston Texans", 93, 8.51),
    (38, 154, "Alec Pierce", 82, 10.05),
    (38, 327, "Mike Williams", 82, 5.28),
    (38, 42, "Jaylen Warren", 62, 9.92),
    (38, 433, "Green Bay Packers", 49, 7.61),
    (38, 375, "Dawson Knox", 44, 6.70),
    (38, 104, "Khalil Herbert", 42, 9.69),
    (38, 919, "Drake Maye", 29, 16.14),
    (38, 520, "Will Dissly", 28, 4.57),
    (38, 182, "Elijah Moore", 26, 4.04),

    # Week 39
    (39, 520, "Will Dissly", 183, 9.37),
    (39, 182, "Elijah Moore", 131, 7.84),
    (39, 373, "Roschon Johnson", 111, 8.09),
    (39, 142, "Christian Watson", 110, 8.96),
    (39, 365, "Anthony Richardson", 76, 9.86),
    (39, 895, "Trey Benson", 76, 5.67),
    (39, 922, "Bo Nix", 56, 11.73),
    (39, 429, "Tampa Bay Buccaneers", 47, 7.53),
    (39, 459, "Nick Westbrook-Ikhine", 46, 5.87),
    (39, 136, "Hunter Henry", 33, 10.52),
    (39, 348, "Quentin Johnston", 33, 8.18),
    (39, 406, "Zach Ertz", 32, 8.13),
    (39, 233, "Cam Akers", 32, 4.53),
    (39, 171, "Wan'Dale Robinson", 27, 5.67),
    (39, 110, "Marquez Valdes-Scantling", 26, 10.38),
    (39, 526, "Ameer Abdullah", 26, 5.58),
    (39, 910, "Jaylen Wright", 23, 2.09),
    (39, 370, "Tank Bigsby", 17, 11.53),
    (39, 919, "Drake Maye", 16, 5.19),
    (39, 906, "Xavier Legette", 14, 3.50),

    # Week 40
    (40, 181, "Gus Edwards", 580, 18.08),
    (40, 973, "Devaughn Vele", 327, 10.78),
    (40, 980, "Jeremy McNichols", 242, 10.90),
    (40, 526, "Ameer Abdullah", 213, 10.86),
    (40, 110, "Marquez Valdes-Scantling", 144, 8.18),
    (40, 459, "Nick Westbrook-Ikhine", 106, 10.47),
    (40, 918, "Kimani Vidal", 88, 7.15),
    (40, 72, "Noah Brown", 62, 10.94),
    (40, 897, "Keon Coleman", 61, 7.26),
    (40, 510, "Noah Gray", 53, 8.00),
    (40, 394, "Dallas Cowboys", 48, 6.23),
    (40, 58, "Tyler Allgeier", 41, 9.56),
    (40, 370, "Tank Bigsby", 28, 6.32),
    (40, 415, "Tyjae Spears", 27, 8.37),
    (40, 896, "Blake Corum", 23, 6.39),
    (40, 367, "Adam Thielen", 18, 7.44),
    (40, 154, "Alec Pierce", 18, 3.67),
    (40, 1, "Jameis Winston", 17, 12.59),
    (40, 895, "Trey Benson", 17, 4.65),
    (40, 481, "Arizona Cardinals", 12, 16.83),
]
# TOPN for top 5 
# TOPN_PER_WEEK = [
#     (29,  88, "Isaiah Likely",            10819, 29.52),
#     (29,  60, "Jordan Mason",              6320, 31.25),
#     (29, 106, "Alexander Mattison",        5155, 14.06),
#     (29, 271, "J.K. Dobbins",              4817, 28.19),
#     (29, 370, "Tank Bigsby",               4156, 12.52),

#     (30, 976, "Carson Steele",            15656, 23.84),
#     (30, 348, "Quentin Johnston",         11021, 17.78),
#     (30, 234, "Samaje Perine",             7030, 14.33),
#     (30, 917, "Braelon Allen",             6538, 13.76),
#     (30, 136, "Hunter Henry",              4038, 11.94),

#     (31, 501, "Jauan Jennings",            3303, 20.44),
#     (31, 915, "Bucky Irving",              2774, 18.70),
#     (31, 917, "Braelon Allen",             2160, 16.70),
#     (31, 373, "Roschon Johnson",           1872,  9.73),
#     (31, 113, "Cole Kmet",                 1576, 10.95),

#     (32, 573, "Dontayvion Wicks",          5608, 20.67),
#     (32, 560, "Trey Sermon",               4075, 14.83),
#     (32, 416, "Kareem Hunt",               3219, 21.79),
#     (32, 505, "Tucker Kraft",              2006, 10.49),
#     (32, 906, "Xavier Legette",            1830, 12.20),

#     (33, 353, "JuJu Smith-Schuster",       2811, 17.29),
#     (33, 370, "Tank Bigsby",               2643, 22.53),
#     (33, 524, "Jalen Tolbert",             1681, 13.30),
#     (33, 924, "Tyrone Tracy Jr.",          1354, 14.66),
#     (33, 191, "Darnell Mooney",             866, 22.42),

#     (34, 460, "Sean Tucker",               2072, 16.12),
#     (34, 933, "Isaac Guerendo",            1591, 10.28),
#     (34, 748, "DeMario Douglas",           1399, 11.22),
#     (34, 900, "Ray Davis",                 1321, 13.00),
#     (34, 918, "Kimani Vidal",               904,  8.92),

#     (35, 501, "Jauan Jennings",            2879, 22.66),
#     (35, 928, "Jalen McMillan",            2557, 14.49),
#     (35, 912, "Ricky Pearsall",            1564, 11.41),
#     (35, 159, "Cade Otton",                 936, 12.99),
#     (35, 457, "Cedric Tillman",             883,  9.65),

#     (36, 457, "Cedric Tillman",            2059, 22.26),
#     (36, 933, "Isaac Guerendo",             896, 10.49),
#     (36, 182, "Elijah Moore",               811,  9.21),
#     (36, 412, "Josh Downs",                 786, 19.63),
#     (36, 897, "Keon Coleman",               516, 12.55),

#     (37, 104, "Khalil Herbert",             909, 12.56),
#     (37, 166, "Mike Gesicki",               448, 11.08),
#     (37, 348, "Quentin Johnston",           380,  9.63),
#     (37,  42, "Jaylen Warren",              235, 10.25),
#     (37,  41, "Taysom Hill",                220,  7.76),

#     (38, 921, "Audric Estime",             1663, 18.86),
#     (38, 912, "Ricky Pearsall",             355, 12.87),
#     (38, 181, "Gus Edwards",                317,  7.48),
#     (38, 110, "Marquez Valdes-Scantling",   250,  9.89),
#     (38, 910, "Jaylen Wright",              194,  7.51),

#     (39, 520, "Will Dissly",                183,  9.37),
#     (39, 182, "Elijah Moore",               131,  7.84),
#     (39, 373, "Roschon Johnson",            111,  8.09),
#     (39, 142, "Christian Watson",           110,  8.96),
#     (39, 365, "Anthony Richardson",          76,  9.86),

#     (40, 181, "Gus Edwards",                580, 18.08),
#     (40, 973, "Devaughn Vele",              327, 10.78),
#     (40, 980, "Jeremy McNichols",           242, 10.90),
#     (40, 526, "Ameer Abdullah",             213, 10.86),
#     (40, 110, "Marquez Valdes-Scantling",   144,  8.18),
# ]

# ---------------------------
# 2) Config
# ---------------------------
MAPPING_PATH = "faab_sleeper_mapping.json"
SCORING = "ppr"
MAX_WEEK = 18

# ---------------------------
# 3) Helpers
# ---------------------------
def nfl_week_from_iso(iso_week: int) -> int:
    wk = iso_week - 28
    return wk if wk <= 11 else 11

def load_mapping(path=MAPPING_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_sleeper_stats_2024(week=None):
    url = f"https://api.sleeper.app/v1/stats/nfl/regular/2024/{week}" if week else \
          "https://api.sleeper.app/v1/stats/nfl/regular/2024"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def get_sleeper_players():
    url = "https://api.sleeper.app/v1/players/nfl"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()  # dict keyed by sleeper_id

def calculate_fantasy_points(stats, scoring='ppr'):
    pts = 0
    pts += stats.get('pass_yd', 0) * 0.04
    pts += stats.get('pass_td', 0) * 4
    pts -= stats.get('int', 0) * 2
    pts += stats.get('pass_2pt', 0) * 2
    pts += stats.get('rush_yd', 0) * 0.1
    pts += stats.get('rush_td', 0) * 6
    pts += stats.get('rush_2pt', 0) * 2
    pts += stats.get('rec_yd', 0) * 0.1
    pts += stats.get('rec_td', 0) * 6
    pts += stats.get('rec_2pt', 0) * 2
    if scoring == 'ppr':
        pts += stats.get('rec', 0) * 1.0
    elif scoring == 'half_ppr':
        pts += stats.get('rec', 0) * 0.5
    pts -= stats.get('fum_lost', 0) * 2
    pts += stats.get('fgm', 0) * 3
    pts += stats.get('xpm', 0) * 1
    pts -= stats.get('fgmiss', 0) * 1
    pts -= stats.get('xpmiss', 0) * 1
    pts += stats.get('def_int', 0) * 2
    pts += stats.get('def_fr', 0) * 2
    pts += stats.get('def_sack', 0) * 1
    pts += stats.get('def_td', 0) * 6
    pts += stats.get('def_safety', 0) * 2
    return round(pts, 2)

def safe_ratio(numer, denom):
    if numer is None or denom in (None, 0):
        return None
    return round(numer / denom, 4)

# ---------------------------
# 4) Core
# ---------------------------
def build_rows():
    rows = []
    for iso_week, pid, name, bid_count, avg_bid in TOPN_PER_WEEK:
        rows.append({
            "iso_week": iso_week,
            "nfl_week_bid": nfl_week_from_iso(iso_week),
            "player_id": pid,
            "player_name": name,
            "bid_count": int(bid_count),
            "avg_bid": float(avg_bid),
        })
    return rows

def fetch_all_weekly_stats(max_week=MAX_WEEK):
    return {wk: get_sleeper_stats_2024(wk) for wk in range(1, max_week + 1)}

def compute_metrics(rows, mapping, weekly_stats, player_meta, scoring=SCORING, max_week=MAX_WEEK):
    faab_to_sleeper = mapping
    out_rows = []

    for r in rows:
        sleeper_id = faab_to_sleeper.get(str(r["player_id"]))
        start_wk = min(max_week, r["nfl_week_bid"] + 1)

        pts_list, pts_next3 = [], []

        if sleeper_id:
            for wk in range(start_wk, max_week + 1):
                stats = weekly_stats.get(wk, {}).get(sleeper_id, {})
                if stats and any(stats.values()):
                    pts = calculate_fantasy_points(stats, scoring)
                    pts_list.append(pts)
                    if wk <= r["nfl_week_bid"] + 3:
                        pts_next3.append(pts)

        avg_pts_after = round(sum(pts_list) / len(pts_list), 2) if pts_list else None
        max_pts_after = round(max(pts_list), 2) if pts_list else None
        avg_next3 = round(sum(pts_next3) / len(pts_next3), 2) if pts_next3 else None
        points_per_dollar = safe_ratio(avg_pts_after, r["avg_bid"])

        # Look up position from Sleeper player data
        position = "N/A"
        if sleeper_id and sleeper_id in player_meta:
            position = player_meta[sleeper_id].get("position", "N/A")

        out_rows.append({
            **r,
            "sleeper_id": sleeper_id or "UNMAPPED",
            "player_position": position,          # NEW
            "post_bid_games": len(pts_list),
            "avg_points_after_bid": avg_pts_after,
            "max_points_after_bid": max_pts_after,
            "avg_points_next_3": avg_next3,
            "points_per_dollar": points_per_dollar,
        })
    return out_rows

# ---------------------------
# 5) Run
# ---------------------------
def main():
    print("FAAB: Points per $, Max week, 3-week avg, with player_position")

    mapping = load_mapping(MAPPING_PATH)
    if not mapping:
        raise SystemExit(f"Mapping not found or empty: {MAPPING_PATH}")

    rows = build_rows()
    weekly_stats = fetch_all_weekly_stats(MAX_WEEK)
    player_meta = get_sleeper_players()

    player_rows = compute_metrics(rows, mapping, weekly_stats, player_meta, SCORING, MAX_WEEK)

    print("\niso  player_name                  pos   pts_per_$  avg_bid  max_after  avg_next3")
    for r in player_rows:   # <- this iterates through every row
        ppd = "-" if r["points_per_dollar"] is None else f"{r['points_per_dollar']:.4f}"
        mx  = "-" if r["max_points_after_bid"] is None else f"{r['max_points_after_bid']:.2f}"
        n3  = "-" if r["avg_points_next_3"] is None else f"{r['avg_points_next_3']:.2f}"
        print(f"{r['iso_week']:>3}  {r['player_name'][:24]:<24} {r['player_position']:<4} {ppd:>9}  "
              f"{r['avg_bid']:>7.2f}  {mx:>9}  {n3:>9}")

    with open("faab_value_metrics_2024.json", "w", encoding="utf-8") as f:
        json.dump({"rows": player_rows}, f, indent=2)
    print("\nSaved → faab_value_metrics_2024.json")

if __name__ == "__main__":
    main()
