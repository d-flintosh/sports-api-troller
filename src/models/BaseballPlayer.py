from dataclasses import dataclass

from src.models.Emojis import Emojis


@dataclass
class BaseballPlayer:
    id: int
    full_name: str
    college: str
    hits: int
    at_bats: int
    home_runs: int

    def is_decent_day(self):
        return self.hits > 0

    def convert_to_tweet(self):
        had_a_tater = f' {self.home_runs} {Emojis.TATER.value}' if self.home_runs > 0 else ''
        return f'{self.full_name} went {self.hits}-{self.at_bats}{had_a_tater}'


def baseball_player_from_dict(player: dict, college: dict):
    return BaseballPlayer(
        id=player.get('person').get('id'),
        full_name=player.get('person').get('fullName'),
        college=college.get('college'),
        hits=player.get('stats', {}).get('batting', {}).get('hits', 0),
        at_bats=player.get('stats', {}).get('batting', {}).get('atBats', 0),
        home_runs=player.get('stats', {}).get('batting', {}).get('homeRuns', 0)
    )