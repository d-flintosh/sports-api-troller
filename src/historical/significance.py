import json
from copy import deepcopy
from typing import List

import humanize

from src.gcp.gcs import Gcs
from src.universal import publish_message
stat_list = [
    ('PTS', 'points'),
    ('REB', 'rebounds'),
    ('AST', 'assists'),
    ('BLK', 'blocks'),
    ('STL', 'steals'),
    ('FG3M', 'threes'),
]


def check_for_historical_significance(data: str, school: str, send_message: bool):
    dict_data = json.loads(data)
    player_stats = dict_data.get('player_stats')
    if any(e for e in player_stats if e.get('league_name') == 'nba'):
        gcs = Gcs(bucket='college-by-player-stats')
        full_path = f'nba/{school}/all_players/players.json'
        original_school_players = gcs.read_as_dict(url=full_path)
        updated_school_players = deepcopy(original_school_players)
        for player in player_stats:
            for all_time_player in updated_school_players.get('PlayerCareerByCollege'):
                if player.get('full_name', '').lower() == all_time_player.get('PLAYER_NAME', '').lower():
                    for stat_key, stat_text in stat_list:
                        all_time_player[stat_key] = all_time_player[stat_key] + player.get(stat_text)

        gcs.write(url=full_path, contents=updated_school_players)

        differences = []
        for stat_key, stat_text in stat_list:
            differences = differences + derive_positive_differences_in_stats(
                updated=updated_school_players,
                original=original_school_players,
                stat_key=stat_key,
                stat_text=stat_text
            )
        for difference in differences:
            publish_message(
                message=difference,
                school=school,
                topic='twitter-message-service-pubsub',
                send_message=send_message
            )


def get_top_3_players_by_stat(school: str, league_name: str, stat_key: str):
    gcs = Gcs(bucket='college-by-player-stats')
    full_path = f'{league_name}/{school}/all_players/players.json'
    players = gcs.read_as_dict(url=full_path)
    sorted_players = sorted(filter(lambda x: x.get(stat_key) is not None, players.get('PlayerCareerByCollege')), key=lambda i: i.get(stat_key), reverse=True)
    return_players = []
    index = 0
    return_players.append(f'1) {sorted_players[index].get("PLAYER_NAME")} - {sorted_players[index].get(stat_key)}')
    return_players.append(f'2) {sorted_players[index + 1].get("PLAYER_NAME")} - {sorted_players[index + 1].get(stat_key)}')
    return_players.append(f'3) {sorted_players[index + 2].get("PLAYER_NAME")} - {sorted_players[index + 2].get(stat_key)}')

    return return_players


def derive_positive_differences_in_stats(updated: dict, original: dict, stat_key: str, stat_text: str) -> List[str]:
    sorted_updated = sorted(filter(lambda x: x.get(stat_key) is not None, updated.get('PlayerCareerByCollege')), key=lambda i: i.get(stat_key), reverse=True)
    sorted_original = sorted(filter(lambda x: x.get(stat_key) is not None, original.get('PlayerCareerByCollege')), key=lambda i: i.get(stat_key), reverse=True)
    positive_differences = []

    for index, value in enumerate(sorted_original):
        if sorted_updated[index].get('PLAYER_NAME', '').lower() != value.get('PLAYER_NAME', '').lower():
            original_index = None
            for inner_index, inner_value in enumerate(sorted_original):
                if inner_value.get('PLAYER_NAME', '').lower() == sorted_updated[index].get('PLAYER_NAME', '').lower():
                    original_index = inner_index
                    break
            if index < original_index and index < 10:
                new_rank = index + 1
                extra_context = []
                if new_rank == 1:
                    extra_context.append(f'{new_rank}) {sorted_updated[index].get("PLAYER_NAME")} - {sorted_updated[index].get(stat_key)}')
                    extra_context.append(f'{new_rank + 1}) {sorted_updated[index + 1].get("PLAYER_NAME")} - {sorted_updated[index + 1].get(stat_key)}')
                    extra_context.append(f'{new_rank + 2}) {sorted_updated[index + 2].get("PLAYER_NAME")} - {sorted_updated[index + 2].get(stat_key)}')
                else:
                    extra_context.append(f'{new_rank-1}) {sorted_updated[index - 1].get("PLAYER_NAME")} - {sorted_updated[index - 1].get(stat_key)}')
                    extra_context.append(f'{new_rank}) {sorted_updated[index].get("PLAYER_NAME")} - {sorted_updated[index].get(stat_key)}')
                    extra_context.append(f'{new_rank+1}) {sorted_updated[index + 1].get("PLAYER_NAME")} - {sorted_updated[index + 1].get(stat_key)}')
                extra_context_str = '\n'.join(extra_context)
                positive_differences.append(f'{sorted_updated[index].get("PLAYER_NAME")} moved into {humanize.ordinal(new_rank)} place on the all time list for {stat_text}.\n\n{extra_context_str}')

    return positive_differences
