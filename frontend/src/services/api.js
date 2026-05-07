import axios from 'axios';

// In production, this should be your Render backend URL
const BASE_URL = 'https://uniguard-backend.onrender.com/api';

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
