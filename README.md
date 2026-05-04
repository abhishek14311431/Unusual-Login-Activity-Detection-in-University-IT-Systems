# 🛡️ UniGuard: Unusual Login Activity Detection System

UniGuard is an advanced security monitoring system designed for University IT infrastructures. It uses unsupervised machine learning (**K-Means** & **DBSCAN**) to detect anomalous login patterns and assess security risks in real-time.

---

## 🚀 Key Features

*   **Anomaly Detection**: Analyzes millions of login records to identify 'Outlier' behavior using spatial clustering and PCA.
*   **Risk Scoring Engine**: A rule-based system that calculates risk levels (Low, Medium, High) based on ML outputs, temporal factors, and login success rates.
*   **Interactive Dashboard**: A modern React-based UI for real-time monitoring and visual analysis of system security health.
*   **Dimensionality Reduction**: Utilizes PCA to project complex login features into 2D/3D spaces for intuitive visualization.

---

## 🛠️ Tech Stack

### Backend (AI & API)
*   **FastAPI**: High-performance Python web framework for real-time inference.
*   **Scikit-Learn**: Powering the K-Means and DBSCAN anomaly detection models.
*   **Pandas & NumPy**: Efficient data processing for 6.4M+ login records.
*   **Joblib**: Model serialization and persistence.

### Frontend (UI)
*   **React + Vite**: Fast, modern frontend development environment.
*   **Tailwind CSS**: Utility-first styling for a clean, professional dashboard.
*   **Recharts**: Interactive data visualizations and risk distribution charts.
*   **Lucide Icons**: Consistent, high-quality iconography.

---

## 📁 Project Structure

```text
uniguard/
├── backend/                # 🧠 AI & API Core
│   ├── main.py             # FastAPI entry point
│   ├── train_model.py      # ML training & validation logic
│   ├── preprocess.py       # Feature engineering & scaling
│   ├── predict.py          # Ensemble anomaly detection
│   ├── risk_score.py       # Heuristic risk assessment
│   ├── config.py           # Global project settings
│   ├── models/             # Saved .pkl models (KMeans, Scaler)
│   └── data/               # Dataset artifacts & samples
├── frontend/               # 💻 React Dashboard
│   ├── src/
│   │   ├── components/     # UI: StatCard, RiskBadge, Charts
│   │   ├── pages/          # Full views: Dashboard, RiskChecker
│   │   └── services/       # API integration layer
│   └── tailwind.config.js
├── notebooks/              # 📓 Research & Documentation
│   ├── 01_eda.ipynb        # Exploratory Data Analysis
│   ├── 02_preprocessing.ipynb
│   └── 03_kmeans_training.ipynb ...
└── README.md
```

---

## 🚥 Getting Started

### 1. Prerequisites
*   Python 3.10+
*   Node.js & npm

### 2. Backend Setup
```bash
# From the root directory
export PYTHONPATH=$PWD
pip install -r backend/requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
*Access API Docs at: http://localhost:8000/docs*

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Access Dashboard at: http://localhost:3000*

---

## 📊 Demo & Analysis

The system identifies anomalies based on several factors:
*   **Spatial Outliers**: Logins originating from rare geographic locations or IPs (detected via DBSCAN).
*   **Risk Windows**: Increased risk scores for activity between **12 AM and 6 AM**.
*   **Ensemble Scoring**: High-precision detection by intersecting K-Means distance and DBSCAN labels.

## ⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details.
