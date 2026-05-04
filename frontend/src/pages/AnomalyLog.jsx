import React, { useEffect, useState } from 'react';
import { AlertCircle, Clock, Globe, ShieldQuestion } from 'lucide-react';
import { getStats } from '../services/api';
import RiskBadge from '../components/RiskBadge';

const AnomalyLog = () => {
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await getStats();
        // Mocking some log entries for visual proof of the structure
        setAnomalies([
          { id: 1, user: 'admin_test', ip: '103.4.22.11', risk: 'High', reason: 'Unusual IP Range + PCA Outlier', time: '10:42 AM' },
          { id: 2, user: 'stud_882', ip: '192.168.4.1', risk: 'Medium', reason: 'Late Night Access Pattern', time: '03:15 AM' },
          { id: 3, user: 'fac_991', ip: '45.1.2.3', risk: 'High', reason: 'DBSCAN Cluster Noise Detected', time: '11:20 PM' },
          { id: 4, user: 'guest_01', ip: '8.8.8.8', risk: 'Low', reason: 'Standard verification', time: '09:00 AM' },
        ]);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setLoading(false);
      }
    };
    fetchLogs();
  }, []);

  return (
    <div className="space-y-10 animate-in fade-in slide-in-from-bottom-8 duration-700">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-black text-slate-800 tracking-tighter">Anomaly Audit Log</h2>
          <p className="text-slate-400 font-bold mt-1 uppercase text-xs tracking-[0.2em]">Secured Behavioral Ledger</p>
        </div>
        <button className="glass-button px-6 py-3 rounded-2xl text-sm font-black tracking-tight">
          Export Intelligence (.csv)
        </button>
      </div>

      <div className="glass-card overflow-hidden border-none shadow-2xl">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-900/5 border-b border-white/20">
              <th className="px-8 py-6 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Subject Signature</th>
              <th className="px-8 py-6 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] text-center">Threat Level</th>
              <th className="px-8 py-6 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Behavioral Reasoning</th>
              <th className="px-8 py-6 text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Temporal Marker</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/10">
            {anomalies.map((item) => (
              <tr key={item.id} className="hover:bg-white/40 transition-all duration-300 group">
                <td className="px-8 py-6">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 rounded-2xl bg-blue-600/10 flex items-center justify-center text-blue-600 group-hover:scale-110 transition-transform duration-500">
                      <Globe size={22} />
                    </div>
                    <div>
                      <div className="font-black text-slate-800 tracking-tight">{item.user}</div>
                      <div className="text-xs font-bold text-slate-400 font-mono tracking-tighter mt-0.5">{item.ip}</div>
                    </div>
                  </div>
                </td>
                <td className="px-8 py-6 text-center">
                  <RiskBadge level={item.risk} />
                </td>
                <td className="px-8 py-6">
                  <div className="flex items-center text-sm font-bold text-slate-600">
                    <div className={`w-2 h-2 rounded-full mr-3 ${item.risk === 'High' ? 'bg-red-500' : 'bg-blue-500'}`} />
                    {item.reason}
                  </div>
                </td>
                <td className="px-8 py-6 text-sm font-bold text-slate-400">
                  {item.time}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {loading && (
          <div className="p-20 text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600/20 border-t-blue-600 mb-4"></div>
            <div className="text-slate-400 font-black text-xs uppercase tracking-widest">Decrypting Logs...</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnomalyLog;
