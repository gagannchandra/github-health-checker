# <img src="https://raw.githubusercontent.com/primer/octicons/main/icons/pulse-24.svg" width="32" height="32" style="vertical-align: middle; filter: invert(1);"> GitHub Repository Health Checker

> **Live Demo:** [https://github-health-checker-ktmb.onrender.com/](https://github-health-checker-ktmb.onrender.com/)

An AI-powered tool that analyzes any public GitHub repository and generates a structured health report — covering activity, strengths, concerns, and an overall health score.

Built with **FastAPI · GitHub REST API · NVIDIA LLaMA 3.1**

---

## 🎥 Demo

> 📽️ **[Watch Demo Video](#)**

---

## ✨ Features

- 🔗 Analyzes any public GitHub repository via `owner/repo` format
- 📊 Fetches live metrics — stars, forks, issues, contributors, last commit, license, and repo size
- 🤖 Uses NVIDIA-hosted **LLaMA 3.1 (8B Instruct)** to generate a plain-English AI health report
- 🏷️ Automatically assigns a status badge: **Active / Inactive / Needs Review**
- 🌙 Clean dark UI with metric cards
- ⚡ Fast async backend powered by FastAPI + Uvicorn

---

## 🛠 Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Python 3.10+, FastAPI               |
| AI / LLM   | NVIDIA API — `meta/llama-3.1-8b-instruct` |
| Data       | GitHub REST API v3                  |
| Frontend   | HTML, CSS, JavaScript               |
| Server     | Uvicorn (ASGI)                      |
| Config     | python-dotenv                       |

---

## 📁 Project Structure

```text
github-health-checker/
├── main.py              # FastAPI application & routes
├── github_api.py        # GitHub API integration (concurrent)
├── llm.py               # NVIDIA LLM integration
├── templates/
│   └── index.html       # Single-page frontend (HTML/CSS/JS)
├── .env                 # Environment variables (private)
├── .env.example         # Environment template
└── requirements.txt     # Python dependencies
```

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.10 or higher
- A GitHub account (for Personal Access Token)
- An NVIDIA Build account (for LLM API key)

---

### 1. Clone the Repository

```bash
git clone https://github.com/gagannchandra/github-health-checker.git
cd github-health-checker
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then fill in your keys:

```env
GITHUB_TOKEN=your_github_personal_access_token
NVIDIA_API_KEY=your_nvidia_api_key
```

**How to get your keys:**

| Key | Steps |
|-----|-------|
| `GITHUB_TOKEN` | Go to [GitHub → Settings → Developer Settings → Tokens](https://github.com/settings/tokens) → Generate new token → enable `repo` scope |
| `NVIDIA_API_KEY` | Sign up at [build.nvidia.com](https://build.nvidia.com) → Get API Key |

### 5. Run the Application

```bash
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000** in your browser.

---

## 🚀 Usage

1. Enter a public GitHub repository in the input field using the format: `owner/repo`
2. Click **Analyze**
3. View your health report with metrics, AI insights, and a status badge

**Example repositories to try:**
```
tiangolo/fastapi
facebook/react
microsoft/vscode
torvalds/linux
```

---

## 📊 Metrics Analyzed

| Metric | What It Tells Us |
|--------|-----------------|
| ⭐ Stars | Community interest and adoption |
| 🍴 Forks | How widely it's being built upon |
| 🕐 Last Commit | Recency of active development |
| 🐛 Open Issues | Maintenance backlog signal |
| 👥 Contributors | Team size and community health |
| 📜 License | Project maturity and openness |
| 📦 Repo Size | Scale of the codebase |

---

## 🤖 How the AI Report Works

The collected metrics are formatted into a structured prompt and sent to **NVIDIA's hosted LLaMA 3.1 (8B Instruct)** model. The model returns:

- **Strengths** of the repository
- **Concerns** or red flags
- **Overall health summary** in plain English
- A recommended **health score** out of 100

---

## 🌱 Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | ✅ Yes | GitHub Personal Access Token (increases rate limit from 60 to 5000 req/hr) |
| `NVIDIA_API_KEY` | ✅ Yes | API key for NVIDIA's hosted LLM models |

---

## 📋 `.env.example`

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxx
```

---

## 🔧 requirements.txt

```text
fastapi
uvicorn
requests
python-dotenv
Jinja2
pydantic
```

---

## 🐛 Known Limitations

- Only works with **public** GitHub repositories
- GitHub API rate limit is 5,000 requests/hr with a token (60/hr without)
- NVIDIA API response time may vary based on model load

---

## 🗺️ Roadmap

- [ ] Support private repositories via OAuth
- [ ] Add repository comparison mode (repo A vs repo B)
- [ ] Export health report as PDF
- [ ] GitHub Actions CI badge integration

---

## 👨‍💻 Author

**Gagan Chandra**
- 🌐 Portfolio: [gagannchandra.vercel.app](https://gagannchandra.vercel.app)
- 💼 LinkedIn: [linkedin.com/in/gagan-chandra](https://linkedin.com/in/gagan-chandra)
- 🐙 GitHub: [@gagannchandra](https://github.com/gagannchandra)

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ using FastAPI + NVIDIA AI</p>
