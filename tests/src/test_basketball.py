from dataclasses import dataclass
from typing import List
from unittest.mock import Mock, call, patch
from datetime import date

import pytest
from nba_api.stats.library.parameters import LeagueID

from src.basketball import get_basketball


class TestBasketball:
    @dataclass
    class Params:
        mock_schedule_return: List
        mock_player_stats_return: List
        expected_publish_calls: List
        expected_boxscore_calls: List
        expected_player_info_calls: List
        mock_school: str

    @dataclass
    class Fixture:
        mock_boxscore: Mock
        mock_scoreboard: Mock
        mock_player_info: Mock
        mock_publish: Mock
        expected_boxscore_calls: List
        expected_player_info_calls: List

    @pytest.fixture(
        ids=['No games found', 'Game Found, No Players', 'Game and Players Found', 'Game and Player Found, No Stats'],
        params=[
            Params(
                mock_schedule_return=[],
                mock_player_stats_return=[],
                expected_publish_calls=[],
                expected_boxscore_calls=[],
                expected_player_info_calls=[],
                mock_school=''
            ),
            Params(
                mock_schedule_return=[{'GAME_ID': 1}],
                mock_player_stats_return=[{'PLAYER_ID': 5}],
                expected_publish_calls=[],
                expected_boxscore_calls=[call(game_id=1)],
                expected_player_info_calls=[call(player_id=5)],
                mock_school='notFSU'
            ),
            Params(
                mock_schedule_return=[{'GAME_ID': 1}],
                mock_player_stats_return=[{'PLAYER_ID': 5, 'PTS': 1, 'REB': 5, 'AST': None, 'PLAYER_NAME': 'Dragon'}],
                expected_publish_calls=[call(message='Dragon 1 pts/5 reb')],
                expected_boxscore_calls=[call(game_id=1)],
                expected_player_info_calls=[call(player_id=5)],
                mock_school='FSU'
            ),
            Params(
                mock_schedule_return=[{'GAME_ID': 1}],
                mock_player_stats_return=[{'PLAYER_ID': 5, 'PTS': 0, 'REB': 0, 'AST': 0, 'PLAYER_NAME': 'Dragon'}],
                expected_publish_calls=[],
                expected_boxscore_calls=[call(game_id=1)],
                expected_player_info_calls=[call(player_id=5)],
                mock_school='FSU'
            )
        ]
    )
    @patch('time.sleep', return_value=None)
    @patch('src.basketball.publish_message', autospec=True)
    @patch('src.basketball.commonplayerinfo', autospec=True)
    @patch('src.basketball.scoreboard', autospec=True)
    @patch('src.basketball.boxscoretraditionalv2', autospec=True)
    def setup(self, mock_boxscore, mock_scoreboard, mock_player_info, mock_publish, mock_sleep, request):
        mock_schedule = Mock()
        mock_schedule.get_normalized_dict.return_value = {
            'GameHeader': request.param.mock_schedule_return
        }

        mock_scoreboard.Scoreboard.return_value = mock_schedule

        mock_player_stats = Mock()
        mock_player_stats.get_normalized_dict.return_value = {
            'PlayerStats': request.param.mock_player_stats_return
        }
        mock_boxscore.BoxScoreTraditionalV2.return_value = mock_player_stats

        mock_player = Mock()
        mock_player.get_normalized_dict.return_value = {
            'CommonPlayerInfo': [{'SCHOOL': request.param.mock_school}]
        }
        mock_player_info.CommonPlayerInfo.return_value = mock_player

        get_basketball(date_to_run=date(2020, 1, 1), league_id=LeagueID.nba, send_message=True)
        return TestBasketball.Fixture(
            mock_boxscore=mock_boxscore,
            mock_scoreboard=mock_scoreboard,
            mock_player_info=mock_player_info,
            mock_publish=mock_publish,
            expected_boxscore_calls=request.param.expected_boxscore_calls,
            expected_player_info_calls=request.param.expected_player_info_calls
        )

    def test_scoreboard_called(self, setup: Fixture):
        setup.mock_scoreboard.Scoreboard.assert_called_once_with(game_date='01/01/2020', league_id=LeagueID.nba)

    def test_boxscore_called(self, setup: Fixture):
        setup.mock_boxscore.BoxScoreTraditionalV2.assert_has_calls(setup.expected_boxscore_calls)

    def test_player_info_called(self, setup: Fixture):
        setup.mock_player_info.CommonPlayerInfo.assert_has_calls(setup.expected_player_info_calls)
