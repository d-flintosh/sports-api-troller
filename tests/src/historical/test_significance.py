import json
from dataclasses import dataclass
from unittest.mock import patch, Mock, call

import pytest

from src.historical.significance import check_for_historical_significance


class TestCheckForHistoricalSignificance:
    @dataclass
    class Params:
        league_name: str

    @dataclass
    class Fixture:
        mock_gcs: Mock
        mock_stat_diff: Mock
        mock_publish: Mock

    @pytest.fixture(
        ids=['nba'],
        params=[
            Params(
                league_name='nba'
            )
        ]
    )
    @patch('src.historical.significance.publish_message', autospec=True)
    @patch('src.historical.significance.Gcs', autospec=True)
    @patch('src.historical.significance.derive_positive_differences_in_stats', autospec=True)
    def setup(self, mock_stat_diff, mock_gcs, mock_publish, request):
        mock_school = 'fsu'
        mock_data = json.dumps({
            'player_stats': [
                {
                    'league_name': request.param.league_name,
                    'full_name': 'Scottie Barnes',
                    'points': 1,
                    'assists': 2,
                    'rebounds': 30,
                    'blocks': 4,
                    'steals': 5,
                    'threes': 6
                }
            ]
        })
        mock_stat_diff.return_value = ['some stuff']
        check_for_historical_significance(data=mock_data, school=mock_school, send_message=False)

        return TestCheckForHistoricalSignificance.Fixture(
                mock_gcs=mock_gcs,
                mock_stat_diff=mock_stat_diff,
                mock_publish=mock_publish
            )

    def test_gcs_constructor(self, setup: Fixture):
        setup.mock_gcs.assert_called_once_with(bucket='college-by-player-stats')

    def test_gcs_read(self, setup: Fixture):
        setup.mock_gcs.return_value.read_as_dict.assert_called_once_with(url='nba/fsu/all_players/players.json')

    def test_derive_differences(self, setup: Fixture):
        setup.mock_stat_diff.assert_has_calls([
            call(updated=setup.mock_gcs.return_value.read_as_dict.return_value, original=setup.mock_gcs.return_value.read_as_dict.return_value, stat_key='PTS', stat_text='points'),
            call(updated=setup.mock_gcs.return_value.read_as_dict.return_value, original=setup.mock_gcs.return_value.read_as_dict.return_value, stat_key='REB', stat_text='rebounds'),
            call(updated=setup.mock_gcs.return_value.read_as_dict.return_value, original=setup.mock_gcs.return_value.read_as_dict.return_value, stat_key='AST', stat_text='assists'),
            call(updated=setup.mock_gcs.return_value.read_as_dict.return_value, original=setup.mock_gcs.return_value.read_as_dict.return_value, stat_key='BLK', stat_text='blocks'),
            call(updated=setup.mock_gcs.return_value.read_as_dict.return_value, original=setup.mock_gcs.return_value.read_as_dict.return_value, stat_key='STL', stat_text='steals'),
            call(updated=setup.mock_gcs.return_value.read_as_dict.return_value, original=setup.mock_gcs.return_value.read_as_dict.return_value, stat_key='FG3M', stat_text='threes')
        ], any_order=True)

    def test_publish_message(self, setup: Fixture):
        setup.mock_publish.assert_has_calls([
            call(message='some stuff', school='fsu', topic='twitter-message-service-pubsub', send_message=False),
            call(message='some stuff', school='fsu', topic='twitter-message-service-pubsub', send_message=False),
            call(message='some stuff', school='fsu', topic='twitter-message-service-pubsub', send_message=False),
            call(message='some stuff', school='fsu', topic='twitter-message-service-pubsub', send_message=False),
            call(message='some stuff', school='fsu', topic='twitter-message-service-pubsub', send_message=False),
            call(message='some stuff', school='fsu', topic='twitter-message-service-pubsub', send_message=False)
        ])