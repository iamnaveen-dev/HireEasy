import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          const response = await axios.post(
            `${API_BASE_URL}/auth/token/refresh/`,
            { refresh: refreshToken }
          );

          const newAccessToken = response.data.access;
          localStorage.setItem('access_token', newAccessToken);

          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return api(originalRequest);

        } catch (refreshError) {
          localStorage.clear();
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      } else {
        localStorage.clear();
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (data) => api.post('/auth/login/', data),
  register: (data) => api.post('/auth/register/', data),
  profile: () => api.get('/auth/profile/'),
};

export const interviewAPI = {
  list: () => api.get('/interviews/'),
  create: (data) => api.post('/interviews/create/', data),
  get: (id) => api.get(`/interviews/${id}/`),
  join: (roomCode) => api.get(`/interviews/join/${roomCode}/`),
  updateStatus: (id, data) => api.patch(`/interviews/${id}/status/`, data),
  addQuestion: (id, data) => api.post(`/interviews/${id}/questions/add/`, data),
  submitAnswer: (id, iqId, data) => api.patch(`/interviews/${id}/questions/${iqId}/answer/`, data),
};

export const questionAPI = {
  list: (params) => api.get('/questions/', { params }),
  create: (data) => api.post('/questions/create/', data),
};

export const reportAPI = {
  list: () => api.get('/reports/'),
  getByInterview: (interviewId) => api.get(`/reports/interview/${interviewId}/`),
};

export default api;