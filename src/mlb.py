from typing import List

import pandas
import statsapi

from src.gcp.gcs import Gcs
from src.models.BaseballPlayer import BaseballPlayer, baseball_player_from_dict
from src.models.SendTweetForSchool import SendTweetForSchool
from src.models.TweetObject import TweetObject


def get_mlb(date_to_run, send_message: bool = True):
    player_boxscores: [BaseballPlayer] = []
    formatted_date = date_to_run.strftime('%m/%d/%Y')
    college_by_player = Gcs().read_as_dict(url='mlb/MLBPlayerDraft.json')

    print(f'Getting games played for date: {formatted_date}')
    schedule = statsapi.schedule(date=formatted_date)
    for game in schedule:
        boxscore = statsapi.boxscore_data(gamePk=game.get('game_id'))
        player_boxscores = player_boxscores + player_stats_iterator(team=boxscore.get('away'),
                                                                    college_by_player=college_by_player)
        player_boxscores = player_boxscores + player_stats_iterator(team=boxscore.get('home'),
                                                                    college_by_player=college_by_player)

    tweetable_objects = list(filter(lambda x: x.tweet_path is not None, map(lambda x: TweetObject(player_object=x), player_boxscores)))

    if tweetable_objects:
        df = pandas.DataFrame([vars(s) for s in tweetable_objects]).groupby('tweet_path')

        for school_group in df:
            school = school_group[0]
            player_stats = school_group[1]["player_object"].to_list()
            SendTweetForSchool(school=str(school), player_stats=player_stats).publish(send_message=send_message, sport='baseball')


def player_stats_iterator(team: dict, college_by_player: dict) -> List[BaseballPlayer]:
    output = []
    team_id = team.get('team', {}).get('id', None)
    players = team.get('players', {})
    for key, player in players.items():
        found_college_for_player = college_by_player.get(str(player.get('person', {}).get('id', None)), None)

        if found_college_for_player:
            player_obj = baseball_player_from_dict(
                player=player,
                team_id=team_id,
                college=found_college_for_player
            )
            if player_obj.is_decent_day():
                output.append(player_obj)

    return output
