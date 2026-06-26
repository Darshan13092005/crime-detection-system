import { NavLink } from "react-router-dom";
import { 
  LayoutDashboard, 
  Cctv, 
  Siren, 
  Fingerprint, 
  Video, 
  FileText, 
  Settings 
} from "lucide-react";
import { motion } from "framer-motion";

const navItems = [
  { path: "/", label: "Dashboard", icon: LayoutDashboard },
  { path: "/live", label: "Live Monitoring", icon: Cctv },
  { path: "/alerts", label: "Alerts", icon: Siren },
  { path: "/criminals", label: "Criminal DB", icon: Fingerprint },
  { path: "/cameras", label: "Cameras", icon: Video },
  { path: "/reports", label: "Reports", icon: FileText },
  { path: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="w-64 glass h-screen flex flex-col fixed left-0 top-0 z-40 border-r border-surface-lighter/50">
      <div className="h-16 flex items-center px-6 border-b border-surface-lighter/50">
        <Siren className="w-6 h-6 text-primary mr-3" />
        <span className="font-bold text-xl tracking-wider text-white">SENTINEL AI</span>
      </div>
      
      <nav className="flex-1 py-6 px-4 flex flex-col gap-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center px-4 py-3 rounded-lg transition-all duration-200 group relative ${
                isActive 
                  ? "bg-primary/10 text-primary" 
                  : "text-slate-400 hover:text-slate-100 hover:bg-surface-lighter/50"
              }`
            }
          >
            {({ isActive }) => (
              <>
                {isActive && (
                  <motion.div
                    layoutId="activeNav"
                    className="absolute left-0 w-1 h-8 bg-primary rounded-r-full"
                    initial={false}
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                  />
                )}
                <item.icon className={`w-5 h-5 mr-3 transition-colors ${isActive ? 'text-primary' : 'text-slate-500 group-hover:text-slate-300'}`} />
                <span className="font-medium">{item.label}</span>
              </>
            )}
          </NavLink>
        ))}
      </nav>
      
      <div className="p-4 border-t border-surface-lighter/50 text-xs text-slate-500 text-center">
        v1.0.0 Enterprise
      </div>
    </aside>
  );
}
