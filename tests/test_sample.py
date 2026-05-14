import pytest
from app.sample import max3

class TestMax3Protocol:
    def test_all_equal_values(self):
        assert max3(0, 0, 0) == 0
        assert max3(-5, -5, -5) == -5
        assert max3(10, 10, 10) == 10

    def test_two_equal_one_different(self):
        assert max3(1000, 1000, 999) == 1000
        assert max3(5, 5, 10) == 10
        assert max3(-1, -1, -5) == -1

    def test_all_different_values(self):
        assert max3(-1, -5, -10) == -1
        assert max3(1, 2, 3) == 3
        assert max3(-10, 0, 5) == 5

    def test_mixed_signs(self):
        assert max3(-5, 0, 5) == 5
        assert max3(-100, -200, 100) == 100
        assert max3(-1, 1, 0) == 1

    def test_large_numbers(self):
        assert max3(2147483647, 2147483646, 2147483645) == 2147483647
        assert max3(-2147483648, -2147483647, -2147483646) == -2147483646

    def test_edge_cases_from_protocol(self):
        assert max3(0, 0, 0) == 0
        assert max3(-1, -5, -10) == -1
        assert max3(1000, 1000, 999) == 1000