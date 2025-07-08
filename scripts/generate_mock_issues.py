import os
import requests

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = os.environ.get('REPO_OWNER')
REPO_NAME = os.environ.get('REPO_NAME')

# Mock issues for testing
issues = [
    {"title": "Test Issue 1", "body": "This is a mock issue for testing purposes."},
    {"title": "Test Issue 2", "body": "Another mock issue to verify issue creation."},
    {"title": "Test Issue 3", "body": "Mock issue to test GitHub Actions integration."}
]

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def create_issue(title, body):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    data = {"title": title, "body": body}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Issue created: {title}")
    elif response.status_code == 422 and "already_exists" in response.text:
        print(f"Issue already exists: {title}")
    else:
        print(f"Error creating issue '{title}': {response.content}")

for issue in issues:
    create_issue(issue["title"], issue["body"])
