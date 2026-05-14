import pytest
from src.main_reviewer import main

@pytest.mark.parametrize(
    "a,b,c,expected",
    [
        # all equal
        (0, 0, 0, 0),
        # all negative
        (-1, -5, -10, -1),
        # duplicate maximum at a and b
        (1000, 1000, 999, 1000),
        # maximum is c
        (5, 2, 7, 7),
        # maximum is b
        (3, 9, 4, 9),
        # mix of negative and positive, max is b
        (-3, 3, 0, 3),
        # all equal large values
        (1500, 1500, 1500, 1500),
    ],
)
def test_main_returns_largest_value(a, b, c, expected):
    assert main(a, b, c) == expected