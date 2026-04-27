import subprocess
import shutil
import re
from tools.language_detector import detect_language


def extract_ccn_lizard(output):
    """
    Extract CCN from Lizard output
    """
    match = re.search(r'\n\s*\d+\s+(\d+)\s+\d+', output)
    if match:
        return int(match.group(1))
    return 1


def extract_ccn_radon(output):
    """
    Extract CCN from Radon output
    Example: A (4)
    """
    matches = re.findall(r'\((\d+)\)', output)
    if matches:
        return max(map(int, matches))  # take max complexity
    return 1


def run_lizard(file_path):
    if not shutil.which("lizard"):
        raise Exception("Lizard not installed")

    result = subprocess.run(
        ["lizard", file_path],
        capture_output=True,
        text=True
    )
    return result.stdout


def run_radon(file_path):
    if not shutil.which("radon"):
        raise Exception("Radon not installed")

    result = subprocess.run(
        ["radon", "cc", file_path],
        capture_output=True,
        text=True
    )
    return result.stdout


def get_complexity(file_path):
    language = detect_language(file_path)

    if language == "cpp":
        print("Using Lizard for C/C++")
        output = run_lizard(file_path)
        ccn = extract_ccn_lizard(output)

    elif language == "python":
        print("Using Radon for Python")
        output = run_radon(file_path)
        ccn = extract_ccn_radon(output)

    else:
        raise Exception("Unsupported language")

    return {
        "raw_output": output,
        "ccn": ccn,
        "language": language
    }
