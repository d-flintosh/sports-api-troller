from dataclasses import dataclass
from typing import List

from src.models.BaseballPlayer import BaseballPlayer
from src.models.Schools import Schools
from src.universal import publish_message


@dataclass
class SendTweetForSchool:
    school: str
    player_stats: List[BaseballPlayer]

    def __init__(self, school: str, player_stats: [BaseballPlayer]):
        self.school = school
        self.player_stats = player_stats

    def publish(self, send_message: bool, sport: str):
        message_header = Schools[self.school].value.get(sport).get('header')
        tweet_message = '. '.join(list(map(lambda x: x.convert_to_tweet(), self.player_stats)))
        publish_message(message=message_header + tweet_message, school=self.school, send_message=send_message)
