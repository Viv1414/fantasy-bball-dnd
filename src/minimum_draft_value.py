"""
Minimum Draft Value (MDV) Calculation

MDV = The lowest pick where you'd be comfortable drafting a player
Based on risk-adjusted value and expected games played.

High-risk players (like Kawhi) may have elite per-game value
but require significant ADP discount (higher MDV).
"""

import pandas as pd
import numpy as np
from config import MDV_CALCULATION


def calculate_mdv(ra_adp_df: pd.DataFrame, risk_scores: dict, availability_scores: pd.Series) -> pd.DataFrame:
    """
    Calculate Minimum Draft Value (MDV) for each player
    
    MDV considers:
    - Risk-adjusted per-game value (RA-ADP)
    - Expected games played (availability)
    - Risk discount factor
    
    Logic:
    - Elite per-game value but high risk → requires discount (higher MDV)
    - Low availability → requires discount
    - Example: Kawhi might be rank 15 per-game but MDV = 32 (need 17 pick discount)
    
    Args:
        ra_adp_df: DataFrame with 'ra_adp' and 'baseline_rank'
        risk_scores: Dict of risk score Series
        availability_scores: Series of expected games played (0-82)
    
    Returns:
        DataFrame with 'mdv' column added
    """
    df = ra_adp_df.copy()
    
    # Get weighted risk score
    from src.risk_adjusted_adp import calculate_weighted_risk_score
    weighted_risk = calculate_weighted_risk_score(risk_scores)
    df['weighted_risk_score'] = df['player_id'].map(weighted_risk).fillna(0)
    
    # Get availability (expected games)
    df['expected_games'] = df['player_id'].map(availability_scores).fillna(82)
    
    # Base MDV starts from RA-ADP
    df['mdv'] = df['ra_adp'].copy()
    
    # Apply risk discount
    # Higher risk = higher MDV (need more discount)
    risk_discount = df['weighted_risk_score'] * MDV_CALCULATION['risk_discount_factor']
    df['mdv'] = df['mdv'] * (1 + risk_discount)
    
    # Apply availability discount
    # Lower games = higher MDV (need more discount)
    games_factor = (82 - df['expected_games']) / 82  # 0 if 82 games, 1 if 0 games
    availability_discount = games_factor * 0.3  # Up to 30% discount for missed games
    df['mdv'] = df['mdv'] * (1 + availability_discount)
    
    # Minimum games threshold
    min_games = MDV_CALCULATION['min_games_threshold']
    df.loc[df['expected_games'] < min_games, 'mdv'] = np.nan  # Don't draft if < min games
    
    # Round to integer
    df['mdv'] = df['mdv'].round().astype(int)
    
    # Cap MDV at reasonable maximum (e.g., 150)
    df['mdv'] = df['mdv'].clip(upper=150)
    
    return df


def calculate_mdv_simple(baseline_rank: int, risk_score: float, expected_games: float) -> int:
    """
    Simple MDV calculation for a single player
    
    Args:
        baseline_rank: Baseline per-game rank
        risk_score: Weighted risk score (0-1)
        expected_games: Expected games played (0-82)
    
    Returns:
        Minimum Draft Value (pick number)
    """
    # Start with baseline rank
    mdv = baseline_rank
    
    # Apply risk discount
    risk_discount = risk_score * MDV_CALCULATION['risk_discount_factor']
    mdv = mdv * (1 + risk_discount)
    
    # Apply availability discount
    games_factor = (82 - expected_games) / 82
    availability_discount = games_factor * 0.3
    mdv = mdv * (1 + availability_discount)
    
    # Minimum games check
    if expected_games < MDV_CALCULATION['min_games_threshold']:
        return np.nan
    
    return int(round(mdv))


if __name__ == "__main__":
    # Test MDV calculation
    print("Testing MDV calculation...")
    
    # Example: Kawhi Leonard
    # Elite per-game (rank 15) but high risk (0.7) and low games (55)
    kawhi_mdv = calculate_mdv_simple(
        baseline_rank=15,
        risk_score=0.7,
        expected_games=55
    )
    print(f"Kawhi: Baseline rank 15, Risk 0.7, Games 55 → MDV = {kawhi_mdv}")
    
    # Example: Mikal Bridges
    # Good per-game (rank 25) but low risk (0.2) and high games (82)
    mikal_mdv = calculate_mdv_simple(
        baseline_rank=25,
        risk_score=0.2,
        expected_games=82
    )
    print(f"Mikal: Baseline rank 25, Risk 0.2, Games 82 → MDV = {mikal_mdv}")
    
    # Example: Zion Williamson
    # Good per-game (rank 20) but high risk (0.6) and medium games (60)
    zion_mdv = calculate_mdv_simple(
        baseline_rank=20,
        risk_score=0.6,
        expected_games=60
    )
    print(f"Zion: Baseline rank 20, Risk 0.6, Games 60 → MDV = {zion_mdv}")
