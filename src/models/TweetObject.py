from dataclasses import dataclass

from src.models.Player import Player
from src.models.Schools import COLLEGES_TO_RUN


@dataclass
class TweetObject:
    player_object: Player
    tweet_path: str

    def __init__(self, player_object: Player):
        self.player_object = player_object
        self.tweet_path = COLLEGES_TO_RUN.get(self.player_object.get_college().lower())
