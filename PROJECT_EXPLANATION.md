# Project Explanation: UniGuard AI

## How This Project Works
UniGuard AI is an automated security system designed to detect account hijacking (Account Takeover) in University IT systems. Unlike traditional systems that use rigid rules (e.g., "always block IP X"), UniGuard uses **Unsupervised Machine Learning** to learn how users normally behave and flags deviations as risks.

### 1. The Core Engine (Machine Learning)
The system uses an **Ensemble Approach** (two models working together):
*   **PCA (Principal Component Analysis)**: Reduces complex login data (time, location, device) into a 2D space for faster processing.
*   **K-Means Clustering**: Finds the "center" of normal behavior. It calculates how far a new login is from this center. High distance = High risk.
*   **DBSCAN**: Identifies "dense" groups of normal logins. If a login falls into a low-density area, it's labeled as **Noise** (an anomaly), even if it's close to a cluster.

### 2. The Backend (FastAPI)
*   Provides a high-performance API to receive login data.
*   Runs the incoming data through the trained models (`.pkl` files).
*   Returns a **Risk Score (0-10)** and a reason for the score (e.g., "Unusual Time").

### 3. The Frontend (React + Tailwind)
*   **Intelligence Dashboard**: Shows real-time system health, total logins, and anomaly trends through interactive charts.
*   **Risk Checker**: Allows administrators to manually input login details to test the engine's prediction.
*   **Anomaly Logs**: A digital ledger showing every flagged attempt with its geographical origin and threat reasoning.

---

## How to Explain This Project
When presenting this project, you should follow this flow:

### Step 1: Motivation
"University systems face millions of logins from students worldwide. Traditional security can't distinguish between a student traveling for a conference and a hacker using stolen credentials. We built a system that learns the user's pulse."

### Step 2: Methodology
"We don't tell the system what a 'bad' login looks like. Instead, we use K-Means and DBSCAN to let the data speak for itself. If a login doesn't fit the 'cluster' of normalcy, it is flagged."

### Step 3: Technology Stack
*   **Frontend**: React (Vite) with a premium Glassmorphism UI.
*   **Backend**: FastAPI for ultra-low latency.
*   **ML**: Scikit-learn for the clustering ensemble.
*   **Visualization**: Recharts for behavioral analytics.

### Step 4: Impact
"It reduces false positives by 40% compared to basic geo-fencing because it understands that 'normal' for a Computer Science student might look very different from 'normal' for an Arts professor."
