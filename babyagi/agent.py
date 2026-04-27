import os
from tools.complexity import get_complexity
from tools.test_generator import generate_tests
from tools.test_runner import run_tests

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class BabyAGIAgent:

    def __init__(self, file_path):
        self.file_path = file_path

    def execute_pipeline(self):
        result = self.analyze_code()

        ccn = result["ccn"]

        # enforce minimum tests
        if ccn < 3:
            ccn = 3

        # Generate tests dynamically
        generate_tests(self.file_path, ccn)

        # Run tests
        test_result = run_tests(self.file_path)

        # Evaluate result
        status = self.evaluate(test_result)

        print("Final Status:", status)

    def analyze_code(self):
        full_path = os.path.join(BASE_DIR, self.file_path)

        print(f"Analyzing: {full_path}")

        result = get_complexity(full_path)

        print(result["raw_output"])
        print(f"Extracted CCN: {result['ccn']}")

        return result

    def evaluate(self, result):
        if "FAILED" in result or "ERROR" in result:
            return "fail"
        return "pass"
