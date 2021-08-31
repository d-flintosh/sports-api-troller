from dataclasses import dataclass
from datetime import date
from typing import List
from unittest.mock import Mock, call, patch

import pytest

from src.api.nfl_sport_radar import NflSportRadar
from src.extraction.FootballLeague import FootballLeague


class TestFootballLeague:
    @dataclass
    class Params:
        mock_schedule_return: List
        mock_boxscore_return: dict
        expected_boxscore_calls: List
        expected_football_player_from_dict: List

    @dataclass
    class Fixture:
        mock_client: Mock
        mock_football_player_from_dict: Mock
        expected_boxscore_calls: List
        expected_football_player_from_dict: List
        mock_gcs: Mock

    @pytest.fixture(
        ids=['Game and Players Found'],
        params=[
            Params(
                mock_schedule_return=[{'id': '1', 'status': 'complete'}],
                expected_boxscore_calls=[call(game_id='1')],
                mock_boxscore_return={
                    'statistics': {
                        'away': {
                            'id': '2',
                            'rushing': {
                                'players': [
                                    {
                                        'name': 'guy',
                                        'id': '1'
                                    }
                                ]
                            },
                            'passing': {
                                'players': [
                                    {
                                        'name': 'guy',
                                        'id': '1'
                                    },
                                    {
                                        'name': 'guy',
                                        'id': '2'
                                    }
                                ]
                            }
                        },
                        'home': {
                            'id': '2',
                            'rushing': {
                                'players': [
                                    {
                                        'name': 'guy',
                                        'id': '3'
                                    }
                                ]
                            },
                            'passing': {
                                'players': [
                                    {
                                        'name': 'guy',
                                        'id': '123'
                                    },
                                    {
                                        'name': 'guy',
                                        'id': '5'
                                    }
                                ]
                            }
                        }
                    }
                },
                expected_football_player_from_dict=[
                    call(player={'team_id': '2', 'player_id': '123', 'full_name': 'guy', 'passing': {'name': 'guy', 'id': '123'}}, college={"id": '123'}),
                    call(player={'team_id': '2', 'player_id': '5', 'full_name': 'guy', 'passing': {'name': 'guy', 'id': '5'}}, college=None),
                    call(player={'team_id': '2', 'player_id': '2', 'full_name': 'guy', 'passing': {'name': 'guy', 'id': '2'}}, college=None),
                    call(player={'team_id': '2', 'player_id': '3', 'full_name': 'guy', 'rushing': {'name': 'guy', 'id': '3'}}, college=None),
                    call(player={'team_id': '2', 'player_id': '1', 'full_name': 'guy', 'rushing': {'name': 'guy', 'id': '1'}, 'passing': {'name': 'guy', 'id': '1'}}, college=None)
                ]
            )
        ]
    )
    @patch('src.extraction.FootballLeague.Gcs', autospec=True)
    @patch('src.extraction.FootballLeague.football_player_from_dict', autospec=True)
    def setup(self, mock_football_player_from_dict, mock_gcs, request):
        mock_gcs.return_value.read_as_dict.return_value = {"123": {"id": '123'}}
        mock_client = Mock(spec=NflSportRadar)
        mock_client.get_daily_schedule.return_value = request.param.mock_schedule_return
        mock_client.get_boxscore.return_value = request.param.mock_boxscore_return

        subject = FootballLeague(league_name='nfl', league_client=mock_client)
        subject.get_games(date=date(2020, 1, 1))
        game_object = request.param.mock_schedule_return[0] if request.param.mock_schedule_return else {}
        subject.get_tweetable_objects(game=game_object)

        return TestFootballLeague.Fixture(
            mock_client=mock_client,
            mock_football_player_from_dict=mock_football_player_from_dict,
            expected_boxscore_calls=request.param.expected_boxscore_calls,
            expected_football_player_from_dict=request.param.expected_football_player_from_dict,
            mock_gcs=mock_gcs
        )

    def test_read_as_dict_called(self, setup: Fixture):
        setup.mock_gcs.return_value.read_as_dict.assert_called_once_with(url='nfl/players.json')

    def test_mock_schedule_called(self, setup: Fixture):
        setup.mock_client.get_daily_schedule.assert_called_once_with(date=date(2020, 1, 1))

    def test_boxscore_data_called(self, setup: Fixture):
        setup.mock_client.get_boxscore.assert_has_calls(setup.expected_boxscore_calls, any_order=True)

    def test_football_player_from_dict_called(self, setup: Fixture):
        setup.mock_football_player_from_dict.assert_has_calls(setup.expected_football_player_from_dict, any_order=True)

