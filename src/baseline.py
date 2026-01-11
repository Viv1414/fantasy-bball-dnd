"""
Baseline Per-Game Value Calculation

Calculates expected per-game fantasy value using:
1. Weighted 3-year average (last year weighted highest)
2. Role adjustments (usage/minutes changes)
3. Age curve adjustments

Baseline represents: "If player plays normally in expected role, how good are they per game?"
"""

import pandas as pd
import numpy as np
from config import BASELINE_WEIGHTS, ROLE_ADJUSTMENT_CAPS, AGE_MODIFIERS
from src.data_collector import get_player_stats, calculate_fantasy_points


def calculate_weighted_3year_average(player_id: int, seasons: list, scoring: dict) -> float:
    """
    Calculate weighted 3-year per-game fantasy average
    
    Args:
        player_id: NBA player ID
        seasons: List of season strings (most recent first)
        scoring: Fantasy scoring dictionary
    
    Returns:
        Weighted average per-game fantasy points
    """
    per_game_averages = []
    
    for i, season in enumerate(seasons):
        stats = get_player_stats(player_id, season)
        if stats is not None and not stats.empty:
            # Calculate fantasy points for each game
            stats['FANTASY_PTS'] = stats.apply(
                lambda row: calculate_fantasy_points(row, scoring),
                axis=1
            )
            avg_fp = stats['FANTASY_PTS'].mean()
            per_game_averages.append((avg_fp, BASELINE_WEIGHTS[f'year_minus_{i}'] if i > 0 else BASELINE_WEIGHTS['last_year']))
    
    if not per_game_averages:
        return np.nan
    
    # Calculate weighted average
    weighted_sum = sum(avg * weight for avg, weight in per_game_averages)
    weight_sum = sum(weight for _, weight in per_game_averages)
    
    return weighted_sum / weight_sum if weight_sum > 0 else np.nan


def apply_role_adjustments(baseline_df: pd.DataFrame, role_changes: dict = None) -> pd.DataFrame:
    """
    Apply role adjustments to baseline based on expected usage/minutes changes
    
    Conservative adjustments:
    - Cap usage changes at ±5% (or ±8% for young players)
    - Cap minutes changes at ±6 (or ±8 for young players)
    
    Args:
        baseline_df: DataFrame with baseline values
        role_changes: Dict of {player_id: {'usage_change': float, 'minutes_change': int}}
                     If None, will need to be calculated from team context
    
    Returns:
        DataFrame with role-adjusted baseline values
    """
    df = baseline_df.copy()
    
    # If role_changes not provided, calculate from team context
    # TODO: Implement team context analysis
    if role_changes is None:
        # Placeholder: no adjustments
        df['role_adjusted_baseline'] = df['baseline_fp']
        df['usage_change'] = 0
        df['minutes_change'] = 0
        return df
    
    # Apply role adjustments
    for player_id, changes in role_changes.items():
        if player_id not in df.index:
            continue
        
        age = df.loc[player_id, 'age']
        is_young = age <= 24
        
        # Cap usage change
        usage_cap = ROLE_ADJUSTMENT_CAPS['usage_change_young'] if is_young else ROLE_ADJUSTMENT_CAPS['usage_change_max']
        usage_change = np.clip(changes.get('usage_change', 0), -usage_cap, usage_cap)
        
        # Cap minutes change
        minutes_cap = ROLE_ADJUSTMENT_CAPS['minutes_change_young'] if is_young else ROLE_ADJUSTMENT_CAPS['minutes_change_max']
        minutes_change = np.clip(changes.get('minutes_change', 0), -minutes_cap, minutes_cap)
        
        # Apply adjustments (conservative: 1 usage% ≈ 0.3 FPTS, 1 minute ≈ 0.5 FPTS)
        fp_adjustment = (usage_change * 0.3) + (minutes_change * 0.5)
        df.loc[player_id, 'role_adjusted_baseline'] = df.loc[player_id, 'baseline_fp'] + fp_adjustment
        df.loc[player_id, 'usage_change'] = usage_change
        df.loc[player_id, 'minutes_change'] = minutes_change
    
    return df


def apply_age_adjustments(baseline_df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply age curve adjustments to baseline
    
    Age buckets:
    - 19-23: +2% (growth potential)
    - 24-27: 0% (peak)
    - 28-30: -2% (slight decline)
    - 31-33: -5% (moderate decline)
    - 34+: -10% (steep decline)
    
    Args:
        baseline_df: DataFrame with role-adjusted baseline values
    
    Returns:
        DataFrame with age-adjusted baseline values
    """
    df = baseline_df.copy()
    df['age_adjusted_baseline'] = df['role_adjusted_baseline'].copy()
    
    for idx, row in df.iterrows():
        age = row.get('age', np.nan)
        if pd.isna(age):
            continue
        
        # Find age bucket
        modifier = 1.0
        for (min_age, max_age, age_mod) in [
            AGE_MODIFIERS['young_growth'],
            AGE_MODIFIERS['peak'],
            AGE_MODIFIERS['slight_decline'],
            AGE_MODIFIERS['mid_decline'],
            AGE_MODIFIERS['steep_decline']
        ]:
            if min_age <= age <= max_age:
                modifier = age_mod
                break
        
        df.loc[idx, 'age_adjusted_baseline'] = row['role_adjusted_baseline'] * modifier
        df.loc[idx, 'age_modifier'] = modifier
    
    return df


def calculate_baseline_per_game(players_list: list, seasons: list, scoring: dict) -> pd.DataFrame:
    """
    Main function to calculate baseline per-game value for all players
    
    Args:
        players_list: List of player dictionaries with 'id' and 'full_name'
        seasons: List of seasons for 3-year average
        scoring: Fantasy scoring dictionary
    
    Returns:
        DataFrame with baseline calculations
    """
    results = []
    
    for player in players_list:
        player_id = player['id']
        player_name = player['full_name']
        
        # Calculate weighted 3-year average
        baseline_fp = calculate_weighted_3year_average(player_id, seasons, scoring)
        
        if not pd.isna(baseline_fp):
            results.append({
                'player_id': player_id,
                'player_name': player_name,
                'baseline_fp': baseline_fp
            })
    
    df = pd.DataFrame(results)
    
    # Rank by baseline
    df['baseline_rank'] = df['baseline_fp'].rank(ascending=False)
    
    return df


if __name__ == "__main__":
    # Test baseline calculation
    from nba_api.stats.static import players
    
    print("Testing baseline calculation...")
    all_players = players.get_players()
    test_players = all_players[:5]  # Test with first 5 players
    
    seasons = ['2023-24', '2022-23', '2021-22']
    from config import FANTASY_SCORING
    
    baseline_df = calculate_baseline_per_game(test_players, seasons, FANTASY_SCORING)
    print(baseline_df.head())
