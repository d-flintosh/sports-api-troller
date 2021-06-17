from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

from src.api.basketball_sport_radar import BasketballSportRadar
from src.college.basketball import write_to_file_readable_for_computers


class TestWriteToFileReadableForComputers:
    @dataclass
    class Fixture:
        mock_league_client: Mock
        mock_gcs: Mock

    @pytest.fixture
    @patch('src.college.basketball.Gcs', autospec=True)
    def setup(self, mock_gcs):
        mock_league_client = Mock(spec=BasketballSportRadar)
        mock_league_client.get_all_players_with_college.return_value = {

        }
        write_to_file_readable_for_computers(league='nba', league_client=mock_league_client)

        return TestWriteToFileReadableForComputers.Fixture(
            mock_league_client=mock_league_client,
            mock_gcs=mock_gcs
        )

    def test_get_all_players_called(self, setup: Fixture):
        setup.mock_league_client.get_all_players_with_college.assert_called_once()

    def test_gcs_called(self, setup: Fixture):
        setup.mock_gcs.assert_called_once_with(bucket='college-by-player')

    def test_gcs_write_called(self, setup: Fixture):
        setup.mock_gcs.return_value.write.assert_called_once_with(url='nba/players.json', contents={})
