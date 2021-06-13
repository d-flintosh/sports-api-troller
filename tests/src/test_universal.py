from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

from src.universal import publish_message, get_team_text


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