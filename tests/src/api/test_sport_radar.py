import json
from dataclasses import dataclass
from unittest.mock import patch, Mock

import pytest
from google.cloud.secretmanager_v1 import AccessSecretVersionResponse, SecretPayload, AccessSecretVersionRequest
from requests import Response

from src.api.sport_radar import SportRadarApi

SIMPLE_RETURN = {
    'fooEndpoint': 'barResponse'
}


def mock_requests_get(*args, **kwargs):
    response_content = json.dumps(SIMPLE_RETURN)

    response = Response()
    response.status_code = 200
    response._content = str.encode(response_content)

    return response


class TestSportRadarApi:
    @dataclass
    class Fixture:
        mock_client: Mock
        mock_request: Mock
        mock_sleep: Mock
        actual: dict

    @pytest.fixture
    @patch('time.sleep', return_value=None)
    @patch('src.api.sport_radar.requests.get', side_effect=mock_requests_get)
    @patch('src.api.sport_radar.secretmanager_v1')
    def setup(self, mock_secret_manager, mock_request, mock_sleep):
        expected = {
            'foo': 'bar'
        }
        mock_client = mock_secret_manager.SecretManagerServiceClient.return_value
        mock_response = Mock(spec=AccessSecretVersionResponse)

        mock_payload = Mock(spec=SecretPayload)

        mock_payload.data = str.encode(json.dumps(expected))
        mock_response.payload = mock_payload
        mock_client.access_secret_version.return_value = mock_response

        return TestSportRadarApi.Fixture(
            mock_client=mock_client,
            mock_request=mock_request,
            mock_sleep=mock_sleep,
            actual=SportRadarApi().make_request(url='http://api.sportradar.us/foo/otherStuff/thing.json')
        )

    def test_access_secret_version_called(self, setup: Fixture):
        request = AccessSecretVersionRequest({
            'name': 'projects/557888643787/secrets/sport-radar/versions/latest'
        })
        setup.mock_client.access_secret_version.assert_called_once_with(
            request=request
        )

    def test_sleep_called(self, setup: Fixture):
        setup.mock_sleep.assert_called_once_with(1)

    def test_get_called(self, setup: Fixture):
        setup.mock_request.assert_called_once_with('http://api.sportradar.us/foo/otherStuff/thing.json?api_key=bar')
