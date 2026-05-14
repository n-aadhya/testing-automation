import subprocess
import time
import json

def run_adaptive_tests(test_files):
    metrics = {
        "tests_passed": False,
        "coverage": 0.0,
        "complexity": 0.0,
        "execution_time_sec": 0.0
    }
    
    start_time = time.time()
    
    # Run Pytest (for Python files)
    python_tests = [f for f in test_files if f.endswith('.py')]
    if python_tests:
        result = subprocess.run(
            ["coverage", "run", "-m", "pytest"] + python_tests,
            capture_output=True, text=True
        )
        metrics['tests_passed'] = (result.returncode == 0)
    
    # Calculate Multi-Language Complexity using LIZARD
    # Lizard natively supports Python, C++, Java, etc.
    complexity_result = subprocess.run(
        ["lizard", "src/", "--warnings_only", "-C", "10"], # Warns if complexity > 10
        capture_output=True, text=True
    )
    
    # If lizard output is empty, complexity is fine. If it has output, complexity is high.
    if complexity_result.stdout.strip():
        metrics['complexity'] = 15.0 # Fails the PR
    else:
        metrics['complexity'] = 5.0  # Passes the PR
        
    metrics['execution_time_sec'] = round(time.time() - start_time, 2)
    
    return metrics
