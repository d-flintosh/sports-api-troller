from dataclasses import dataclass
from typing import List
from unittest.mock import Mock, patch, call

import pytest

from src.models.SendTweetForSchool import SendTweetForSchool


class TestSendTweetForSchool:
    @dataclass
    class Params:
        had_great_day: bool
        expected_publish_calls: List

    @dataclass
    class Fixture:
        mock_publish: Mock
        expected_publish_calls: List

    @pytest.fixture(
        ids=['has stats', 'had great day'],
        params=[
            Params(
                had_great_day=False,
                expected_publish_calls=[
                    call(message='🍢⚾️ FSU ⚾️🍢\nsome text',
                         school='fsu',
                         topic='twitter-message-service-pubsub',
                         send_message=True)
                ]
            ),
            Params(
                had_great_day=True,
                expected_publish_calls=[
                    call(message='some json',
                         school='fsu',
                         topic='twitter-retweet-service-pubsub',
                         send_message=True),
                    call(message='🍢⚾️ FSU ⚾️🍢\nsome text',
                         school='fsu',
                         topic='twitter-message-service-pubsub',
                         send_message=True),
                ]
            ),
        ]
    )
    @patch('src.models.SendTweetForSchool.Player', autospec=True)
    @patch('src.models.SendTweetForSchool.publish_message', autospec=True)
    def setup(self, mock_publish, mock_player, request):
        mock_player.convert_to_tweet.return_value = 'some text'
        mock_player.convert_dataclass_to_json.return_value = 'some json'
        mock_player.had_a_great_day.return_value = request.param.had_great_day

        SendTweetForSchool(
            school='fsu', player_stats=[mock_player], send_message=True
        ).publish(sport='baseball', league_name='mlb')

        return TestSendTweetForSchool.Fixture(
            mock_publish=mock_publish,
            expected_publish_calls=request.param.expected_publish_calls
        )

    def test_publish_message_called(self, setup: Fixture):
        assert setup.mock_publish.mock_calls == setup.expected_publish_calls
