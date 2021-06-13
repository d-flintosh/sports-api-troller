from dataclasses import dataclass

from src.models.Player import Player


@dataclass
class BasketballPlayer(Player):
    id: int
    full_name: str
    college: str
    points: int
    assists: int
    rebounds: int

    def is_decent_day(self):
        return self.points > 0 or self.assists > 0 or self.rebounds > 0 and self.college is not None

    def convert_to_tweet(self):
        stat_line = []
        if self.points > 0:
            stat_line.append(f'{self.points} pts')
        if self.rebounds > 0:
            stat_line.append(f'{self.rebounds} reb')
        if self.assists > 0:
            stat_line.append(f'{self.assists} ast')

        return f'{self.full_name} {"/".join(stat_line)}'

    def get_college(self):
        return self.college


def basketball_player_from_dict(player: dict, college: dict):
    return BasketballPlayer(
        id=player.get('PLAYER_ID'),
        full_name=player.get('PLAYER_NAME'),
        college=college.get('college', '') if college else '',
        points=player.get('PTS', 0) or 0,
        assists=player.get('AST', 0) or 0,
        rebounds=player.get('REB', 0) or 0
    )
