import { create } from 'zustand';
import { apiClient } from '../api/client';

interface AuthState {
  token: string | null;
  user: any | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('auth_token'),
  user: null, // Ideally decode JWT or fetch profile
  isAuthenticated: !!localStorage.getItem('auth_token'),
  
  login: async (email, password) => {
    try {
      const res = await apiClient.post('/auth/login', { email, password });
      // Assuming Supabase returns session with access_token
      const token = res.data.session?.access_token || res.data.access_token;
      
      if (token) {
        localStorage.setItem('auth_token', token);
        set({ token, isAuthenticated: true, user: res.data.user });
      } else {
        throw new Error('No token received');
      }
    } catch (error) {
      console.error("Login failed", error);
      throw error;
    }
  },
  
  logout: () => {
    localStorage.removeItem('auth_token');
    set({ token: null, isAuthenticated: false, user: null });
  },
}));
