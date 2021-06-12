from dataclasses import dataclass
from typing import Set, List
from unittest.mock import patch, call, Mock

import pytest
from nba_api.stats.library.parameters import LeagueID

from src.college.basketball import extract_all_basketball_players_draft_info, write_to_file_readable_for_computers
from src.models.PlayerDraft import PlayerDraft


class TestExtractAllBasketballPlayersDraftInfo:
    @dataclass
    class Params:
        expected: Set

    @dataclass
    class Fixture:
        mock_draft_history: Mock
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
    @patch('src.college.basketball.drafthistory')
    def setup(self, mock_draft_history, request):
        mock_draft_history.DraftHistory.return_value.get_normalized_dict.return_value = {
            'foo': [
                {
                    'PERSON_ID': 123,
                    'ORGANIZATION': 'someThing',
                    'PLAYER_NAME': 'Bo'
                }
            ]
        }
        return TestExtractAllBasketballPlayersDraftInfo.Fixture(
            mock_draft_history=mock_draft_history,
            actual=extract_all_basketball_players_draft_info(league_id=LeagueID.nba),
            expected=request.param.expected
        )

    def test_stats_api_called(self, setup: Fixture):
        setup.mock_draft_history.DraftHistory.assert_called_once_with(league_id=LeagueID.nba)

    def test_output_correct(self, setup: Fixture):
        assert setup.actual == setup.expected


@pytest.mark.skip(reason="only run this manually")
def test_extract_basketball_draft_info():
    print(write_to_file_readable_for_computers(league_id=LeagueID.nba))
    print(write_to_file_readable_for_computers(league_id=LeagueID.wnba))