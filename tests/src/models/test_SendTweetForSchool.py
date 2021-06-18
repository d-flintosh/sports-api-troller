from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

from src.models.SendTweetForSchool import SendTweetForSchool


class TestSendTweetForSchool:
    @dataclass
    class Fixture:
        mock_publish: Mock

    @pytest.fixture
    @patch('src.models.SendTweetForSchool.Player', autospec=True)
    @patch('src.models.SendTweetForSchool.publish_message', autospec=True)
    def setup(self, mock_publish, mock_player):
        mock_player.convert_to_tweet.return_value = 'some text'
        SendTweetForSchool(school='fsu', player_stats=[mock_player]).publish(
            send_message=True, sport='baseball', league_name='mlb'
        )

        return TestSendTweetForSchool.Fixture(
            mock_publish=mock_publish
        )

    def test_publish_message_called(self, setup: Fixture):
        setup.mock_publish.assert_called_once_with(
            message='🍢⚾️ @FSUBaseball ⚾️🍢\nsome text',
            school='fsu',
            send_message=True
        )
