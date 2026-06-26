import { create } from 'zustand';
import { apiClient } from '../api/client';

export interface Criminal {
  id: string;
  first_name: string;
  last_name: string;
  alias?: string;
  known_crimes?: string;
  threat_level: string;
  status: string;
  image_url?: string;
}

interface CriminalState {
  criminals: Criminal[];
  fetchCriminals: () => Promise<void>;
}

export const useCriminalStore = create<CriminalState>((set) => ({
  criminals: [],
  
  fetchCriminals: async () => {
    try {
      const res = await apiClient.get('/criminals');
      set({ criminals: res.data });
    } catch (error) {
      console.error("Failed to fetch criminals", error);
    }
  }
}));
