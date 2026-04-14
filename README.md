# CI/CD Docker Pipeline

A FastAPI app containerised with Docker and deployed automatically via a full CI/CD pipeline. Built as a portfolio project to demonstrate automation, containerisation, and cloud deployment.

**Live Endpoint:** [https://ci-cd-docker-pipeline-latest.onrender.com](https://ci-cd-docker-pipeline-latest.onrender.com)

---

## 📦 Technologies

**Backend**
- Python + FastAPI
- pytest

**Infrastructure**
- Docker
- GitHub Actions
- Docker Hub (image registry)
- Render (cloud deployment)

---

## ⚙️ Pipeline

Every push to `main` triggers the full pipeline automatically:

```
Push to main
    → Run pytest tests
    → Build Docker image
    → Push image to Docker Hub
    → Render pulls new image and redeploys
```

The deploy step only runs if tests pass - broken code never reaches production.

---

## 🏗️ Architecture

```
ci-cd-docker-pipeline/
├── app/
│   └── main.py               ← FastAPI app
├── tests/
│   └── test_main.py          ← pytest tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml         ← GitHub Actions pipeline
├── Dockerfile                ← Container definition
└── requirements.txt
```

---

## 🚦 Running Locally

**Prerequisites:** Python 3.11+

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API runs at `http://localhost:8000` - interactive docs at `http://localhost:8000/docs`

**Run tests**
```bash
pytest tests/ -v
```

---

## ☁️ Deployment

| Service | Platform | Notes |
|---|---|---|
| Backend | Render | Auto-deploys on push to `main` via webhook |
| Image registry | Docker Hub | Public image, tagged with `latest` and commit SHA |

> **Note:** Render's free tier spins down after 15 minutes of inactivity. The first request after a sleep may take ~30 seconds to respond. This is expected behaviour on the free plan.

---

## 🔐 GitHub Secrets Required

| Secret | Description |
|---|---|
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub access token |
| `RENDER_DEPLOY_HOOK` | Render webhook URL |

---

## 💭 Future Improvements

- Add staging environment with separate pipeline branch
- Docker layer caching to speed up builds
- Slack or email notification on pipeline failure
- Health check endpoint monitored post-deploy

