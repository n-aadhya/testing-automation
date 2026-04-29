import os
import re
from tools.complexity import get_complexity
from tools.test_generator import generate_tests
from tools.test_runner import run_tests

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class BabyAGIAgent:

    def __init__(self, file_path):
        self.file_path = file_path

    # -------------------------------
    # MAIN BABYAGI LOOP
    # -------------------------------
    def execute_pipeline(self):
        print("Starting BabyAGI Loop...\n")

        result = self.analyze_code()
        ccn = result["ccn"]

        if ccn < 3:
            ccn = 3

        max_iterations = 5
        coverage_threshold = 80
        prev_coverage = 0

        for iteration in range(max_iterations):
            print(f"\n--- Iteration {iteration+1} ---")

            # Step 1: Generate tests
            generate_tests(self.file_path, ccn)

            # Step 2: Run tests
            test_result = run_tests(self.file_path)

            # Step 3: Evaluate test results
            status = self.evaluate(test_result)

            # Step 4: Extract coverage
            coverage = self.extract_coverage(test_result)
            print(f"Coverage: {coverage}%")

            # Step 5: Stop condition (success)
            if coverage >= coverage_threshold and status == "pass":
                print("✅ Sufficient coverage achieved. Stopping loop.")
                break

            # Step 6: Stop condition (stagnation)
            if iteration > 1 and abs(coverage - prev_coverage) < 3:
                print("⚠️ Coverage stagnating. Stopping.")
                break

            # Step 7: Adaptive scaling (VERY IMPORTANT)
            if coverage < 50:
                ccn += 5
            elif coverage < 80:
                ccn += 3
            else:
                ccn += 1

            print(f"⚠️ Improving test cases → New CCN: {ccn}")

            prev_coverage = coverage

        print("\nFinal Status:", status)

    # -------------------------------
    # COMPLEXITY ANALYSIS
    # -------------------------------
    def analyze_code(self):
        full_path = os.path.join(BASE_DIR, self.file_path)

        print(f"Analyzing: {full_path}")

        result = get_complexity(full_path)

        print(result["raw_output"])
        print(f"Extracted CCN: {result['ccn']}")

        return result

    # -------------------------------
    # COVERAGE EXTRACTION
    # -------------------------------
    def extract_coverage(self, output):
        # Python coverage format
        match_py = re.search(r'TOTAL.*?(\d+)%', output)

        # C++ lcov format
        match_cpp = re.search(r'lines\.*:\s*(\d+\.\d+)%', output)

        if match_py:
            return int(match_py.group(1))

        if match_cpp:
            return int(float(match_cpp.group(1)))

        return 0

    # -------------------------------
    # TEST RESULT EVALUATION
    # -------------------------------
    def evaluate(self, result):
        if "FAILED" in result or "ERROR" in result:
            return "fail"
        return "pass"
