from abc import ABC, abstractmethod
from typing import List, Optional, Union


class League(ABC):
    def __init__(self, league_name, sport):
        self.league_name = league_name
        self.sport = sport

    @abstractmethod
    def get_game_id(self, game: dict) -> Union[str, int]:
        raise NotImplementedError

    @abstractmethod
    def get_games(self, date) -> Optional[List]:
        raise NotImplementedError

    @abstractmethod
    def get_tweetable_objects(self, game: dict) -> Optional[List]:
        raise NotImplementedError
