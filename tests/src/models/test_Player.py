from dataclasses import dataclass

import pytest

from src.models.Player import Player


@dataclass
class FakePlayer(Player):
    name: str
    points: int

    def has_stats(self) -> bool:
        pass

    def had_a_great_day(self) -> bool:
        pass

    def convert_to_tweet(self) -> str:
        pass

    def get_college(self) -> str:
        pass

    def get_league_name(self) -> str:
        pass

    def get_player_id(self) -> str:
        pass


class TestPlayer:
    @dataclass
    class Fixture:
        subject: FakePlayer

    @pytest.fixture
    def setup(self):
        subject = FakePlayer(name='Bo', points=2)
        return TestPlayer.Fixture(
            subject=subject
        )

    def test_get_all_players_called(self, setup: Fixture):
        assert setup.subject.convert_dataclass_to_json() == '{"name": "Bo", "points": 2}'
