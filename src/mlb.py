from typing import Set, List

import statsapi

from src.college.mlb import get_fsu_baseball_players
from src.models.BaseballPlayer import BaseballPlayer, baseball_player_from_dict
from src.models.Emojis import Emojis
from src.models.MessageObject import MessageObject
from src.universal import publish_message


def get_mlb(date_to_run) -> MessageObject:
    player_ids_to_check = get_fsu_baseball_players(use_static_list=True)
    fsu_player_boxscores: [BaseballPlayer] = []
    formatted_date = date_to_run.strftime('%m/%d/%Y')

    print(f'Getting games played for date: {formatted_date}')
    schedule = statsapi.schedule(date=formatted_date)
    for game in schedule:
        boxscore = statsapi.boxscore_data(gamePk=game.get('game_id'))
        fsu_player_boxscores = fsu_player_boxscores + player_stats_iterator(team=boxscore.get('away'),
                                                                            player_ids=player_ids_to_check)
        fsu_player_boxscores = fsu_player_boxscores + player_stats_iterator(team=boxscore.get('home'),
                                                                            player_ids=player_ids_to_check)

    tweet_message = '. '.join(list(map(lambda x: x.convert_to_tweet(), fsu_player_boxscores))) + '.'

    if fsu_player_boxscores:
        message_prefix = f'{Emojis.FSU_SPEAR.value}{Emojis.BASEBALL.value} @FSUBaseball {Emojis.BASEBALL.value}{Emojis.FSU_SPEAR.value}\n'
        publish_message(message=message_prefix + tweet_message)

    return MessageObject(raw_data=fsu_player_boxscores, message=tweet_message)


def player_stats_iterator(team: dict, player_ids: Set[int]) -> List[BaseballPlayer]:
    output = []
    players = team.get('players', {})
    for key, player in players.items():
        player_obj = baseball_player_from_dict(player=player)
        if player_obj.id in player_ids and player_obj.is_decent_day():
            output.append(player_obj)

    return output
