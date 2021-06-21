from dataclasses import dataclass
from datetime import date, timedelta
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
        mock_hockey: Mock
        mock_nhl: Mock
        mock_golf: Mock
        mock_pga: Mock
        mock_lpga: Mock

    @pytest.fixture
    @patch('main.tweet_driver', autospec=True)
    @patch('main.GolfLeague', autospec=True)
    @patch('main.HockeyLeague', autospec=True)
    @patch('main.BaseballLeague', autospec=True)
    @patch('main.BasketballLeague', autospec=True)
    @patch('main.LpgaSportRadar', autospec=True)
    @patch('main.PgaSportRadar', autospec=True)
    @patch('main.NhlSportRadar', autospec=True)
    @patch('main.WnbaSportRadar', autospec=True)
    @patch('main.NbaSportRadar', autospec=True)
    @patch('main.SportRadarApi', autospec=True)
    @patch('main.date', autospec=True)
    def setup_time_delta_1(self, mock_date, mock_api, mock_nba, mock_wnba, mock_nhl, mock_pga, mock_lpga,
              mock_basketball, mock_baseball,
              mock_hockey, mock_golf, mock_tweet_driver):
        mock_date.today.return_value = date(2020, 1, 2)
        mock_event = {
            'attributes': {
                'time_delta': '1'
            }
        }
        entrypoint(event=mock_event, context=Mock())

        return TestEntrypoint.Fixture(
            mock_basketball=mock_basketball,
            mock_hockey=mock_hockey,
            mock_baseball=mock_baseball,
            mock_golf=mock_golf,
            mock_api=mock_api,
            mock_nba=mock_nba,
            mock_wnba=mock_wnba,
            mock_nhl=mock_nhl,
            mock_pga=mock_pga,
            mock_lpga=mock_lpga,
            mock_tweet_driver=mock_tweet_driver
        )

    def test_get_mlb_called_1(self, setup_time_delta_1: Fixture):
        setup_time_delta_1.mock_baseball.assert_not_called()

    def test_sport_radar_api_1(self, setup_time_delta_1: Fixture):
        setup_time_delta_1.mock_api.assert_called_once()

    def test_nba_client_1(self, setup_time_delta_1: Fixture):
        setup_time_delta_1.mock_nba.assert_not_called()

    def test_wnba_client_1(self, setup_time_delta_1: Fixture):
        setup_time_delta_1.mock_wnba.assert_not_called()

    def test_nhl_client_1(self, setup_time_delta_1: Fixture):
        setup_time_delta_1.mock_nhl.assert_not_called()

    def test_basketball_called_1(self, setup_time_delta_1: Fixture):
        setup_time_delta_1.mock_basketball.assert_not_called()

    def test_golf_called_1(self, setup_time_delta_1: Fixture):
        setup_time_delta_1.mock_golf.assert_has_calls([
            call(league_name='pga', league_client=setup_time_delta_1.mock_pga.return_value),
            call(league_name='lpga', league_client=setup_time_delta_1.mock_lpga.return_value)
        ])

    def test_hockey_called_1(self, setup_time_delta_1: Fixture):
        setup_time_delta_1.mock_hockey.assert_not_called()

    def test_tweet_driver_called_1(self, setup_time_delta_1: Fixture):
        setup_time_delta_1.mock_tweet_driver.assert_called_once_with(
            leagues=[
                setup_time_delta_1.mock_golf.return_value,
                setup_time_delta_1.mock_golf.return_value
            ],
            date_to_run=date(2020, 1, 1),
            send_message=True,
            skip_filter=True
        )

    @pytest.fixture
    @patch('main.tweet_driver', autospec=True)
    @patch('main.GolfLeague', autospec=True)
    @patch('main.HockeyLeague', autospec=True)
    @patch('main.BaseballLeague', autospec=True)
    @patch('main.BasketballLeague', autospec=True)
    @patch('main.LpgaSportRadar', autospec=True)
    @patch('main.PgaSportRadar', autospec=True)
    @patch('main.NhlSportRadar', autospec=True)
    @patch('main.WnbaSportRadar', autospec=True)
    @patch('main.NbaSportRadar', autospec=True)
    @patch('main.SportRadarApi', autospec=True)
    @patch('main.date', autospec=True)
    def setup_time_delta_0(self, mock_date, mock_api, mock_nba, mock_wnba, mock_nhl, mock_pga, mock_lpga,
              mock_basketball, mock_baseball,
              mock_hockey, mock_golf, mock_tweet_driver):
        mock_date.today.return_value = date(2020, 1, 2)
        mock_event = {
            'attributes': {
                'time_delta': '0'
            }
        }
        entrypoint(event=mock_event, context=Mock())

        return TestEntrypoint.Fixture(
            mock_basketball=mock_basketball,
            mock_hockey=mock_hockey,
            mock_baseball=mock_baseball,
            mock_golf=mock_golf,
            mock_api=mock_api,
            mock_nba=mock_nba,
            mock_wnba=mock_wnba,
            mock_nhl=mock_nhl,
            mock_pga=mock_pga,
            mock_lpga=mock_lpga,
            mock_tweet_driver=mock_tweet_driver
        )

    def test_get_mlb_called_0(self, setup_time_delta_0: Fixture):
        setup_time_delta_0.mock_baseball.assert_called_once()

    def test_sport_radar_api_0(self, setup_time_delta_0: Fixture):
        setup_time_delta_0.mock_api.assert_called_once()

    def test_nba_client_0(self, setup_time_delta_0: Fixture):
        setup_time_delta_0.mock_nba.assert_called_once_with(api_client=setup_time_delta_0.mock_api.return_value)

    def test_wnba_client_0(self, setup_time_delta_0: Fixture):
        setup_time_delta_0.mock_wnba.assert_called_once_with(api_client=setup_time_delta_0.mock_api.return_value)

    def test_nhl_client_0(self, setup_time_delta_0: Fixture):
        setup_time_delta_0.mock_nhl.assert_called_once_with(api_client=setup_time_delta_0.mock_api.return_value)

    def test_basketball_called_0(self, setup_time_delta_0: Fixture):
        setup_time_delta_0.mock_basketball.assert_has_calls([
            call(league_name='nba', league_client=setup_time_delta_0.mock_nba.return_value),
            call(league_name='wnba', league_client=setup_time_delta_0.mock_wnba.return_value)
        ])

    def test_golf_called_0(self, setup_time_delta_0: Fixture):
        setup_time_delta_0.mock_golf.assert_not_called()

    def test_hockey_called_0(self, setup_time_delta_0: Fixture):
        setup_time_delta_0.mock_hockey.assert_called_once_with(league_name='nhl', league_client=setup_time_delta_0.mock_nhl.return_value)

    def test_tweet_driver_called_0(self, setup_time_delta_0: Fixture):
        setup_time_delta_0.mock_tweet_driver.assert_called_once_with(
            leagues=[
                setup_time_delta_0.mock_baseball.return_value,
                setup_time_delta_0.mock_basketball.return_value,
                setup_time_delta_0.mock_basketball.return_value,
                setup_time_delta_0.mock_hockey.return_value
            ],
            date_to_run=date(2020, 1, 2),
            send_message=True,
            skip_filter=False
        )
