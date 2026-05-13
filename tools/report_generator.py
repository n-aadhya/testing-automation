import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def generate_review_report(file_path, ccn, coverage, status, decision):

    report_path = os.path.join(BASE_DIR, "review_report.txt")

    with open(report_path, "w") as f:

        f.write("AI Pull Request Review Report\n")
        f.write("===================================\n\n")

        f.write(f"File: {file_path}\n")
        f.write(f"Cyclomatic Complexity: {ccn}\n")
        f.write(f"Coverage: {coverage}%\n")
        f.write(f"Test Status: {status}\n")
        f.write(f"Decision: {decision['decision']}\n\n")

        f.write("Reasons:\n")

        for reason in decision["reasons"]:
            f.write(f"- {reason}\n")
