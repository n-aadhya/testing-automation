import pytest
from app.calculator import multiply


class TestMultiply:
    """Test cases for multiply function covering various scenarios."""

    def test_multiply_positive_numbers(self):
        """Test multiplication of positive integers."""
        assert multiply(5, 3) == 15
        assert multiply(10, 7) == 70

    def test_multiply_negative_numbers(self):
        """Test multiplication of negative integers."""
        assert multiply(-5, 3) == -15
        assert multiply(-5, -3) == 15
        assert multiply(5, -3) == -15

    def test_multiply_with_zero(self):
        """Test multiplication involving zero."""
        assert multiply(0, 5) == 0
        assert multiply(5, 0) == 0
        assert multiply(0, 0) == 0

    def test_multiply_equal_values(self):
        """Test multiplication with equal values."""
        assert multiply(7, 7) == 49
        assert multiply(-4, -4) == 16
        assert multiply(0, 0) == 0

    def test_multiply_edge_case_all_zeros(self):
        """Test multiplication based on [0, 0, 0] edge case."""
        assert multiply(0, 0) == 0
        assert multiply(0, 0) == 0

    def test_multiply_edge_case_negative_values(self):
        """Test multiplication based on [-1, -5, -10] edge case."""
        assert multiply(-1, -5) == 5
        assert multiply(-1, -10) == 10
        assert multiply(-5, -10) == 50

    def test_multiply_edge_case_large_equal_values(self):
        """Test multiplication based on [1000, 1000, 999] edge case."""
        assert multiply(1000, 1000) == 1000000
        assert multiply(1000, 999) == 999000

    def test_multiply_large_numbers(self):
        """Test multiplication of large integers."""
        assert multiply(1000000, 1000000) == 1000000000000

    def test_multiply_identity(self):
        """Test multiplication by one (identity property)."""
        assert multiply(5, 1) == 5
        assert multiply(1, 5) == 5
        assert multiply(1, 1) == 1
        assert multiply(-1, 1) == -1

    def test_multiply_commutative_property(self):
        """Test that multiplication is commutative."""
        assert multiply(6, 7) == multiply(7, 6)
        assert multiply(-3, 8) == multiply(8, -3)

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 6),
        (-2, 3, -6),
        (2, -3, -6),
        (-2, -3, 6),
        (0, 100, 0),
        (100, 0, 0),
    ])
    def test_multiply_parametrized(self, a, b, expected):
        """Parametrized test for various multiplication scenarios."""
        assert multiply(a, b) == expected