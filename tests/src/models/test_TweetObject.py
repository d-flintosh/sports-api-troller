from dataclasses import dataclass
from typing import Optional
from unittest.mock import Mock

import pytest

from src.models.Player import Player
from src.models.TweetObject import TweetObject


class TestTweetObject:
    @dataclass
    class Params:
        college: Optional[str]
        expected_tweet_path: Optional[str]

    @dataclass
    class Fixture:
        expected_tweet_path: Optional[str]
        actual: TweetObject

    @pytest.fixture(
        ids=['Found College', 'None College', 'Not Found College'],
        params=[
            Params(
                college='FsU',
                expected_tweet_path='fsu'
            ),
            Params(
                college=None,
                expected_tweet_path=None
            ),
            Params(
                college='Upstate Chucklefucker',
                expected_tweet_path=None
            )
        ])
    def setup(self, request):
        mock_player = Mock(spec=Player)
        mock_player.get_college.return_value = request.param.college

        return TestTweetObject.Fixture(
            actual=TweetObject(player_object=mock_player),
            expected_tweet_path=request.param.expected_tweet_path
        )

    def test_tweet_path_correct(self, setup: Fixture):
        assert setup.actual.tweet_path == setup.expected_tweet_path