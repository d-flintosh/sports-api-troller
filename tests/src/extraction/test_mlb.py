import pytest

from src.extraction.mlb import get_stuff


@pytest.mark.skip(reason="only run this manually")
def test_foo():
    get_stuff(start_date='2000-04-10', end_date='2021-06-13')
