import axios from 'axios'

const API_BASE = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      // Optionally redirect to login
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const eventService = {
  getEvents: () => api.get('/events/'),
  getEvent: (id: number) => api.get(`/events/${id}`),
  createEvent: (data: any) => api.post('/events/', data),
  updateEvent: (id: number, data: any) => api.put(`/events/${id}`, data),
  deleteEvent: (id: number) => api.delete(`/events/${id}`),
}

export const authService = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  register: (email: string, displayName: string, password: string) =>
    api.post('/auth/register', { email, displayName, password }),
  getMe: () => api.get('/auth/me'),
}

export const adminService = {
  deleteUser: (id: number) => api.delete(`/admin/users/${id}`),
  setUserAdmin: (id: number, isAdmin: boolean) => api.put(`/admin/users/${id}/admin`, { is_admin: isAdmin }),
  getUsers: () => api.get('/admin/users'),
}

export default api
