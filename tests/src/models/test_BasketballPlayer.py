from dataclasses import dataclass
from typing import Optional

import pytest

from src.models.BasketballPlayer import BasketballPlayer, basketball_player_from_dict


class TestBasketballPlayer:
    @dataclass
    class Params:
        input: dict
        expected: BasketballPlayer
        expected_is_decent_day: bool
        expected_tweet: str
        college_map: Optional[dict]

    @dataclass
    class Fixture:
        actual: BasketballPlayer
        expected: BasketballPlayer
        expected_is_decent_day: bool
        expected_tweet: str

    @pytest.fixture(
        ids=['Has Decent Stats', 'Not Decent', 'No College', 'None Stats', 'Missing Stats'],
        params=[
            Params(
                input={'PLAYER_NAME': 'Bo', 'PLAYER_ID': 1, 'PTS': 1, 'AST': 2, 'REB': 3},
                expected=BasketballPlayer(
                    id=1,
                    full_name='Bo',
                    college='someCollege',
                    points=1,
                    assists=2,
                    rebounds=3
                ),
                expected_is_decent_day=True,
                expected_tweet='Bo 1 pts/3 reb/2 ast',
                college_map={'college': 'someCollege'}
            ),
            Params(
                input={'PLAYER_NAME': 'Bo', 'PLAYER_ID': 1, 'PTS': 0, 'AST': 0, 'REB': 0},
                expected=BasketballPlayer(
                    id=1,
                    full_name='Bo',
                    college='someCollege',
                    points=0,
                    assists=0,
                    rebounds=0
                ),
                expected_is_decent_day=False,
                expected_tweet='Bo ',
                college_map={'college': 'someCollege'}
            ),
            Params(
                input={'PLAYER_NAME': 'Bo', 'PLAYER_ID': 1, 'PTS': 0, 'AST': 0, 'REB': 0},
                expected=BasketballPlayer(
                    id=1,
                    full_name='Bo',
                    college='',
                    points=0,
                    assists=0,
                    rebounds=0
                ),
                expected_is_decent_day=False,
                expected_tweet='Bo ',
                college_map=None
            ),
            Params(
                input={'PLAYER_NAME': 'Bo', 'PLAYER_ID': 1, 'PTS': None, 'AST': None, 'REB': None},
                expected=BasketballPlayer(
                    id=1,
                    full_name='Bo',
                    college='',
                    points=0,
                    assists=0,
                    rebounds=0
                ),
                expected_is_decent_day=False,
                expected_tweet='Bo ',
                college_map=None
            ),
            Params(
                input={'PLAYER_NAME': 'Bo', 'PLAYER_ID': 1},
                expected=BasketballPlayer(
                    id=1,
                    full_name='Bo',
                    college='someCollege',
                    points=0,
                    assists=0,
                    rebounds=0
                ),
                expected_is_decent_day=False,
                expected_tweet='Bo ',
                college_map={'college': 'someCollege'}
            )
        ]
    )
    def setup(self, request):
        return TestBasketballPlayer.Fixture(
            actual=basketball_player_from_dict(player=request.param.input, college=request.param.college_map),
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
