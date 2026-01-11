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
        # getting the stats for a player for every game of a season and making it into a df
        game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
        game_log_df = game_log.get_data_frames()[0]

        # making list of their fantasy points for each game
        fpts_list = []
        # making list for players minutes to determine usage
        mins_list = []
        for game in game_log_df.iterrows():
            game_data = game[1]
            fpts = calculate_fpts(game_data)
            fpts_list.append(fpts)
            mins_list.append(game_data['MIN'])

        # if empty list (no games played in season)
        if not fpts_list:
            return -1, -1
        # otherwise calculate average fpts for season
        else:
            avg = np.mean(fpts_list)
            mins_avg = np.mean(mins_list)
            return avg, mins_avg

    except Exception as e:
        print(f"Error fetching stats for player {player_id}: {e}")
        return -1

def calculate_3yr_avg_fpts(yr1, yr2, yr3, yr1mins, yr2mins, yr3mins):

    # baseline weights (how much each season counts towards the average)
    yr3_weight = 0.65
    yr2_weight = 0.25
    yr1_weight = 0.1

    # redistributing weight if player was unavailable for 1+ seasons
    if yr1 < 0:
        yr1_weight = 0
        yr2_weight += yr1_weight * (yr2_weight / (yr2_weight + yr3_weight))
        yr3_weight += yr1_weight * (yr3_weight / (yr2_weight + yr3_weight))

        if yr2 < 0:
            yr2_weight = 0
            yr3_weight = 1

            if yr3 < 0:
                return 0, 0

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

    # recalculating average fantasy points for past three years, valuing later years
    avg_fpts = (yr1 * yr1_weight) + (yr2 * yr2_weight) + (yr3 * yr3_weight)
    avg_mins = (yr1mins * yr1_weight) + (yr2mins * yr2_weight) + (yr3mins * yr3_weight)
    return avg_fpts, avg_mins

def main():

    # get all active players in a list
    all_players = players.get_active_players()
    test_players = all_players[:20]  # Take the first 20 players for testing

    # Calculating baseline per-game value
    seasons = ['2021-22', '2022-23', '2023-24']
    
    # testing with Giannis
    yr1avg, yr1mins = get_avg_fpts(203507, seasons[0])
    yr2avg, yr2mins = get_avg_fpts(203507, seasons[1])
    yr3avg, yr3mins = get_avg_fpts(203507, seasons[2])
    # print(calculate_3yr_avg_fpts(yr1avg, yr2avg, yr3avg))

    
    # making list with players who have played at least 1/3 season 
    # (some players considered active in api haven't)
    kept_players = []
    for player in test_players: # SWITCH TO ALL
        yr1avg, yr1mins = get_avg_fpts(player['id'], seasons[0])
        yr2avg, yr2mins = get_avg_fpts(player['id'], seasons[1])
        yr3avg, yr3mins = get_avg_fpts(player['id'], seasons[2])
        pre_avg_fpts, avg_mins = calculate_3yr_avg_fpts(yr1avg, yr2avg, yr3avg, yr1mins, yr2mins, yr3mins)
        if pre_avg_fpts == 0:
            continue
        kept_players.append({'player': player, 'avg_fpts': pre_avg_fpts, 'avg_mins': avg_mins})

    # sort by avg_fpts descending and take top 150
    kept_players.sort(key=lambda x: x['avg_fpts'], reverse=True)
    top150 = kept_players[:20] # SWITCH TO 150

    # print first 20 names (with rank and score)
    for i, player in enumerate(top150, start=1): # ADD [:20]
        name = player['player'].get('full_name') 
        print(f"{i}. {name} - {player['avg_fpts']:.2f}")
    


main()




