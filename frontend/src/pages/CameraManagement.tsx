import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Plus, Trash2, Video } from "lucide-react";
import { useCameraStore } from "../store/cameraStore";

export function CameraManagement() {
  const { cameras, fetchCameras, addCamera, deleteCamera } = useCameraStore();
  
  // Quick hacky form state for demonstration
  const [showAddForm, setShowAddForm] = useState(false);
  const [newCam, setNewCam] = useState({ name: '', location: '', stream_url: '' });

  useEffect(() => {
    fetchCameras();
  }, [fetchCameras]);

  const handleAdd = async () => {
    if (newCam.name && newCam.stream_url) {
      await addCamera({ ...newCam, is_active: true });
      setShowAddForm(false);
      setNewCam({ name: '', location: '', stream_url: '' });
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold tracking-tight">Camera Management</h1>
        <button 
          onClick={() => setShowAddForm(!showAddForm)}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-slate-950 rounded-lg text-sm font-semibold hover:bg-primary-dark transition-colors"
        >
          <Plus className="w-4 h-4" />
          {showAddForm ? 'Cancel' : 'Add Camera'}
        </button>
      </div>

      {showAddForm && (
        <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} className="glass p-6 rounded-xl flex gap-4">
          <input type="text" placeholder="Name (e.g. Entrance)" className="bg-surface-lighter/50 border border-surface-lighter rounded p-2 text-sm w-full focus:outline-none" value={newCam.name} onChange={e => setNewCam({...newCam, name: e.target.value})} />
          <input type="text" placeholder="Location" className="bg-surface-lighter/50 border border-surface-lighter rounded p-2 text-sm w-full focus:outline-none" value={newCam.location} onChange={e => setNewCam({...newCam, location: e.target.value})} />
          <input type="text" placeholder="RTSP Stream URL" className="bg-surface-lighter/50 border border-surface-lighter rounded p-2 text-sm w-full focus:outline-none" value={newCam.stream_url} onChange={e => setNewCam({...newCam, stream_url: e.target.value})} />
          <button onClick={handleAdd} className="bg-emerald-500 hover:bg-emerald-600 text-white px-6 rounded font-semibold text-sm transition-colors">Save</button>
        </motion.div>
      )}

      <div className="glass rounded-xl overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-surface-lighter/50 text-slate-400">
            <tr>
              <th className="px-6 py-4 font-medium">Camera ID</th>
              <th className="px-6 py-4 font-medium">Name</th>
              <th className="px-6 py-4 font-medium">Location</th>
              <th className="px-6 py-4 font-medium">Stream URL</th>
              <th className="px-6 py-4 font-medium">Status</th>
              <th className="px-6 py-4 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-lighter/50">
            {cameras.map((cam, i) => (
              <motion.tr 
                key={cam.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                className="hover:bg-surface-lighter/20 transition-colors"
              >
                <td className="px-6 py-4 font-mono text-slate-300">
                  <div className="flex items-center gap-2">
                    <Video className="w-4 h-4 text-slate-500" />
                    {cam.id.slice(0,8)}
                  </div>
                </td>
                <td className="px-6 py-4 font-medium text-white">{cam.name}</td>
                <td className="px-6 py-4 text-slate-400">{cam.location}</td>
                <td className="px-6 py-4 font-mono text-slate-400 truncate max-w-[200px]">{cam.stream_url}</td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${cam.is_active ? 'bg-emerald-500' : 'bg-slate-600'}`} />
                    <span className={cam.is_active ? 'text-emerald-400' : 'text-slate-500'}>{cam.is_active ? 'Online' : 'Offline'}</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-right">
                  <div className="flex items-center justify-end gap-3">
                    <button onClick={() => deleteCamera(cam.id)} className="text-slate-400 hover:text-accent transition-colors">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </motion.tr>
            ))}
            {cameras.length === 0 && (
              <tr><td colSpan={6} className="text-center py-8 text-slate-500">No cameras configured.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
