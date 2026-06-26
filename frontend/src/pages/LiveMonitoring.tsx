import { useEffect } from "react";
import { motion } from "framer-motion";
import { Maximize2, Camera, AlertTriangle } from "lucide-react";
import { useCameraStore } from "../store/cameraStore";
import { useAlertStore } from "../store/alertStore";

export function LiveMonitoring() {
  const { cameras, fetchCameras } = useCameraStore();
  const { alerts, fetchAlerts } = useAlertStore();

  useEffect(() => {
    fetchCameras();
    fetchAlerts();
    const interval = setInterval(() => {
      fetchAlerts(); // Poll for alerts to highlight cameras
    }, 3000);
    return () => clearInterval(interval);
  }, [fetchCameras, fetchAlerts]);

  const activeCameras = cameras.filter(c => c.is_active);

  // Check if a camera has a recent active alert (within last 15 seconds)
  const isCameraAlerting = (cameraId: string) => {
    return alerts.some(a => 
      a.camera_id === cameraId && 
      a.status !== 'resolved' && 
      (new Date().getTime() - new Date(a.created_at).getTime()) < 15000
    );
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-accent animate-pulse" />
          Live Feed Wall
        </h1>
        <div className="flex gap-2">
          <button className="px-4 py-2 glass rounded-lg text-sm hover:bg-surface-lighter transition-colors">
            Grid View
          </button>
          <button className="px-4 py-2 bg-primary text-slate-950 rounded-lg text-sm font-semibold hover:bg-primary-dark transition-colors">
            Full Screen
          </button>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {activeCameras.length === 0 ? (
          <div className="col-span-full flex items-center justify-center text-slate-500 glass rounded-xl">
            No active cameras found in database. Add one in Camera Management.
          </div>
        ) : activeCameras.map((feed, i) => {
          const alerting = isCameraAlerting(feed.id);
          return (
            <motion.div
              key={feed.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.05 }}
              className={`relative rounded-xl overflow-hidden group border-2 transition-colors ${
                alerting ? "border-accent shadow-[0_0_15px_rgba(244,63,94,0.3)]" : "border-surface-lighter/50"
              }`}
            >
              <div className="absolute inset-0 bg-slate-900 flex items-center justify-center overflow-hidden">
                {/* Normally an img tag streaming MJPEG or HLS video tag goes here */}
                {/* <img src={feed.stream_url} className="w-full h-full object-cover" /> */}
                <Camera className="w-12 h-12 text-slate-800" />
                <span className="text-slate-800 absolute bottom-4 text-xs font-mono">{feed.stream_url}</span>
              </div>
              
              <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:20px_20px] pointer-events-none" />
              
              <div className="absolute inset-0 p-3 flex flex-col justify-between pointer-events-none">
                <div className="flex justify-between items-start">
                  <div className="bg-slate-950/80 backdrop-blur-sm px-2 py-1 rounded text-xs font-mono font-bold tracking-widest border border-surface-lighter">
                    {feed.name}
                  </div>
                  {alerting && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: [1, 0.5, 1] }}
                      transition={{ repeat: Infinity, duration: 1 }}
                      className="bg-accent/20 border border-accent text-accent px-2 py-1 rounded flex items-center gap-1 text-xs font-bold"
                    >
                      <AlertTriangle className="w-3 h-3" />
                      ALERT
                    </motion.div>
                  )}
                </div>
                <div className="flex justify-between items-end">
                  <div className="text-xs text-white/70 bg-slate-950/50 px-2 py-1 rounded backdrop-blur-sm">
                    {feed.location}
                  </div>
                  <button className="p-2 rounded bg-slate-950/50 hover:bg-slate-950/80 pointer-events-auto transition-colors text-white backdrop-blur-sm">
                    <Maximize2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
