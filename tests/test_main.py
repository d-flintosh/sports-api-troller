from datetime import date
from dataclasses import dataclass
from typing import List
from unittest.mock import Mock, patch, call

import pytest

from main import publish_message, is_fsu, get_fsu_players, is_a_decent_day, player_stats_iterator, entrypoint, \
    fsu_player_ids


class TestPublishMessage:
    @dataclass
    class Fixture:
        mock_publisher: Mock
        mock_future: Mock

    @pytest.fixture
    @patch('main.pubsub_v1')
    def setup(self, mock_pub_sub):
        mock_publisher = mock_pub_sub.PublisherClient.return_value
        mock_future = Mock()
        mock_publisher.publish.return_value = mock_future

        publish_message(message='shoot and score')
        return TestPublishMessage.Fixture(
            mock_publisher=mock_publisher,
            mock_future=mock_future
        )

    def test_publish_called(self, setup: Fixture):
        setup.mock_publisher.publish.assert_called_once_with(
            'projects/sports-data-service/topics/twitter-message-service-pubsub',
            str.encode('shoot and score')
        )

    def test_future_result_called(self, setup: Fixture):
        setup.mock_future.result.assert_called_once()


class TestIsFsu:
    @pytest.mark.parametrize("school,expected", [
        ('florida', False),
        ('florida state university', True),
        ('florida state', True),
        ('fsu', True),
        ('fSu', True)
    ])
    def test_is_fsu(self, school, expected):
        assert is_fsu(school={'name': school}) == expected


class TestGetFsuPlayers:
    @dataclass
    class Fixture:
        mock_stats_api: Mock
        actual: List

    @pytest.fixture
    @patch('main.statsapi')
    def setup(self, mock_stats_api):
        mock_stats_api.get.return_value = {
            'drafts': {
                'rounds': [
                    {
                        'picks': [
                            {
                                'school': {'name': 'fsu'},
                                'person': {
                                    'id': 123
                                }
                            }
                        ]
                    }
                ]
            }
        }
        return TestGetFsuPlayers.Fixture(
            mock_stats_api=mock_stats_api,
            actual=get_fsu_players()
        )

    def test_stats_api_called(self, setup: Fixture):
        setup.mock_stats_api.get.assert_has_calls([
            call('draft', params={'year': '2000'}),
            call('draft', params={'year': '2001'}),
            call('draft', params={'year': '2002'}),
            call('draft', params={'year': '2003'}),
            call('draft', params={'year': '2004'}),
            call('draft', params={'year': '2005'}),
            call('draft', params={'year': '2006'}),
            call('draft', params={'year': '2007'}),
            call('draft', params={'year': '2008'}),
            call('draft', params={'year': '2009'}),
            call('draft', params={'year': '2010'}),
            call('draft', params={'year': '2011'}),
            call('draft', params={'year': '2012'}),
            call('draft', params={'year': '2013'}),
            call('draft', params={'year': '2014'}),
            call('draft', params={'year': '2015'}),
            call('draft', params={'year': '2016'}),
            call('draft', params={'year': '2017'}),
            call('draft', params={'year': '2018'}),
            call('draft', params={'year': '2019'})
        ])

    def test_output_correct(self, setup: Fixture):
        assert setup.actual == [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123,
                                123, 123, 123]


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


class TestPlayerStatsIterator:
    @pytest.mark.parametrize("team,is_decent_day,expected", [
        ({}, False, []),
        ({'players': {'ID123': {'person': {'id': 123}}}}, False, []),
        ({'players': {'ID123': {'person': {'id': 123}}}}, True, [{'person': {'id': 123}}]),
    ])
    @patch('main.is_a_decent_day', autospec=True)
    def test_player_stats_iterator(self, mock_decent_day, team, is_decent_day, expected):
        mock_decent_day.return_value = is_decent_day
        assert player_stats_iterator(team=team, fsu_player_ids=[123]) == expected


class TestEntrypoint:
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
                    call(team={'foo': 'bar'}, fsu_player_ids=fsu_player_ids),
                    call(team={'bar': 'foo'}, fsu_player_ids=fsu_player_ids)
                ]
            ),
            Params(
                mock_schedule_return=[{'game_id': 1}],
                mock_player_stats_return=[{'person': {'fullName': 'Bo'}, 'stats': {'batting': {'hits': 1, 'atBats': 2}}}],
                expected_publish_calls=[call(message='Bo went 1-2. Bo went 1-2. ')],
                expected_boxscore_calls=[call(gamePk=1)],
                mock_boxscore_return={
                    'away': {'foo': 'bar'},
                    'home': {'bar': 'foo'}
                },
                expected_player_stats_calls=[
                    call(team={'foo': 'bar'}, fsu_player_ids=fsu_player_ids),
                    call(team={'bar': 'foo'}, fsu_player_ids=fsu_player_ids)
                ]
            )
        ]
    )
    @patch('main.date', autospec=True)
    @patch('main.publish_message', autospec=True)
    @patch('main.player_stats_iterator', autospec=True)
    @patch('main.statsapi', autospec=True)
    def setup(self, mock_stats_api, mock_player_stats, mock_publish, mock_date, request):
        mock_date.today.return_value = date(2020, 1, 2)
        mock_stats_api.schedule.return_value = request.param.mock_schedule_return
        mock_stats_api.boxscore_data.return_value = request.param.mock_boxscore_return
        mock_player_stats.return_value = request.param.mock_player_stats_return

        entrypoint(event=Mock(), context=Mock())

        return TestEntrypoint.Fixture(
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
