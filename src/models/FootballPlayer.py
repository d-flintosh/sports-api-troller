from dataclasses import dataclass

from src.models.NflTeams import nfl_team_map
from src.models.Player import Player
from src.universal import get_team_text


@dataclass
class FootballPlayer(Player):
    id: str
    full_name: str
    team_id: str
    college: str
    rushing_attempts: int
    rushing_yards: int
    rushing_td: int
    receiving_receptions: int
    receiving_yards: int
    receiving_td: int
    passing_attempts: int
    passing_completions: int
    passing_td: int
    passing_yards: int
    def_sacks: float
    def_tackles: int
    def_int: int
    def_ff: int
    def_fr: int
    def_pd: int
    fg_made: int
    fg_attempts: int
    league_name: str = 'nfl'

    def has_stats(self):
        return self.rushing_attempts > 0 or self.receiving_receptions > 0 or self.passing_attempts > 0 or self.def_tackles > 0 or self.def_int > 0 or self.fg_attempts > 0

    def had_a_great_day(self) -> bool:
        return (self.receiving_yards + self.receiving_yards) > 100 or self.receiving_yards > 100 or self.rushing_yards > 100 or self.passing_yards > 300 or (self.passing_td + self.rushing_td) > 4 or self.def_int > 1 or self.def_sacks > 1.5

    def convert_to_tweet(self):
        team_text = get_team_text(team_map=nfl_team_map, team_id=self.team_id)
        stat_line = []
        if self.rushing_attempts > 0:
            line = f'{self.rushing_attempts} CAR/{self.rushing_yards} YDS'
            line = line if self.rushing_td == 0 else f'{line}/{self.rushing_td} TD'
            stat_line.append(line)
        if self.receiving_receptions > 0:
            line = f'{self.receiving_receptions} REC/{self.receiving_yards} YDS'
            line = line if self.receiving_td == 0 else f'{line}/{self.receiving_td} TD'
            stat_line.append(line)
        if self.passing_attempts > 0:
            line = f'{self.passing_completions}-{self.passing_attempts} {self.passing_yards} YDS'
            line = line if self.passing_td == 0 else f'{line}/{self.passing_td} TD'
            stat_line.append(line)
        if self.def_tackles > 0 or self.def_int > 0:
            line = f'{self.def_tackles} TAK'
            line = line if self.def_sacks == 0 else f'{line}/{self.def_sacks} SCK'
            line = line if self.def_int == 0 else f'{line}/{self.def_int} INT'
            line = line if self.def_ff == 0 else f'{line}/{self.def_ff} FF'
            line = line if self.def_fr == 0 else f'{line}/{self.def_fr} FR'
            line = line if self.def_pd == 0 else f'{line}/{self.def_pd} PD'
            stat_line.append(line)
        if self.fg_attempts > 0:
            line = f'{self.fg_made}/{self.fg_attempts} FGs'
            stat_line.append(line)
        return f'{self.full_name}{team_text} {". ".join(stat_line)}'

    def get_college(self):
        return self.college


def football_player_from_dict(player: dict, college: dict):
    return FootballPlayer(
        id=player.get('player_id'),
        full_name=player.get("full_name"),
        team_id=player.get('team_id'),
        college=college.get('college') if college else None,
        rushing_attempts=player.get('rushing', {}).get('attempts', 0),
        rushing_yards=player.get('rushing', {}).get('yards', 0),
        rushing_td=player.get('rushing', {}).get('touchdowns', 0),
        receiving_receptions=player.get('receiving', {}).get('receptions', 0),
        receiving_yards=player.get('receiving', {}).get('yards', 0),
        receiving_td=player.get('receiving', {}).get('touchdowns', 0),
        passing_attempts=player.get('passing', {}).get('attempts', 0),
        passing_completions=player.get('passing', {}).get('completions', 0),
        passing_td=player.get('passing', {}).get('touchdowns', 0),
        passing_yards=player.get('passing', {}).get('yards', 0),
        def_sacks=player.get('defense', {}).get('sacks', 0),
        def_tackles=player.get('defense', {}).get('tackles', 0),
        def_int=player.get('defense', {}).get('interceptions', 0),
        def_ff=player.get('defense', {}).get('forced_fumbles', 0),
        def_fr=player.get('defense', {}).get('fumble_recoveries', 0),
        def_pd=player.get('defense', {}).get('passes_defended', 0),
        fg_made=player.get('field_goals', {}).get('made', 0),
        fg_attempts=player.get('field_goals', {}).get('attempts', 0)
    )
