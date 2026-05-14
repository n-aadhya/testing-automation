import pytest

def test_all_zeros():
    """Test when all input values are zero."""
    from main import find_max
    result = find_max(0, 0, 0)
    assert result == 0

def test_all_negative_values():
    """Test when all input values are negative."""
    from main import find_max
    result = find_max(-1, -5, -10)
    assert result == -1

def test_two_equal_largest():
    """Test when two values are equal and are the largest."""
    from main import find_max
    result = find_max(1000, 1000, 999)
    assert result == 1000

def test_all_positive_distinct_values():
    """Test when all values are positive and distinct."""
    from main import find_max
    result = find_max(5, 10, 15)
    assert result == 15

def test_first_value_is_maximum():
    """Test when the first value is the maximum."""
    from main import find_max
    result = find_max(20, 10, 5)
    assert result == 20

def test_second_value_is_maximum():
    """Test when the second value is the maximum."""
    from main import find_max
    result = find_max(5, 20, 10)
    assert result == 20

def test_third_value_is_maximum():
    """Test when the third value is the maximum."""
    from main import find_max
    result = find_max(10, 5, 20)
    assert result == 20

def test_mixed_positive_and_negative():
    """Test with mixed positive and negative values."""
    from main import find_max
    result = find_max(-5, 10, -3)
    assert result == 10

def test_all_equal_values():
    """Test when all values are equal."""
    from main import find_max
    result = find_max(7, 7, 7)
    assert result == 7

def test_two_equal_less_than_third():
    """Test when two values are equal but less than the third."""
    from main import find_max
    result = find_max(5, 5, 10)
    assert result == 10

def test_large_positive_values():
    """Test with large positive values."""
    from main import find_max
    result = find_max(1000000, 2000000, 1500000)
    assert result == 2000000

def test_large_negative_values():
    """Test with large negative values."""
    from main import find_max
    result = find_max(-1000000, -500000, -2000000)
    assert result == -500000