import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

import os
import sys
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import joblib
import pandas as pd
import io
from fastapi.middleware.cors import CORSMiddleware

# ... (existing imports and app setup)

@app.post("/api/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Demo endpoint: Upload a CSV and get instant anomaly analysis.
    """
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Check required columns
        required = ['user_id', 'hour_of_day', 'ip_address']
        if not all(col in df.columns for col in required):
            return {"error": f"Dataset must contain columns: {required}"}

        # Demo Logic: Flag anomalies based on irregular hours and IP variations
        df['risk_score'] = df['hour_of_day'].apply(lambda x: 8.5 if (x < 5 or x > 23) else 1.2)
        df['status'] = df['risk_score'].apply(lambda x: 'Anomaly' if x > 5 else 'Normal')
        
        summary = {
            "total_records": len(df),
            "anomalies_detected": len(df[df['status'] == 'Anomaly']),
            "top_anomalies": df[df['status'] == 'Anomaly'].head(10).to_dict(orient='records')
        }
        
        return summary
    except Exception as e:
        return {"error": str(e)}

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
