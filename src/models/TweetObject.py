from dataclasses import dataclass

from src.models.Player import Player
from src.models.Schools import COLLEGES_TO_RUN


@dataclass
class TweetObject:
    player_object: Player
    tweet_path: str

    def __init__(self, player_object: Player):
        print(player_object)
        self.player_object = player_object
        college = self.player_object.get_college()
        tweet_path = college.lower() if college else ''
        self.tweet_path = COLLEGES_TO_RUN.get(tweet_path)
