"""
Risk-Adjusted ADP (RA-ADP) Calculation

Takes baseline per-game rank and adjusts it based on risk scores.
High-risk players get pushed down in draft order.

RA-ADP = Baseline Rank × (1 + Weighted Risk Score)
"""

import pandas as pd
import numpy as np
from config import RISK_WEIGHTS, RISK_PENALTY_MULTIPLIER


def calculate_weighted_risk_score(risk_scores: dict) -> pd.Series:
    """
    Calculate weighted risk score from individual risk components
    
    Args:
        risk_scores: Dict with keys 'injury', 'availability', 'shutdown', 'usage_fragility'
                    Each value is a Series indexed by player_id
    
    Returns:
        Series of weighted risk scores
    """
    weighted_risk = pd.Series(0.0, index=risk_scores['injury'].index)
    
    for risk_type, weight in RISK_WEIGHTS.items():
        if risk_type in risk_scores:
            weighted_risk += risk_scores[risk_type] * weight
    
    return weighted_risk


def calculate_ra_adp(baseline_df: pd.DataFrame, risk_scores: dict) -> pd.DataFrame:
    """
    Calculate Risk-Adjusted ADP
    
    Formula: RA-ADP = Baseline Rank × (1 + Weighted Risk Score × Multiplier)
    
    Higher risk = higher RA-ADP (worse draft position)
    
    Args:
        baseline_df: DataFrame with 'baseline_rank' column
        risk_scores: Dict of risk score Series
    
    Returns:
        DataFrame with 'ra_adp' column added
    """
    df = baseline_df.copy()
    
    # Calculate weighted risk score
    weighted_risk = calculate_weighted_risk_score(risk_scores)
    
    # Align risk scores with baseline_df
    df['weighted_risk_score'] = df['player_id'].map(weighted_risk).fillna(0)
    
    # Calculate RA-ADP
    # Higher risk pushes rank up (worse position)
    df['ra_adp'] = df['baseline_rank'] * (1 + df['weighted_risk_score'] * RISK_PENALTY_MULTIPLIER)
    
    # Round to integer
    df['ra_adp'] = df['ra_adp'].round().astype(int)
    
    return df


if __name__ == "__main__":
    # Test RA-ADP calculation
    print("Testing RA-ADP calculation...")
    
    # Example data
    baseline_df = pd.DataFrame({
        'player_id': [1, 2, 3, 4, 5],
        'player_name': ['Player A', 'Player B', 'Player C', 'Player D', 'Player E'],
        'baseline_rank': [10, 20, 30, 40, 50]
    })
    
    # Example risk scores (0-1 scale, higher = more risky)
    risk_scores = {
        'injury': pd.Series([0.8, 0.2, 0.5, 0.3, 0.1], index=[1, 2, 3, 4, 5]),
        'availability': pd.Series([0.7, 0.1, 0.4, 0.2, 0.1], index=[1, 2, 3, 4, 5]),
        'shutdown': pd.Series([0.1, 0.2, 0.3, 0.4, 0.5], index=[1, 2, 3, 4, 5]),
        'usage_fragility': pd.Series([0.2, 0.1, 0.3, 0.2, 0.1], index=[1, 2, 3, 4, 5])
    }
    
    ra_adp_df = calculate_ra_adp(baseline_df, risk_scores)
    print(ra_adp_df[['player_name', 'baseline_rank', 'weighted_risk_score', 'ra_adp']])
