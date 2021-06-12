import json
from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

from src.gcp.gcs import Gcs


class TestEntrypoint:
    @dataclass
    class Fixture:
        mock_client_constructor: Mock
        mock_client: Mock
        mock_bucket: Mock
        mock_blob: Mock
        gcs: Gcs

    @pytest.fixture
    @patch('src.gcp.gcs.Client', autospec=True)
    def setup(self, mock_client_constructor):
        mock_client = mock_client_constructor.return_value
        mock_blob = Mock()
        mock_blob.download_as_string.return_value = json.dumps({"foo": "bar"})
        mock_bucket = Mock()
        mock_client.get_bucket.return_value = mock_bucket
        mock_bucket.get_blob.return_value = mock_blob
        mock_bucket.blob.return_value = mock_blob

        return TestEntrypoint.Fixture(
            mock_client_constructor=mock_client_constructor,
            mock_client=mock_client,
            mock_bucket=mock_bucket,
            mock_blob=mock_blob,
            gcs=Gcs()
        )

    def test_client_constructor(self, setup: Fixture):
        setup.mock_client_constructor.assert_called_once_with(project='sports-data-service')

    def test_get_bucket(self, setup: Fixture):
        setup.mock_client.get_bucket.assert_called_once_with('college-by-player')

    def test_get_blob(self, setup: Fixture):
        setup.gcs.read_as_dict(url='some/file.json')
        setup.mock_bucket.get_blob.assert_called_once_with('some/file.json')

    def test_read_as_dict(self, setup: Fixture):
        assert setup.gcs.read_as_dict(url='some/file.json') == {'foo': 'bar'}

    def test_write(self, setup: Fixture):
        the_contents = {'foo': 'bar'}
        setup.gcs.write(url='some/file.json', contents=the_contents)
        setup.mock_blob.upload_from_string.assert_called_once_with(json.dumps(the_contents))
