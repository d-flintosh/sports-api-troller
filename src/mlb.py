import logging
from typing import Set

import statsapi

from src.college.mlb import get_fsu_baseball_players
from src.models.MessageObject import MessageObject
from src.universal import publish_message


def get_mlb(date_to_run) -> MessageObject:
    player_ids_to_check = get_fsu_baseball_players(use_static_list=True)
    fsu_player_boxscores = []
    formatted_date = date_to_run.strftime('%m/%d/%Y')
    print(f'Getting games played for date: {formatted_date}')
    schedule = statsapi.schedule(date=formatted_date)
    for game in schedule:
        boxscore = statsapi.boxscore_data(gamePk=game.get('game_id'))
        fsu_player_boxscores = fsu_player_boxscores + player_stats_iterator(team=boxscore.get('away'),
                                                                            player_ids=player_ids_to_check)
        fsu_player_boxscores = fsu_player_boxscores + player_stats_iterator(team=boxscore.get('home'),
                                                                            player_ids=player_ids_to_check)
    tweet_message = ''
    for fsu_player in fsu_player_boxscores:
        tweet_message = tweet_message + f'{fsu_player.get("person").get("fullName")} went {fsu_player.get("stats").get("batting").get("hits")}-{fsu_player.get("stats").get("batting").get("atBats")}. '

    if fsu_player_boxscores:
        publish_message(message=tweet_message)

    return MessageObject(raw_data=fsu_player_boxscores, message=tweet_message)


def player_stats_iterator(team: dict, player_ids: Set[int]):
    output = []
    players = team.get('players', {})
    for key, player in players.items():
        if player.get('person').get('id') in player_ids and is_a_decent_day(player=player):
            output.append(player)

    return output


def is_a_decent_day(player: dict):
    try:
        if player.get('stats', {}).get('batting', {}).get('hits', 0) > 0:
            return True
    except TypeError as e:
        logging.error(f'Failed to parse player: {player}')
    return False



