from dataclasses import dataclass
from datetime import date
from typing import List
from unittest.mock import Mock, call, patch

import pytest

from src.college.mlb import mlb_fsu_player_ids
from src.mlb import get_mlb, player_stats_iterator, is_a_decent_day


class TestGetMlb:
    @dataclass
    class Params:
        mock_schedule_return: List
        mock_boxscore_return: dict
        mock_player_stats_return: List
        expected_publish_calls: List
        expected_boxscore_calls: List
        expected_player_stats_calls: List

    @dataclass
    class Fixture:
        mock_stats_api: Mock
        mock_player_stats: Mock
        mock_publish: Mock
        expected_publish_calls: List
        expected_boxscore_calls: List
        expected_player_stats_calls: List

    @pytest.fixture(
        ids=['No games found', 'Game Found, No Players', 'Game and Players Found'],
        params=[
            Params(
                mock_schedule_return=[],
                mock_player_stats_return=[],
                expected_publish_calls=[],
                expected_boxscore_calls=[],
                mock_boxscore_return={},
                expected_player_stats_calls=[]
            ),
            Params(
                mock_schedule_return=[{'game_id': 1}],
                mock_player_stats_return=[],
                expected_publish_calls=[],
                expected_boxscore_calls=[call(gamePk=1)],
                mock_boxscore_return={
                    'away': {'foo': 'bar'},
                    'home': {'bar': 'foo'}
                },
                expected_player_stats_calls=[
                    call(team={'foo': 'bar'}, player_ids=mlb_fsu_player_ids),
                    call(team={'bar': 'foo'}, player_ids=mlb_fsu_player_ids)
                ]
            ),
            Params(
                mock_schedule_return=[{'game_id': 1}],
                mock_player_stats_return=[
                    {'person': {'fullName': 'Bo'}, 'stats': {'batting': {'hits': 1, 'atBats': 2}}}],
                expected_publish_calls=[call(message='Bo went 1-2. Bo went 1-2. ')],
                expected_boxscore_calls=[call(gamePk=1)],
                mock_boxscore_return={
                    'away': {'foo': 'bar'},
                    'home': {'bar': 'foo'}
                },
                expected_player_stats_calls=[
                    call(team={'foo': 'bar'}, player_ids=mlb_fsu_player_ids),
                    call(team={'bar': 'foo'}, player_ids=mlb_fsu_player_ids)
                ]
            )
        ]
    )
    @patch('src.mlb.publish_message', autospec=True)
    @patch('src.mlb.player_stats_iterator', autospec=True)
    @patch('src.mlb.statsapi', autospec=True)
    def setup(self, mock_stats_api, mock_player_stats, mock_publish, request):
        mock_stats_api.schedule.return_value = request.param.mock_schedule_return
        mock_stats_api.boxscore_data.return_value = request.param.mock_boxscore_return
        mock_player_stats.return_value = request.param.mock_player_stats_return

        get_mlb(date_to_run=date(2020, 1, 1))

        return TestGetMlb.Fixture(
            mock_stats_api=mock_stats_api,
            mock_player_stats=mock_player_stats,
            mock_publish=mock_publish,
            expected_publish_calls=request.param.expected_publish_calls,
            expected_boxscore_calls=request.param.expected_boxscore_calls,
            expected_player_stats_calls=request.param.expected_player_stats_calls
        )

    def test_mock_schedule_called(self, setup: Fixture):
        setup.mock_stats_api.schedule.assert_called_once_with(date='01/01/2020')

    def test_boxscore_data_called(self, setup: Fixture):
        setup.mock_stats_api.boxscore_data.assert_has_calls(setup.expected_boxscore_calls)

    def test_player_stats_iterator_called(self, setup: Fixture):
        setup.mock_player_stats.assert_has_calls(setup.expected_player_stats_calls)

    def test_publish_message_called(self, setup: Fixture):
        setup.mock_publish.assert_has_calls(setup.expected_publish_calls)


class TestPlayerStatsIterator:
    @pytest.mark.parametrize("team,is_decent_day,expected", [
        ({}, False, []),
        ({'players': {'ID123': {'person': {'id': 123}}}}, False, []),
        ({'players': {'ID123': {'person': {'id': 123}}}}, True, [{'person': {'id': 123}}]),
    ])
    @patch('src.mlb.is_a_decent_day', autospec=True)
    def test_player_stats_iterator(self, mock_decent_day, team, is_decent_day, expected):
        mock_decent_day.return_value = is_decent_day
        assert player_stats_iterator(team=team, player_ids=[123]) == expected


class TestIsADecentDay:
    @pytest.mark.parametrize("player,expected", [
        ({}, False),
        ({'stats': {}}, False),
        ({'stats': {'batting': {}}}, False),
        ({'stats': {'batting': {'hits': None}}}, False),
        ({'stats': {'batting': {'hits': 0}}}, False),
        ({'stats': {'batting': {'hits': 1}}}, True)
    ])
    def test_is_a_decent_day(self, player, expected):
        assert is_a_decent_day(player=player) == expected


