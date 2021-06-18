from typing import List, Optional, Union

import statsapi

from src.gcp.gcs import Gcs
from src.models.BaseballPlayer import BaseballPlayer, baseball_player_from_dict
from src.extraction.League import League
from src.models.TweetObject import TweetObject


class BaseballLeague(League):
    def __init__(self):
        super().__init__(league_name='mlb', sport='baseball')
        self.college_by_player = Gcs(bucket='college-by-player').read_as_dict(url=f'{self.league_name}/MLBPlayerDraft.json')

    def get_game_id(self, game: dict) -> Union[str, int]:
        return game.get('game_id')

    def get_games(self, date) -> Optional[List]:
        formatted_date = date.strftime('%m/%d/%Y')
        schedule = statsapi.schedule(date=formatted_date)
        return self.get_filtered_games(schedule)

    def get_tweetable_objects(self, game: dict) -> Optional[List]:
        boxscore = statsapi.boxscore_data(gamePk=game.get('game_id'))
        player_boxscores: [BaseballPlayer] = []
        player_boxscores = player_boxscores + self.player_stats_iterator(team=boxscore.get('away'),
                                                                         college_by_player=self.college_by_player)
        player_boxscores = player_boxscores + self.player_stats_iterator(team=boxscore.get('home'),
                                                                         college_by_player=self.college_by_player)

        tweetable_objects = list(
            filter(lambda x: x.tweet_path is not None, map(lambda x: TweetObject(player_object=x), player_boxscores)))

        return tweetable_objects

    @staticmethod
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

                if player_obj.has_stats():
                    output.append(player_obj)

        return output

    @staticmethod
    def get_filtered_games(daily_schedule: List):
        games = list(filter(lambda game: game.get('status') == 'Final', daily_schedule))
        return games
