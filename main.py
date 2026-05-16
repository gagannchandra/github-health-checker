from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from github_api import collect_metrics
from llm import analyze_repo
from pydantic import BaseModel

class RepoRequest(BaseModel):
    repo: str

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# for uptotime robot

@app.get("/health")
@app.head("/health")
async def health():
    return JSONResponse({"status": "ok"})

# homepage
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/analyze")
def analyze(request: RepoRequest):
    repo_input = request.repo.strip()
    
    if not repo_input:
        return {"error": "Repository name is required"}

    # handle full github URL
    if "github.com" in repo_input:
        repo_input = repo_input.split("github.com/")[-1]
        repo_input = repo_input.strip("/")

    try:
        parts = repo_input.split("/")
        if len(parts) < 2:
             raise ValueError("Invalid format")
        owner, repo = parts[:2]
    except ValueError:
        return {"error": "Please enter in format: owner/repo or full GitHub URL"}

    try:
        metrics = collect_metrics(owner, repo)
        
        if "error" in metrics:
            return {"error": metrics["error"]}

        report = analyze_repo(metrics)

        return {
            "metrics": metrics,
            "report": report
        }
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}