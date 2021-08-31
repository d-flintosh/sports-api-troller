from typing import List, Optional, Union

import pandas as pd

from src.api.nfl_sport_radar import NflSportRadar
from src.extraction.League import League
from src.gcp.gcs import Gcs
from src.models.FootballPlayer import football_player_from_dict, FootballPlayer
from src.models.TweetObject import TweetObject


class FootballLeague(League):
    def __init__(self, league_name: str, league_client: NflSportRadar):
        super().__init__(league_name=league_name, sport='football')
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
        home_team = boxscore.get('statistics', {}).get('home')
        away_team = boxscore.get('statistics', {}).get('away')

        all_players = {}

        statistical_categories = [
            'rushing',
            'receiving',
            'passing',
            'defense',
            'field_goals'
        ]
        for team in [home_team, away_team]:
            for stat in statistical_categories:
                for player in team.get(stat, {}).get('players', {}):
                    if all_players.get(player.get('id', None)):
                        new_stat = {
                            stat: player
                        }
                        all_players[player.get('id')] = all_players[player.get('id')] | new_stat
                    elif player != {}:
                        all_players[player.get('id')] = {
                            'team_id': team.get('id', None),
                            'player_id': player.get('id'),
                            'full_name': player.get('name'),
                            stat: player
                        }

        for player_id, player_stats in all_players.items():
            football_player: FootballPlayer = football_player_from_dict(
                player=player_stats,
                college=self.college_by_player.get(player_id)
            )

            if football_player and football_player.has_stats():
                tweetable_objects.append(TweetObject(player_object=football_player))

        return tweetable_objects

    @staticmethod
    def get_filtered_games(daily_schedule: List):
        games = list(filter(lambda game: game.get('status') in ['complete', 'closed'], daily_schedule))
        return games
