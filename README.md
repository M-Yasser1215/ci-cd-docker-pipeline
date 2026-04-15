# CI/CD Docker Pipeline

![CI](https://github.com/m-yasser1215/ci-cd-docker-pipeline/actions/workflows/ci-cd.yml/badge.svg)

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
    → Push image to Docker Hub (latest + commit SHA tags)  
    → Trigger Render deploy via webhook  
    → Render pulls latest image and redeploys 
```

Pull requests to `main` run tests only (no build or deploy), enabling safe validation before merging.

The deploy step only runs if tests pass - broken code never reaches production.

The deployment job depends on the test job (`needs: test`), ensuring only passing builds are deployed.

---

## 🏗️ Architecture

Developer → GitHub  
      ↓  
  GitHub Actions  
      ↓  
  Docker Hub  
      ↓  
   Render  
      ↓  
   Users  

---

## 📁 Project Structure

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

## 🔧 GitHub Actions Workflow (simplified)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v

  build-and-deploy:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'

    steps:
      - uses: actions/checkout@v4

      - uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/ci-cd-docker-pipeline:latest
            ${{ secrets.DOCKER_USERNAME }}/ci-cd-docker-pipeline:${{ github.sha }}

      - run: curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK }}"
```

---

## 🚦 Running Locally

**Prerequisites:** Python 3.11+

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API runs at `http://localhost:8000`
Interactive docs available at `http://localhost:8000/docs`

**Run tests**
```bash
pytest tests/ -v
```

---

## ☁️ Deployment

| Service | Platform | Notes |
|---|---|---|
| Backend | Render | Deploy triggered via webhook after successful CI pipeline |
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

## 🧠 Key Learnings

- CI/CD ensures only tested code reaches production  
- Containerisation guarantees consistency across environments  
- Using commit SHA tags enables versioned deployments and traceability  
- Webhooks enable fully automated deployments without manual intervention  
- Secrets must be handled securely using GitHub Actions  

---

## 💭 Future Improvements

- Add staging environment with separate pipeline branch
- Docker layer caching to speed up builds
- Slack or email notification on pipeline failure
- Health check endpoint monitored post-deploy

