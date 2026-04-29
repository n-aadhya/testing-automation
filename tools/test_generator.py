import os
import random
from tools.language_detector import detect_language
from tools.ast_parser import extract_conditions, extract_cpp_conditions
from tools.input_synthesizer import generate_inputs_from_conditions

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# -------------------------------
# FALLBACK RANDOM INPUTS
# -------------------------------
def generate_random_inputs(n):
    inputs = []
    for _ in range(n):
        a = random.randint(-20, 20)
        b = random.randint(-20, 20)
        c = random.randint(-20, 20)
        inputs.append((a, b, c, max(a, b, c)))
    return inputs


# -------------------------------
# UNIFIED INPUT GENERATION
# -------------------------------
def get_test_inputs(file_path, ccn, language):
    full_path = os.path.join(BASE_DIR, file_path)

    # Step 1: extract conditions
    if language == "python":
        conditions = extract_conditions(full_path)
    else:
        conditions = extract_cpp_conditions(full_path)

    print("Extracted Conditions:", conditions)

    # Step 2: generate directed inputs
    inputs = generate_inputs_from_conditions(conditions, ccn)

    # Step 3: fallback random if needed
    if len(inputs) < ccn:
        inputs.extend(generate_random_inputs(ccn - len(inputs)))

    return inputs[:ccn]


# -------------------------------
# C++ TEST GENERATION
# -------------------------------
def generate_cpp_tests(file_path, ccn):
    file_name = os.path.basename(file_path)
    function_name = file_name.split('.')[0]

    output_path = os.path.join(BASE_DIR, "tests", "test_generated.cpp")

    test_code = f"""
#include <gtest/gtest.h>

int {function_name}(int, int, int);
"""

    test_inputs = get_test_inputs(file_path, ccn, "cpp")

    for i, (a, b, c, expected) in enumerate(test_inputs):
        test_code += f"""
TEST(AutoTest, Case{i+1}) {{
    EXPECT_EQ({function_name}({a}, {b}, {c}), {expected});
}}
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(test_code)

    print(f"Generated {ccn} C++ test cases")


# -------------------------------
# PYTHON TEST GENERATION
# -------------------------------
def generate_python_tests(file_path, ccn):
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    output_path = os.path.join(BASE_DIR, "tests", "test_generated.py")

    test_code = f"""
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import {module_name}
"""

    function_name = "max3"

    test_inputs = get_test_inputs(file_path, ccn, "python")

    for i, (a, b, c, expected) in enumerate(test_inputs):
        test_code += f"""
def test_case_{i+1}():
    assert {module_name}.{function_name}({a}, {b}, {c}) == {expected}
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(test_code)

    print(f"Generated {ccn} Python test cases")


# -------------------------------
# MAIN
# -------------------------------
def generate_tests(file_path, ccn):
    language = detect_language(file_path)

    if language == "cpp":
        generate_cpp_tests(file_path, ccn)

    elif language == "python":
        generate_python_tests(file_path, ccn)

    else:
        raise Exception("Unsupported language")
