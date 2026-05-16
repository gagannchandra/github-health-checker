import concurrent.futures
import requests
import os
from dotenv import load_dotenv

from typing import Dict, List, Any, Optional

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

HEADERS: Dict[str, str] = {
    "Authorization" : f"Bearer {GITHUB_TOKEN}",
    "Accept" : "application/vnd.github+json"
}

def fetch_json(url: str) -> Any:
    """Helper to fetch JSON and handle errors."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 404:
            return {"error": "not_found"}
        if response.status_code == 403:
            return {"error": "rate_limited"}
        response.raise_for_status()
        return response.json()
    except Exception:
        return {"error": "fetch_failed"}

def collect_metrics(owner: str, repo: str) -> dict:
    base_url = f"https://api.github.com/repos/{owner}/{repo}"
    
    endpoints = {
        "repo": base_url,
        "commits": f"{base_url}/commits?per_page=10",
        "contributors": f"{base_url}/contributors?per_page=30",
        "issues": f"{base_url}/issues?state=open&per_page=10",
        "readme": f"{base_url}/readme"
    }

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_key = {executor.submit(fetch_json, url): key for key, url in endpoints.items()}
        for future in concurrent.futures.as_completed(future_to_key):
            key = future_to_key[future]
            try:
                results[key] = future.result()
            except Exception:
                results[key] = {"error": "exception"}

    repo_data = results.get("repo")
    
    # Error handling
    if isinstance(repo_data, dict) and repo_data.get("error") == "not_found":
        return {"error": f"Repository '{owner}/{repo}' not found on GitHub."}
    if isinstance(repo_data, dict) and repo_data.get("error") == "rate_limited":
        return {"error": "GitHub API rate limit exceeded. Please try again later."}
    if not isinstance(repo_data, dict) or "full_name" not in repo_data:
        return {"error": "Failed to fetch repository data."}

    commits = results.get("commits", [])
    contributors = results.get("contributors", [])
    issues = results.get("issues", [])
    readme_data = results.get("readme", {})

    metrics = {
        "name": repo_data.get("full_name"),
        "description": repo_data.get("description"),
        "stars": repo_data.get("stargazers_count"),
        "forks": repo_data.get("forks_count"),
        "open_issues": repo_data.get("open_issues_count"),
        "language": repo_data.get("language"),
        "license": repo_data.get("license", {}).get("name") if repo_data.get("license") else "None",
        "created_at": repo_data.get("created_at"),
        "last_updated": repo_data.get("updated_at"),
        "last_commit": commits[0]["commit"]["author"]["date"] if isinstance(commits, list) and len(commits) > 0 else "N/A",
        "total_recent_commits": len(commits) if isinstance(commits, list) else 0,
        "contributors": len(contributors) if isinstance(contributors, list) else 0,
        "has_readme": True if isinstance(readme_data, dict) and "name" in readme_data else False,
        "watchers": repo_data.get("watchers_count"),
        "size_kb": repo_data.get("size"),
        "recent_open_issues": len(issues) if isinstance(issues, list) else 0,
    }

    return metrics
