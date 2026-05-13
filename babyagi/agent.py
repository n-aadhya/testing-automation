import os
import re
from tools.complexity import get_complexity
from tools.test_generator import generate_tests
from tools.test_runner import run_tests
from tools.performance_monitor import PerformanceMonitor
from tools.rtm_manager import (
    get_requirements_for_file,
    update_rtm
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class BabyAGIAgent:

    def __init__(self, file_path):
        self.file_path = file_path

    def execute_pipeline(self):
        print("Starting BabyAGI Loop...\n")

        monitor = PerformanceMonitor()

        result = self.analyze_code()
        ccn = result["ccn"]

        if ccn < 3:
            ccn = 3

        max_iterations = 5
        coverage_threshold = 80
        prev_coverage = 0

        performance_log = []

        for iteration in range(max_iterations):
            print(f"\n--- Iteration {iteration+1} ---")

            generate_tests(self.file_path, ccn)
            test_result = run_tests(self.file_path)

            status = self.evaluate(test_result)
            coverage = self.extract_coverage(test_result)

            metrics = monitor.get_metrics()

            print(f"Coverage: {coverage}%")
            print(f"CPU: {metrics['cpu']}% | RAM: {metrics['memory']}% | Time: {metrics['time']}s")

            performance_log.append({
                "iteration": iteration + 1,
                "coverage": coverage,
                "cpu": metrics["cpu"],
                "memory": metrics["memory"],
                "time": metrics["time"]
            })

            if coverage >= coverage_threshold and status == "pass":
                print("Sufficient coverage achieved.")
                break

            if iteration > 1 and abs(coverage - prev_coverage) < 3:
                print("Coverage stagnating.")
                break

            if coverage < 50:
                ccn += 5
            elif coverage < 80:
                ccn += 3
            else:
                ccn += 1

            prev_coverage = coverage

        self.save_performance(performance_log)

        print("\nFinal Status:", status)

    def analyze_code(self):
        full_path = os.path.join(BASE_DIR, self.file_path)

        print(f"Analyzing: {full_path}")

        result = get_complexity(full_path)

        print(result["raw_output"])
        print(f"Extracted CCN: {result['ccn']}")

        return result

    def extract_coverage(self, output):
        match_py = re.search(r'TOTAL.*?(\d+)%', output)
        match_cpp = re.search(r'branches\.*:\s*(\d+\.\d+)%', output)

        if not match_cpp:
            match_cpp = re.search(r'lines\.*:\s*(\d+\.\d+)%', output)    

        if match_py:
            return int(match_py.group(1))

        if match_cpp:
            return int(float(match_cpp.group(1)))

        return 0

    def evaluate(self, result):
        if "FAILED" in result or "ERROR" in result:
            return "fail"
        return "pass"

    def save_performance(self, log):
        file_path = os.path.join(BASE_DIR, "results.txt")

        with open(file_path, "w") as f:
            f.write("Iteration | Coverage | CPU% | RAM% | Time(s)\n")
            f.write("------------------------------------------------\n")

            for entry in log:
                f.write(
                    f"{entry['iteration']} | "
                    f"{entry['coverage']}% | "
                    f"{entry['cpu']}% | "
                    f"{entry['memory']}% | "
                    f"{entry['time']}s\n"
                )

        print(f"\nPerformance report saved to {file_path}")
