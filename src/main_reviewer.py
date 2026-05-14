
import os
import sys
from git import Repo

from analyzer.ast_parser import parse_code_constraints
from generator.ai_test_gen import generate_tests
from monitor.performance_monitor import run_adaptive_tests
from tools.github_client import publish_pr_review

def main():
    repo_path = os.getcwd()
    repo = Repo(repo_path)
    
    # 1. Extract changed files in PR
    # In GitHub Actions, HEAD is the merge commit, HEAD^1 is base, HEAD^2 is PR branch
    changed_files = [item.a_path for item in repo.index.diff("HEAD~1")]
    
    code_changes = []
    for file in changed_files:
        # ONLY analyze files that exist, are Python/C++, AND live in the 'app/' folder
        if (file.endswith('.py') or file.endswith('.cpp')) and os.path.exists(file):
            if file.startswith('app/'):  # <--- THIS IS THE CRITICAL FILTER
                code_changes.append(file)
            
    if not code_changes:
        print("No Python or C++ files changed in the 'app/' directory. Skipping AI review.")
        sys.exit(0)
        
    print(f"Analyzing target changes in: {code_changes}")
    
    # 2. Extract Control-flow & Behavioral constraints
    constraints = parse_code_constraints(code_changes)
    
    # 3. Intelligent Test Generation using RTM & PCM
    test_files = generate_tests(constraints, rtm_path="rtm/", pcm_path="pcm/")
    
    # 4. Execute Adaptive Unit Tests & Monitor Performance
    metrics = run_adaptive_tests(test_files)
    print("\n--- AI PERFORMANCE METRICS ---")
    print(metrics)
    print("------------------------------\n")
    
    # 5. Review Decision Logic
    verdict = "APPROVE"
    comments = []
    
    if not metrics['semgrep_passed']:
        verdict = "REQUEST_CHANGES"
        comments.append("🚨 **SECURITY ALERT:** Semgrep found vulnerabilities in the code. Review semantic constraints.")

    if not metrics['rma_safe']:
        verdict = "REQUEST_CHANGES"
        comments.append(f"⏱️ **PERFORMANCE ALERT (RMA):** CPU utilization reached {metrics['cpu_utilization']:.2f}%. This exceeds the Rate Monotonic Analysis safe threshold of 69.3%. PR rejected due to real-time safety violations.")

    if metrics['coverage'] < 80.0:
        verdict = "REQUEST_CHANGES"
        comments.append(f"📉 **COVERAGE LOW:** Code coverage is {metrics['coverage']}%. Minimum required is 80%.")
        
    if metrics['complexity'] > 10:
        verdict = "REQUEST_CHANGES"
        comments.append(f"🧠 **COMPLEXITY HIGH:** Cyclomatic complexity exceeds limits. Refactor for safety-oriented validation.")
        
    if not metrics['tests_passed']:
        verdict = "REQUEST_CHANGES"
        comments.append("❌ **TESTS FAILED:** AI-generated adaptive unit tests failed.")
    
    # 6. Autonomously Approve or Reject
    publish_pr_review(
        pr_number=os.getenv("PR_NUMBER"),
        verdict=verdict,
        comments=comments,
        metrics=metrics
    )

if __name__ == "__main__":
    main()
