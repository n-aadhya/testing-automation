import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from generator.ai_test_gen import load_context, generate_tests


class TestLoadContext:
    def test_load_context_returns_dict(self):
        result = load_context()
        assert isinstance(result, dict)
    
    def test_load_context_contains_max3_protocol(self):
        result = load_context()
        assert 'MAX3_PROTOCOL' in result
    
    def test_load_context_max3_inputs(self):
        result = load_context()
        protocol = result.get('MAX3_PROTOCOL', {})
        inputs = protocol.get('inputs', {})
        assert 'a' in inputs
        assert 'b' in inputs
        assert 'c' in inputs
        assert inputs['a'] == 'integer'
        assert inputs['b'] == 'integer'
        assert inputs['c'] == 'integer'
    
    def test_load_context_max3_constraints(self):
        result = load_context()
        protocol = result.get('MAX3_PROTOCOL', {})
        constraints = protocol.get('constraints', [])
        assert len(constraints) == 3
        assert "values may be negative" in constraints
        assert "values may be equal" in constraints
        assert "system must return largest value" in constraints
    
    def test_load_context_max3_edge_cases(self):
        result = load_context()
        protocol = result.get('MAX3_PROTOCOL', {})
        edge_cases = protocol.get('edge_cases', [])
        assert len(edge_cases) == 3
        assert [0, 0, 0] in edge_cases
        assert [-1, -5, -10] in edge_cases
        assert [1000, 1000, 999] in edge_cases
    
    def test_load_context_handles_invalid_protocol(self):
        result = load_context()
        assert not isinstance(result, str)


class TestGenerateTests:
    def test_generate_tests_returns_list(self):
        context = load_context()
        result = generate_tests(context)
        assert isinstance(result, list)
    
    def test_generate_tests_includes_edge_cases(self):
        context = load_context()
        result = generate_tests(context)
        edge_case_tuples = [tuple(case) for case in context['MAX3_PROTOCOL']['edge_cases']]
        result_inputs = [tuple(test['input']) for test in result]
        for ec in edge_case_tuples:
            assert ec in result_inputs
    
    def test_generate_tests_structure(self):
        context = load_context()
        result = generate_tests(context)
        for test in result:
            assert 'input' in test
            assert 'expected' in test
            assert len(test['input']) == 3
    
    def test_generate_tests_all_positive_values(self):
        context = load_context()
        result = generate_tests(context)
        all_positive_tests = [t for t in result if all(v > 0 for v in t['input'])]
        assert len(all_positive_tests) > 0
    
    def test_generate_tests_negative_values(self):
        context = load_context()
        result = generate_tests(context)
        negative_tests = [t for t in result if all(v < 0 for v in t['input'])]
        assert len(negative_tests) > 0
    
    def test_generate_tests_equal_values(self):
        context = load_context()
        result = generate_tests(context)
        equal_tests = [t for t in result if t['input'][0] == t['input'][1] == t['input'][2]]
        assert len(equal_tests) > 0
    
    def test_generate_tests_mixed_values(self):
        context = load_context()
        result = generate_tests(context)
        mixed_tests = [t for t in result if len(set(t['input'])) == 3]
        assert len(mixed_tests) > 0
    
    def test_generate_tests_expected_max_value(self):
        context = load_context()
        result = generate_tests(context)
        for test in result:
            expected = test['expected']
            inputs = test['input']
            assert expected == max(inputs[0], inputs[1], inputs[2])
    
    def test_generate_tests_handles_empty_context(self):
        result = generate_tests({})
        assert isinstance(result, list)
    
    def test_generate_tests_duplicate_detection(self):
        context = load_context()
        result = generate_tests(context)
        seen_inputs = set()
        for test in result:
            input_tuple = tuple(test['input'])
            assert input_tuple not in seen_inputs, f"Duplicate input found: {input_tuple}"
            seen_inputs.add(input_tuple)