import axios from 'axios';

// Updated to match your exact Render URL from screenshot
const BASE_URL = 'https://unusual-login-activity-detection-in.onrender.com/api';

const api = axios.create({
  baseURL: BASE_URL
});

export const getStats = () => api.get('/stats');
export const checkLogin = (data) => api.post('/predict', data);
export const uploadDataset = (formData) => api.post('/upload-dataset', formData, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});

export default api;
