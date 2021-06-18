from datetime import date, datetime, timedelta
from typing import List, Optional, Union

from src.api.golf_sport_radar import GolfSportRadar
from src.gcp.gcs import Gcs
from src.extraction.League import League
from src.models.GolfPlayer import golf_player_from_dict
from src.models.TweetObject import TweetObject


class GolfLeague(League):
    def __init__(self, league_name: str, league_client: GolfSportRadar):
        super().__init__(league_name=league_name, sport='golf')
        self.league_client = league_client
        self.college_by_player = Gcs(bucket='college-by-player').read_as_dict(url=f'{self.league_name}/players.json')

    def get_game_id(self, game: dict) -> Union[str, int]:
        return game.get('id')

    def get_games(self, date) -> Optional[List]:
        schedule = self.league_client.get_tournament_schedule()
        return self.get_filtered_games(schedule=schedule, date=date)

    def get_tweetable_objects(self, game: dict) -> Optional[List]:
        tweetable_objects: [TweetObject] = []
        tournament_id = self.get_game_id(game=game)
        leaderboard = self.league_client.get_tournament_leaderboard(tournament_id=tournament_id)

        for player in leaderboard.get('leaderboard'):
            player_id = player.get('id')
            golf_player = golf_player_from_dict(
                player=player,
                league_name=self.league_name,
                college=self.college_by_player.get(player_id)
            )

            if golf_player and golf_player.has_stats():
                tweetable_objects.append(TweetObject(player_object=golf_player))

        return tweetable_objects

    @staticmethod
    def get_filtered_games(schedule: dict, date):
        tournament = schedule.get('tournaments', [])

        def is_date_in_range(start: str, end: str, reference_date: date):
            start_date = datetime.strptime(start, '%Y-%m-%d').date()
            end_date = datetime.strptime(end, '%Y-%m-%d').date() + timedelta(1)
            is_in_range = start_date <= reference_date <= end_date
            return is_in_range

        tournament = list(
            filter(
                lambda x: is_date_in_range(start=x.get('start_date'), end=x.get('end_date'), reference_date=date)
                          and x.get('status') in ['inprogress', 'closed']
                          and x.get('event_type') == 'stroke', tournament
            )
        )
        return tournament
