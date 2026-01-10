import pandas as pd
import numpy as np
import time
from nba_api.stats.endpoints import playergamelog, commonplayerinfo
from nba_api.stats.static import players
from config import *

def calculate_fpts(game_stats):
    fpts = 0
    fpts += (game_stats['PTS'] * 1) + \
            (game_stats['REB'] * 1) + \
            (game_stats['AST'] * 2) + \
            (game_stats['STL'] * 4) + \
            (game_stats['BLK'] * 4) - \
            (game_stats['TOV'] * 2) + \
            (game_stats['FGM'] * 2) - \
            (game_stats['FGA'] * 1) + \
            (game_stats['FTM'] * 1) - \
            (game_stats['FTA'] * 1) + \
            (game_stats['FG3M'] * 1)
    return fpts

def get_avg_fpts(player_id, season):
    try:
        time.sleep(0.6)
        game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
        game_log_df = game_log.get_data_frames()[0]

        fpts_list = []
        for game in game_log_df.iterrows():
            game_data = game[1]
            fpts = calculate_fpts(game_data)
            fpts_list.append(fpts)
        
        if not fpts_list:
            return -1
        else:
            avg = np.mean(fpts_list)
            return avg

    except Exception as e:
        print(f"Error fetching stats for player {player_id}: {e}")
        return -1

def calculate_3yr_avg_fpts(yr1, yr2, yr3):
    # baseline weights (how much each season counts towards the average)

    yr3_weight = 0.5
    yr2_weight = 0.3
    yr1_weight = 0.2

    if yr1 < 0:
        yr1_weight = 0
        yr2_weight += yr1_weight * (yr2_weight / (yr2_weight + yr3_weight))
        yr3_weight += yr1_weight * (yr3_weight / (yr2_weight + yr3_weight))

        if yr2 < 0:
            yr2_weight = 0
            yr3_weight = 1

            if yr3 < 0:
                return 0

        elif yr3 < 0:
            yr3_weight = 0
            yr2_weight = 1

    elif yr2 < 0:
       yr2_weight = 0
       yr3_weight += yr2_weight * (yr3_weight / (yr1_weight + yr3_weight))
       yr1_weight += yr2_weight * (yr1_weight / (yr1_weight + yr3_weight))

       if yr3 < 0:
            yr3_weight = 0
            yr1_weight = 1

    elif yr3 < 0:
       yr1_weight = 0
       yr3_weight += yr3_weight * (yr3_weight / (yr2_weight + yr3_weight))
       yr2_weight += yr3_weight * (yr2_weight / (yr2_weight + yr3_weight))

    avg_fpts = (yr1 * yr1_weight) + (yr2 * yr2_weight) + (yr3 * yr3_weight)
    return avg_fpts

def main():

    all_players = players.get_active_players()
    test_players = all_players[:20]  # Take the first 20 players for testing

    # Calculating baseline per-game value
    seasons = ['2021-22', '2022-23', '2023-24']
    
    yr1avg = get_avg_fpts(203507, seasons[0])
    yr2avg = get_avg_fpts(203507, seasons[1])
    yr3avg = get_avg_fpts(203507, seasons[2])
    print(calculate_3yr_avg_fpts(yr1avg, yr2avg, yr3avg))

    kept_players = []
    for player in test_players:
        yr1avg = get_avg_fpts(player['id'], seasons[0])
        yr2avg = get_avg_fpts(player['id'], seasons[1])
        yr3avg = get_avg_fpts(player['id'], seasons[2])
        pre_avg_fpts = calculate_3yr_avg_fpts(yr1avg, yr2avg, yr3avg)
        if pre_avg_fpts == 0:
            continue
        kept_players.append(player)

main()




