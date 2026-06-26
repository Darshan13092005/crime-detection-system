import { Bell, Search, User, VolumeX, Sun, Moon } from "lucide-react";
import { useAuthStore } from "../store/authStore";
import { useAlertStore } from "../store/alertStore";
import { useThemeStore } from "../store/themeStore";
import { motion } from "framer-motion";

export function Topbar() {
  const logout = useAuthStore(state => state.logout);
  const { isAlarmActive, muteAlarm } = useAlertStore();
  const { isDark, toggleTheme } = useThemeStore();

  return (
    <header className="h-16 glass fixed top-0 right-0 left-64 z-30 border-b border-surface-lighter/50 flex items-center justify-between px-8">
      {/* Search */}
      <div className="relative w-96">
        <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
        <input 
          type="text" 
          placeholder="Search cameras, alerts, or suspects..." 
          className="w-full bg-surface-lighter/30 border border-surface-lighter rounded-full py-2 pl-10 pr-4 text-sm text-slate-200 focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all placeholder:text-slate-500"
        />
      </div>

      {/* Actions */}
      <div className="flex items-center gap-6">
        
        {isAlarmActive && (
          <motion.button 
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            onClick={muteAlarm}
            className="flex items-center gap-2 bg-accent/20 border border-accent text-accent px-4 py-1.5 rounded-full text-sm font-bold animate-pulse hover:bg-accent hover:text-white transition-colors"
          >
            <VolumeX className="w-4 h-4" />
            MUTE ALARM
          </motion.button>
        )}

        {/* Status Indicator */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-xs font-medium text-emerald-400">System Online</span>
        </div>

        {/* Theme Toggle */}
        <button 
          onClick={toggleTheme}
          className="relative p-2 text-slate-400 hover:text-white transition-colors rounded-full hover:bg-surface-lighter/50"
        >
          {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
        </button>

        {/* Notifications */}
        <button className="relative p-2 text-slate-400 hover:text-white transition-colors rounded-full hover:bg-surface-lighter/50">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-2 w-2 h-2 bg-accent rounded-full border-2 border-slate-950" />
        </button>

        {/* Profile */}
        <button onClick={logout} className="flex items-center gap-3 pl-6 border-l border-surface-lighter/50 hover:opacity-80 transition-opacity">
          <div className="text-right hidden md:block">
            <p className="text-sm font-semibold text-white">Commander</p>
            <p className="text-xs text-slate-400">Station 42</p>
          </div>
          <div className="w-10 h-10 rounded-full bg-primary/20 border border-primary/50 flex items-center justify-center">
            <User className="w-5 h-5 text-primary" />
          </div>
        </button>
      </div>
    </header>
  );
}
