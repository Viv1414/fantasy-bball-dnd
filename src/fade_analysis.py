"""
Fade Analysis

Flags players where ADP < MDV (overvalued in drafts)
These are players to avoid at their current draft cost.
"""

import pandas as pd
import numpy as np
from config import ADP_DISCOUNT_THRESHOLD


def flag_fades(mdv_df: pd.DataFrame, adp_data: pd.Series = None) -> pd.DataFrame:
    """
    Flag players as fades when ADP < MDV
    
    Fade = Player is being drafted too early relative to their risk-adjusted value
    
    Args:
        mdv_df: DataFrame with 'mdv' column
        adp_data: Series of ADP values indexed by player_id
                  If None, will need to be provided separately
    
    Returns:
        DataFrame with fade flags and analysis
    """
    df = mdv_df.copy()
    
    # If ADP data provided, merge it
    if adp_data is not None:
        df['adp'] = df['player_id'].map(adp_data)
    elif 'adp' not in df.columns:
        # No ADP data - can't calculate fades
        df['adp'] = np.nan
        df['is_fade'] = False
        df['fade_reason'] = 'No ADP data'
        return df
    
    # Calculate fade flags
    df['is_fade'] = df['adp'] < df['mdv']
    
    # Calculate discount percentage
    df['adp_discount'] = (df['mdv'] - df['adp']) / df['mdv'] * 100
    df['adp_discount'] = df['adp_discount'].fillna(0)
    
    # Categorize fade severity
    df['fade_severity'] = 'None'
    df.loc[df['is_fade'], 'fade_severity'] = 'Moderate'
    df.loc[df['adp_discount'] > 20, 'fade_severity'] = 'High'
    df.loc[df['adp_discount'] > 35, 'fade_severity'] = 'Extreme'
    
    # Fade reason
    df['fade_reason'] = ''
    fade_mask = df['is_fade']
    for idx in df[fade_mask].index:
        adp_val = int(df.loc[idx, 'adp'])
        mdv_val = int(df.loc[idx, 'mdv'])
        discount_val = round(df.loc[idx, 'adp_discount'], 1)
        df.loc[idx, 'fade_reason'] = f"ADP {adp_val} is below MDV {mdv_val} ({discount_val}% discount needed)"
    
    return df


def generate_fade_report(fade_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate summary report of fades
    
    Args:
        fade_df: DataFrame with fade analysis
    
    Returns:
        Summary DataFrame sorted by fade severity
    """
    fades = fade_df[fade_df['is_fade']].copy()
    
    if fades.empty:
        return pd.DataFrame()
    
    # Sort by discount percentage (highest first)
    fades = fades.sort_values('adp_discount', ascending=False)
    
    report = fades[[
        'player_name',
        'baseline_rank',
        'ra_adp',
        'mdv',
        'adp',
        'adp_discount',
        'fade_severity',
        'weighted_risk_score',
        'expected_games'
    ]].copy()
    
    return report


if __name__ == "__main__":
    # Test fade analysis
    print("Testing fade analysis...")
    
    # Example data
    mdv_df = pd.DataFrame({
        'player_id': [1, 2, 3, 4, 5],
        'player_name': ['Kawhi', 'Mikal', 'Zion', 'Embiid', 'Player E'],
        'baseline_rank': [15, 25, 20, 10, 50],
        'ra_adp': [22, 26, 32, 12, 55],
        'mdv': [32, 18, 40, 10, 60],
        'weighted_risk_score': [0.7, 0.2, 0.6, 0.5, 0.3],
        'expected_games': [55, 82, 60, 65, 70]
    })
    
    # Example ADP data
    adp_data = pd.Series({
        1: 25,  # Kawhi: ADP 25 < MDV 32 → FADE
        2: 20,  # Mikal: ADP 20 > MDV 18 → Not fade
        3: 35,  # Zion: ADP 35 < MDV 40 → FADE
        4: 8,   # Embiid: ADP 8 < MDV 10 → FADE
        5: 55   # Player E: ADP 55 < MDV 60 → FADE
    })
    
    fade_df = flag_fades(mdv_df, adp_data)
    print("\nFade Analysis:")
    print(fade_df[['player_name', 'adp', 'mdv', 'is_fade', 'adp_discount', 'fade_severity']])
    
    print("\nFade Report:")
    report = generate_fade_report(fade_df)
    print(report)
