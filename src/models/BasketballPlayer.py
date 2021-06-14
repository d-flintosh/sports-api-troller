from dataclasses import dataclass

from nba_api.stats.library.parameters import LeagueID

from src.models.NbaTeams import nba_team_map
from src.models.Player import Player
from src.models.WnbaTeams import wnba_team_map
from src.universal import get_team_text


@dataclass
class BasketballPlayer(Player):
    id: int
    league_id: LeagueID
    team_id: int
    full_name: str
    college: str
    points: int
    assists: int
    rebounds: int

    def has_stats(self):
        return self.points > 0 or self.assists > 0 or self.rebounds > 0 and self.college is not None

    def convert_to_tweet(self):
        stat_line = []
        if self.points > 0:
            stat_line.append(f'{self.points} pts')
        if self.rebounds > 0:
            stat_line.append(f'{self.rebounds} reb')
        if self.assists > 0:
            stat_line.append(f'{self.assists} ast')
        team_map_to_use = nba_team_map if self.league_id == LeagueID.nba else wnba_team_map

        team_text = get_team_text(team_map=team_map_to_use, team_id=self.team_id)
        return f'{self.full_name}{team_text} {"/".join(stat_line)}'

    def get_college(self):
        return self.college


def basketball_player_from_dict(player: dict, league_id: LeagueID, college: dict):
    return BasketballPlayer(
        id=player.get('PLAYER_ID'),
        full_name=player.get('PLAYER_NAME'),
        league_id=league_id,
        team_id=player.get('TEAM_ID'),
        college=college.get('college', '') if college else '',
        points=player.get('PTS', 0) or 0,
        assists=player.get('AST', 0) or 0,
        rebounds=player.get('REB', 0) or 0
    )
