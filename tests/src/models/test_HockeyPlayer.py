from dataclasses import dataclass
from typing import Optional
from unittest.mock import patch, Mock

import pytest

from src.models.HockeyPlayer import HockeyPlayer, hockey_player_from_dict
from src.models.NhlTeams import nhl_team_map


class TestHockeyPlayer:
    @dataclass
    class Params:
        input: dict
        expected: HockeyPlayer
        expected_has_stats: bool
        expected_had_great_day: bool
        expected_tweet: str
        expected_team_map: dict
        college_map: Optional[dict]

    @dataclass
    class Fixture:
        actual: HockeyPlayer
        expected: HockeyPlayer
        expected_team_map: dict
        expected_has_stats: bool
        expected_had_great_day: bool
        expected_tweet: str
        mock_get_team_text: Mock
        actual_tweet: str

    @pytest.fixture(
        ids=['Has Decent Stats', 'Not Decent', 'No College', 'None Stats', 'Missing Stats'],
        params=[
            Params(
                input={'full_name': 'Bo', 'id': '1', 'statistics': {'total': { 'goals': 1, 'assists': 2}}},
                expected=HockeyPlayer(
                    id='1',
                    full_name='Bo',
                    league_name='nhl',
                    team_id='1',
                    college='someCollege',
                    goals=1,
                    assists=2,
                ),
                expected_has_stats=True,
                expected_had_great_day=True,
                expected_tweet='Bo (#some team) 1 g/2 ast',
                college_map={'college': 'someCollege'},
                expected_team_map=nhl_team_map
            ),
            Params(
                input={'full_name': 'Bo', 'id': '1', 'statistics': {'total': {'goals': 0, 'assists': 0}}},
                expected=HockeyPlayer(
                    id='1',
                    full_name='Bo',
                    league_name='wnhl',
                    team_id='1',
                    college='someCollege',
                    goals=0,
                    assists=0,
                ),
                expected_has_stats=False,
                expected_had_great_day=False,
                expected_tweet='Bo (#some team) ',
                college_map={'college': 'someCollege'},
                expected_team_map=nhl_team_map
            ),
            Params(
                input={'full_name': 'Bo', 'id': '1', 'statistics': {'total': {'goals': 0, 'assists': 0}}},
                expected=HockeyPlayer(
                    id='1',
                    full_name='Bo',
                    league_name='nhl',
                    team_id='1',
                    college='',
                    goals=0,
                    assists=0
                ),
                expected_has_stats=False,
                expected_had_great_day=False,
                expected_tweet='Bo (#some team) ',
                college_map=None,
                expected_team_map=nhl_team_map
            ),
            Params(
                input={'full_name': 'Bo', 'id': '1', 'statistics': {'total': {'goals': None, 'assists': None}}},
                expected=HockeyPlayer(
                    id='1',
                    full_name='Bo',
                    league_name='nhl',
                    team_id='1',
                    college='',
                    goals=0,
                    assists=0
                ),
                expected_has_stats=False,
                expected_had_great_day=False,
                expected_tweet='Bo (#some team) ',
                college_map=None,
                expected_team_map=nhl_team_map
            ),
            Params(
                input={'full_name': 'Bo', 'id': '1'},
                expected=HockeyPlayer(
                    id='1',
                    full_name='Bo',
                    college='someCollege',
                    league_name='nhl',
                    team_id='1',
                    assists=0,
                    goals=0
                ),
                expected_has_stats=False,
                expected_had_great_day=False,
                expected_tweet='Bo (#some team) ',
                college_map={'college': 'someCollege'},
                expected_team_map=nhl_team_map
            )
        ]
    )
    @patch('src.models.HockeyPlayer.get_team_text', autospec=True)
    def setup(self, mock_get_team_text, request):
        mock_get_team_text.return_value = ' (#some team)'
        actual = hockey_player_from_dict(
            player=request.param.input,
            league_name=request.param.expected.league_name,
            team_id='1',
            college=request.param.college_map
        )
        return TestHockeyPlayer.Fixture(
            actual=actual,
            expected=request.param.expected,
            expected_has_stats=request.param.expected_has_stats,
            expected_tweet=request.param.expected_tweet,
            mock_get_team_text=mock_get_team_text,
            actual_tweet=actual.convert_to_tweet(),
            expected_team_map=request.param.expected_team_map,
            expected_had_great_day=request.param.expected_had_great_day
        )

    def test_object_correct(self, setup: Fixture):
        assert setup.actual == setup.expected

    def test_has_stats(self, setup: Fixture):
        assert setup.actual.has_stats() == setup.expected_has_stats

    def test_had_a_great_day(self, setup: Fixture):
        assert setup.actual.had_a_great_day() == setup.expected_had_great_day

    def test_get_team_text_called(self, setup: Fixture):
        setup.mock_get_team_text.assert_called_once_with(team_map=setup.expected_team_map, team_id='1')

    def test_convert_to_tweet(self, setup: Fixture):
        assert setup.actual_tweet == setup.expected_tweet
