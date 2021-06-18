from dataclasses import dataclass
from datetime import date
from unittest.mock import Mock, patch, call

import pytest

from main import entrypoint


class TestEntrypoint:
    @dataclass
    class Fixture:
        mock_basketball: Mock
        mock_baseball: Mock
        mock_api: Mock
        mock_nba: Mock
        mock_wnba: Mock
        mock_tweet_driver: Mock

    @pytest.fixture
    @patch('main.tweet_driver', autospec=True)
    @patch('main.BaseballLeague', autospec=True)
    @patch('main.BasketballLeague', autospec=True)
    @patch('main.WnbaSportRadar', autospec=True)
    @patch('main.NbaSportRadar', autospec=True)
    @patch('main.SportRadarApi', autospec=True)
    @patch('main.date', autospec=True)
    def setup(self, mock_date, mock_api, mock_nba, mock_wnba, mock_basketball, mock_baseball, mock_tweet_driver):
        mock_date.today.return_value = date(2020, 1, 2)

        entrypoint(event=Mock(), context=Mock())

        return TestEntrypoint.Fixture(
            mock_basketball=mock_basketball,
            mock_baseball=mock_baseball,
            mock_api=mock_api,
            mock_nba=mock_nba,
            mock_wnba=mock_wnba,
            mock_tweet_driver=mock_tweet_driver
        )

    def test_get_mlb_called(self, setup: Fixture):
        setup.mock_baseball.assert_called_once()

    def test_sport_radar_api(self, setup: Fixture):
        setup.mock_api.assert_called_once()

    def test_nba_client(self, setup: Fixture):
        setup.mock_nba.assert_called_once_with(api_client=setup.mock_api.return_value)

    def test_wnba_client(self, setup: Fixture):
        setup.mock_wnba.assert_called_once_with(api_client=setup.mock_api.return_value)

    def test_get_basketball_called(self, setup: Fixture):
        setup.mock_basketball.assert_has_calls([
            call(league_name='nba', league_client=setup.mock_nba.return_value),
            call(league_name='wnba', league_client=setup.mock_wnba.return_value)
        ])
