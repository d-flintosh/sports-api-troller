from dataclasses import dataclass
from typing import Set
from unittest.mock import patch, Mock

import pytest
from nba_api.stats.library.parameters import LeagueID

from src.college.basketball import extract_all_basketball_players_draft_info
from src.models.PlayerDraft import PlayerDraft


class TestExtractAllBasketballPlayersDraftInfo:
    @dataclass
    class Params:
        expected: Set

    @dataclass
    class Fixture:
        mock_all_players: Mock
        mock_player_info: Mock
        actual: Set
        expected: Set

    @pytest.fixture(
        ids=['Get Players'],
        params=[
            Params(
                expected={PlayerDraft(
                    id=123,
                    full_name='Bo',
                    college='someThing'
                )}
            )
        ])
    @patch('time.sleep', return_value=None)
    @patch('src.college.basketball.commonplayerinfo')
    @patch('src.college.basketball.commonallplayers')
    def setup(self, mock_all_players, mock_player_info, mock_sleep, request):
        mock_all_players.CommonAllPlayers.return_value.get_normalized_dict.return_value = {
            'CommonAllPlayers': [
                {
                    'PERSON_ID': 123
                }
            ]
        }

        mock_player_info.CommonPlayerInfo.return_value.get_normalized_dict.return_value = {
            'CommonPlayerInfo': [
                {
                    'PERSON_ID': 123,
                    'DISPLAY_FIRST_LAST': 'Bo',
                    'SCHOOL': 'someThing'
                }
            ]
        }
        return TestExtractAllBasketballPlayersDraftInfo.Fixture(
            mock_all_players=mock_all_players,
            mock_player_info=mock_player_info,
            actual=extract_all_basketball_players_draft_info(league_id=LeagueID.nba),
            expected=request.param.expected
        )

    def test_all_players_called(self, setup: Fixture):
        setup.mock_all_players.CommonAllPlayers.assert_called_once_with(
            is_only_current_season=1,
            league_id=LeagueID.nba
        )

    def test_player_info_called(self, setup: Fixture):
        setup.mock_player_info.CommonPlayerInfo.assert_called_once_with(player_id=123)

    def test_output_correct(self, setup: Fixture):
        assert setup.actual == setup.expected
