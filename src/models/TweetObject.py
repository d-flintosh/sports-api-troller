from dataclasses import dataclass

from src.models.BaseballPlayer import BaseballPlayer
from src.models.Schools import COLLEGES_TO_RUN


@dataclass
class TweetObject:
    player_object: BaseballPlayer
    tweet_path: str

    def __init__(self, player_object: BaseballPlayer):
        self.player_object = player_object
        self.tweet_path = COLLEGES_TO_RUN.get(self.player_object.college.lower())
