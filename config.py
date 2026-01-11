"""
Configuration file for Fantasy Basketball Minimum Draft Value Model
Adjust weights and thresholds here
"""

# Baseline Calculation Weights - 
BASELINE_WEIGHTS = {
    'last_year': 0.5,      # Most recent season
    'year_minus_1': 0.3,   # Year -1
    'year_minus_2': 0.2    # Year -2
}

# Role Adjustment Caps (conservative)
ROLE_ADJUSTMENT_CAPS = {
    'usage_change_max': 0.05,      # Max ±5% usage change
    'usage_change_young': 0.08,    # Max ±8% for players ≤24
    'minutes_change_max': 6,       # Max ±6 minutes
    'minutes_change_young': 8      # Max ±8 minutes for players ≤24
}

# Age Adjustment Modifiers
AGE_MODIFIERS = {
    'young_growth': (19, 23, 1.02),    # +2% for 19-23
    'peak': (24, 27, 1.0),             # No adjustment 24-27
    'slight_decline': (28, 30, 0.98),  # -2% for 28-30
    'mid_decline': (31, 33, 0.95), # -5% for 31-33
    'steep_decline': (34, 100, 0.90)   # -10% for 34+
}

# Risk Score Weights (applied to get RA-ADP)
RISK_WEIGHTS = {
    'injury': 0.35,
    'availability': 0.30,
    'shutdown': 0.20,
    'usage_fragility': 0.15
}

# Injury Score Weights
INJURY_WEIGHTS = {
    'games_played_trend': 0.40,
    'injury_type': 0.30,
    'age': 0.20,
    'load_management': 0.10
}

# Fantasy Points Scoring (adjust based on your league)
FANTASY_SCORING = {
    'points': 1,
    'field_goals_made': 1,
    'field_goals_attempted': -1,
    'three_points_made': 1,
    'free_throws_made': 1,
    'free_throws_attempted': -1,
    'rebounds': 1,
    'assists': 2,
    'steals': 4,
    'blocks': 4,
    'turnovers': -2,
}

# Draft Analysis Thresholds
TOP_N_PLAYERS = 150  # Number of players to analyze
ADP_DISCOUNT_THRESHOLD = 0.15  # If ADP is >15% below MDV, flag as fade
RISK_PENALTY_MULTIPLIER = 1.5  # How much risk score affects RA-ADP

# MDV Calculation
MDV_CALCULATION = {
    'min_games_threshold': 50,  # Minimum expected games for consideration
    'risk_discount_factor': 0.8  # Discount factor for high-risk players
}

# Seasons (update for new season)
CURRENT_SEASON = '2024-25'  # Season being projected
LAST_SEASON = '2023-24'     # Most recent completed season
SEASONS_FOR_BASELINE = ['2023-24', '2022-23', '2021-22']  # 3-year baseline

# Shutdown Risk Factors
TANKING_TEAMS_THRESHOLD = 4  # Bottom N teams considered "tanking"
CONTENDING_TEAMS_THRESHOLD = 11  # Top N teams in conference
PLAYOFF_CERTAINTY_GAMES = 5  # Games ahead/behind 8th seed threshold
