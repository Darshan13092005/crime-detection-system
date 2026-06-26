import { useEffect } from "react";
import { motion } from "framer-motion";
import { Filter, Search, ShieldAlert, CheckCircle2, Image as ImageIcon } from "lucide-react";
import { useAlertStore } from "../store/alertStore";

export function Alerts() {
  const { alerts, fetchAlerts, updateAlertStatus } = useAlertStore();

  useEffect(() => {
    fetchAlerts();
  }, [fetchAlerts]);

  const toggleStatus = (id: string, currentStatus: string) => {
    const newStatus = currentStatus === 'resolved' ? 'active' : 'resolved';
    updateAlertStatus(id, newStatus);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold tracking-tight">Alert Management</h1>
        <div className="flex gap-3">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search ID..." 
              className="bg-surface-lighter/30 border border-surface-lighter rounded-lg py-2 pl-9 pr-4 text-sm text-slate-200 focus:outline-none focus:border-primary/50 w-48"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 glass rounded-lg text-sm hover:bg-surface-lighter transition-colors">
            <Filter className="w-4 h-4" />
            Filter
          </button>
        </div>
      </div>

      <div className="glass rounded-xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-surface-lighter/50 text-slate-400">
            <tr>
              <th className="px-6 py-4 font-medium">Alert ID</th>
              <th className="px-6 py-4 font-medium">Type</th>
              <th className="px-6 py-4 font-medium">Severity</th>
              <th className="px-6 py-4 font-medium">Camera</th>
              <th className="px-6 py-4 font-medium">Time</th>
              <th className="px-6 py-4 font-medium">Snapshot</th>
              <th className="px-6 py-4 font-medium">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-lighter/50">
            {alerts.map((alert, i) => (
              <motion.tr 
                key={alert.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                className="hover:bg-surface-lighter/20 transition-colors"
              >
                <td className="px-6 py-4 font-mono text-slate-300">{alert.id.slice(0,8)}</td>
                <td className="px-6 py-4 font-medium capitalize">{alert.alert_type.replace('_', ' ')}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded text-xs font-bold border ${
                    alert.severity === 'critical' ? 'bg-accent/10 border-accent/30 text-accent' :
                    alert.severity === 'high' ? 'bg-warning/10 border-warning/30 text-warning' :
                    'bg-primary/10 border-primary/30 text-primary'
                  }`}>
                    {alert.severity.toUpperCase()}
                  </span>
                </td>
                <td className="px-6 py-4 text-slate-400">{alert.camera_id}</td>
                <td className="px-6 py-4 text-slate-400">{new Date(alert.created_at).toLocaleString()}</td>
                <td className="px-6 py-4">
                  {alert.snapshot_url ? (
                    <button className="text-primary hover:text-primary-dark transition-colors font-medium flex items-center gap-1">
                      <ImageIcon className="w-4 h-4" /> View
                    </button>
                  ) : (
                    <span className="text-slate-600">-</span>
                  )}
                </td>
                <td className="px-6 py-4">
                  <button 
                    onClick={() => toggleStatus(alert.id, alert.status)}
                    className="flex items-center gap-2 hover:bg-surface-lighter/50 p-1.5 rounded transition-colors"
                  >
                    {alert.status === 'resolved' ? (
                      <><CheckCircle2 className="w-4 h-4 text-emerald-500" /> <span className="text-slate-400">Resolved</span></>
                    ) : (
                      <><ShieldAlert className="w-4 h-4 text-accent" /> <span className="text-white">Active</span></>
                    )}
                  </button>
                </td>
              </motion.tr>
            ))}
            {alerts.length === 0 && (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-500">No alerts found in database.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
