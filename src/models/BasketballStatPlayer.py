from dataclasses import dataclass
from typing import Optional

from src.models.Player import Player


@dataclass
class BasketballStatPlayer(Player):
    college: str
    stat_name: str
    current_player_name: str
    current_player_stat_value: int
    previous_player_name: Optional[str]
    previous_player_stat_value: Optional[int]
    previous_player_date: Optional[str]

    def has_stats(self) -> bool:
        return True

    def had_a_great_day(self) -> bool:
        return False

    def convert_to_tweet(self) -> str:
        if self.previous_player_name is None:
            return f'{self.current_player_name}\'s {self.current_player_stat_value} {self.stat_name} this season is the most ever by a former player.'
        elif self.current_player_name == self.previous_player_name:
            name_text = 'he had'
        else:
            name_text = f'{self.previous_player_name}\'s'
        return f'{self.current_player_name}\'s {self.current_player_stat_value} {self.stat_name} this season are the most in a game by a former player since {name_text} {self.previous_player_stat_value} on {self.previous_player_date}.'

    def get_college(self) -> str:
        return self.college
