from dataclasses import dataclass
from datetime import date
from typing import List
from unittest.mock import Mock, call, patch

import pytest

from src.extraction.BaseballLeague import BaseballLeague
from src.models.BaseballPlayer import BaseballPlayer


def _get_mock_baseball_player(id: int, at_bats: int = 1):
    return BaseballPlayer(
        id=id, full_name='Bo', team_id=1, college='FSU', hits=1, at_bats=at_bats, home_runs=0,
        pitching_losses=0, pitching_innings='', pitching_hits=0, pitching_note='', pitching_wins=0,
        pitching_strikeouts=0, pitching_earned_runs=0
    )


class TestBaseballLeague:
    @dataclass
    class Params:
        mock_schedule_return: List
        mock_boxscore_return: dict
        mock_player_stats_return: List
        expected_boxscore_calls: List
        expected_player_stats_calls: List

    @dataclass
    class Fixture:
        mock_stats_api: Mock
        mock_player_stats: Mock
        expected_boxscore_calls: List
        expected_player_stats_calls: List
        mock_gcs: Mock

    @pytest.fixture(
        ids=['No games found', 'Game Found, No Players', 'Game and Players Found'],
        params=[
            Params(
                mock_schedule_return=[],
                mock_player_stats_return=[],
                expected_boxscore_calls=[],
                mock_boxscore_return={},
                expected_player_stats_calls=[]
            ),
            Params(
                mock_schedule_return=[{'game_id': 1}],
                mock_player_stats_return=[],
                expected_boxscore_calls=[call(gamePk=1)],
                mock_boxscore_return={
                    'away': {'foo': 'bar'},
                    'home': {'bar': 'foo'}
                },
                expected_player_stats_calls=[
                    call(team={'foo': 'bar'}, college_by_player={"123": {"id": 123}}),
                    call(team={'bar': 'foo'}, college_by_player={"123": {"id": 123}})
                ]
            ),
            Params(
                mock_schedule_return=[{'game_id': 1}],
                mock_player_stats_return=[_get_mock_baseball_player(id=1)],
                expected_boxscore_calls=[call(gamePk=1)],
                mock_boxscore_return={
                    'away': {'foo': 'bar'},
                    'home': {'bar': 'foo'}
                },
                expected_player_stats_calls=[
                    call(team={'foo': 'bar'}, college_by_player={"123": {"id": 123}}),
                    call(team={'bar': 'foo'}, college_by_player={"123": {"id": 123}})
                ]
            )
        ]
    )
    @patch('src.extraction.BaseballLeague.Gcs', autospec=True)
    @patch.object(BaseballLeague, 'player_stats_iterator')
    @patch('src.extraction.BaseballLeague.statsapi', autospec=True)
    def setup(self, mock_stats_api, mock_player_stats, mock_gcs, request):
        mock_gcs.return_value.read_as_dict.return_value = {"123": {"id": 123}}
        mock_stats_api.schedule.return_value = request.param.mock_schedule_return
        mock_stats_api.boxscore_data.return_value = request.param.mock_boxscore_return
        mock_player_stats.return_value = request.param.mock_player_stats_return

        subject = BaseballLeague()
        subject.get_games(date=date(2020, 1, 1))
        game_object = request.param.mock_schedule_return[0] if request.param.mock_schedule_return else {}

        subject.get_tweetable_objects(game=game_object)
        return TestBaseballLeague.Fixture(
            mock_stats_api=mock_stats_api,
            mock_player_stats=mock_player_stats,
            expected_boxscore_calls=request.param.expected_boxscore_calls,
            expected_player_stats_calls=request.param.expected_player_stats_calls,
            mock_gcs=mock_gcs
        )

    def test_read_as_dict_called(self, setup: Fixture):
        setup.mock_gcs.return_value.read_as_dict.assert_called_once_with(url='mlb/MLBPlayerDraft.json')

    def test_mock_schedule_called(self, setup: Fixture):
        setup.mock_stats_api.schedule.assert_called_once_with(date='01/01/2020')

    def test_boxscore_data_called(self, setup: Fixture):
        setup.mock_stats_api.boxscore_data.assert_has_calls(setup.expected_boxscore_calls)

    def test_player_stats_iterator_called(self, setup: Fixture):
        setup.mock_player_stats.assert_has_calls(setup.expected_player_stats_calls)


class TestPlayerStatsIterator:
    @dataclass
    class Params:
        expected: List
        at_bats: int
        team: dict
        expected_baseball_player_from_dict_calls: List

    @dataclass
    class Fixture:
        actual: List
        expected: List
        mock_baseball_player_from_dict: Mock
        expected_baseball_player_from_dict_calls: List

    @pytest.fixture(
        ids=['Not Decent Day', 'Is Decent Batter Day', 'Player not in College Map'],
        params=[
            Params(
                team={'team': {'id': 1}, 'players': {'123': {'person': {'id': 123}}}},
                at_bats=0,
                expected=[],
                expected_baseball_player_from_dict_calls=[
                    call(player={'person': {'id': 123}}, team_id=1, college={'id': 123, 'college': 'FSU'})]
            ),
            Params(
                team={'team': {'id': 1}, 'players': {'123': {'person': {'id': 123}}}},
                at_bats=1,
                expected=[
                    _get_mock_baseball_player(id=123)],
                expected_baseball_player_from_dict_calls=[
                    call(player={'person': {'id': 123}}, team_id=1, college={'id': 123, 'college': 'FSU'})]
            ),
            Params(
                team={'team': {'id': 1}, 'players': {'123': {'person': {'id': 0}}}},
                at_bats=1,
                expected=[],
                expected_baseball_player_from_dict_calls=[]
            ),
        ]
    )
    @patch('src.extraction.BaseballLeague.baseball_player_from_dict', autospec=True)
    def setup(self, mock_baseball_player, request):
        mock_baseball_player.return_value = _get_mock_baseball_player(id=123, at_bats =request.param.at_bats)
        return TestPlayerStatsIterator.Fixture(
            expected=request.param.expected,
            actual=BaseballLeague.player_stats_iterator(team=request.param.team,
                                         college_by_player={'123': {'id': 123, 'college': 'FSU'}}),
            expected_baseball_player_from_dict_calls=request.param.expected_baseball_player_from_dict_calls,
            mock_baseball_player_from_dict=mock_baseball_player
        )

    def test_baseball_player_from_dict_called(self, setup: Fixture):
        assert setup.mock_baseball_player_from_dict.mock_calls == setup.expected_baseball_player_from_dict_calls

    def test_player_stats_iterator_return(self, setup: Fixture):
        assert setup.actual == setup.expected
