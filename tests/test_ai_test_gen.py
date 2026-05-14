import json
import pathlib
import builtins
import types
import pytest
from src.generator.ai_test_gen import load_context, generate_tests

# Helper to create a temporary context file
@pytest.fixture
def temp_context_file(tmp_path):
    context = {
        "MAX3_PROTOCOL": {
            "inputs": {"a": "integer", "b": "integer", "c": "integer"},
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
    file_path = tmp_path / "context.json"
    file_path.write_text(json.dumps(context))
    return file_path

def test_load_context_returns_correct_structure(temp_context_file):
    # Load the context from the temporary file
    loaded = load_context(str(temp_context_file))
    # Ensure the top‑level key exists
    assert "MAX3_PROTOCOL" in loaded
    proto = loaded["MAX3_PROTOCOL"]
    # Verify inputs definition
    assert proto["inputs"] == {"a": "integer", "b": "integer", "c": "integer"}
    # Verify constraints list
    assert set(proto["constraints"]) == {
        "values may be negative",
        "values may be equal",
        "system must return largest value",
    }
    # Verify edge cases list length and content
    assert isinstance(proto["edge_cases"], list)
    assert proto["edge_cases"] == [
        [0, 0, 0],
        [-1, -5, -10],
        [1000, 1000, 999],
    ]

def test_generate_tests_creates_expected_number_of_cases(temp_context_file):
    # Generate tests for the protocol
    test_cases = generate_tests(str(temp_context_file), "MAX3_PROTOCOL")
    # We expect at least the three edge cases plus additional cases for constraints
    # The requirement mentions 6 branches, so enforce a minimum of 6 distinct cases
    assert isinstance(test_cases, list)
    assert len(test_cases) >= 6

    # Ensure each generated case contains the required keys
    for case in test_cases:
        assert "inputs" in case
        assert "expected" in case
        assert isinstance(case["inputs"], dict)

def test_generate_tests_covers_edge_cases(temp_context_file):
    test_cases = generate_tests(str(temp_context_file), "MAX3_PROTOCOL")
    edge_cases = [
        (0, 0, 0),
        (-1, -5, -10),
        (1000, 1000, 999),
    ]
    # Helper to normalise a case to a tuple for comparison
    def inputs_to_tuple(case):
        inp = case["inputs"]
        return (inp["a"], inp["b"], inp["c"])

    generated = {inputs_to_tuple(c) for c in test_cases}
    for ec in edge_cases:
        assert ec in generated, f"Edge case {ec} not generated"

def test_generate_tests_respects_constraints_negative_values(temp_context_file):
    test_cases = generate_tests(str(temp_context_file), "MAX3_PROTOCOL")
    # There must be at least one case where at least one value is negative
    has_negative = any(
        any(v < 0 for v in case["inputs"].values())
        for case in test_cases
    )
    assert has_negative, "No test case with negative values generated"

def test_generate_tests_respects_constraints_equal_values(temp_context_file):
    test_cases = generate_tests(str(temp_context_file), "MAX3_PROTOCOL")
    # There must be at least one case where two or more inputs are equal
    has_equal = any(
        len({case["inputs"]["a"], case["inputs"]["b"], case["inputs"]["c"]}) < 3
        for case in test_cases
    )
    assert has_equal, "No test case with equal input values generated"

def test_generate_tests_expected_is_largest_value(temp_context_file):
    test_cases = generate_tests(str(temp_context_file), "MAX3_PROTOCOL")
    for case in test_cases:
        inputs = case["inputs"]
        expected = case["expected"]
        # The generator should set expected to the max of the inputs
        assert expected == max(inputs["a"], inputs["b"], inputs["c"]), (
            f"Expected {expected} does not match max of inputs {inputs}"
        )