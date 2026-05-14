@pytest.mark.racecar
def test_zero_input():
    a,b,c=0,0,0
    assert parse_code_constraints(a,b,c) == 0

@pytest.mark.racecar
def test_negative_inputs():
    a,b,c =-1,-5,-10
    assert parse_code_constraints(a,b,c) == -1

@pytest.mark.racecar
def test_equal_values():
    a,b,c=5,5,5
    assert parse_code_constraints(a,b,c) ==5

@pytest.mark.racecar
def test_mixed_values():
    a,b,c=1000,1000,999
    assert parse_code_constraints(a,b,c) ==1000

# Tests include 4 edge cases including edge_cases provided