# UniGuard

UniGuard is a login anomaly detection system for university IT environments. It combines a FastAPI backend with a React + Vite dashboard to help visualize unusual login behavior and risk levels.

## Highlights

- FastAPI backend for risk scoring and dataset upload
- React dashboard for monitoring and review
- Dockerized deployment for local demos and presentation
- Jenkins CI/CD pipeline for automated build and smoke testing

## Tech Stack

- Backend: Python, FastAPI, Pandas, Joblib
- Frontend: React, Vite, Axios, Recharts, Tailwind CSS
- DevOps: GitHub, Jenkins, Docker, Docker Compose

## Quick Start

### Backend

```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm ci
npm run dev
```

### Docker Compose

```bash
docker compose up -d --build
```

Open the dashboard at `http://localhost:3000` and the API at `http://localhost:8000`.

## DevOps Guide

The full beginner-friendly DevOps implementation, Jenkins pipeline explanation, Docker setup, screenshots list, viva questions, and presentation script are documented in [DEVOPS_IMPLEMENTATION.md](DEVOPS_IMPLEMENTATION.md).

## Project Structure

```text
Unusual-Login-Activity-Detection-in-University-IT-Systems/
├── backend/
├── frontend/
├── docker-compose.yml
├── Jenkinsfile
└── DEVOPS_IMPLEMENTATION.md
```

## License

This project is intended for academic and demonstration use.
