from dataclasses import dataclass
from typing import Optional
from unittest.mock import patch, Mock

import pytest

from src.models.BasketballPlayer import BasketballPlayer, basketball_player_from_dict
from src.models.NbaTeams import nba_team_map
from src.models.WnbaTeams import wnba_team_map


class TestBasketballPlayer:
    @dataclass
    class Params:
        input: dict
        expected: BasketballPlayer
        expected_is_decent_day: bool
        expected_tweet: str
        expected_team_map: dict
        college_map: Optional[dict]

    @dataclass
    class Fixture:
        actual: BasketballPlayer
        expected: BasketballPlayer
        expected_team_map: dict
        expected_is_decent_day: bool
        expected_tweet: str
        mock_get_team_text: Mock
        actual_tweet: str

    @pytest.fixture(
        ids=['Has Decent Stats', 'Not Decent WNBA', 'No College', 'None Stats', 'Missing Stats'],
        params=[
            Params(
                input={'full_name': 'Bo', 'id': '1', 'statistics': { 'points': 1, 'assists': 2, 'rebounds': 3}},
                expected=BasketballPlayer(
                    id='1',
                    full_name='Bo',
                    league_name='nba',
                    team_id='1',
                    college='someCollege',
                    points=1,
                    assists=2,
                    rebounds=3
                ),
                expected_is_decent_day=True,
                expected_tweet='Bo (#some team) 1 pts/3 reb/2 ast',
                college_map={'college': 'someCollege'},
                expected_team_map=nba_team_map
            ),
            Params(
                input={'full_name': 'Bo', 'id': '1', 'statistics': {'points': 0, 'assists': 0, 'rebounds': 0}},
                expected=BasketballPlayer(
                    id='1',
                    full_name='Bo',
                    league_name='wnba',
                    team_id='1',
                    college='someCollege',
                    points=0,
                    assists=0,
                    rebounds=0
                ),
                expected_is_decent_day=False,
                expected_tweet='Bo (#some team) ',
                college_map={'college': 'someCollege'},
                expected_team_map=wnba_team_map
            ),
            Params(
                input={'full_name': 'Bo', 'id': '1', 'statistics': {'points': 0, 'assists': 0, 'rebounds': 0}},
                expected=BasketballPlayer(
                    id='1',
                    full_name='Bo',
                    league_name='nba',
                    team_id='1',
                    college='',
                    points=0,
                    assists=0,
                    rebounds=0
                ),
                expected_is_decent_day=False,
                expected_tweet='Bo (#some team) ',
                college_map=None,
                expected_team_map=nba_team_map
            ),
            Params(
                input={'full_name': 'Bo', 'id': '1', 'statistics': {'points': None, 'assists': None, 'rebounds': None}},
                expected=BasketballPlayer(
                    id='1',
                    full_name='Bo',
                    league_name='nba',
                    team_id='1',
                    college='',
                    points=0,
                    assists=0,
                    rebounds=0
                ),
                expected_is_decent_day=False,
                expected_tweet='Bo (#some team) ',
                college_map=None,
                expected_team_map=nba_team_map
            ),
            Params(
                input={'full_name': 'Bo', 'id': '1'},
                expected=BasketballPlayer(
                    id='1',
                    full_name='Bo',
                    college='someCollege',
                    league_name='nba',
                    team_id='1',
                    points=0,
                    assists=0,
                    rebounds=0
                ),
                expected_is_decent_day=False,
                expected_tweet='Bo (#some team) ',
                college_map={'college': 'someCollege'},
                expected_team_map=nba_team_map
            )
        ]
    )
    @patch('src.models.BasketballPlayer.get_team_text', autospec=True)
    def setup(self, mock_get_team_text, request):
        mock_get_team_text.return_value = ' (#some team)'
        actual = basketball_player_from_dict(
            player=request.param.input,
            league_name=request.param.expected.league_name,
            team_id='1',
            college=request.param.college_map
        )
        return TestBasketballPlayer.Fixture(
            actual=actual,
            expected=request.param.expected,
            expected_is_decent_day=request.param.expected_is_decent_day,
            expected_tweet=request.param.expected_tweet,
            mock_get_team_text=mock_get_team_text,
            actual_tweet=actual.convert_to_tweet(),
            expected_team_map=request.param.expected_team_map
        )

    def test_object_correct(self, setup: Fixture):
        assert setup.actual == setup.expected

    def test_is_decent_day(self, setup: Fixture):
        assert setup.actual.has_stats() == setup.expected_is_decent_day

    def test_get_team_text_called(self, setup: Fixture):
        setup.mock_get_team_text.assert_called_once_with(team_map=setup.expected_team_map, team_id='1')

    def test_convert_to_tweet(self, setup: Fixture):
        assert setup.actual_tweet == setup.expected_tweet
