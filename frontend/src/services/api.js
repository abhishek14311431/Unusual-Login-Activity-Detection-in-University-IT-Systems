import axios from 'axios';

const api = axios.create({
  baseURL: '/api'
});

export const getStats = () => api.get('/stats');
export const checkLogin = (data) => api.post('/predict', data);
export const uploadDataset = (formData) => api.post('/upload-dataset', formData, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});

export default api;
