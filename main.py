import logging
import time
from dataclasses import dataclass
from datetime import date, timedelta
from typing import List

import statsapi
from google.cloud import pubsub_v1
from nba_api.stats.endpoints import commonplayerinfo, scoreboard, boxscoretraditionalv2
from nba_api.stats.library.parameters import LeagueID


@dataclass
class MessageObject:
    raw_data: List
    message: str


def publish_message(message: str):
    publisher = pubsub_v1.PublisherClient()
    topic_id = 'projects/sports-data-service/topics/twitter-message-service-pubsub'
    print(f'Publishing message: {message}')
    future = publisher.publish(topic_id, str.encode(message))
    future.result()


def is_fsu(school: str):
    _fsu = ['florida state', 'fsu', 'florida state university']

    if school and school and any(list(map(lambda x: x == school.lower(), _fsu))):
        return True
    return False


def get_fsu_players() -> List:
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


def is_a_decent_day(player: dict):
    try:
        if player.get('stats', {}).get('batting', {}).get('hits', 0) > 0:
            return True
    except TypeError as e:
        logging.error(f'Failed to parse player: {player}')
    return False


def player_stats_iterator(team: dict, player_ids: List[int]):
    output = []
    players = team.get('players', {})
    for key, player in players.items():
        if player.get('person').get('id') in player_ids and is_a_decent_day(player=player):
            output.append(player)

    return output


mlb_fsu_player_ids = [424706, 461881, 449142, 460368, 453625, 424366, 453625, 451795, 461749, 453461, 458245, 455072, 458233, 451795, 444360, 458244, 451196, 456650, 452220, 452245, 453593, 453561, 446564, 489075, 488778, 446135, 453203, 502086, 446135, 502228, 506917, 446273, 506912, 450572, 446344, 506925, 506927, 506914, 457763, 475424, 446344, 506927, 506918, 534631, 502076, 502219, 502781, 457748, 518713, 534630, 534627, 506924, 518642, 519010, 543219, 519010, 607257, 581639, 607256, 518642, 607256, 581532, 581530, 622212, 581527, 582473, 543747, 572879, 643440, 595328, 592247, 642006, 643260, 643540, 596133, 605335, 595328, 572879, 595895, 657763, 596056, 621466, 641507, 650327, 650393, 664928, 605282, 605208, 623518, 670764, 656275, 676811, 656586, 656290, 641429, 656604, 663947, 650397, 663728, 663485, 656604, 663622, 663947, 680501, 656586, 666141, 669001, 669283, 663682]


def entrypoint(event, context):
    # fsu_player_ids = get_fsu_players()
    yesterday = date.today() - timedelta(1)

    get_mlb(date_to_run=yesterday)
    get_basketball(date_to_run=yesterday, league_id=LeagueID.nba)
    get_basketball(date_to_run=yesterday, league_id=LeagueID.wnba)


def get_mlb(date_to_run) -> MessageObject:
    fsu_player_boxscores = []
    formatted_date = date_to_run.strftime('%m/%d/%Y')
    print(f'Getting games played for date: {formatted_date}')
    schedule = statsapi.schedule(date=formatted_date)
    for game in schedule:
        boxscore = statsapi.boxscore_data(gamePk=game.get('game_id'))
        fsu_player_boxscores = fsu_player_boxscores + player_stats_iterator(team=boxscore.get('away'),
                                                                            player_ids=mlb_fsu_player_ids)
        fsu_player_boxscores = fsu_player_boxscores + player_stats_iterator(team=boxscore.get('home'),
                                                                            player_ids=mlb_fsu_player_ids)
    tweet_message = ''
    for fsu_player in fsu_player_boxscores:
        tweet_message = tweet_message + f'{fsu_player.get("person").get("fullName")} went {fsu_player.get("stats").get("batting").get("hits")}-{fsu_player.get("stats").get("batting").get("atBats")}. '

    if fsu_player_boxscores:
        publish_message(message=tweet_message)

    return MessageObject(raw_data=fsu_player_boxscores, message=tweet_message)


def get_basketball(date_to_run, league_id: str) -> MessageObject:
    fsu_player_boxscores = []
    formatted_date = date_to_run.strftime('%m/%d/%Y')
    print(f'Getting games played for date: {formatted_date}')
    schedule = scoreboard.Scoreboard(game_date=formatted_date, league_id=league_id)
    game_ids = set(map(lambda x: x.get('GAME_ID'), schedule.get_normalized_dict().get('GameHeader')))

    for game_id in game_ids:
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)

        for player in boxscore.get_normalized_dict().get('PlayerStats'):
            time.sleep(2)
            player_id = player.get('PLAYER_ID')
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_normalized_dict()
            if any(list(map(lambda x: is_fsu(x.get('SCHOOL')), player_info.get('CommonPlayerInfo')))):
                fsu_player_boxscores.append(player)

    tweet_message = ''
    for fsu_player in fsu_player_boxscores:
        stat_line = []
        player_points = fsu_player.get('PTS', 0)
        player_rebounds = fsu_player.get('REB', 0)
        player_assists = fsu_player.get('AST', 0)
        if player_points or player_rebounds or player_assists:
            if player_points and player_points > 0:
                stat_line.append(f'{player_points} pts')
            if player_rebounds and player_rebounds > 0:
                stat_line.append(f'{player_rebounds} reb')
            if player_assists and player_assists > 0:
                stat_line.append(f'{player_assists} ast')

            tweet_message = tweet_message + f'{fsu_player.get("PLAYER_NAME")} {"/".join(stat_line)}'

    if fsu_player_boxscores:
        print(tweet_message)
        publish_message(message=tweet_message)

    return MessageObject(raw_data=fsu_player_boxscores, message=tweet_message)
