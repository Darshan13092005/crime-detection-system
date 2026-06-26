import { create } from 'zustand';
import { apiClient } from '../api/client';
import { systemAlarm } from '../utils/alarm';

export interface Alert {
  id: string;
  camera_id: string;
  alert_type: string;
  severity: string;
  description: string;
  status: string;
  created_at: string;
  snapshot_url?: string;
}

interface AlertState {
  alerts: Alert[];
  loading: boolean;
  isAlarmActive: boolean;
  fetchAlerts: () => Promise<void>;
  updateAlertStatus: (id: string, status: string) => Promise<void>;
  muteAlarm: () => void;
}

export const useAlertStore = create<AlertState>((set, get) => ({
  alerts: [],
  loading: false,
  isAlarmActive: false,

  fetchAlerts: async () => {
    try {
      const res = await apiClient.get('/alerts');
      const newAlerts: Alert[] = res.data;
      
      const currentAlerts = get().alerts;
      
      // Check if there's any NEW critical alert
      const hasNewCritical = newAlerts.some(newAlert => 
        newAlert.severity === 'critical' && 
        newAlert.status === 'active' && 
        !currentAlerts.some(old => old.id === newAlert.id)
      );

      if (hasNewCritical) {
        systemAlarm.play();
        set({ isAlarmActive: true });
      }

      set({ alerts: newAlerts });
    } catch (error) {
      console.error("Failed to fetch alerts", error);
    }
  },

  updateAlertStatus: async (id, status) => {
    try {
      const res = await apiClient.put(`/alerts/${id}`, { status });
      set((state) => ({
        alerts: state.alerts.map(a => a.id === id ? { ...a, status: res.data.status } : a)
      }));
    } catch (error) {
      console.error("Failed to update alert", error);
    }
  },

  muteAlarm: () => {
    systemAlarm.stop();
    set({ isAlarmActive: false });
  }
}));
