from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

from src.universal import publish_message


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
