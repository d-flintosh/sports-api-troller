from dataclasses import dataclass
from typing import List
from unittest.mock import Mock, patch, call
from datetime import date
import pytest

from src.universal import publish_message, get_team_text, update_tweet_checkpoint


class TestPublishMessage:
    @dataclass
    class Fixture:
        mock_publisher: Mock
        mock_future: Mock

    @pytest.fixture
    @patch('src.universal.pubsub_v1')
    def setup(self, mock_pub_sub):
        mock_publisher = mock_pub_sub.PublisherClient.return_value
        mock_future = Mock()
        mock_publisher.publish.return_value = mock_future

        publish_message(message='shoot and score', school='fsu', send_message=True)
        return TestPublishMessage.Fixture(
            mock_publisher=mock_publisher,
            mock_future=mock_future
        )

    def test_publish_called(self, setup: Fixture):
        setup.mock_publisher.publish.assert_called_once_with(
            'projects/sports-data-service/topics/twitter-message-service-pubsub',
            str.encode('shoot and score'),
            school='fsu'
        )

    def test_future_result_called(self, setup: Fixture):
        setup.mock_future.result.assert_called_once()


class TestGetTeamText:
    @dataclass
    class Params:
        team_map: dict
        team_id: int
        expected: str

    @dataclass
    class Fixture:
        actual: str
        expected: str

    @pytest.fixture(
        ids=['Normal Path', 'ID not found', 'TwitterCode not found', 'Twitter Code is None'],
        params=[
            Params(
                team_id=1,
                team_map={'1': {'twitterCode': '#FOO'}},
                expected=' (#FOO)'
            ),
            Params(
                team_id=2,
                team_map={'1': {'twitterCode': '#FOO'}},
                expected=''
            ),
            Params(
                team_id=1,
                team_map={'1': {}},
                expected=''
            ),
            Params(
                team_id=1,
                team_map={'1': {'twitterCode': None}},
                expected=''
            )
        ])
    def setup(self, request):
        return TestGetTeamText.Fixture(
            actual=get_team_text(team_map=request.param.team_map, team_id=request.param.team_id),
            expected=request.param.expected
        )

    def test_output_correct(self, setup: Fixture):
        assert setup.actual == setup.expected


class TestUpdateTweetCheckpoint:
    @dataclass
    class Params:
        send_message: bool
        expected_write_calls: List
        games_published: List

    @dataclass
    class Fixture:
        mock_gcs: Mock
        expected_write_calls: List

    @pytest.fixture(
        ids=['False Send Message', 'No games to publish', 'Has games'],
        params=[
            Params(
                send_message=False,
                expected_write_calls=[],
                games_published=[]
            ),
            Params(
                send_message=True,
                expected_write_calls=[],
                games_published=[]
            ),
            Params(
                send_message=True,
                expected_write_calls=[call(url='foo/2021-01-05.json', contents={'games_published': [123]})],
                games_published=[123]
            )
        ])
    @patch('src.universal.Gcs', autospec=True)
    def setup(self, mock_gcs, request):
        date_to_use = date(2021, 1, 5)
        update_tweet_checkpoint(
            league_name='foo',
            send_message=request.param.send_message,
            date=date_to_use,
            games_published=request.param.games_published
        )
        return TestUpdateTweetCheckpoint.Fixture(
            expected_write_calls=request.param.expected_write_calls,
            mock_gcs=mock_gcs
        )

    def test_calls_write(self, setup: Fixture):
        print(setup.mock_gcs.return_value.write)
        setup.mock_gcs.return_value.write.assert_has_calls(setup.expected_write_calls)
