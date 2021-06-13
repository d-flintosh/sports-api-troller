from dataclasses import dataclass

from src.models.Emojis import Emojis
from src.models.MlbTeams import mlb_team_map
from src.models.Player import Player
from src.universal import get_team_text


@dataclass
class BaseballPlayer(Player):
    id: int
    full_name: str
    team_id: int
    college: str
    hits: int
    at_bats: int
    home_runs: int

    def is_decent_day(self):
        return self.hits > 0

    def convert_to_tweet(self):
        team_text = get_team_text(team_map=mlb_team_map, team_id=self.team_id)

        had_a_tater = f' {self.home_runs} {Emojis.TATER.value}' if self.home_runs > 0 else ''
        return f'{self.full_name}{team_text} went {self.hits}-{self.at_bats}{had_a_tater}'

    def get_college(self):
        return self.college


def baseball_player_from_dict(player: dict, team_id: int, college: dict):
    return BaseballPlayer(
        id=player.get('person').get('id'),
        full_name=player.get('person').get('fullName'),
        team_id=team_id,
        college=college.get('college'),
        hits=player.get('stats', {}).get('batting', {}).get('hits', 0),
        at_bats=player.get('stats', {}).get('batting', {}).get('atBats', 0),
        home_runs=player.get('stats', {}).get('batting', {}).get('homeRuns', 0)
    )
