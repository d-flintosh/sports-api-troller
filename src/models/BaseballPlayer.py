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
    pitching_strikeouts: int
    pitching_hits: int
    pitching_earned_runs: int
    pitching_losses: int
    pitching_wins: int
    pitching_note: str
    pitching_innings: str

    def has_stats(self):
        return self.at_bats > 0 or self.pitching_innings != ''

    def convert_to_tweet(self):
        team_text = get_team_text(team_map=mlb_team_map, team_id=self.team_id)
        player_text = f'{self.full_name}{team_text}'
        if self.pitching_innings == '':
            had_a_tater = f' {self.home_runs} {Emojis.TATER.value}' if self.home_runs > 0 else ''
            return f'{player_text} went {self.hits}-{self.at_bats}{had_a_tater}'
        else:
            note = ''
            if self.pitching_note != '':
                note = f' {self.pitching_note}'
            return f'{player_text} {self.pitching_innings}IP {self.pitching_earned_runs}ER {self.pitching_hits}H {self.pitching_strikeouts}K{note}'

    def get_college(self):
        return self.college


def baseball_player_from_dict(player: dict, team_id: int, college: dict):
    batting_stats = player.get('stats', {}).get('batting', {})
    pitching_stats = player.get('stats', {}).get('pitching', {})
    return BaseballPlayer(
        id=player.get('person').get('id'),
        full_name=player.get('person').get('fullName'),
        team_id=team_id,
        college=college.get('college'),
        hits=batting_stats.get('hits', 0),
        at_bats=batting_stats.get('atBats', 0),
        home_runs=batting_stats.get('homeRuns', 0),
        pitching_strikeouts=pitching_stats.get('strikeouts', 0),
        pitching_hits=pitching_stats.get('hits', 0),
        pitching_earned_runs=pitching_stats.get('earnedRuns', 0),
        pitching_losses=pitching_stats.get('losses', 0),
        pitching_wins=pitching_stats.get('wins', 0),
        pitching_note=pitching_stats.get('note', ''),
        pitching_innings=pitching_stats.get('inningsPitched', '')
    )
