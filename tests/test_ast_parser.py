import pytest
from src.analyzer.ast_parser import parse_code_constraints


def test_all_values_equal_returns_same_value():
    """Branch: all three integers are equal."""
    result = parse_code_constraints({"a": 0, "b": 0, "c": 0})
    assert result == 0
def test_all_values_negative_returns_largest_negative():
    """Branch: all integers are negative and distinct."""
    result = parse_code_constraints({"a": -1, "b": -5, "c": -10})
    assert result == -1


def test_duplicate_max_value_returns_the_max():
    """Branch: multiple values are equal and represent the maximum."""
    result = parse_code_constraints({"a": 1000, "b": 1000, "c": 999})
    assert result == 1000


def test_mixed_sign_returns_positive_largest():
    """Branch: includes negative and positive integers; returns the largest positive."""
    result = parse_code_constraints({"a": -10, "b": 5, "c": 2})
    assert result == 5


def test_large_distinct_numbers_returns_highest():
    """Branch: distinct large integers, testing boundary of magnitude."""
    result = parse_code_constraints({"a": 2000, "b": 1500, "c": 1800})
    assert result == 2000