import os
import sys
from git import Repo
from analyzer.ast_parser import parse_code_constraints
from generator.ai_test_gen import generate_tests
from performance_monitor import run_adaptive_tests
from tools.github_client import publish_pr_review

def main():
    repo_path = os.getcwd()
    repo = Repo(repo_path)
    
    # 1. Extract changed files in PR
    # In GitHub Actions, HEAD is the merge commit, HEAD^1 is base, HEAD^2 is PR branch
    changed_files = [item.a_path for item in repo.index.diff("HEAD~1")]
    
    code_changes =[]
    for file in changed_files:
        if file.endswith('.py') or file.endswith('.cpp'):
            code_changes.append(file)
            
    if not code_changes:
        print("No Python or C++ files changed. Skipping AI review.")
        sys.exit(0)
        
    print(f"Analyzing changes in: {code_changes}")
    
    # 2. Extract Control-flow & Behavioral constraints
    constraints = parse_code_constraints(code_changes)
    
    # 3. Intelligent Test Generation using RTM & PCM
    test_files = generate_tests(constraints, rtm_path="rtm/", pcm_path="pcm/")
    
    # 4. Execute Adaptive Unit Tests & Monitor Performance
    metrics = run_adaptive_tests(test_files)
    
    # 5. Review Decision Logic (Complexity, Coverage, Correctness)
    verdict = "APPROVE"
    comments = []
    
    if metrics['coverage'] < 80.0:
        verdict = "REQUEST_CHANGES"
        comments.append(f"Code coverage dropped to {metrics['coverage']}%. Minimum required is 80%.")
        
    if metrics['complexity'] > 10:
        verdict = "REQUEST_CHANGES"
        comments.append(f"Cyclomatic complexity is {metrics['complexity']}. Refactor for safety-oriented validation.")
        
    if not metrics['tests_passed']:
        verdict = "REQUEST_CHANGES"
        comments.append("AI-generated adaptive tests failed. Correctness criteria not met.")
    
    # 6. Autonomously Approve or Reject
    publish_pr_review(
        pr_number=os.getenv("PR_NUMBER"),
        verdict=verdict,
        comments=comments,
        metrics=metrics
    )

if __name__ == "__main__":
    main()
