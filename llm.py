import requests
import os 
from dotenv import load_dotenv

from typing import Dict, Any

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

HEADERS: Dict[str, str] = {
    "Authorization" : f"Bearer {NVIDIA_API_KEY}",
    "Content-Type" : "application/json"
}

def analyze_repo(metrics: dict) -> str :
    prompt = f"""
You are a GitHub repository health analyst.

Analyze the following repository metrics and provide a structured health report.

Repository Metrics:
- Name: {metrics.get('name')}
- Description: {metrics.get('description')}
- Stars: {metrics.get('stars')}
- Forks: {metrics.get('forks')}
- Watchers: {metrics.get('watchers')}
- Language: {metrics.get('language')}
- License: {metrics.get('license')}
- Created At: {metrics.get('created_at')}
- Last Updated: {metrics.get('last_updated')}
- Last Commit: {metrics.get('last_commit')}
- Recent Commits (last 10): {metrics.get('total_recent_commits')}
- Contributors: {metrics.get('contributors')}
- Open Issues: {metrics.get('open_issues')}
- Recent Open Issues: {metrics.get('recent_open_issues')}
- Repo Size (KB): {metrics.get('size_kb')}
- Has README: {metrics.get('has_readme')}

Provide your report in this exact format:

STATUS: [Active / Inactive / Abandoned / Archived]

HEALTH SCORE: [score out of 100]

SUMMARY:
[2-3 sentences about overall health]

STRENGTHS:
- [strength 1]
- [strength 2]
- [strength 3]

CONCERNS:
- [concern 1]
- [concern 2]

RECOMMENDATION:
[1-2 sentences on whether to use/contribute to this repo]
"""
    payload: Dict[str, Any] = {
        "model":"meta/llama-3.1-8b-instruct",
        "messages" : [{"role" : "user", "content" : prompt}],
        "max_tokens" : 1000
    }

    try:
        response = requests.post(NVIDIA_URL, headers = HEADERS, json = payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error generating AI report: {str(e)}"



if __name__ == "__main__":
    from github_api import collect_metrics
    metrics = collect_metrics("tiangolo", "fastapi")
    report = analyze_repo(metrics)
    print(report)