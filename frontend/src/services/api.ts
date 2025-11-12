import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { access_token, refresh_token: newRefreshToken } = response.data;

          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', newRefreshToken);

          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        } catch (refreshError) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data: any) => api.post('/api/v1/auth/register', data),
  login: (data: any) => api.post('/api/v1/auth/login', data),
  getMe: () => api.get('/api/v1/auth/me'),
};

// Agents API
export const agentsAPI = {
  list: () => api.get('/api/v1/agents/'),
  get: (id: number) => api.get(`/api/v1/agents/${id}`),
  create: (data: any) => api.post('/api/v1/agents/', data),
  update: (id: number, data: any) => api.put(`/api/v1/agents/${id}`, data),
  delete: (id: number) => api.delete(`/api/v1/agents/${id}`),
};

// Phone Numbers API
export const phoneNumbersAPI = {
  list: () => api.get('/api/v1/phone-numbers/'),
  create: (data: any) => api.post('/api/v1/phone-numbers/', data),
  update: (id: number, data: any) => api.put(`/api/v1/phone-numbers/${id}`, data),
  delete: (id: number) => api.delete(`/api/v1/phone-numbers/${id}`),
};

// Calls API
export const callsAPI = {
  listConversations: (params?: any) => api.get('/api/v1/calls/conversations', { params }),
  getConversation: (id: number) => api.get(`/api/v1/calls/conversations/${id}`),
  getMessages: (id: number) => api.get(`/api/v1/calls/conversations/${id}/messages`),
  getCallLog: (id: number) => api.get(`/api/v1/calls/conversations/${id}/log`),
};

// GDPR API
export const gdprAPI = {
  exportData: () => api.get('/api/v1/gdpr/export', { responseType: 'blob' }),
  requestDeletion: () => api.post('/api/v1/gdpr/delete-account'),
  confirmDeletion: (requestId: number) => api.delete(`/api/v1/gdpr/delete-account/${requestId}`),
  getPrivacyPolicy: () => api.get('/api/v1/gdpr/privacy-policy'),
  getTermsOfService: () => api.get('/api/v1/gdpr/terms-of-service'),
};

// Tools API
export const toolsAPI = {
  getAvailableTools: () => api.get('/api/v1/tools/available-tools'),
};

// Testing API
export const testingAPI = {
  getVoices: () => api.get('/api/v1/testing/voices'),
};

export default api;
