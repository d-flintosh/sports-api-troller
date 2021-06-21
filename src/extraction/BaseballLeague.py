from typing import List, Optional

from src.api.mlb_sport_radar import MlbSportRadar
from src.extraction.League import League
from src.gcp.gcs import Gcs
from src.models.BaseballPlayer import BaseballPlayer, baseball_player_from_dict
from src.models.TweetObject import TweetObject


class BaseballLeague(League):
    def __init__(self, league_client: MlbSportRadar):
        super().__init__(league_name='mlb', sport='baseball')
        self.league_client = league_client
        self.college_by_player = Gcs(bucket='college-by-player').read_as_dict(url=f'{self.league_name}/players.json')

    def get_game_id(self, game: dict) -> str:
        return game.get('id')

    def get_games(self, date) -> Optional[List]:
        daily_schedule = self.league_client.get_daily_schedule(date=date)
        return self.get_filtered_games(daily_schedule.get('games'))

    def get_tweetable_objects(self, game: dict) -> Optional[List]:
        player_boxscores: [BaseballPlayer] = []

        game_id = self.get_game_id(game=game)
        boxscore = self.league_client.get_boxscore(game_id=game_id)

        home_team = boxscore.get('game', {}).get('home', {})
        away_team = boxscore.get('game', {}).get('away', {})
        player_boxscores = player_boxscores + self.player_stats_iterator(
            team=away_team,
            college_by_player=self.college_by_player
        )

        player_boxscores = player_boxscores + self.player_stats_iterator(
            team=home_team,
            college_by_player=self.college_by_player
        )

        tweetable_objects = list(
            filter(lambda x: x.tweet_path is not None, map(lambda x: TweetObject(player_object=x), player_boxscores)))

        return tweetable_objects

    @staticmethod
    def player_stats_iterator(team: dict, college_by_player: dict) -> List[BaseballPlayer]:
        output = []
        team_id = team.get('id')
        for player in team.get('players', {}):
            found_college_for_player = college_by_player.get(player.get('id', None))

            if found_college_for_player:
                player_obj = baseball_player_from_dict(
                    player=player,
                    team_id=team_id,
                    college=found_college_for_player
                )

                if player_obj.has_stats():
                    output.append(player_obj)

        return output

    @staticmethod
    def get_filtered_games(daily_schedule: List):
        games = list(filter(lambda game: game.get('status') in ['complete', 'closed'], daily_schedule))
        return games
