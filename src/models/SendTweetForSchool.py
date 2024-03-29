import dataclasses
import json
from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.gcp.gcs import Gcs
from src.models.Player import Player
from src.models.Schools import Schools
from src.universal import publish_message


@dataclass
class SendTweetForSchool:
    school: str
    player_stats: List[Player]

    def __init__(self, school: str, player_stats: [Player], send_message: bool):
        self.school = school
        self.player_stats = player_stats
        self.send_message = send_message

    def publish(self, sport: str, league_name: str, date: datetime):
        school_header = Schools[self.school].value.get(sport).get(league_name)
        message_header = school_header.get('header')
        message_header = message_header + school_header.get('hashtag_header') if school_header.get('hashtag_header', None) else message_header
        tweet_message = '\n'.join(list(map(self.map_player_to_tweet, self.player_stats)))
        publish_message(
            message=message_header + tweet_message,
            school=self.school,
            topic='twitter-message-service-pubsub',
            send_message=self.send_message
        )
        self.save(date=date)
        historical_message = {
            'date': date.strftime('%Y-%m-%d'),
            'player_stats': list(map(lambda x: dataclasses.asdict(x), self.player_stats))
        }
        publish_message(
            message=json.dumps(historical_message),
            school=self.school,
            topic='historical-significance-pubsub',
            send_message=self.send_message
        )

    def save(self, date: datetime):
        gcs = Gcs(bucket='college-by-player-stats')
        for player in self.player_stats:
            player.save(gcs=gcs, date=date, college=self.school)

    def map_player_to_tweet(self, player: Player):
        if player.had_a_great_day():
            publish_message(
                message=player.convert_dataclass_to_json(),
                school=self.school,
                topic='twitter-retweet-service-pubsub',
                send_message=self.send_message
            )
        return player.convert_to_tweet()
