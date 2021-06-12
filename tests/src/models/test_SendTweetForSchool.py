from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

from src.models.BaseballPlayer import BaseballPlayer
from src.models.SendTweetForSchool import SendTweetForSchool


class TestSendTweetForSchool:
    @dataclass
    class Fixture:
        mock_publish: Mock

    @pytest.fixture
    @patch('src.models.SendTweetForSchool.publish_message', autospec=True)
    def setup(self, mock_publish):
        baseball_player = BaseballPlayer(
            id=1,
            college='fsu',
            full_name='Bo',
            at_bats=1,
            hits=1,
            home_runs=0
        )
        SendTweetForSchool(school='fsu', player_stats=[baseball_player]).publish(send_message=True, sport='baseball')

        return TestSendTweetForSchool.Fixture(
            mock_publish=mock_publish
        )

    def test_publish_message_called(self, setup: Fixture):
        setup.mock_publish.assert_called_once_with(
            message='🍢⚾️ @FSUBaseball ⚾️🍢\nBo went 1-1',
            school='fsu',
            send_message=True
        )
