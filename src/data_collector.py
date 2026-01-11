"""
Data Collection Module

Fetches NBA player data from various sources:
- nba_api for player stats
- Basketball Reference for historical data
- Injury reports
"""

from nba_api.stats.endpoints import playergamelog, commonplayerinfo, playerdashboardbygeneralsplits
from nba_api.stats.static import players, teams
import pandas as pd
import time
from typing import Dict, List, Optional


def get_all_players() -> pd.DataFrame:
    """
    Get list of all NBA players
    
    Returns:
        DataFrame with player information
    """
    try:
        all_players = players.get_players()
        return pd.DataFrame(all_players)
    except Exception as e:
        print(f"Error fetching players: {e}")
        return pd.DataFrame()


def get_player_stats(player_id: int, season: str = '2023-24') -> Optional[pd.DataFrame]:
    """
    Get player statistics for a given season
    
    Args:
        player_id: NBA player ID
        season: Season string (e.g., '2023-24')
    
    Returns:
        DataFrame with player stats or None if error
    """
    try:
        # Get game log for the season
        game_log = playergamelog.PlayerGameLog(
            player_id=player_id,
            season=season
        )
        df = game_log.get_data_frames()[0]
        return df
    except Exception as e:
        print(f"Error fetching stats for player {player_id}: {e}")
        return None


def get_player_info(player_id: int) -> Optional[Dict]:
    """
    Get basic player information
    
    Args:
        player_id: NBA player ID
    
    Returns:
        Dictionary with player info or None if error
    """
    try:
        info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        df = info.get_data_frames()[0]
        if not df.empty:
            return df.iloc[0].to_dict()
        return None
    except Exception as e:
        print(f"Error fetching info for player {player_id}: {e}")
        return None


def calculate_fantasy_points(row: pd.Series, scoring: Dict) -> float:
    """
    Calculate fantasy points for a player game
    
    Args:
        row: Series with game stats
        scoring: Dictionary with scoring weights
    
    Returns:
        Fantasy points total
    """
    fp = (
        row.get('PTS', 0) * scoring.get('points', 1.0) +
        row.get('REB', 0) * scoring.get('rebounds', 1.2) +
        row.get('AST', 0) * scoring.get('assists', 1.5) +
        row.get('STL', 0) * scoring.get('steals', 3.0) +
        row.get('BLK', 0) * scoring.get('blocks', 3.0) +
        row.get('TOV', 0) * scoring.get('turnovers', -1.0)
    )
    return fp


def fetch_top_players_data(season: str = '2023-24', top_n: int = 150) -> pd.DataFrame:
    """
    Fetch data for top N players by fantasy points
    
    Args:
        season: Season string
        top_n: Number of top players to fetch
    
    Returns:
        DataFrame with aggregated player data
    """
    print(f"Fetching data for top {top_n} players from {season}...")
    
    # This is a placeholder - you'll need to:
    # 1. Get list of active players
    # 2. Fetch stats for each player
    # 3. Calculate fantasy points
    # 4. Sort and take top N
    # 5. Add rate limiting to avoid API limits
    
    # Example structure:
    # players_data = []
    # for player in active_players[:top_n]:
    #     stats = get_player_stats(player['id'], season)
    #     if stats is not None:
    #         # Calculate per-game fantasy points
    #         # Aggregate data
    #         players_data.append(...)
    #     time.sleep(0.6)  # Rate limiting
    
    return pd.DataFrame()  # Placeholder


if __name__ == "__main__":
    # Test data collection
    print("Testing data collection...")
    players_df = get_all_players()
    print(f"Found {len(players_df)} players")
    
    if len(players_df) > 0:
        # Test with first player
        test_player = players_df.iloc[0]
        print(f"\nTesting with player: {test_player['full_name']}")
        info = get_player_info(test_player['id'])
        if info:
            print(f"Position: {info.get('POSITION', 'N/A')}")
            print(f"Age: {info.get('AGE', 'N/A')}")
