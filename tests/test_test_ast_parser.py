import pytest

def test_zero_input():
    assert parse_expression("0") == "0"

def test_negative_inputs():
    assert parse_expression("-3") == "-3"
    assert parse_expression("-5") == "-5"
    assert parse_expression("-10") == "-10"

def test_equal_values():
    assert parse_expression("3") == "3"
    assert parse_expression("5") == "5"

def test_mixed_values():
    assert parse_expression("2, 8, 7") == "7"

def test_edge_cases():
    assert parse_expression("0, 0, 0") == "0"
    assert parse_expression("-1, -5, -10") == "-5"
    assert parse_expression("1000, 1000, 999") == "999"