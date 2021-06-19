from typing import List, Optional, Union

from src.api.basketball_sport_radar import BasketballSportRadar
from src.gcp.gcs import Gcs
from src.models.BasketballPlayer import BasketballPlayer, basketball_player_from_dict
from src.extraction.League import League
from src.models.TweetObject import TweetObject


class BasketballLeague(League):
    def __init__(self, league_name: str, league_client: BasketballSportRadar):
        super().__init__(league_name=league_name, sport='basketball')
        self.league_client = league_client
        self.college_by_player = Gcs(bucket='college-by-player').read_as_dict(url=f'{self.league_name}/players.json')

    def get_game_id(self, game: dict) -> Union[str, int]:
        return game.get('id')

    def get_games(self, date) -> Optional[List]:
        daily_schedule = self.league_client.get_daily_schedule(date=date)
        return self.get_filtered_games(daily_schedule)

    def get_tweetable_objects(self, game: dict) -> Optional[List]:
        tweetable_objects: [TweetObject] = []
        game_id = self.get_game_id(game=game)

        boxscore = self.league_client.get_boxscore(game_id=game_id)
        home_team = boxscore.get('home')
        away_team = boxscore.get('away')
        for player in home_team.get('players'):
            player_id = player.get('id')
            basketball_player: BasketballPlayer = basketball_player_from_dict(
                player=player,
                team_id=home_team.get('id'),
                league_name=self.league_name,
                college=self.college_by_player.get(player_id)
            )

            if basketball_player and basketball_player.has_stats():
                tweetable_objects.append(TweetObject(player_object=basketball_player))

        for player in away_team.get('players'):
            player_id = player.get('id')
            basketball_player: BasketballPlayer = basketball_player_from_dict(
                player=player,
                team_id=away_team.get('id'),
                league_name=self.league_name,
                college=self.college_by_player.get(player_id)
            )
            if basketball_player and basketball_player.has_stats():
                tweetable_objects.append(TweetObject(player_object=basketball_player))

        return tweetable_objects

    @staticmethod
    def get_filtered_games(daily_schedule: dict):
        games = daily_schedule.get('games', [])
        games = list(filter(lambda game: game.get('status') in ['complete', 'closed'], games))
        return games
