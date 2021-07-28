from dataclasses import dataclass

from src.models.MlbTeams import mlb_team_map
from src.models.Player import Player
from src.universal import get_team_text


@dataclass
class BaseballPlayer(Player):
    id: str
    full_name: str
    team_id: str
    college: str
    hits: int
    rbis: int
    runs: int
    stolen_bases: int
    at_bats: int
    home_runs: int
    pitching_strikeouts: int
    pitching_hits: int
    pitching_earned_runs: int
    pitching_losses: int
    pitching_wins: int
    pitching_saves: int
    pitching_innings: str
    league_name: str = 'mlb'

    def has_stats(self):
        return self.at_bats > 0 or self.pitching_innings != ''

    def had_a_great_day(self) -> bool:
        return self.home_runs > 0 or self.pitching_wins > 0

    def convert_to_tweet(self):
        team_text = get_team_text(team_map=mlb_team_map, team_id=self.team_id)
        player_text = f'{self.full_name}{team_text}'
        stat_line = []
        if self.pitching_innings == '':
            stat_line.append(f'went {self.hits}-{self.at_bats}')
            if self.home_runs:
                stat_line.append(f'{self.home_runs}HR')
            if self.rbis:
                stat_line.append(f'{self.rbis}RBI')
            if self.runs:
                stat_line.append(f'{self.runs}R')
            if self.stolen_bases:
                stat_line.append(f'{self.stolen_bases}SB')
        else:
            if self.pitching_wins:
                stat_line.append('W')
            if self.pitching_losses:
                stat_line.append('L')
            if self.pitching_saves:
                stat_line.append('SV')

            stat_line.append(f'{self.pitching_innings}IP')
            stat_line.append(f'{self.pitching_earned_runs}ER')
            stat_line.append(f'{self.pitching_hits}H')
            stat_line.append(f'{self.pitching_strikeouts}K')

        stat_line_text = ' '.join(stat_line)
        return f'{player_text} {stat_line_text}'

    def get_college(self):
        return self.college


def baseball_player_from_dict(player: dict, team_id: str, college: dict):
    batting_stats = player.get('statistics', {}).get('hitting', {}).get('overall', {})
    pitching_stats = player.get('statistics', {}).get('pitching', {}).get('overall', {})
    return BaseballPlayer(
        id=player.get('id'),
        full_name=f'{player.get("preferred_name")} {player.get("last_name")}',
        team_id=team_id,
        college=college.get('college'),
        hits=batting_stats.get('onbase', {}).get('h', 0),
        rbis=batting_stats.get('rbi', 0),
        runs=batting_stats.get('runs', {}).get('total', 0),
        stolen_bases=batting_stats.get('steal', {}).get('stolen', 0),
        at_bats=batting_stats.get('ab', 0),
        home_runs=batting_stats.get('onbase', {}).get('hr', 0),
        pitching_strikeouts=pitching_stats.get('outs', {}).get('ktotal', 0),
        pitching_hits=pitching_stats.get('onbase', {}).get('h', 0),
        pitching_earned_runs=pitching_stats.get('runs', {}).get('earned', 0),
        pitching_losses=pitching_stats.get('games', {}).get('loss', 0),
        pitching_saves=pitching_stats.get('games', {}).get('save', 0),
        pitching_wins=pitching_stats.get('games', {}).get('win', 0),
        pitching_innings=str(pitching_stats.get('ip_2', ''))
    )
