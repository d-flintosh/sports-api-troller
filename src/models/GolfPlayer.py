from dataclasses import dataclass
from typing import List

from src.models.Player import Player


@dataclass
class GolfRound:
    score: int
    sequence: int


@dataclass
class GolfPlayer(Player):
    id: str
    league_name: str
    full_name: str
    college: str
    tied: bool
    position: int
    score: int
    rounds: List[GolfRound]
    status: str

    def has_stats(self):
        return self.status == 'PROBABLY_NOT_CUT'

    def had_a_great_day(self) -> bool:
        return self. position <= 5

    def convert_to_tweet(self):
        position_text = f'({"T" if self.tied else ""}{self.position})'
        score_text = 'E' if self.score == 0 else str(self.score)
        return f'{self.full_name} {score_text} {position_text}'

    def get_college(self):
        return self.college

    def get_player_id(self) -> str:
        return self.id

    def get_league_name(self) -> str:
        return self.league_name


def golf_player_from_dict(player: dict, league_name: str, college: dict):
    rounds = player.get('rounds', [])
    rounds = list(map(
        lambda x: GolfRound(
            score=x.get('score'),
            sequence=x.get('sequence')
        ),
        rounds
    ))

    return GolfPlayer(
        id=player.get('id'),
        full_name=f'{player.get("first_name")} {player.get("last_name")}',
        league_name=league_name,
        college=college.get('college', '') if college else '',
        score=player.get('score'),
        tied=player.get('tied', False),
        position=player.get('position'),
        rounds=rounds,
        status=player.get('status', 'PROBABLY_NOT_CUT')
    )
