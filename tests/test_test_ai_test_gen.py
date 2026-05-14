import pytest

# Assuming the functions to be tested are defined in a module named `ai_test_gen`
# If the actual module name differs, adjust the import accordingly.
try:
    from ai_test_gen import load_context, generate_tests
except Exception as e:
    pytest.skip(f"Could not import ai_test_gen module: {e}", allow_module_level=True)

# Protocol context for reference
PROTOCOL_CTX = {
    "MAX3_PROTOCOL": {
        "inputs": {
            "a": "integer",
            "b": "integer",
            "c": "integer"
        },
        "constraints": [
            "values may be negative",
            "values may be equal",
            "system must return largest value"
        ],
        "edge_cases": [
            [0, 0, 0],
            [-1, -5, -10],
            [1000, 1000, 999]
        ]
    }
}


def test_load_context_returns_dict():
    """`load_context` should return a dictionary."""
    ctx = load_context()
    assert isinstance(ctx, dict), "Context should be a dictionary"


def test_load_context_contains_max3_protocol():
    """The context should contain the MAX3_PROTOCOL key."""
    ctx = load_context()
    assert "MAX3_PROTOCOL" in ctx, "Context missing MAX3_PROTOCOL key"


def test_load_context_max3_inputs():
    """Check that inputs for MAX3_PROTOCOL are correctly defined."""
    ctx = load_context()
    inputs = ctx["MAX3_PROTOCOL"]["inputs"]
    expected = {"a": "integer", "b": "integer", "c": "integer"}
    assert inputs == expected, f"Expected inputs {expected}, got {inputs}"


def test_load_context_max3_constraints():
    """Constraints for MAX3_PROTOCOL should be a list of strings."""
    ctx = load_context()
    constraints = ctx["MAX3_PROTOCOL"]["constraints"]
    assert isinstance(constraints, list), "Constraints should be a list"
    assert all(isinstance(c, str) for c in constraints), "All constraints should be strings"
    assert len(constraints) >= 3, "There should be at least three constraints"


def test_load_context_max3_edge_cases():
    """Edge cases should be a list of lists each containing three integers."""
    ctx = load_context()
    edge_cases = ctx["MAX3_PROTOCOL"]["edge_cases"]
    assert isinstance(edge_cases, list), "Edge cases should be a list"
    for case in edge_cases:
        assert isinstance(case, list) and len(case) == 3, "Each edge case should be a list of three values"
        assert all(isinstance(v, int) for v in case), "All edge case values should be integers"


def test_load_context_handles_invalid_protocol(monkeypatch):
    """Loading context should raise a KeyError when accessing a non-existent protocol."""
    ctx = load_context()
    with pytest.raises(KeyError):
        _ = ctx["NON_EXISTENT_PROTOCOL"]


def test_generate_tests_returns_list():
    """`generate_tests` should return a list of test cases."""
    ctx = load_context()
    tests = generate_tests(ctx["MAX3_PROTOCOL"])
    assert isinstance(tests, list), "generate_tests should return a list"


def test_generate_tests_includes_edge_cases():
    """Generated tests must include all edge cases."""
    ctx = load_context()
    edge_cases = ctx["MAX3_PROTOCOL"]["edge_cases"]
    tests = generate_tests(ctx["MAX3_PROTOCOL"])
    # Normalize to lists of inputs for comparison
    test_inputs = [t["inputs"] for t in tests]
    for ec in edge_cases:
        assert ec in test_inputs, f"Edge case {ec} missing from generated tests"


def test_generate_tests_structure():
    """Each test entry should be a dict with 'name', 'inputs', and 'expected' keys."""
    ctx = load_context()
    tests = generate_tests(ctx["MAX3_PROTOCOL"])
    for t in tests:
        assert isinstance(t, dict), "Each test case should be a dict"
        assert {"name", "inputs", "expected"} <= t.keys(), f"Missing keys in test case {t}"


def test_generate_tests_all_positive_values():
    """Include a test case where all inputs are positive integers."""
    ctx = load_context()
    pos_case = {"inputs": [5, 10, 3], "expected": 10}
    tests = generate_tests(ctx["MAX3_PROTOCOL"])
    assert any(t["inputs"] == pos_case["inputs"] and t["expected"] == pos_case["expected"]
               for t in tests), "Positive values test case missing"


def test_generate_tests_negative_values():
    """Include a test case where negative numbers are present."""
    ctx = load_context()
    neg_case = {"inputs": [-3, -2, -5], "expected": -2}
    tests = generate_tests(ctx["MAX3_PROTOCOL"])
    assert any(t["inputs"] == neg_case["inputs"] and t["expected"] == neg_case["expected"]
               for t in tests), "Negative values test case missing"


def test_generate_tests_equal_values():
    """Include a test case where all values are equal."""
    ctx = load_context()
    equal_case = {"inputs": [7, 7, 7], "expected": 7}
    tests = generate_tests(ctx["MAX3_PROTOCOL"])
    assert any(t["inputs"] == equal_case["inputs"] and t["expected"] == equal_case["expected"]
               for t in tests), "Equal values test case missing"


def test_generate_tests_mixed_values():
    """Include a test case with mixed positive, negative, and zero values."""
    ctx = load_context()
    mixed_case = {"inputs": [0, -1, 1], "expected": 1}
    tests = generate_tests(ctx["MAX3_PROTOCOL"])
    assert any(t["inputs"] == mixed_case["inputs"] and t["expected"] == mixed_case["expected"]
               for t in tests), "Mixed values test case missing"


def test_generate_tests_expected_max_value():
    """Verify that the expected result for each test matches the maximum of the inputs."""
    ctx = load_context()
    tests = generate_tests(ctx["MAX3_PROTOCOL"])
    for t in tests:
        inputs = t["inputs"]
        expected = max(inputs)
        assert t["expected"] == expected, f"For inputs {inputs}, expected {expected} but got {t['expected']}"


def test_generate_tests_handles_empty_context():
    """When provided an empty protocol dict, generate_tests should return an empty list."""
    empty_protocol = {}
    tests = generate_tests(empty_protocol)
    assert tests == [], "generate_tests should return an empty list for an empty protocol"


def test_generate_tests_duplicate_detection():
    """Generated tests should not contain duplicate input cases."""
    ctx = load_context()
    tests = generate_tests(ctx["MAX3_PROTOCOL"])
    seen = set()
    for t in tests:
        inputs_tup = tuple(t["inputs"])
        assert inputs_tup not in seen, f"Duplicate test case found: {t}"
        seen.add(inputs_tup)

# Four‑branch edge case checks (000, negative, large, mixed extremes)
@pytest.mark.parametrize("case,expected", [
    ([0, 0, 0], 0),
    ([-1, -5, -10], -1),
    ([1000, 1000, 999], 1000),
    ([42, -100, 42], 42)
])
def test_generate_tests_edge_branches(case, expected):
    """Test that generate_tests correctly identifies the maximum for key edge branches."""
    ctx = load_context()
    tests = generate_tests(ctx["MAX3_PROTOCOL"])
    matching = next((t for t in tests if t["inputs"] == case), None)
    assert matching is not None, f"Test case {case} not generated"
    assert matching["expected"] == expected, f"Expected {expected} for inputs {case}"