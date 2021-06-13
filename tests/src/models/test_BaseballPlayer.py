from dataclasses import dataclass

import pytest

from src.models.BaseballPlayer import BaseballPlayer, baseball_player_from_dict
from src.models.Emojis import Emojis


class TestBaseballPlayer:
    @dataclass
    class Params:
        input: dict
        team_id: int
        expected: BaseballPlayer
        expected_is_decent_day: bool
        expected_tweet: str

    @dataclass
    class Fixture:
        actual: BaseballPlayer
        expected: BaseballPlayer
        expected_is_decent_day: bool
        expected_tweet: str

    @pytest.fixture(
        ids=['Missing Batting Stats', 'W/ stats bad day', 'Decent Day and team lookup'],
        params=[
            Params(
                input={
                    'person': {
                        'id': 1,
                        'fullName': 'Bo'
                    },
                    'stats': {
                        'batting': {}
                    }
                },
                team_id=1,
                expected=BaseballPlayer(
                    id=1,
                    full_name='Bo',
                    team_id=1,
                    college='someCollege',
                    hits=0,
                    at_bats=0,
                    home_runs=0
                ),
                expected_is_decent_day=False,
                expected_tweet='Bo went 0-0'
            ),
            Params(
                input={
                    'person': {
                        'id': 1,
                        'fullName': 'Bo'
                    },
                    'stats': {
                        'batting': {
                            'hits': 0,
                            'atBats': 4,
                            'homeRuns': 0
                        }
                    }
                },
                team_id=1,
                expected=BaseballPlayer(
                    id=1,
                    full_name='Bo',
                    team_id=1,
                    hits=0,
                    college='someCollege',
                    at_bats=4,
                    home_runs=0
                ),
                expected_is_decent_day=False,
                expected_tweet='Bo went 0-4'
            ),
            Params(
                input={
                    'person': {
                        'id': 1,
                        'fullName': 'Bo'
                    },
                    'stats': {
                        'batting': {
                            'hits': 1,
                            'atBats': 4,
                            'homeRuns': 1
                        }
                    }
                },
                team_id=135,
                expected=BaseballPlayer(
                    id=1,
                    full_name='Bo',
                    team_id=135,
                    college='someCollege',
                    hits=1,
                    at_bats=4,
                    home_runs=1
                ),
                expected_is_decent_day=True,
                expected_tweet=f'Bo (#HungryForMore) went 1-4 1 {Emojis.TATER.value}'
            )
        ]
    )
    def setup(self, request):
        return TestBaseballPlayer.Fixture(
            actual=baseball_player_from_dict(
                player=request.param.input,
                team_id=request.param.team_id,
                college={'college': 'someCollege'}
            ),
            expected=request.param.expected,
            expected_is_decent_day=request.param.expected_is_decent_day,
            expected_tweet=request.param.expected_tweet
        )

    def test_object_correct(self, setup: Fixture):
        assert setup.actual == setup.expected

    def test_is_decent_day(self, setup: Fixture):
        assert setup.actual.is_decent_day() == setup.expected_is_decent_day

    def test_convert_to_tweet(self, setup: Fixture):
        assert setup.actual.convert_to_tweet() == setup.expected_tweet
