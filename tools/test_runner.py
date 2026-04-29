import subprocess
import os
from tools.language_detector import detect_language

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_cpp_tests():
    print("Running C++ tests using gtest...")

    result = subprocess.run(
        ["bash", "gtest_runner.sh"],
        cwd=os.path.join(BASE_DIR, "tools"),
        capture_output=True,
        text=True
    )

    print(result.stdout)
    print(result.stderr)
    return result.stdout + result.stderr   
    


def run_python_tests():
    print("Running Python tests with coverage...")

    result = subprocess.run(
        ["coverage", "run", "-m", "pytest", "../tests/test_generated.py"],
        cwd=os.path.join(BASE_DIR, "tools"),
        capture_output=True,
        text=True
    )

    report = subprocess.run(
        ["coverage", "report"],
        cwd=os.path.join(BASE_DIR, "tools"),
        capture_output=True,
        text=True
    )

    print(report.stdout)

    return result.stdout + result.stderr + report.stdout
    


def run_tests(file_path):
    language = detect_language(file_path)

    if language == "cpp":
        return run_cpp_tests()

    elif language == "python":
        return run_python_tests()

    else:
        raise Exception("Unsupported language")
