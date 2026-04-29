
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import sample

def test_case_1():
    assert sample.max3(10, 5, 1) == 10

def test_case_2():
    assert sample.max3(1, 10, 5) == 10

def test_case_3():
    assert sample.max3(1, 5, 10) == 10
