import { useEffect } from "react";
import { motion } from "framer-motion";
import { Search, ShieldAlert, FileText, UserPlus } from "lucide-react";
import { useCriminalStore } from "../store/criminalStore";

export function CriminalDatabase() {
  const { criminals, fetchCriminals } = useCriminalStore();

  useEffect(() => {
    fetchCriminals();
  }, [fetchCriminals]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold tracking-tight">Criminal Database</h1>
        <div className="flex gap-3">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search suspect..." 
              className="bg-surface-lighter/30 border border-surface-lighter rounded-lg py-2 pl-9 pr-4 text-sm text-slate-200 focus:outline-none focus:border-primary/50 w-64"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-primary text-slate-950 rounded-lg text-sm font-semibold hover:bg-primary-dark transition-colors">
            <UserPlus className="w-4 h-4" />
            Add Suspect
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        {criminals.length === 0 ? (
          <div className="col-span-full text-center py-12 text-slate-500">Database is empty.</div>
        ) : criminals.map((criminal, i) => (
          <motion.div
            key={criminal.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="glass rounded-xl overflow-hidden group hover:border-surface-lighter transition-all"
          >
            <div className="h-48 relative overflow-hidden bg-slate-900 flex items-center justify-center">
              <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent z-10" />
              {criminal.image_url ? (
                <img src={criminal.image_url} alt={criminal.first_name} className="w-full h-full object-cover opacity-60 group-hover:opacity-80 transition-opacity grayscale" />
              ) : (
                <UserPlus className="w-12 h-12 text-slate-800" />
              )}
              
              <div className="absolute top-3 left-3 z-20 bg-slate-950/80 backdrop-blur-sm border border-surface-lighter px-2 py-1 rounded text-xs font-mono font-bold">
                {criminal.id.slice(0,6)}
              </div>
              <div className={`absolute top-3 right-3 z-20 px-2 py-1 rounded text-xs font-bold border ${
                  criminal.threat_level === 'high' ? 'bg-accent/20 border-accent text-accent' :
                  criminal.threat_level === 'medium' ? 'bg-warning/20 border-warning text-warning' :
                  'bg-primary/20 border-primary text-primary'
                }`}>
                {criminal.threat_level.toUpperCase()}
              </div>
            </div>

            <div className="p-5">
              <h3 className="text-lg font-bold text-white">{criminal.first_name} {criminal.last_name}</h3>
              <p className="text-sm text-slate-400 mb-4">Alias: "{criminal.alias || 'Unknown'}"</p>
              
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-xs text-slate-300">
                  <ShieldAlert className="w-3.5 h-3.5 text-slate-500" />
                  Known Crimes:
                </div>
                <div className="flex flex-wrap gap-2">
                  {criminal.known_crimes ? criminal.known_crimes.split(',').map(crime => (
                    <span key={crime} className="px-2 py-1 bg-surface-lighter/50 rounded-md text-xs text-slate-300">
                      {crime.trim()}
                    </span>
                  )) : <span className="text-xs text-slate-500">None documented</span>}
                </div>
              </div>

              <button className="w-full mt-6 py-2 rounded-lg border border-surface-lighter text-sm font-medium hover:bg-surface-lighter/50 transition-colors flex items-center justify-center gap-2">
                <FileText className="w-4 h-4" />
                View Profile
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
