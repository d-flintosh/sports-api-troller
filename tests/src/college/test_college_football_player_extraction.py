import pytest

from src.college.college_football_player_extraction import do_things


@pytest.mark.skip(reason="only run this manually")
def test_do_things():
    do_things()
