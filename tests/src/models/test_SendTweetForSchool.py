from dataclasses import dataclass
from datetime import datetime
from typing import List
from unittest.mock import Mock, patch, call

import pytest

from src.models.Player import Player
from src.models.SendTweetForSchool import SendTweetForSchool


@dataclass
class FakePlayer(Player):
    def __init__(self, is_great_day: bool):
        self.is_great_day = is_great_day

    def has_stats(self) -> bool:
        pass

    def had_a_great_day(self) -> bool:
        return self.is_great_day

    def convert_to_tweet(self) -> str:
        return 'some text'

    def get_college(self) -> str:
        pass

    def get_league_name(self) -> str:
        pass

    def get_player_id(self) -> str:
        pass

    def convert_dataclass_to_json(self) -> str:
        return 'some json'


class TestSendTweetForSchool:
    @dataclass
    class Params:
        had_great_day: bool
        school: str
        expected_publish_calls: List

    @dataclass
    class Fixture:
        mock_publish: Mock
        expected_publish_calls: List
        mock_save: Mock

    @pytest.fixture(
        ids=['has stats', 'had great day'],
        params=[
            Params(
                had_great_day=False,
                school='fsu',
                expected_publish_calls=[
                    call(message='🍢⚾️ #GoNoles ⚾️🍢\n#ProNoles\nsome text',
                         school='fsu',
                         topic='twitter-message-service-pubsub',
                         send_message=True),
                    call(message='{"date": "2021-01-01", "player_stats": [{}]}',
                         school='fsu',
                         topic='historical-significance-pubsub',
                         send_message=True)
                ]
            ),
            Params(
                had_great_day=True,
                school='wisconsin',
                expected_publish_calls=[
                    call(message='some json',
                         school='wisconsin',
                         topic='twitter-retweet-service-pubsub',
                         send_message=True),
                    call(message='⚾️ #Badgers ⚾️\nsome text',
                         school='wisconsin',
                         topic='twitter-message-service-pubsub',
                         send_message=True),
                    call(message='{"date": "2021-01-01", "player_stats": [{}]}',
                         school='wisconsin',
                         topic='historical-significance-pubsub',
                         send_message=True),
                ]
            ),
        ]
    )
    @patch.object(SendTweetForSchool, 'save')
    @patch('src.models.SendTweetForSchool.publish_message', autospec=True)
    def setup(self, mock_publish, mock_save, request):
        mock_player = FakePlayer(is_great_day=request.param.had_great_day)
        mock_date = datetime(2021, 1, 1)
        SendTweetForSchool(
            school=request.param.school, player_stats=[mock_player], send_message=True
        ).publish(sport='baseball', league_name='mlb', date=mock_date)

        return TestSendTweetForSchool.Fixture(
            mock_publish=mock_publish,
            expected_publish_calls=request.param.expected_publish_calls,
            mock_save=mock_save
        )

    def test_publish_message_called(self, setup: Fixture):
        assert setup.mock_publish.mock_calls == setup.expected_publish_calls

    def test_save(self, setup: Fixture):
        setup.mock_save.assert_called_once_with(date=datetime(2021, 1, 1))
