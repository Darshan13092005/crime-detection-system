import { motion } from "framer-motion";
import { Save, Shield, Cpu } from "lucide-react";

export function Settings() {
  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold tracking-tight">System Settings</h1>
        <button className="flex items-center gap-2 px-4 py-2 bg-primary text-slate-950 rounded-lg text-sm font-semibold hover:bg-primary-dark transition-colors">
          <Save className="w-4 h-4" />
          Save Changes
        </button>
      </div>

      <div className="space-y-4">
        {/* AI Confidence Thresholds */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="glass rounded-xl p-6">
          <div className="flex items-center gap-3 mb-6">
            <Cpu className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-bold">AI Inference Thresholds</h2>
          </div>
          
          <div className="space-y-6">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-slate-300">Weapon Detection Confidence</span>
                <span className="text-primary font-mono">0.65</span>
              </div>
              <input type="range" min="0" max="100" defaultValue="65" className="w-full accent-primary" />
            </div>
            
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-slate-300">Face Recognition Match (Cosine)</span>
                <span className="text-primary font-mono">0.60</span>
              </div>
              <input type="range" min="0" max="100" defaultValue="60" className="w-full accent-primary" />
            </div>
          </div>
        </motion.div>

        {/* Security */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="glass rounded-xl p-6">
          <div className="flex items-center gap-3 mb-6">
            <Shield className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-bold">Security & Storage</h2>
          </div>
          
          <div className="space-y-4">
            <label className="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" defaultChecked className="w-4 h-4 accent-primary bg-surface-lighter border-surface-lighter rounded" />
              <span className="text-sm text-slate-300">Upload event snapshots to Supabase Cloud Storage</span>
            </label>
            <label className="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" defaultChecked className="w-4 h-4 accent-primary bg-surface-lighter border-surface-lighter rounded" />
              <span className="text-sm text-slate-300">Require 2FA for Admin login</span>
            </label>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
