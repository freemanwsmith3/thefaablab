# ---------------------------
# 0) Dependencies (install with: pip install pandas matplotlib seaborn requests)
# ---------------------------
import json
import requests
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict

# ---------------------------
# 1) Config & Data
# ---------------------------
MAPPING_PATH = "faab_sleeper_mapping.json"
SCORING = "ppr"
MAX_WEEK = 18

# Actual FAAB bid data: (iso_week, db_id, name, bid_count, avg_bid_price)
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

# ---------------------------
# 2) Helpers
# ---------------------------
def load_mapping(path=MAPPING_PATH):
    """Load the player ID mapping from FAAB system to Sleeper"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Mapping file {path} not found. Players will be unmapped.")
        return {}

def get_sleeper_stats_2024(week=None):
    """Fetch NFL stats from Sleeper API"""
    url = f"https://api.sleeper.app/v1/stats/nfl/regular/2024/{week}" if week else \
          "https://api.sleeper.app/v1/stats/nfl/regular/2024"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def get_sleeper_players():
    """Fetch player metadata from Sleeper API"""
    url = "https://api.sleeper.app/v1/players/nfl"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def calculate_fantasy_points(stats, scoring='ppr'):
    """Calculate fantasy points from NFL stats"""
    pts = 0
    # Passing
    pts += stats.get('pass_yd', 0) * 0.04
    pts += stats.get('pass_td', 0) * 4
    pts -= stats.get('int', 0) * 2
    pts += stats.get('pass_2pt', 0) * 2
    # Rushing
    pts += stats.get('rush_yd', 0) * 0.1
    pts += stats.get('rush_td', 0) * 6
    pts += stats.get('rush_2pt', 0) * 2
    # Receiving
    pts += stats.get('rec_yd', 0) * 0.1
    pts += stats.get('rec_td', 0) * 6
    pts += stats.get('rec_2pt', 0) * 2
    if scoring == 'ppr':
        pts += stats.get('rec', 0) * 1.0
    elif scoring == 'half_ppr':
        pts += stats.get('rec', 0) * 0.5
    # Misc
    pts -= stats.get('fum_lost', 0) * 2
    # Kicking
    pts += stats.get('fgm', 0) * 3
    pts += stats.get('xpm', 0) * 1
    pts -= stats.get('fgmiss', 0) * 1
    pts -= stats.get('xpmiss', 0) * 1
    # Defense
    pts += stats.get('def_int', 0) * 2
    pts += stats.get('def_fr', 0) * 2
    pts += stats.get('def_sack', 0) * 1
    pts += stats.get('def_td', 0) * 6
    pts += stats.get('def_safety', 0) * 2
    return round(pts, 2)

def safe_ratio(numer, denom):
    """Safe division to avoid divide by zero"""
    if numer is None or denom in (None, 0):
        return None
    return round(numer / denom, 4)

def nfl_week_from_iso(iso_week: int) -> int:
    """Convert ISO week to NFL week (29 -> 1, 30 -> 2, etc.)"""
    wk = iso_week - 28
    return wk if wk <= 11 else 11

def build_rows_from_data():
    """Convert hardcoded TOPN_PER_WEEK data into standardized format"""
    rows = []
    for iso_week, pid, name, bid_count, avg_bid in TOPN_PER_WEEK:
        rows.append({
            "iso_week": iso_week,
            "nfl_week_bid": nfl_week_from_iso(iso_week),
            "player_id": pid,
            "player_name": name,
            "player_position": "N/A",  # Will be filled from Sleeper data
            "bid_count": int(bid_count),
            "avg_bid": float(avg_bid),
        })
    
    print(f"Loaded {len(rows)} players from hardcoded bid data")
    return rows

def find_sleeper_id_by_name(player_name, player_meta):
    """Try to find Sleeper ID by matching player name"""
    # First try exact match
    for sleeper_id, player_data in player_meta.items():
        sleeper_name = f"{player_data.get('first_name', '')} {player_data.get('last_name', '')}".strip()
        if sleeper_name.lower() == player_name.lower():
            return sleeper_id
    
    # Try partial matches
    for sleeper_id, player_data in player_meta.items():
        sleeper_name = f"{player_data.get('first_name', '')} {player_data.get('last_name', '')}".strip()
        # Check if all words in player_name appear in sleeper_name
        player_words = player_name.lower().split()
        sleeper_words = sleeper_name.lower().split()
        if all(any(pw in sw for sw in sleeper_words) for pw in player_words):
            return sleeper_id
    
    return None

def filter_skill_positions(rows):
    """Filter out kickers (K) and defenses (D/DST)"""
    excluded_positions = ['K', 'D', 'DST', 'DEF']
    filtered = []
    
    for r in rows:
        pos = r.get("player_position", "N/A").upper()
        if pos not in excluded_positions:
            filtered.append(r)
    
    excluded_count = len(rows) - len(filtered)
    print(f"Filtered out {excluded_count} kickers/defenses, {len(filtered)} skill position players remaining")
    return filtered

def create_bubble_charts(player_rows):
    """Create bubble charts for FAAB analysis"""
    # Filter for players with complete data
    chart_data = [r for r in player_rows if r["avg_points_next_3"] is not None and r["avg_bid"] > 0]
    
    if not chart_data:
        print("No data available for charts")
        return
    
    df = pd.DataFrame(chart_data)
    
    # Set up the plotting style
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('FAAB Waiver Wire Analysis - Bubble Charts', fontsize=16, fontweight='bold')
    
    # Chart 1: Overall bubble chart
    ax1 = axes[0, 0]
    scatter = ax1.scatter(df['nfl_week_bid'], df['avg_points_next_3'], 
                         s=df['avg_bid']*3, alpha=0.6, c=df['avg_bid'], 
                         cmap='viridis', edgecolors='black', linewidth=0.5)
    ax1.set_xlabel('NFL Week of Pickup')
    ax1.set_ylabel('Avg Points Next 3 Weeks')
    ax1.set_title('All Positions: Pickup Week vs Performance\n(Bubble size = Avg Bid)')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax1, label='Avg Bid ($)')
    
    # Chart 2: By Position
    ax2 = axes[0, 1]
    positions = df['player_position'].unique()
    colors = plt.cm.Set3(np.linspace(0, 1, len(positions)))
    
    for i, pos in enumerate(positions):
        if pos != "N/A":
            pos_data = df[df['player_position'] == pos]
            ax2.scatter(pos_data['nfl_week_bid'], pos_data['avg_points_next_3'],
                       s=pos_data['avg_bid']*3, alpha=0.7, c=[colors[i]], 
                       label=pos, edgecolors='black', linewidth=0.5)
    
    ax2.set_xlabel('NFL Week of Pickup')
    ax2.set_ylabel('Avg Points Next 3 Weeks')
    ax2.set_title('By Position: Pickup Week vs Performance')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    # Chart 3: Value Efficiency (Points per Dollar)
    ax3 = axes[1, 0]
    df_with_ppd = df[df['points_per_dollar'].notna()]
    if not df_with_ppd.empty:
        scatter3 = ax3.scatter(df_with_ppd['nfl_week_bid'], df_with_ppd['points_per_dollar'],
                              s=df_with_ppd['avg_bid']*3, alpha=0.6, 
                              c=df_with_ppd['avg_points_next_3'], cmap='coolwarm',
                              edgecolors='black', linewidth=0.5)
        ax3.set_xlabel('NFL Week of Pickup')
        ax3.set_ylabel('Points per Dollar')
        ax3.set_title('Value Efficiency by Week\n(Color = Avg Points Next 3)')
        ax3.grid(True, alpha=0.3)
        plt.colorbar(scatter3, ax=ax3, label='Avg Points Next 3')
    
    # Chart 4: Weekly Average Trends
    ax4 = axes[1, 1]
    weekly_stats = df.groupby('nfl_week_bid').agg({
        'avg_points_next_3': 'mean',
        'avg_bid': 'mean',
        'points_per_dollar': 'mean'
    }).reset_index()
    
    ax4_twin = ax4.twinx()
    
    line1 = ax4.plot(weekly_stats['nfl_week_bid'], weekly_stats['avg_points_next_3'], 
                     'o-', color='blue', linewidth=2, markersize=8, label='Avg Points Next 3')
    line2 = ax4_twin.plot(weekly_stats['nfl_week_bid'], weekly_stats['avg_bid'], 
                          's-', color='red', linewidth=2, markersize=8, label='Avg Bid Amount')
    
    ax4.set_xlabel('NFL Week')
    ax4.set_ylabel('Avg Points Next 3 Weeks', color='blue')
    ax4_twin.set_ylabel('Avg Bid Amount ($)', color='red')
    ax4.set_title('Weekly Trends: Performance vs Bid Amount')
    ax4.grid(True, alpha=0.3)
    
    # Combine legends
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_twin.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.tight_layout()
    plt.savefig('faab_bubble_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def analyze_pickup_timing(player_rows):
    """Analyze optimal pickup timing by week and position"""
    # Filter for players with complete data
    analysis_data = [r for r in player_rows if r["avg_points_next_3"] is not None and r["avg_bid"] > 0]
    
    if not analysis_data:
        print("No data available for timing analysis")
        return
    
    df = pd.DataFrame(analysis_data)
    
    print("\n" + "="*80)
    print("PICKUP TIMING INSIGHTS")
    print("="*80)
    
    # Overall weekly analysis
    print("\n1. BEST WEEKS TO PICKUP PLAYERS (Overall)")
    print("-" * 50)
    
    weekly_summary = df.groupby('nfl_week_bid').agg({
        'avg_points_next_3': ['mean', 'median', 'max'],
        'points_per_dollar': ['mean', 'median'],
        'avg_bid': ['mean', 'count']
    }).round(2)
    
    weekly_summary.columns = ['_'.join(col).strip() for col in weekly_summary.columns]
    weekly_summary = weekly_summary.reset_index()
    
    # Sort by average points next 3 weeks
    best_weeks = weekly_summary.sort_values('avg_points_next_3_mean', ascending=False)
    
    print(f"{'Week':<4} {'Avg Pts 3wk':<11} {'Med Pts 3wk':<11} {'Max Pts 3wk':<11} {'Avg $/pt':<10} {'Players':<7}")
    print("-" * 70)
    
    for _, row in best_weeks.head(8).iterrows():
        ppd_inv = 1/row['points_per_dollar_mean'] if pd.notna(row['points_per_dollar_mean']) and row['points_per_dollar_mean'] > 0 else float('inf')
        ppd_display = f"${ppd_inv:.2f}" if ppd_inv != float('inf') else "N/A"
        
        print(f"{int(row['nfl_week_bid']):<4} {row['avg_points_next_3_mean']:<11} "
              f"{row['avg_points_next_3_median']:<11} {row['avg_points_next_3_max']:<11} "
              f"{ppd_display:<10} {int(row['avg_bid_count']):<7}")
    
    # OPTIMAL WEEK ANALYSIS BY POSITION AND METRIC
    print("\n2. OPTIMAL PICKUP WEEKS BY POSITION & METRIC")
    print("-" * 80)
    
    positions = ['QB', 'RB', 'WR', 'TE']
    metrics = {
        'points_per_dollar': 'Points per Dollar',
        'max_points_after_bid': 'Max Points After',
        'avg_points_next_3': 'Avg Points Next 3'
    }
    
    optimal_weeks = {}
    
    for metric_key, metric_name in metrics.items():
        print(f"\n🎯 BEST WEEKS FOR {metric_name.upper()}:")
        header = f"{'Position':<8} {'Best Week':<10} {'Value':<12} {'Sample Size':<11} {'Runner-up Week':<13}"
        print(header)
        print("-" * len(header))
        
        optimal_weeks[metric_name] = {}
        
        for pos in positions:
            pos_data = df[df['player_position'] == pos]
            if pos_data.empty:
                continue
            
            # Group by week and calculate metric
            if metric_key == 'points_per_dollar':
                weekly_metric = pos_data[pos_data[metric_key].notna()].groupby('nfl_week_bid').agg({
                    metric_key: 'mean',
                    'player_name': 'count'
                }).round(3)
            else:
                weekly_metric = pos_data[pos_data[metric_key].notna()].groupby('nfl_week_bid').agg({
                    metric_key: 'mean',
                    'player_name': 'count'
                }).round(2)
            
            weekly_metric = weekly_metric.reset_index()
            weekly_metric = weekly_metric.sort_values(metric_key, ascending=False)
            
            if not weekly_metric.empty:
                best_week = weekly_metric.iloc[0]
                runner_up = weekly_metric.iloc[1] if len(weekly_metric) > 1 else None
                
                # Store for summary
                optimal_weeks[metric_name][pos] = {
                    'week': int(best_week['nfl_week_bid']),
                    'value': best_week[metric_key],
                    'count': int(best_week['player_name'])
                }
                
                # Format display value
                if metric_key == 'points_per_dollar':
                    value_display = f"{best_week[metric_key]:.3f}"
                else:
                    value_display = f"{best_week[metric_key]:.1f}"
                
                runner_up_text = f"Week {int(runner_up['nfl_week_bid'])}" if runner_up is not None else "N/A"
                
                print(f"{pos:<8} Week {int(best_week['nfl_week_bid']):<5} {value_display:<12} "
                      f"{int(best_week['player_name']):<11} {runner_up_text:<13}")
    
    # POSITION STRATEGY SUMMARY
    print("\n3. POSITION STRATEGY SUMMARY")
    print("-" * 80)
    
    print("📊 QUICK REFERENCE - Best Weeks by Position:")
    print(f"{'Position':<8} {'For Value':<12} {'For Ceiling':<14} {'For Consistency':<15}")
    print("-" * 50)
    
    for pos in positions:
        value_week = optimal_weeks.get('Points per Dollar', {}).get(pos, {}).get('week', 'N/A')
        ceiling_week = optimal_weeks.get('Max Points After', {}).get(pos, {}).get('week', 'N/A')
        consistency_week = optimal_weeks.get('Avg Points Next 3', {}).get(pos, {}).get('week', 'N/A')
        
        print(f"{pos:<8} Week {value_week:<7} Week {ceiling_week:<9} Week {consistency_week:<11}")
    
    # Value insights
    print("\n4. VALUE INSIGHTS")
    print("-" * 50)
    
    # Best values overall
    best_values = df[df['points_per_dollar'].notna()].nlargest(10, 'points_per_dollar')
    print("\nTOP 10 VALUE PICKUPS (Points per Dollar):")
    print(f"{'Player':<20} {'Pos':<3} {'Week':<4} {'Pts/$':<7} {'Bid':<5} {'Pts 3wk':<7}")
    print("-" * 60)
    
    for _, row in best_values.iterrows():
        print(f"{row['player_name'][:19]:<20} {row['player_position']:<3} {int(row['nfl_week_bid']):<4} "
              f"{row['points_per_dollar']:.3f}  ${row['avg_bid']:<4.0f} {row['avg_points_next_3']:<7}")
    
    # Overpaid analysis
    overpaid = df[(df['points_per_dollar'].notna()) & (df['avg_bid'] > 20)].nsmallest(10, 'points_per_dollar')
    if not overpaid.empty:
        print("\nMOST OVERPAID PICKUPS (High bids, low production):")
        print(f"{'Player':<20} {'Pos':<3} {'Week':<4} {'Pts/$':<7} {'Bid':<5} {'Pts 3wk':<7}")
        print("-" * 60)
        
        for _, row in overpaid.iterrows():
            print(f"{row['player_name'][:19]:<20} {row['player_position']:<3} {int(row['nfl_week_bid']):<4} "
                  f"{row['points_per_dollar']:.3f}  ${row['avg_bid']:<4.0f} {row['avg_points_next_3']:<7}")

def create_position_timing_heatmap(player_rows):
    """Create heatmap showing best weeks to pickup each position"""
    analysis_data = [r for r in player_rows if r["avg_points_next_3"] is not None]
    if not analysis_data:
        return
        
    df = pd.DataFrame(analysis_data)
    
    # Create pivot table for heatmap
    positions = ['QB', 'RB', 'WR', 'TE']
    heatmap_data = []
    
    for pos in positions:
        pos_data = df[df['player_position'] == pos]
        if pos_data.empty:
            continue
            
        weekly_avg = pos_data.groupby('nfl_week_bid')['avg_points_next_3'].mean()
        heatmap_data.append(weekly_avg)
    
    if heatmap_data:
        heatmap_df = pd.DataFrame(heatmap_data, index=positions).fillna(0)
        
        plt.figure(figsize=(12, 6))
        sns.heatmap(heatmap_df, annot=True, fmt='.1f', cmap='RdYlGn', 
                   cbar_kws={'label': 'Avg Points Next 3 Weeks'})
        plt.title('Position Pickup Timing Heatmap\n(Average Points Next 3 Weeks by Position & Week)')
        plt.xlabel('NFL Week')
        plt.ylabel('Position')
        plt.tight_layout()
        plt.savefig('position_timing_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()

# ---------------------------
# 4) Core Analysis
# ---------------------------
def fetch_all_weekly_stats(max_week=MAX_WEEK):
    """Fetch stats for all weeks"""
    print("Fetching weekly stats from Sleeper API...")
    weekly_stats = {}
    for wk in range(1, max_week + 1):
        print(f"  Week {wk}...")
        weekly_stats[wk] = get_sleeper_stats_2024(wk)
    return weekly_stats

def compute_metrics(rows, mapping, weekly_stats, player_meta, scoring=SCORING, max_week=MAX_WEEK):
    """Compute performance metrics for each player"""
    print("Computing performance metrics...")
    
    out_rows = []
    
    for r in rows:
        # Try to find Sleeper ID from mapping first, then by name matching
        sleeper_id = mapping.get(str(r["player_id"]))
        if not sleeper_id:
            sleeper_id = find_sleeper_id_by_name(r["player_name"], player_meta)
        
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
        
        # Calculate metrics
        avg_pts_after = round(sum(pts_list) / len(pts_list), 2) if pts_list else None
        max_pts_after = round(max(pts_list), 2) if pts_list else None
        avg_next3 = round(sum(pts_next3) / len(pts_next3), 2) if pts_next3 else None
        points_per_dollar = safe_ratio(avg_pts_after, r["avg_bid"])
        
        # Get position from Sleeper if not already available
        if r.get("player_position") == "N/A" and sleeper_id and sleeper_id in player_meta:
            r["player_position"] = player_meta[sleeper_id].get("position", "N/A")
        
        out_rows.append({
            **r,
            "sleeper_id": sleeper_id or "UNMAPPED",
            "post_bid_games": len(pts_list),
            "avg_points_after_bid": avg_pts_after,
            "max_points_after_bid": max_pts_after,
            "avg_points_next_3": avg_next3,
            "points_per_dollar": points_per_dollar,
        })
    
    return out_rows

# ---------------------------
# 5) Main Function
# ---------------------------
def main():
    print("FAAB Analysis: Points per $, Max week, 3-week avg")
    print("=" * 60)
    
    # Load player mapping
    mapping = load_mapping(MAPPING_PATH)
    print(f"Loaded {len(mapping)} player mappings")
    
    # Build rows from hardcoded data
    rows = build_rows_from_data()
    
    if not rows:
        print("No data found!")
        return
    
    # Fetch Sleeper data
    weekly_stats = fetch_all_weekly_stats(MAX_WEEK)
    player_meta = get_sleeper_players()
    print(f"Loaded {len(player_meta)} players from Sleeper")
    
    # Compute metrics
    player_rows = compute_metrics(rows, mapping, weekly_stats, player_meta, SCORING, MAX_WEEK)
    
    # Filter out kickers and defenses
    skill_players = filter_skill_positions(player_rows)
    
    # Display results
    print(f"\n{'Week':<4} {'Player Name':<24} {'Pos':<4} {'Pts/

if __name__ == "__main__":
    main()
:<9} {'Avg Bid':<8} {'Max After':<9} {'Avg 3wk':<9} {'Games':<5}")
    print("-" * 80)
    
    for r in sorted(skill_players, key=lambda x: (x["nfl_week_bid"], -x["avg_bid"])):
        ppd = "-" if r["points_per_dollar"] is None else f"{r['points_per_dollar']:.4f}"
        mx = "-" if r["max_points_after_bid"] is None else f"{r['max_points_after_bid']:.2f}"
        n3 = "-" if r["avg_points_next_3"] is None else f"{r['avg_points_next_3']:.2f}"
        
        print(f"{r['nfl_week_bid']:<4} {r['player_name'][:23]:<24} {r['player_position']:<4} "
              f"{ppd:>9} ${r['avg_bid']:>6.2f} {mx:>9} {n3:>9} {r['post_bid_games']:>5}")
    
    # Create visualizations
    print("\nGenerating bubble charts...")
    create_bubble_charts(skill_players)
    
    print("\nGenerating position timing heatmap...")
    create_position_timing_heatmap(skill_players)
    
    # Provide insights
    analyze_pickup_timing(skill_players)
    
    # Save results
    output_file = "faab_analysis_2024.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"rows": skill_players}, f, indent=2)
    print(f"\nResults saved to: {output_file}")
    
    # Summary stats
    mapped_players = sum(1 for r in skill_players if r["sleeper_id"] != "UNMAPPED")
    players_with_data = sum(1 for r in skill_players if r["avg_points_after_bid"] is not None)
    
    print(f"\nSummary:")
    print(f"  Total skill position players: {len(skill_players)}")
    print(f"  Mapped to Sleeper: {mapped_players}")
    print(f"  With post-bid performance data: {players_with_data}")
    
    if players_with_data > 0:
        valid_ppd = [r["points_per_dollar"] for r in skill_players if r["points_per_dollar"] is not None]
        if valid_ppd:
            print(f"  Best value (pts/$): {max(valid_ppd):.4f}")
            print(f"  Average value (pts/$): {sum(valid_ppd)/len(valid_ppd):.4f}")

def analyze_csv_structure():
    """Helper function to examine CSV structure before running main analysis"""
    csv_files = glob.glob(CSV_PATTERN)
    if not csv_files:
        print(f"No CSV files found matching pattern: {CSV_PATTERN}")
        return
    
    print("CSV Structure Analysis:")
    print("=" * 40)
    
    for csv_file in sorted(csv_files)[:3]:  # Check first 3 files
        print(f"\nFile: {csv_file}")
        try:
            df = pd.read_csv(csv_file)
            df.columns = df.columns.str.strip()
            print(f"Columns: {list(df.columns)}")
            print(f"Shape: {df.shape}")
            print("Sample data:")
            print(df.head(3).to_string())
            print("-" * 40)
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")

if __name__ == "__main__":
    # Analyze CSV structure first to see what columns are available
    analyze_csv_structure()
    
    print("\n" + "="*60)
    input("Press Enter to continue with full analysis...")
    
    main()