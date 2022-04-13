import json
from typing import List

import humanize

from src.gcp.gcs import Gcs
from src.historical import historical_stats_bucket
from src.historical.basketball_significance import get_basketball_historical_stats
from src.historical.mlb_significance import get_mlb_historical_stats
from src.historical.nhl_significance import get_nhl_historical_stats
from src.universal import publish_message


def check_for_historical_significance(data: str, school: str, send_message: bool):
    dict_data = json.loads(data)
    player_stats = dict_data.get('player_stats')
    historical_significance = None

    if any(e for e in player_stats if e.get('league_name') == 'nba'):
        pass
        # historical_significance = get_basketball_historical_stats(school=school, player_stats=player_stats)
    elif any(e for e in player_stats if e.get('league_name') == 'nhl'):
        historical_significance = get_nhl_historical_stats(school=school, player_stats=player_stats)
    elif any(e for e in player_stats if e.get('league_name') == 'mlb'):
        historical_significance = get_mlb_historical_stats(school=school, player_stats=player_stats)

    if historical_significance is not None:
        differences = []
        for stat_key, stat_text in historical_significance.get('stat_list'):
            differences = differences + derive_positive_differences_in_stats(
                inputs=historical_significance,
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


def get_top_3_players_by_stat(school: str, league_name: str, stat_key: str, dictionary_key: str, player_name_key: str):
    gcs = Gcs(bucket=historical_stats_bucket)
    full_path = f'{league_name}/{school}/all_players/players.json'
    players = gcs.read_as_dict(url=full_path)
    sorted_players = sorted(filter(lambda x: x.get(stat_key) is not None, players.get(dictionary_key)), key=lambda i: i.get(stat_key), reverse=True)
    return_players = []
    index = 0
    return_players.append(f'1) {sorted_players[index].get(player_name_key)} - {sorted_players[index].get(stat_key)}')
    return_players.append(f'2) {sorted_players[index + 1].get(player_name_key)} - {sorted_players[index + 1].get(stat_key)}')
    return_players.append(f'3) {sorted_players[index + 2].get(player_name_key)} - {sorted_players[index + 2].get(stat_key)}')

    return return_players


def derive_positive_differences_in_stats(inputs: dict, stat_key: str, stat_text: str) -> List[str]:
    updated = inputs.get('updated_school_players')
    original = inputs.get('original_school_players')
    dictionary_key = inputs.get('dictionary_key')
    player_name_key = inputs.get('player_name_key')
    sorted_updated = sorted(filter(lambda x: x.get(stat_key) is not None, updated.get(dictionary_key)), key=lambda i: i.get(stat_key), reverse=True)
    sorted_original = sorted(filter(lambda x: x.get(stat_key) is not None, original.get(dictionary_key)), key=lambda i: i.get(stat_key), reverse=True)
    positive_differences = []

    for index, value in enumerate(sorted_original):
        if sorted_updated[index].get(player_name_key, '').lower() != value.get(player_name_key, '').lower():
            original_index = None
            for inner_index, inner_value in enumerate(sorted_original):
                if inner_value.get(player_name_key, '').lower() == sorted_updated[index].get(player_name_key, '').lower():
                    original_index = inner_index
                    break
            if index < original_index and index < 10:
                new_rank = index + 1
                extra_context = []
                if new_rank == 1:
                    extra_context.append(f'{new_rank}) {sorted_updated[index].get(player_name_key)} - {sorted_updated[index].get(stat_key)}')
                    extra_context.append(f'{new_rank + 1}) {sorted_updated[index + 1].get(player_name_key)} - {sorted_updated[index + 1].get(stat_key)}')
                    extra_context.append(f'{new_rank + 2}) {sorted_updated[index + 2].get(player_name_key)} - {sorted_updated[index + 2].get(stat_key)}')
                else:
                    extra_context.append(f'{new_rank-1}) {sorted_updated[index - 1].get(player_name_key)} - {sorted_updated[index - 1].get(stat_key)}')
                    extra_context.append(f'{new_rank}) {sorted_updated[index].get(player_name_key)} - {sorted_updated[index].get(stat_key)}')
                    extra_context.append(f'{new_rank+1}) {sorted_updated[index + 1].get(player_name_key)} - {sorted_updated[index + 1].get(stat_key)}')
                extra_context_str = '\n'.join(extra_context)
                positive_differences.append(f'{sorted_updated[index].get(player_name_key)} moved into {humanize.ordinal(new_rank)} place on the all time list for {stat_text}.\n\n{extra_context_str}')

    return positive_differences
