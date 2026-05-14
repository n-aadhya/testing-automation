import subprocess
import time
import json
import psutil
import os

def run_adaptive_tests(test_files):
    metrics = {
        "tests_passed": False,
        "coverage": 0.0,
        "complexity": 0.0,
        "cpu_utilization": 0.0,
        "semgrep_passed": False,
        "execution_time_sec": 0.0,
        "rma_safe": True
    }
    
    # ---------------------------------------------------------
    # 1. SEMGREP STATIC SECURITY ANALYSIS
    # ---------------------------------------------------------
    print("Running Semgrep Security Scan...")
    # Scans the 'app' directory using standard CI security rules
    semgrep_result = subprocess.run(
        ["semgrep", "scan", "--config=auto", "--json", "app/"],
        capture_output=True, text=True
    )
    
    # If semgrep finds errors, returncode is non-zero
    metrics['semgrep_passed'] = (semgrep_result.returncode == 0)

    # ---------------------------------------------------------
    # 2. RUN TESTS & MEASURE CPU/RMA
    # ---------------------------------------------------------
    start_time = time.time()
    
    # Run Pytest (for Python files)
    python_tests = [f for f in test_files if f.endswith('.py')]
    if python_tests:
        # Run pytest and capture it to measure CPU
        process = subprocess.Popen(
            ["coverage", "run", "-m", "pytest"] + python_tests,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        # Monitor CPU Utilization of the testing process
        p_cpu = psutil.Process(process.pid)
        cpu_percentages = []
        
        while process.poll() is None:
            try:
                # Get CPU % of the process (divided by core count for accurate overall usage)
                cpu_percentages.append(p_cpu.cpu_percent(interval=0.1) / psutil.cpu_count())
            except psutil.NoSuchProcess:
                break
                
        metrics['tests_passed'] = (process.returncode == 0)
        
        # Calculate average CPU Utilization during the test
        if cpu_percentages:
            metrics['cpu_utilization'] = sum(cpu_percentages) / len(cpu_percentages)

    # ---------------------------------------------------------
    # 3. RATE MONOTONIC ANALYSIS (RMA) EVALUATION
    # ---------------------------------------------------------
    # RMA Bound for infinite tasks is mathematically ln(2) = ~0.693 (69.3%)
    # If CPU utilization exceeds 69.3%, the real-time system is mathematically unsafe!
    RMA_THRESHOLD = 69.3  
    
    if metrics['cpu_utilization'] > RMA_THRESHOLD:
        metrics['rma_safe'] = False
    else:
        metrics['rma_safe'] = True

    # ---------------------------------------------------------
    # 4. COVERAGE & COMPLEXITY (Lizard)
    # ---------------------------------------------------------
    # Get coverage percentage
    subprocess.run(["coverage", "json", "-o", "coverage.json"])
    try:
        with open("coverage.json", "r") as f:
            cov_data = json.load(f)
            metrics['coverage'] = cov_data["totals"]["percent_covered"]
    except FileNotFoundError:
        pass

    # Lizard Multi-language Complexity
    complexity_result = subprocess.run(
        ["lizard", "app/", "--warnings_only", "-C", "10"], 
        capture_output=True, text=True
    )
    metrics['complexity'] = 15.0 if complexity_result.stdout.strip() else 5.0

    metrics['execution_time_sec'] = round(time.time() - start_time, 2)
    
    return metrics
