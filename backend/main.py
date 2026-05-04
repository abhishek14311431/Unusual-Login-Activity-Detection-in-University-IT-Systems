import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

# Ensure the project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from preprocessing import preprocess_data
# from utils import calculate_risk_score

app = FastAPI(title="UniGuard AI API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
try:
    kmeans = joblib.load(os.path.join(MODEL_DIR, "kmeans_model.pkl"))
    scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
    pca = joblib.load(os.path.join(MODEL_DIR, "pca_model.pkl"))
except Exception as e:
    print(f"Warning: Models not loaded. Please train first. {e}")

class LoginAttempt(BaseModel):
    user_id: str
    ip_address: str
    browser: str
    os: str
    hour_of_day: int
    day_of_week: int

@app.get("/")
async def root():
    return {"status": "UniGuard AI API is operational"}

@app.get("/api/stats")
async def get_stats():
    return {
        "total_logins": 6400000,
        "anomalies": 142,
        "active_sessions": 842,
        "system_health": "99.9%"
    }

@app.post("/api/predict")
async def predict_risk(attempt: LoginAttempt):
    try:
        # Simple placeholder risk calculation logic (for frontend demo)
        # In production, this would use the loaded models
        score = 0
        factors = []
        
        # Heuristic for demo
        if attempt.hour_of_day < 5 or attempt.hour_of_day > 23:
            score += 3
            factors.append("Irregular Login Time")
        
        if attempt.browser == "Other":
            score += 2
            factors.append("Uncommon Browser")
            
        risk_level = "Low"
        if score > 5:
            risk_level = "High"
        elif score > 2:
            risk_level = "Medium"
            
        return {
            "risk_score": score,
            "risk_level": risk_level,
            "factors": factors or ["Valid session signature"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
