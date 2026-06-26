import { create } from 'zustand';
import { apiClient } from '../api/client';

export interface Camera {
  id: string;
  name: string;
  location: string;
  stream_url: string;
  is_active: boolean;
  created_at?: string;
}

interface CameraState {
  cameras: Camera[];
  fetchCameras: () => Promise<void>;
  addCamera: (camera: Partial<Camera>) => Promise<void>;
  deleteCamera: (id: string) => Promise<void>;
}

export const useCameraStore = create<CameraState>((set, get) => ({
  cameras: [],
  
  fetchCameras: async () => {
    try {
      const res = await apiClient.get('/cameras');
      set({ cameras: res.data });
    } catch (error) {
      console.error("Failed to fetch cameras", error);
    }
  },

  addCamera: async (camera) => {
    try {
      const res = await apiClient.post('/cameras', camera);
      set({ cameras: [...get().cameras, res.data] });
    } catch (error) {
      console.error("Failed to add camera", error);
    }
  },

  deleteCamera: async (id) => {
    try {
      await apiClient.delete(`/cameras/${id}`);
      set({ cameras: get().cameras.filter(c => c.id !== id) });
    } catch (error) {
      console.error("Failed to delete camera", error);
    }
  }
}));
