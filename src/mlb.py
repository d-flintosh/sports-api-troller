import logging
from typing import List

import statsapi

from main import publish_message, MessageObject
from src.universal import is_fsu


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


def player_stats_iterator(team: dict, player_ids: List[int]):
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


mlb_fsu_player_ids = [424706, 461881, 449142, 460368, 453625, 424366, 453625, 451795, 461749, 453461, 458245, 455072, 458233, 451795, 444360, 458244, 451196, 456650, 452220, 452245, 453593, 453561, 446564, 489075, 488778, 446135, 453203, 502086, 446135, 502228, 506917, 446273, 506912, 450572, 446344, 506925, 506927, 506914, 457763, 475424, 446344, 506927, 506918, 534631, 502076, 502219, 502781, 457748, 518713, 534630, 534627, 506924, 518642, 519010, 543219, 519010, 607257, 581639, 607256, 518642, 607256, 581532, 581530, 622212, 581527, 582473, 543747, 572879, 643440, 595328, 592247, 642006, 643260, 643540, 596133, 605335, 595328, 572879, 595895, 657763, 596056, 621466, 641507, 650327, 650393, 664928, 605282, 605208, 623518, 670764, 656275, 676811, 656586, 656290, 641429, 656604, 663947, 650397, 663728, 663485, 656604, 663622, 663947, 680501, 656586, 666141, 669001, 669283, 663682]


def get_fsu_baseball_players(use_static_list: bool) -> List:
    if use_static_list:
        return mlb_fsu_player_ids

    output = []
    for year in range(2000, 2020):
        params = {
            'year': str(year)
        }
        print(f'Making Draft Call for the Year {year}')
        draft = statsapi.get('draft', params=params)

        for round in draft.get('drafts').get('rounds'):
            for pick in round.get('picks'):
                if is_fsu(pick.get('school', {}).get('name', None)):
                    output.append(pick.get('person').get('id'))
    return output
