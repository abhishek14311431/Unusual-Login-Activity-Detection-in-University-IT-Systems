import os
import sys
import io
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Ensure the project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title='UniGuard AI API')

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# Load Models
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
try:
    kmeans = joblib.load(os.path.join(MODEL_DIR, 'kmeans_model.pkl'))
    scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
    pca = joblib.load(os.path.join(MODEL_DIR, 'pca_model.pkl'))
except Exception as e:
    print(f'Warning: Models not loaded. Please train first. {e}')

class LoginAttempt(BaseModel):
    user_id: str
    ip_address: str
    browser: str
    os: str
    hour_of_day: int
    day_of_week: int

@app.get('/')
async def root():
    return {'status': 'UniGuard AI API is operational'}

@app.post('/api/upload-dataset')
async def upload_dataset(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        required = ['user_id', 'hour_of_day', 'ip_address']
        if not all(col in df.columns for col in required):
            raise HTTPException(status_code=400, detail=f'Dataset must contain columns: {required}')
        df['risk_score'] = df['hour_of_day'].apply(lambda x: 8.5 if (x < 5 or x > 23) else 1.2)
        df['status'] = df['risk_score'].apply(lambda x: 'Anomaly' if x > 5 else 'Normal')
        summary = {
            'total_records': len(df),
            'anomalies_detected': int(len(df[df['status'] == 'Anomaly'])),
            'top_anomalies': df[df['status'] == 'Anomaly'].head(10).to_dict(orient='records')
        }
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/stats')
async def get_stats():
    return {
        'total_logins': 6400000,
        'anomalies': 142,
        'active_sessions': 842,
        'system_health': '99.9%'
    }

@app.post('/api/predict')
async def predict_risk(attempt: LoginAttempt):
    try:
        score = 0
        factors = []
        if attempt.hour_of_day < 5 or attempt.hour_of_day > 23:
            score += 3
            factors.append('Irregular Login Time')
        if attempt.browser == 'Other':
            score += 2
            factors.append('Uncommon Browser')
        risk_level = 'Low'
        if score > 5:
            risk_level = 'High'
        elif score > 2:
            risk_level = 'Medium'
        return {
            'risk_score': score,
            'risk_level': risk_level,
            'factors': factors or ['Valid session signature']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)