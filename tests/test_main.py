from dataclasses import dataclass
from datetime import date
from unittest.mock import Mock, patch, call

import pytest
from nba_api.stats.library.parameters import LeagueID

from main import entrypoint


class TestEntrypoint:
    @dataclass
    class Fixture:
        mock_basketball: Mock
        mock_mlb: Mock

    @pytest.fixture
    @patch('main.date', autospec=True)
    @patch('main.get_mlb', autospec=True)
    @patch('main.get_basketball', autospec=True)
    def setup(self, mock_basketball, mock_mlb, mock_date):
        mock_date.today.return_value = date(2020, 1, 2)

        entrypoint(event=Mock(), context=Mock())

        return TestEntrypoint.Fixture(
            mock_basketball=mock_basketball,
            mock_mlb=mock_mlb
        )

    def test_get_mlb_called(self, setup: Fixture):
        setup.mock_mlb.assert_called_once_with(date_to_run=date(2020, 1, 1))

    def test_get_basketball_called(self, setup: Fixture):
        setup.mock_basketball.assert_has_calls([
            call(date_to_run=date(2020, 1, 1), league_id=LeagueID.nba),
            call(date_to_run=date(2020, 1, 1), league_id=LeagueID.wnba)
        ])
