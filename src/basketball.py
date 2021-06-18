import pandas

from src.api.basketball_sport_radar import BasketballSportRadar
from src.gcp.gcs import Gcs
from src.models.BasketballPlayer import basketball_player_from_dict, BasketballPlayer
from src.models.SendTweetForSchool import SendTweetForSchool
from src.models.TweetObject import TweetObject


def get_basketball(date_to_run, league_client: BasketballSportRadar, league_name: str, send_message: bool):
    tweetable_objects: [TweetObject] = []

    formatted_date = date_to_run.strftime('%m/%d/%Y')
    print(f'Getting games played for date: {formatted_date}')

    college_by_player = Gcs('college-by-player').read_as_dict(url=f'{league_name}/players.json')

    daily_schedule = league_client.get_daily_schedule(date=date_to_run)
    games = get_filtered_games(daily_schedule)

    for game in games:
        game_id = game.get('id')

        boxscore = league_client.get_boxscore(game_id=game_id)
        home_team = boxscore.get('home')
        away_team = boxscore.get('away')
        for player in home_team.get('players'):
            player_id = player.get('id')
            basketball_player: BasketballPlayer = basketball_player_from_dict(
                player=player,
                team_id=home_team.get('id'),
                league_name=league_name,
                college=college_by_player.get(player_id)
            )

            if basketball_player.has_stats():
                tweetable_objects.append(TweetObject(player_object=basketball_player))

        for player in away_team.get('players'):
            player_id = player.get('id')
            basketball_player: BasketballPlayer = basketball_player_from_dict(
                player=player,
                team_id=away_team.get('id'),
                league_name=league_name,
                college=college_by_player.get(player_id)
            )
            if basketball_player.has_stats():
                tweetable_objects.append(TweetObject(player_object=basketball_player))

    if tweetable_objects:
        df = pandas.DataFrame([vars(s) for s in tweetable_objects]).groupby('tweet_path')

        for school_group in df:
            school = school_group[0]
            player_stats = school_group[1]["player_object"].to_list()
            SendTweetForSchool(school=str(school), player_stats=player_stats).publish(send_message=send_message, sport='basketball')


def get_filtered_games(daily_schedule: dict):
    games = daily_schedule.get('games', [])
    games = list(filter(lambda game: game.get('status') == 'closed', games))
    return games
