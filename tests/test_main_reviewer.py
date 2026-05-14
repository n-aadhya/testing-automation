import pytest
from src.main_reviewer import main


class TestMainMax3:
    """Test suite for main function following MAX3_PROTOCOL."""

    def test_all_zeros(self):
        """Test edge case where all values are zero."""
        result = main(0, 0, 0)
        assert result == 0

    def test_all_negative_values(self):
        """Test with all negative values."""
        result = main(-1, -5, -10)
        assert result == -1

    def test_two_equal_largest(self):
        """Test when two values are equal and largest."""
        result = main(1000, 1000, 999)
        assert result == 1000

    def test_all_positive_distinct_values(self):
        """Test with all positive distinct values."""
        result = main(1, 5, 3)
        assert result == 5

    def test_first_value_is_maximum(self):
        """Test when first value is the maximum."""
        result = main(100, 50, 75)
        assert result == 100

    def test_second_value_is_maximum(self):
        """Test when second value is the maximum."""
        result = main(10, 100, 50)
        assert result == 100

    def test_third_value_is_maximum(self):
        """Test when third value is the maximum."""
        result = main(10, 20, 100)
        assert result == 100

    def test_mixed_positive_and_negative(self):
        """Test with mix of positive and negative values."""
        result = main(-10, 5, -3)
        assert result == 5

    def test_all_equal_values(self):
        """Test when all three values are equal."""
        result = main(42, 42, 42)
        assert result == 42

    def test_two_equal_less_than_third(self):
        """Test when two values are equal but less than third."""
        result = main(5, 5, 10)
        assert result == 10

    def test_large_positive_values(self):
        """Test with large positive values."""
        result = main(1000000, 2000000, 1500000)
        assert result == 2000000

    def test_large_negative_values(self):
        """Test with large negative values."""
        result = main(-1000, -2000, -1500)
        assert result == -1000