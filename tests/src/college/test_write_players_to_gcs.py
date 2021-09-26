from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

from src.api.basketball_sport_radar import BasketballSportRadar
from src.college.write_players_to_gcs import write_to_file_readable_for_computers
from src.models.PlayerDraft import PlayerDraft


class TestWriteToFileReadableForComputers:
    @dataclass
    class Fixture:
        mock_league_client: Mock
        mock_gcs: Mock

    @pytest.fixture
    @patch('src.college.write_players_to_gcs.Gcs', autospec=True)
    def setup(self, mock_gcs):
        mock_league_client = Mock(spec=BasketballSportRadar)
        mock_league_client.get_all_players_with_college.return_value = [
            PlayerDraft(id=1, full_name='Bo', college='some college')
        ]
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
        setup.mock_gcs.return_value.write.assert_called_once_with(
            url='nba/players.json',
            contents={1: {'id': 1, 'full_name': 'Bo', 'college': 'some college'}}
        )
