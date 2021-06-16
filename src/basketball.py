import pandas
from nba_api.stats.endpoints import scoreboard, boxscoretraditionalv2
from nba_api.stats.library.parameters import LeagueID

from src.college.basketball import convert_league_id_to_string
from src.gcp.gcs import Gcs
from src.models.BasketballPlayer import basketball_player_from_dict, BasketballPlayer
from src.models.SendTweetForSchool import SendTweetForSchool
from src.models.TweetObject import TweetObject


def get_basketball(date_to_run, league_id: LeagueID, send_message: bool):
    tweetable_objects: [TweetObject] = []

    formatted_date = date_to_run.strftime('%m/%d/%Y')
    print(f'Getting games played for date: {formatted_date}')
    league_name = convert_league_id_to_string(league_id=league_id)
    college_by_player = Gcs('college-by-player').read_as_dict(url=f'{league_name}/players.json')

    schedule = scoreboard.Scoreboard(game_date=formatted_date, league_id=league_id)
    game_ids = set(map(lambda x: x.get('GAME_ID'), schedule.get_normalized_dict().get('GameHeader')))

    for game_id in game_ids:
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)

        for player in boxscore.get_normalized_dict().get('PlayerStats'):
            player_id = player.get('PLAYER_ID')
            basketball_player: BasketballPlayer = basketball_player_from_dict(
                player=player,
                league_id=league_id,
                college=college_by_player.get(str(player_id))
            )
            if basketball_player.has_stats():
                tweetable_objects.append(TweetObject(player_object=basketball_player))

    if tweetable_objects:
        df = pandas.DataFrame([vars(s) for s in tweetable_objects]).groupby('tweet_path')

        for school_group in df:
            school = school_group[0]
            player_stats = school_group[1]["player_object"].to_list()
            print(f'42: {school} and stats: {str(player_stats)}')
            SendTweetForSchool(school=str(school), player_stats=player_stats).publish(send_message=send_message, sport='basketball')
