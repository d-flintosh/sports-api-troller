from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

from src.models.BaseballPlayer import BaseballPlayer, baseball_player_from_dict
from src.models.MlbTeams import mlb_team_map


class TestBaseballPlayer:
    @dataclass
    class Params:
        input: dict
        expected: BaseballPlayer
        expected_has_stats: bool
        expected_had_a_great_day: bool
        expected_tweet: str

    @dataclass
    class Fixture:
        actual: BaseballPlayer
        expected: BaseballPlayer
        expected_has_stats: bool
        expected_had_a_great_day: bool
        expected_tweet: str
        mock_get_team_text: Mock
        actual_tweet: str

    @pytest.fixture(
        ids=['Missing Batting Stats', 'W/ stats No AtBats', 'W/pitching stats', 'W/ hittings stats'],
        params=[
            Params(
                input={
                    'id': '1',
                    'preferred_name': 'Bo',
                    'last_name': 'Jack',
                    'statistics': {
                        'hitting': {}
                    }
                },
                expected=BaseballPlayer(
                    id='1',
                    full_name='Bo Jack',
                    team_id='1',
                    college='someCollege',
                    hits=0,
                    at_bats=0,
                    home_runs=0,
                    rbis=0,
                    runs=0,
                    stolen_bases=0,
                    pitching_hits=0,
                    pitching_wins=0,
                    pitching_innings='',
                    pitching_losses=0,
                    pitching_saves=0,
                    pitching_strikeouts=0,
                    pitching_earned_runs=0
                ),
                expected_has_stats=False,
                expected_had_a_great_day=False,
                expected_tweet='Bo Jack (#some team) went 0-0'
            ),
            Params(
                input={
                    'id': '1',
                    'preferred_name': 'Bo',
                    'last_name': 'Jack',
                    'statistics': {
                        'hitting': {
                            'overall': {
                                'onbase': {
                                    'h': 0,
                                    'hr': 0
                                },
                                'ab': 0,
                            }
                        }
                    }
                },
                expected=BaseballPlayer(
                    id='1',
                    full_name='Bo Jack',
                    team_id='1',
                    hits=0,
                    college='someCollege',
                    at_bats=0,
                    home_runs=0,
                    rbis=0,
                    runs=0,
                    stolen_bases=0,
                    pitching_hits=0,
                    pitching_wins=0,
                    pitching_innings='',
                    pitching_losses=0,
                    pitching_saves=0,
                    pitching_strikeouts=0,
                    pitching_earned_runs=0
                ),
                expected_has_stats=False,
                expected_had_a_great_day=False,
                expected_tweet='Bo Jack (#some team) went 0-0'
            ),
            Params(
                input={
                    'id': '1',
                    'preferred_name': 'Bo',
                    'last_name': 'Jack',
                    'statistics': {
                        'hitting': {
                            'overall': {
                                'onbase': {
                                    'h': 1,
                                    'hr': 1
                                },
                                'ab': 4,
                            }
                        },
                        'pitching': {
                            'overall': {
                                'outs': {
                                    'ktotal': 2,
                                },
                                'ip_2': 1.2,
                                'onbase': {
                                    'h': 4,
                                },
                                'runs': {
                                    'earned': 3,
                                },
                                'games': {
                                    'loss': 1,
                                    'win': 0,
                                    'save': 0
                                }
                            }
                        }
                    }
                },
                expected=BaseballPlayer(
                    id='1',
                    full_name='Bo Jack',
                    team_id='1',
                    college='someCollege',
                    hits=1,
                    at_bats=4,
                    home_runs=1,
                    rbis=0,
                    runs=0,
                    stolen_bases=0,
                    pitching_hits=4,
                    pitching_wins=0,
                    pitching_innings='1.2',
                    pitching_losses=1,
                    pitching_saves=0,
                    pitching_strikeouts=2,
                    pitching_earned_runs=3
                ),
                expected_has_stats=True,
                expected_had_a_great_day=True,
                expected_tweet=f'Bo Jack (#some team) L 1.2IP 3ER 4H 2K'
            ),
            Params(
                input={
                    'id': '1',
                    'preferred_name': 'Bo',
                    'last_name': 'Jack',
                    'statistics': {
                        'hitting': {
                            'overall': {
                                'onbase': {
                                    'h': 1,
                                    'hr': 4
                                },
                                'steal': {
                                    'stolen': 1
                                },
                                'runs': {
                                    'total': 2
                                },
                                'ab': 4,
                                'rbi': 3
                            }
                        },
                        'pitching': {}
                    }
                },
                expected=BaseballPlayer(
                    id='1',
                    full_name='Bo Jack',
                    team_id='1',
                    college='someCollege',
                    hits=1,
                    at_bats=4,
                    home_runs=4,
                    rbis=3,
                    runs=2,
                    stolen_bases=1,
                    pitching_hits=0,
                    pitching_wins=0,
                    pitching_innings='',
                    pitching_losses=0,
                    pitching_saves=0,
                    pitching_strikeouts=0,
                    pitching_earned_runs=0
                ),
                expected_has_stats=True,
                expected_had_a_great_day=True,
                expected_tweet=f'Bo Jack (#some team) went 1-4 4HR 3RBI 2R 1SB'
            )
        ]
    )
    @patch('src.models.BaseballPlayer.get_team_text', autospec=True)
    def setup(self, mock_get_team_text, request):
        mock_get_team_text.return_value = ' (#some team)'
        actual = baseball_player_from_dict(
            player=request.param.input,
            team_id='1',
            college={'college': 'someCollege'}
        )

        return TestBaseballPlayer.Fixture(
            actual=actual,
            expected=request.param.expected,
            expected_has_stats=request.param.expected_has_stats,
            expected_tweet=request.param.expected_tweet,
            mock_get_team_text=mock_get_team_text,
            actual_tweet=actual.convert_to_tweet(),
            expected_had_a_great_day=request.param.expected_had_a_great_day
        )

    def test_object_correct(self, setup: Fixture):
        assert setup.actual == setup.expected

    def test_has_stats(self, setup: Fixture):
        assert setup.actual.has_stats() == setup.expected_has_stats

    def test_had_a_great_day(self, setup: Fixture):
        assert setup.actual.had_a_great_day() == setup.expected_had_a_great_day

    def test_get_team_text_called(self, setup: Fixture):
        setup.mock_get_team_text.assert_called_once_with(team_map=mlb_team_map, team_id='1')

    def test_convert_to_tweet(self, setup: Fixture):
        assert setup.actual_tweet == setup.expected_tweet
