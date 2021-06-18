from dataclasses import dataclass
from datetime import date
from typing import List
from unittest.mock import Mock, patch

import pytest

from src.api.golf_sport_radar import GolfSportRadar
from src.extraction.GolfLeague import GolfLeague


class TestGolfLeague:
    @dataclass
    class Params:
        mock_schedule_return: List

    @dataclass
    class Fixture:
        mock_league_client: Mock
        mock_gcs: Mock
        subject: GolfLeague
        expected_games: List

    @pytest.fixture(
        ids=['No games found'],
        params=[
            Params(
                mock_schedule_return=[]
            )
        ]
    )
    @patch('src.extraction.GolfLeague.Gcs', autospec=True)
    def setup(self, mock_gcs, request):
        mock_league_client = Mock(spec=GolfSportRadar)
        schedule_return = request.param.mock_schedule_return

        mock_league_client.get_tournament_schedule.return_value = {
            'games': schedule_return
        }
        mock_gcs.return_value.read_as_dict.return_value = {'123': {'id': '123', 'college': 'someSchool'}}

        subject = GolfLeague(
            league_client=mock_league_client,
            league_name='nba',
        )
        date_to_use = date(2021, 1, 1)
        actual_games = subject.get_games(date=date_to_use)
        game_object = schedule_return[0] if schedule_return else {}
        actual_objects = subject.get_tweetable_objects(game=game_object)

        return TestGolfLeague.Fixture(
            mock_league_client=mock_league_client,
            mock_gcs=mock_gcs,
            subject=subject,
            expected_games=schedule_return
        )

    def test_get_games(self, setup: Fixture):
        setup.mock_league_client.get_tournament_schedule.assert_called_once()


class TestGetFilteredGames:
    @dataclass
    class Params:
        input_date: date
        expected_tournaments: List

    @dataclass
    class Fixture:
        expected_tournaments: List
        actual: List

    @pytest.fixture(
        ids=['No games', 'Has games'],
        params=[
            Params(
                input_date=date(2020, 6, 18),
                expected_tournaments=[]
            ),
            Params(
                input_date=date(2021, 6, 18),
                expected_tournaments=[{'end_date': '2021-06-20', 'event_type': 'stroke', 'id': '5', 'start_date': '2021-06-17', 'status': 'closed'},{'end_date': '2021-06-20', 'event_type': 'stroke', 'id': '3', 'start_date': '2021-06-17', 'status': 'inprogress'}]
            )
        ]
    )
    def setup(self, request):
        api_response = {
            'tournaments': [
                {
                    'id': '7',
                    'start_date': '2021-06-10',
                    'end_date': '2021-06-13',
                    'status': 'closed',
                    'event_type': 'stroke'
                },
                {
                    'id': '1',
                    'start_date': '2021-06-10',
                    'end_date': '2021-06-13',
                    'status': 'cancelled',
                    'event_type': 'stroke'
                },
                {
                    'id': '5',
                    'start_date': '2021-06-17',
                    'end_date': '2021-06-20',
                    'status': 'closed',
                    'event_type': 'stroke'
                },
                {
                    'id': '6',
                    'start_date': '2021-06-17',
                    'end_date': '2021-06-20',
                    'status': 'cancelled',
                    'event_type': 'stroke'
                },
                {
                    'id': '4',
                    'start_date': '2021-06-17',
                    'end_date': '2021-06-20',
                    'status': 'closed',
                    'event_type': 'match'
                },
                {
                    'id': '3',
                    'start_date': '2021-06-17',
                    'end_date': '2021-06-20',
                    'status': 'inprogress',
                    'event_type': 'stroke'
                },
                {
                    'id': '2',
                    'start_date': '2021-06-24',
                    'end_date': '2021-06-27',
                    'status': 'scheduled',
                    'event_type': 'stroke'
                },
                {
                    'id': '8',
                    'start_date': '2021-06-24',
                    'end_date': '2021-06-27',
                    'status': 'closed',
                    'event_type': 'stroke'
                }
            ]
        }
        return TestGetFilteredGames.Fixture(
            expected_tournaments=request.param.expected_tournaments,
            actual=GolfLeague.get_filtered_games(schedule=api_response, date=request.param.input_date)
        )

    def test_get_filtered_games_result(self, setup: Fixture):
        assert setup.actual == setup.expected_tournaments
