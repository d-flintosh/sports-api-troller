from dataclasses import dataclass
from datetime import date
from typing import List
from unittest.mock import patch, Mock, call

import pytest

from src.extraction.League import League
from src.models.Player import Player
from src.models.TweetObject import TweetObject
from src.tweet_driver import tweet_driver


class TestTweetDriver:
    @dataclass
    class Params:
        mock_games: List
        mock_tweetable_objects: List
        expected_get_tweetable_objects_calls: List
        expected_tweet_calls: List
        expected_checkpoint_calls: List
        skip_filter: bool

    @dataclass
    class Fixture:
        mock_tweet: Mock
        mock_checkpoint: Mock
        mock_league: Mock
        expected_get_tweetable_objects_calls: List
        expected_tweet_calls: List
        expected_checkpoint_calls: List
        mock_published_games: Mock

    @pytest.fixture(
        ids=['No games', 'With Games No Tweets', 'With Games And Tweets Skip Filter', 'With Games And Tweets No Skip Filter'],
        params=[
            Params(
                mock_games=[],
                mock_tweetable_objects=[],
                expected_get_tweetable_objects_calls=[],
                expected_tweet_calls=[],
                expected_checkpoint_calls=[],
                skip_filter=False
            ),
            Params(
                mock_games=[{'id': 1}],
                mock_tweetable_objects=[],
                expected_get_tweetable_objects_calls=[],
                expected_tweet_calls=[],
                expected_checkpoint_calls=[],
                skip_filter=False
            ),
            Params(
                mock_games=[{'id': 1}],
                mock_tweetable_objects=[Mock(spec=TweetObject)],
                expected_get_tweetable_objects_calls=[
                    call(game={'id': 1})
                ],
                expected_tweet_calls=[
                    call(sport='some sport', league_name='some league')
                ],
                expected_checkpoint_calls=[
                    call(league_name='some league', send_message=True, date=date(2021, 1, 1), games_published=[1, 1])
                ],
                skip_filter=True
            ),
            Params(
                mock_games=[{'id': 1}],
                mock_tweetable_objects=[Mock(spec=TweetObject)],
                expected_get_tweetable_objects_calls=[],
                expected_tweet_calls=[],
                expected_checkpoint_calls=[],
                skip_filter=False
            )
        ]
    )
    @patch('src.tweet_driver.get_previously_published_games', autospec=True)
    @patch('src.tweet_driver.update_tweet_checkpoint', autospec=True)
    @patch('src.tweet_driver.SendTweetForSchool', autospec=True)
    def setup(self, mock_tweet, mock_checkpoint, mock_published_games, request):
        mock_league = Mock(spec=League)
        mock_league.sport = 'some sport'
        mock_league.league_name = 'some league'
        mock_league.get_game_id.return_value = 1
        mock_league.get_games.return_value = request.param.mock_games
        for tweetable in  request.param.mock_tweetable_objects:
            tweetable.tweet_path = 'foo'
            tweetable.player_object = Mock(spec=Player)

        mock_league.get_tweetable_objects.return_value = request.param.mock_tweetable_objects
        mock_published_games.return_value = [1]

        tweet_driver(
            leagues=[mock_league],
            date_to_run=date(2021, 1, 1),
            send_message=True,
            skip_filter=request.param.skip_filter
        )

        return TestTweetDriver.Fixture(
            mock_tweet=mock_tweet,
            mock_checkpoint=mock_checkpoint,
            mock_league=mock_league,
            expected_get_tweetable_objects_calls=request.param.expected_get_tweetable_objects_calls,
            expected_tweet_calls=request.param.expected_tweet_calls,
            expected_checkpoint_calls=request.param.expected_checkpoint_calls,
            mock_published_games=mock_published_games
        )

    def test_get_games_called(self, setup: Fixture):
        setup.mock_league.get_games.assert_called_once_with(date=date(2021, 1, 1))

    def test_get_previously_published_games_called(self, setup: Fixture):
        setup.mock_published_games.assert_called_once_with(date=date(2021, 1, 1), league_name='some league')

    def test_get_tweetable_objects_called(self, setup: Fixture):
        assert setup.mock_league.get_tweetable_objects.mock_calls == setup.expected_get_tweetable_objects_calls

    def test_send_tweet_for_school_called(self, setup: Fixture):
        assert setup.mock_tweet.return_value.publish.mock_calls == setup.expected_tweet_calls

    def test_update_tweet_checkpoint_called(self, setup: Fixture):
        assert setup.mock_checkpoint.mock_calls == setup.expected_checkpoint_calls
