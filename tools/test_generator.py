import os
from tools.language_detector import detect_language

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# -------------------------------
# C++ TEST GENERATION (gtest)
# -------------------------------
def generate_cpp_tests(file_path, ccn):
    file_name = os.path.basename(file_path)
    function_name = file_name.split('.')[0]   # e.g., max3.cpp → max3

    output_path = os.path.join(BASE_DIR, "tests", "test_generated.cpp")

    test_code = f"""
#include <gtest/gtest.h>

// forward declaration (assumes function name = file name)
int {function_name}(int, int, int);
"""

    # basic input pool (can improve later)
    test_inputs = [
        (5,2,1,5),
        (1,6,2,6),
        (1,2,7,7),
        (5,5,5,5),
        (0,-1,-2,0),
        (-5,-2,-1,-1)
    ]

    for i in range(min(ccn, len(test_inputs))):
        a, b, c, expected = test_inputs[i]

        test_code += f"""
TEST(AutoTest, Case{i+1}) {{
    EXPECT_EQ({function_name}({a}, {b}, {c}), {expected});
}}
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(test_code)

    print(f"Generated {ccn} C++ test cases at {output_path}")


# -------------------------------
# PYTHON TEST GENERATION (pytest)
# -------------------------------
def generate_python_tests(file_path, ccn):
    import os

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    module_name = os.path.splitext(os.path.basename(file_path))[0]

    output_path = os.path.join(BASE_DIR, "tests", "test_generated.py")

    test_code = f"""
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import {module_name}
"""

    # assume function name = max3 (for now)
    function_name = "max3"

    test_inputs = [
        (5,2,1,5),
        (1,6,2,6),
        (1,2,7,7),
        (5,5,5,5),
        (0,-1,-2,0),
        (-5,-2,-1,-1)
    ]

    for i in range(min(ccn, len(test_inputs))):
        a, b, c, expected = test_inputs[i]

        test_code += f"""
def test_case_{i+1}():
    assert {module_name}.{function_name}({a}, {b}, {c}) == {expected}
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(test_code)

    print(f"Generated {ccn} Python test cases at {output_path}")


# -------------------------------
# MAIN ENTRY (IMPORTANT)
# -------------------------------
def generate_tests(file_path, ccn):
    language = detect_language(file_path)

    if language == "cpp":
        generate_cpp_tests(file_path, ccn)

    elif language == "python":
        generate_python_tests(file_path, ccn)

    else:
        raise Exception("Unsupported language")
