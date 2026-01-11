"""
Quick test script to verify data collection works
Run this to test if you can fetch NBA data
"""

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, commonplayerinfo
import pandas as pd
import time

def test_basic_data_collection():
    """Test basic data fetching"""
    print("🧪 Testing NBA Data Collection")
    print("=" * 50)
    
    # Test 1: Get players list
    print("\n1. Fetching players list...")
    try:
        all_players = players.get_players()
        print(f"   ✅ Found {len(all_players)} players")
        
        # Find a well-known player (LeBron James)
        lebron = [p for p in all_players if p['full_name'] == 'LeBron James']
        if lebron:
            player_id = lebron[0]['id']
            print(f"   ✅ Found test player: LeBron James (ID: {player_id})")
        else:
            # Use first player as fallback
            player_id = all_players[0]['id']
            print(f"   ✅ Using test player: {all_players[0]['full_name']} (ID: {player_id})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Get player info
    print("\n2. Fetching player info...")
    try:
        time.sleep(0.6)  # Rate limiting
        info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        info_df = info.get_data_frames()[0]
        if not info_df.empty:
            player_name = info_df.iloc[0]['DISPLAY_FIRST_LAST']
            position = info_df.iloc[0].get('POSITION', 'N/A')
            age = info_df.iloc[0].get('AGE', 'N/A')
            print(f"   ✅ Player: {player_name}")
            print(f"   ✅ Position: {position}")
            print(f"   ✅ Age: {age}")
        else:
            print("   ⚠️  No info found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Get game log (last season)
    print("\n3. Fetching game log for 2023-24 season...")
    try:
        time.sleep(0.6)  # Rate limiting
        game_log = playergamelog.PlayerGameLog(
            player_id=player_id,
            season='2023-24'
        )
        games_df = game_log.get_data_frames()[0]
        
        if not games_df.empty:
            games_played = len(games_df)
            avg_pts = games_df['PTS'].mean()
            avg_reb = games_df['REB'].mean()
            avg_ast = games_df['AST'].mean()
            
            print(f"   ✅ Games played: {games_played}")
            print(f"   ✅ Avg Points: {avg_pts:.1f}")
            print(f"   ✅ Avg Rebounds: {avg_reb:.1f}")
            print(f"   ✅ Avg Assists: {avg_ast:.1f}")
            
            # Calculate sample fantasy points
            from config import FANTASY_SCORING
            games_df['FANTASY_PTS'] = (
                games_df['PTS'] * FANTASY_SCORING['points'] +
                games_df['REB'] * FANTASY_SCORING['rebounds'] +
                games_df['AST'] * FANTASY_SCORING['assists'] +
                games_df['STL'] * FANTASY_SCORING['steals'] +
                games_df['BLK'] * FANTASY_SCORING['blocks'] +
                games_df['TOV'] * FANTASY_SCORING['turnovers']
            )
            avg_fp = games_df['FANTASY_PTS'].mean()
            print(f"   ✅ Avg Fantasy Points: {avg_fp:.1f}")
        else:
            print("   ⚠️  No games found (player may not have played in 2023-24)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   ⚠️  This might be due to rate limiting or player not active")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! Data collection is working.")
    print("\nNext steps:")
    print("1. Start building the baseline value module")
    print("2. Implement usage score calculation")
    print("3. Add injury scoring")
    return True

if __name__ == "__main__":
    test_basic_data_collection()
