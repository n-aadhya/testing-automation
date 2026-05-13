import os
import requests

def publish_pr_review(pr_number, verdict, comments, metrics):
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY") # e.g., n-aadhya/testing-automation
    
    if not token or not repo or not pr_number:
        print("Missing GitHub context. Cannot post review.")
        return

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    body = f"### AI Autonomous Review: {verdict}\n\n"
    body += f"**Coverage:** {metrics['coverage']}%\n"
    body += f"**Complexity:** {metrics['complexity']}\n"
    body += f"**Execution Time:** {metrics['execution_time_sec']}s\n\n"
    
    if comments:
        body += "#### Review Notes:\n"
        for comment in comments:
            body += f"- {comment}\n"
            
    data = {
        "body": body,
        "event": verdict # APPROVE, REQUEST_CHANGES, or COMMENT
    }
    
    requests.post(url, headers=headers, json=data)
