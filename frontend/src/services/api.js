import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

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
