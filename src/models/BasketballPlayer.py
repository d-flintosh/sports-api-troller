from dataclasses import dataclass

from src.models.NbaTeams import nba_team_map
from src.models.Player import Player
from src.models.WnbaTeams import wnba_team_map
from src.universal import get_team_text


@dataclass
class BasketballPlayer(Player):
    id: str
    league_name: str
    team_id: str
    full_name: str
    college: str
    points: int
    assists: int
    rebounds: int
    steals: int
    blocks: int
    threes: int

    def has_stats(self):
        return self.points > 0 \
               or self.assists > 0 \
               or self.rebounds > 0 \
               or self.steals > 0 \
               or self.blocks > 0 \
               or self.threes >= 5 \
               and self.college is not None

    def had_a_great_day(self) -> bool:
        return self.points >= 20 \
               or self.assists >= 10 \
               or self.rebounds >= 10 \
               or self.threes >= 5 \
               and self.college is not None

    def convert_to_tweet(self):
        stat_line = []
        if self.points > 0:
            stat_line.append(f'{self.points} pts')
        if self.rebounds > 0:
            stat_line.append(f'{self.rebounds} reb')
        if self.assists > 0:
            stat_line.append(f'{self.assists} ast')
        if self.steals > 0:
            stat_line.append(f'{self.steals} stl')
        if self.blocks > 0:
            stat_line.append(f'{self.blocks} blk')
        if self.threes >= 5:
            stat_line.append(f'{self.threes} 3s')
        team_map_to_use = nba_team_map if self.league_name == 'nba' else wnba_team_map

        team_text = get_team_text(team_map=team_map_to_use, team_id=self.team_id)
        return f'{self.full_name}{team_text} {"/".join(stat_line)}'

    def get_college(self):
        return self.college

    def get_player_id(self) -> str:
        return self.id

    def get_league_name(self) -> str:
        return self.league_name


def basketball_player_from_dict(player: dict, league_name: str, team_id: str, college: dict):
    player_stats = player.get('statistics', {})
    return BasketballPlayer(
        id=player.get('id'),
        full_name=player.get('full_name'),
        league_name=league_name,
        team_id=team_id,
        college=college.get('college', '') if college else '',
        points=player_stats.get('points', 0) or 0,
        assists=player_stats.get('assists', 0) or 0,
        rebounds=player_stats.get('rebounds', 0) or 0,
        steals=player_stats.get('steals', 0) or 0,
        blocks=player_stats.get('blocks', 0) or 0,
        threes=player_stats.get('three_points_made', 0) or 0
    )
