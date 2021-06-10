from dataclasses import dataclass

import pytest

from src.models.BaseballPlayer import BaseballPlayer, baseball_player_from_dict


class TestBaseballPlayer:
    @dataclass
    class Params:
        input: dict
        expected: BaseballPlayer
        expected_is_decent_day: bool

    @dataclass
    class Fixture:
        actual: BaseballPlayer
        expected: BaseballPlayer
        expected_is_decent_day: bool

    @pytest.fixture(
        ids=['Missing Batting Stats', 'W/ stats bad day', 'Decent Day'],
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
                expected=BaseballPlayer(
                    id=1,
                    full_name='Bo',
                    hits=0,
                    at_bats=0,
                    home_runs=0
                ),
                expected_is_decent_day=False
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
                expected=BaseballPlayer(
                    id=1,
                    full_name='Bo',
                    hits=0,
                    at_bats=4,
                    home_runs=0
                ),
                expected_is_decent_day=False
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
                expected=BaseballPlayer(
                    id=1,
                    full_name='Bo',
                    hits=1,
                    at_bats=4,
                    home_runs=1
                ),
                expected_is_decent_day=True
            )
        ]
    )
    def setup(self, request):
        return TestBaseballPlayer.Fixture(
            actual=baseball_player_from_dict(request.param.input),
            expected=request.param.expected,
            expected_is_decent_day=request.param.expected_is_decent_day
        )

    def test_object_correct(self, setup: Fixture):
        assert setup.actual == setup.expected

    def test_is_decent_day(self, setup: Fixture):
        assert setup.actual.is_decent_day() == setup.expected_is_decent_day