import time
from dataclasses import dataclass
from datetime import date, timedelta
from typing import List

from google.cloud import pubsub_v1
from nba_api.stats.endpoints import commonplayerinfo, scoreboard, boxscoretraditionalv2
from nba_api.stats.library.parameters import LeagueID

from src.mlb import get_mlb
from src.universal import is_fsu


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


def entrypoint(event, context):
    yesterday = date.today() - timedelta(1)

    get_mlb(date_to_run=yesterday)
    get_basketball(date_to_run=yesterday, league_id=LeagueID.nba)
    get_basketball(date_to_run=yesterday, league_id=LeagueID.wnba)


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
        publish_message(message=tweet_message)

    return MessageObject(raw_data=fsu_player_boxscores, message=tweet_message)
