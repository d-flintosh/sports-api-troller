from copy import deepcopy
from typing import List

from src.gcp.gcs import Gcs
from src.historical import historical_stats_bucket

nhl_stat_list = [
    ('goals', 'goals'),
    ('assists', 'assists')
]


def get_nhl_historical_stats(school: str, player_stats: List) -> dict:
    gcs = Gcs(bucket=historical_stats_bucket)
    full_path = f'nhl/{school}/all_players/players.json'
    original_school_players = gcs.read_as_dict(url=full_path)
    updated_school_players = deepcopy(original_school_players)
    player_name_key = 'full_name'
    dictionary_key = 'player_stats'
    for player in player_stats:
        for all_time_player in updated_school_players.get(dictionary_key):
            if player.get('full_name', '').lower() == all_time_player.get(player_name_key, '').lower():
                for stat_key, stat_text in nhl_stat_list:
                    all_time_player[stat_key] = all_time_player[stat_key] + player.get(stat_text)

    gcs.write(url=full_path, contents=updated_school_players)

    return {
        'original_school_players': original_school_players,
        'updated_school_players': updated_school_players,
        'stat_list': nhl_stat_list,
        'player_name_key': player_name_key,
        'dictionary_key': dictionary_key
    }
