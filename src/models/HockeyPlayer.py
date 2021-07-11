from dataclasses import dataclass

from src.models.NhlTeams import nhl_team_map
from src.models.Player import Player
from src.universal import get_team_text


@dataclass
class HockeyPlayer(Player):
    id: str
    league_name: str
    team_id: str
    full_name: str
    college: str
    goals: int
    assists: int

    def has_stats(self):
        return self.goals > 0 or self.assists > 0 and self.college is not None

    def had_a_great_day(self) -> bool:
        return self.has_stats()

    def convert_to_tweet(self):
        stat_line = []
        if self.goals > 0:
            stat_line.append(f'{self.goals} g')
        if self.assists > 0:
            stat_line.append(f'{self.assists} ast')

        team_text = get_team_text(team_map=nhl_team_map, team_id=self.team_id)
        return f'{self.full_name}{team_text} {"/".join(stat_line)}'

    def get_college(self):
        return self.college


def hockey_player_from_dict(player: dict, league_name: str, team_id: str, college: dict):
    player_stats = player.get('statistics', {}).get('total', {})
    return HockeyPlayer(
        id=player.get('id'),
        full_name=player.get('full_name'),
        league_name=league_name,
        team_id=team_id,
        college=college.get('college', '') if college else '',
        goals=player_stats.get('goals', 0) or 0,
        assists=player_stats.get('assists', 0) or 0
    )
