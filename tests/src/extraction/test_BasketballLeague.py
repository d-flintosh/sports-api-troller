from dataclasses import dataclass
from datetime import date
from typing import List, Optional
from unittest.mock import Mock, patch, call

import pytest

from src.api.basketball_sport_radar import BasketballSportRadar
from src.extraction.BasketballLeague import BasketballLeague
from src.models.BasketballPlayer import BasketballPlayer


class TestBasketballLeague:
    @dataclass
    class Params:
        mock_schedule_return: List
        mock_player_stats_return: Optional[BasketballPlayer]
        expected_boxscore_calls: List
        expected_basketball_player_from_dict: List

    @dataclass
    class Fixture:
        mock_league_client: Mock
        mock_gcs: Mock
        expected_boxscore_calls: List
        mock_basketball_player: Mock
        expected_basketball_player_from_dict: List
        subject: BasketballLeague
        expected_games: List

    @pytest.fixture(
        ids=['No games found', 'Game and Players Found'],
        params=[
            Params(
                mock_schedule_return=[],
                mock_player_stats_return=None,
                expected_boxscore_calls=[],
                expected_basketball_player_from_dict=[]
            ),
            Params(
                mock_schedule_return=[{'id': '1', 'status': 'closed'}],
                mock_player_stats_return=BasketballPlayer(
                    id='5',
                    league_name='nba',
                    team_id='1',
                    full_name='Dragon',
                    college='FSU',
                    points=1,
                    rebounds=5,
                    assists=0
                ),
                expected_boxscore_calls=[call(game_id='1')],
                expected_basketball_player_from_dict=[
                    call(
                        player={'id': '123'},
                        team_id='5',
                        league_name='nba',
                        college={"id": '123', "college": "someSchool"}
                    ),
                    call(
                        player={'id': '321'},
                        team_id='8',
                        league_name='nba',
                        college=None
                    )
                ]
            )
        ]
    )
    @patch('src.extraction.BasketballLeague.basketball_player_from_dict', autospec=True)
    @patch('src.extraction.BasketballLeague.Gcs', autospec=True)
    def setup(self, mock_gcs, mock_basketball_player, request):
        mock_league_client = Mock(spec=BasketballSportRadar)
        schedule_return = request.param.mock_schedule_return

        mock_league_client.get_daily_schedule.return_value = {
            'games': schedule_return
        }
        mock_league_client.get_boxscore.return_value = {
            'home': {
                'id': '5',
                'players': [{
                    'id': '123'
                }]
            },
            'away': {
                'id': '8',
                'players': [{
                    'id': '321'
                }]
            }
        }
        mock_gcs.return_value.read_as_dict.return_value = {'123': {'id': '123', 'college': 'someSchool'}}

        mock_basketball_player.return_value = request.param.mock_player_stats_return

        subject = BasketballLeague(
            league_client=mock_league_client,
            league_name='nba',
        )
        date_to_use = date(2021, 1, 1)
        actual_games = subject.get_games(date=date_to_use)
        game_object = schedule_return[0] if schedule_return else {}
        actual_objects = subject.get_tweetable_objects(game=game_object)

        return TestBasketballLeague.Fixture(
            mock_league_client=mock_league_client,
            mock_gcs=mock_gcs,
            expected_boxscore_calls=request.param.expected_boxscore_calls,
            mock_basketball_player=mock_basketball_player,
            expected_basketball_player_from_dict=request.param.expected_basketball_player_from_dict,
            subject=subject,
            expected_games=schedule_return
        )

    def test_get_games(self, setup: Fixture):
        setup.mock_league_client.get_daily_schedule.assert_called_once_with(date=date(2021, 1, 1))

    def test_get_get_boxscore(self, setup: Fixture):
        setup.mock_league_client.get_boxscore.assert_has_calls(setup.expected_boxscore_calls)


class TestGetFilteredGames:
    @dataclass
    class Params:
        input: dict
        expected_games: List

    @dataclass
    class Fixture:
        expected_games: List
        actual: List

    @pytest.fixture(
        ids=['No games object', 'No games', 'No closed games', 'Found Game'],
        params=[
            Params(
                input={},
                expected_games=[]
            ),
            Params(
                input={'games': []},
                expected_games=[]
            ),
            Params(
                input={'games': [{'status': 'not closed'}]},
                expected_games=[]
            ),
            Params(
                input={'games': [{'status': 'closed'}]},
                expected_games=[{'status': 'closed'}]
            )
        ]
    )
    def setup(self, request):

        return TestGetFilteredGames.Fixture(
            expected_games=request.param.expected_games,
            actual=BasketballLeague.get_filtered_games(daily_schedule=request.param.input)
        )

    def test_get_filtered_games_result(self, setup: Fixture):
        assert setup.actual == setup.expected_games
