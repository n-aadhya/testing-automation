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
    
    # 1. Run Tests and measure Coverage
    # Using pytest and coverage module
    result = subprocess.run(
        ["coverage", "run", "-m", "pytest"] + test_files,
        capture_output=True, text=True
    )
    
    metrics['tests_passed'] = (result.returncode == 0)
    
    # 2. Extract Coverage Percentage
    subprocess.run(["coverage", "json", "-o", "coverage.json"])
    try:
        with open("coverage.json", "r") as f:
            cov_data = json.load(f)
            metrics['coverage'] = cov_data["totals"]["percent_covered"]
    except FileNotFoundError:
        metrics['coverage'] = 0.0

    # 3. Calculate Cyclomatic Complexity (Safety Criteria)
    complexity_result = subprocess.run(
        ["radon", "cc", "src/", "-s", "-a", "-j"],
        capture_output=True, text=True
    )
    try:
        comp_data = json.loads(complexity_result.stdout)
        # Average complexity calculation logic...
        metrics['complexity'] = 5.2 # (Example parsed average)
    except Exception:
        metrics['complexity'] = 0.0
        
    metrics['execution_time_sec'] = round(time.time() - start_time, 2)
    
    # Save results similarly to your existing outputs.txt / results.txt
    with open("results.txt", "w") as f:
        f.write(json.dumps(metrics, indent=4))
        
    return metrics
