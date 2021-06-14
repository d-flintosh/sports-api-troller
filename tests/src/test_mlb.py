from dataclasses import dataclass
from datetime import date
from typing import List
from unittest.mock import Mock, call, patch

import pytest

from src.mlb import get_mlb, player_stats_iterator
from src.models.BaseballPlayer import BaseballPlayer


def _get_mock_baseball_player(id: int, at_bats: int = 1):
    return BaseballPlayer(
        id=id, full_name='Bo', team_id=1, college='FSU', hits=1, at_bats=at_bats, home_runs=0,
        pitching_losses=0, pitching_innings='', pitching_hits=0, pitching_note='', pitching_wins=0,
        pitching_strikeouts=0, pitching_earned_runs=0
    )


class TestGetMlb:
    @dataclass
    class Params:
        mock_schedule_return: List
        mock_boxscore_return: dict
        mock_player_stats_return: List
        expected_send_tweet_calls: List
        expected_boxscore_calls: List
        expected_player_stats_calls: List

    @dataclass
    class Fixture:
        mock_stats_api: Mock
        mock_player_stats: Mock
        mock_send_tweet: Mock
        expected_send_tweet_calls: List
        expected_boxscore_calls: List
        expected_player_stats_calls: List
        mock_gcs: Mock

    @pytest.fixture(
        ids=['No games found', 'Game Found, No Players', 'Game and Players Found'],
        params=[
            Params(
                mock_schedule_return=[],
                mock_player_stats_return=[],
                expected_send_tweet_calls=[],
                expected_boxscore_calls=[],
                mock_boxscore_return={},
                expected_player_stats_calls=[]
            ),
            Params(
                mock_schedule_return=[{'game_id': 1}],
                mock_player_stats_return=[],
                expected_send_tweet_calls=[],
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
                expected_send_tweet_calls=[
                    call(school='fsu', player_stats=[
                        _get_mock_baseball_player(id=1),
                        _get_mock_baseball_player(id=1)
                    ])
                ],
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
    @patch('src.mlb.Gcs', autospec=True)
    @patch('src.mlb.SendTweetForSchool', autospec=True)
    @patch('src.mlb.player_stats_iterator', autospec=True)
    @patch('src.mlb.statsapi', autospec=True)
    def setup(self, mock_stats_api, mock_player_stats, mock_send_tweet, mock_gcs, request):
        mock_send_tweet.reset_mock()
        mock_gcs.return_value.read_as_dict.return_value = {"123": {"id": 123}}
        mock_stats_api.schedule.return_value = request.param.mock_schedule_return
        mock_stats_api.boxscore_data.return_value = request.param.mock_boxscore_return
        mock_player_stats.return_value = request.param.mock_player_stats_return

        get_mlb(date_to_run=date(2020, 1, 1))

        return TestGetMlb.Fixture(
            mock_stats_api=mock_stats_api,
            mock_player_stats=mock_player_stats,
            mock_send_tweet=mock_send_tweet,
            expected_send_tweet_calls=request.param.expected_send_tweet_calls,
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

    def test_send_tweet_constructor_called(self, setup: Fixture):
        setup.mock_send_tweet.assert_has_calls(setup.expected_send_tweet_calls)

    def test_send_tweet_called(self, setup: Fixture):
        if setup.expected_send_tweet_calls:
            setup.mock_send_tweet.return_value.publish.assert_called_once_with(
                send_message=True,
                sport='baseball'
            )
        else:
            setup.mock_send_tweet.return_value.publish.assert_not_called()


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
    @patch('src.mlb.baseball_player_from_dict', autospec=True)
    def setup(self, mock_baseball_player, request):
        mock_baseball_player.return_value = _get_mock_baseball_player(id=123, at_bats =request.param.at_bats)
        return TestPlayerStatsIterator.Fixture(
            expected=request.param.expected,
            actual=player_stats_iterator(team=request.param.team,
                                         college_by_player={'123': {'id': 123, 'college': 'FSU'}}),
            expected_baseball_player_from_dict_calls=request.param.expected_baseball_player_from_dict_calls,
            mock_baseball_player_from_dict=mock_baseball_player
        )

    def test_baseball_player_from_dict_called(self, setup: Fixture):
        assert setup.mock_baseball_player_from_dict.mock_calls == setup.expected_baseball_player_from_dict_calls

    def test_player_stats_iterator_return(self, setup: Fixture):
        assert setup.actual == setup.expected
