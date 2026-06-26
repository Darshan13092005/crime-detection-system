import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Users, AlertTriangle, ShieldCheck, Cctv } from "lucide-react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { useAlertStore } from "../store/alertStore";
import { useCameraStore } from "../store/cameraStore";

export function Dashboard() {
  const { alerts, fetchAlerts } = useAlertStore();
  const { cameras, fetchCameras } = useCameraStore();

  useEffect(() => {
    fetchAlerts();
    fetchCameras();
    // Poll for alerts every 5 seconds
    const interval = setInterval(() => fetchAlerts(), 5000);
    return () => clearInterval(interval);
  }, [fetchAlerts, fetchCameras]);

  const activeCameras = cameras.filter(c => c.is_active).length;
  const criticalAlerts = alerts.filter(a => a.severity === 'critical' && a.status !== 'resolved').length;
  const activeAlertsList = alerts.filter(a => a.status !== 'resolved').slice(0, 5);

  const stats = [
    { label: "Active Cameras", value: activeCameras.toString(), icon: Cctv, color: "text-emerald-500", bg: "bg-emerald-500/10" },
    { label: "Critical Alerts", value: criticalAlerts.toString(), icon: AlertTriangle, color: "text-accent", bg: "bg-accent/10" },
    { label: "Wanted Spotted", value: alerts.filter(a => a.alert_type === 'criminal_spotted').length.toString(), icon: Users, color: "text-warning", bg: "bg-warning/10" },
    { label: "System Status", value: criticalAlerts > 0 ? "Alert" : "Optimal", icon: ShieldCheck, color: "text-primary", bg: "bg-primary/10" },
  ];

  const [chartData, setChartData] = useState<any[]>([
    { time: "00:00", alerts: 0 }, { time: "04:00", alerts: 0 },
    { time: "08:00", alerts: 0 }, { time: "12:00", alerts: 0 },
    { time: "16:00", alerts: 0 }, { time: "20:00", alerts: 0 }
  ]);

  useEffect(() => {
    import('../api/client').then(({ apiClient }) => {
      apiClient.get('/analytics').then(res => {
        if(res.data.recent_alerts) {
           setChartData(res.data.recent_alerts.map((a:any) => ({ time: a.time, alerts: a.count })));
        }
      });
    });
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold tracking-tight">System Overview</h1>
        <div className="text-sm text-slate-400">Live Updating</div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="glass rounded-xl p-6 flex items-center gap-4"
          >
            <div className={`p-4 rounded-xl ${stat.bg}`}>
              <stat.icon className={`w-8 h-8 ${stat.color}`} />
            </div>
            <div>
              <div className="text-sm font-medium text-slate-400">{stat.label}</div>
              <div className="text-2xl font-bold mt-1">{stat.value}</div>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-6">Alert Frequency (24h)</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorAlerts" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#f43f5e" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis dataKey="time" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc' }} itemStyle={{ color: '#f43f5e' }} />
                <Area type="monotone" dataKey="alerts" stroke="#f43f5e" strokeWidth={3} fillOpacity={1} fill="url(#colorAlerts)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-6">Recent Alerts</h2>
          <div className="space-y-4">
            {activeAlertsList.length === 0 ? (
              <div className="text-slate-400 text-sm">No active alerts.</div>
            ) : activeAlertsList.map((alert) => (
              <div key={alert.id} className="flex items-start gap-4 p-3 rounded-lg bg-surface-lighter/30 border border-surface-lighter/50 hover:border-surface-lighter transition-colors cursor-pointer">
                <div className={`w-2 h-2 mt-2 rounded-full ${alert.severity === 'critical' ? 'bg-accent animate-pulse' : 'bg-warning'}`} />
                <div>
                  <div className="text-sm font-medium capitalize">{alert.alert_type.replace('_', ' ')}</div>
                  <div className="text-xs text-slate-400 mt-1">Cam: {alert.camera_id}</div>
                  <div className="text-xs text-slate-500 mt-1">{new Date(alert.created_at).toLocaleTimeString()}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
