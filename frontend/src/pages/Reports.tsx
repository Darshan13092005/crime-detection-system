import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Calendar, BarChart3, FileText, Table } from "lucide-react";
import { apiClient } from "../api/client";
import { jsPDF } from "jspdf";
import Papa from "papaparse";
import toast from "react-hot-toast";

export function Reports() {
  const [analytics, setAnalytics] = useState<any>(null);

  useEffect(() => {
    apiClient.get('/analytics').then(res => setAnalytics(res.data)).catch(console.error);
  }, []);

  const exportPDF = () => {
    if (!analytics) return toast.error("Data not loaded yet");
    const doc = new jsPDF();
    doc.setFontSize(20);
    doc.text("Sentinel AI - System Report", 20, 20);
    
    doc.setFontSize(12);
    doc.text(`Generated: ${new Date().toLocaleString()}`, 20, 30);
    
    doc.text("Incident Summary:", 20, 45);
    doc.text(`Total Incidents Today: ${analytics.total_incidents_today}`, 30, 55);
    doc.text(`Weapons Detected: ${analytics.incidents_by_type.weapon_detected}`, 30, 65);
    doc.text(`Fights Detected: ${analytics.incidents_by_type.fight_detected}`, 30, 75);
    doc.text(`Suspicious Activity: ${analytics.incidents_by_type.suspicious_activity}`, 30, 85);
    
    doc.text("Camera Status:", 20, 105);
    doc.text(`Active: ${analytics.active_cameras} | Offline: ${analytics.offline_cameras}`, 30, 115);
    
    doc.save("sentinel-report.pdf");
    toast.success("PDF Exported Successfully");
  };

  const exportCSV = () => {
    if (!analytics) return toast.error("Data not loaded yet");
    const data = analytics.recent_alerts.map((a: any) => ({
      Time: a.time,
      AlertCount: a.count
    }));
    const csv = Papa.unparse(data);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", "incident-timeline.csv");
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    toast.success("CSV Exported Successfully");
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold tracking-tight">System Reports</h1>
        <div className="flex gap-3">
          <button onClick={exportCSV} className="flex items-center gap-2 px-4 py-2 border border-surface-lighter rounded-lg text-sm font-semibold hover:bg-surface-lighter/50 transition-colors">
            <Table className="w-4 h-4" />
            CSV Data
          </button>
          <button onClick={exportPDF} className="flex items-center gap-2 px-4 py-2 bg-primary text-slate-950 rounded-lg text-sm font-semibold hover:bg-primary-dark transition-colors">
            <FileText className="w-4 h-4" />
            PDF Report
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-xl p-6"
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="p-3 rounded-lg bg-surface-lighter">
              <BarChart3 className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h2 className="text-lg font-bold">Incident Summary</h2>
              <p className="text-sm text-slate-400">Monthly detection breakdown</p>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center text-sm">
              <span className="text-slate-300">Weapons Detected</span>
              <span className="font-bold text-accent">{analytics?.incidents_by_type?.weapon_detected || 0}</span>
            </div>
            <div className="w-full bg-surface-lighter rounded-full h-2">
              <div className="bg-accent h-2 rounded-full" style={{ width: '45%' }}></div>
            </div>
            
            <div className="flex justify-between items-center text-sm pt-2">
              <span className="text-slate-300">Fights / Violence</span>
              <span className="font-bold text-warning">{analytics?.incidents_by_type?.fight_detected || 0}</span>
            </div>
            <div className="w-full bg-surface-lighter rounded-full h-2">
              <div className="bg-warning h-2 rounded-full" style={{ width: '25%' }}></div>
            </div>

            <div className="flex justify-between items-center text-sm pt-2">
              <span className="text-slate-300">Suspicious Activity</span>
              <span className="font-bold text-primary">{analytics?.incidents_by_type?.suspicious_activity || 0}</span>
            </div>
            <div className="w-full bg-surface-lighter rounded-full h-2">
              <div className="bg-primary h-2 rounded-full" style={{ width: '75%' }}></div>
            </div>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass rounded-xl p-6 flex flex-col items-center justify-center text-center"
        >
          <Calendar className="w-12 h-12 text-slate-500 mb-4" />
          <h3 className="text-lg font-medium text-slate-300">Custom Date Range</h3>
          <p className="text-sm text-slate-500 mt-2 mb-6">Select a date range to generate detailed compliance and incident reports for law enforcement handover.</p>
          <button className="px-4 py-2 border border-surface-lighter rounded-lg text-sm hover:bg-surface-lighter/50 transition-colors">
            Select Dates
          </button>
        </motion.div>
      </div>
    </div>
  );
}
