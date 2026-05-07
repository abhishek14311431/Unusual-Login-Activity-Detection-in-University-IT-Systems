import React, { useEffect, useState } from 'react';
import { AlertCircle, Clock, Globe, ShieldQuestion, Upload, FileCheck, CheckCircle, AlertTriangle } from 'lucide-react';
import { getStats, uploadDataset } from '../services/api';
import RiskBadge from '../components/RiskBadge';

const AnomalyLog = () => {
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [isAuditActive, setIsAuditActive] = useState(false);
  const [auditStats, setAuditStats] = useState(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploadLoading(true);
    setAnomalies([]); // Clear previous to show loading state
    
    // Artificial 3-second delay for realistic analysis effect
    await new Promise(resolve => setTimeout(resolve, 3000));

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await uploadDataset(formData);
      setAuditStats({
        scanned: response.data.total_records,
        anomalies: response.data.anomalies_detected
      });
      const results = response.data.top_anomalies.map((item, index) => ({
        id: `audit-${index}`,
        user: item.user_id,
        ip: item.ip_address,
        risk: item.risk_level,
        score: item.risk_score,
        reason: item.reason,
        time: `${item.hour_of_day}:00`
      }));
      setAnomalies(results);
      setIsAuditActive(true);
    } catch (error) {
      console.error('Audit failed:', error);
      const errorMsg = error.response?.data?.detail || 'Audit failed. Ensure CSV format is correct.';
      alert(`Audit failed: ${errorMsg}`);
    } finally {
      setUploadLoading(false);
      setLoading(false);
      event.target.value = ''; // Clear input to allow re-upload of same file
    }
  };

  useEffect(() => {
    // We remove the default sample data strictly to keep it clean before upload
    setAnomalies([]);
    setLoading(false);
  }, []);

  return (
    <div className="space-y-10 animate-in fade-in slide-in-from-bottom-8 duration-700">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-black text-slate-800 tracking-tighter drop-shadow-sm">
            {isAuditActive ? 'AI Audit Report' : 'Security Ledger'}
          </h2>
          {isAuditActive && (
            <div className="flex items-center space-x-3 mt-2">
              <span className="px-3 py-1 bg-blue-600/10 text-blue-700 rounded-full text-xs font-black tracking-widest uppercase border border-blue-200/50">
                SCANNED: {auditStats.scanned}
              </span>
              <span className="px-3 py-1 bg-red-600/10 text-red-700 rounded-full text-xs font-black tracking-widest uppercase border border-red-200/50">
                THREATS: {auditStats.anomalies}
              </span>
            </div>
          )}
          {!isAuditActive && (
            <p className="text-slate-400 font-bold mt-1 uppercase text-xs tracking-[0.2em]">
              Behavioral Signal Intelligence
            </p>
          )}
        </div>
        
        <div className="flex items-center space-x-4">
          {isAuditActive && (
            <button 
              onClick={() => setIsAuditActive(false)}
              className="text-slate-500 font-bold text-sm hover:text-blue-600 transition-colors"
            >
              Reset to Live Logs
            </button>
          )}
          <label className="glass-button px-6 py-3 rounded-2xl text-sm font-black tracking-tight cursor-pointer flex items-center space-x-2">
            {uploadLoading ? (
               <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
            ) : (
              <Upload size={18} />
            )}
            <span>{isAuditActive ? 'Re-Audit Dataset' : 'Audit Dataset (.csv)'}</span>
            <input type="file" className="hidden" accept=".csv" onChange={handleFileUpload} disabled={uploadLoading} />
          </label>
        </div>
      </div>

      <div className="bg-white/40 backdrop-blur-3xl rounded-[2.5rem] border border-white/40 shadow-[0_8px_32px_0_rgba(31,38,135,0.07)] overflow-hidden transition-all duration-500 hover:shadow-[0_8px_32px_0_rgba(31,38,135,0.12)]">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-900/5 border-b border-white/30">
              <th className="px-8 py-6 text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Subject Signature</th>
              <th className="px-8 py-6 text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] text-center">Threat Level</th>
              <th className="px-8 py-6 text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Risk Score</th>
              <th className="px-8 py-6 text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Behavioral Reasoning</th>
              <th className="px-8 py-6 text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Login Time</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/20">
            {anomalies.length > 0 ? anomalies.map((item) => (
              <tr key={item.id} className="hover:bg-white/60 transition-all duration-300 group">
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
                  <span className={`font-mono font-black text-sm px-3 py-1 rounded-lg ${
                    item.score > 7 ? 'bg-red-500/10 text-red-600' : 
                    item.score > 4 ? 'bg-orange-500/10 text-orange-600' : 
                    'bg-blue-500/10 text-blue-600'
                  }`}>
                    {item.score || '---'}
                  </span>
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
            )) : (
              <tr>
                <td colSpan="5" className="px-8 py-32 text-center">
                  <div className="flex flex-col items-center justify-center space-y-4 opacity-40">
                    <div className="p-8 bg-white/50 rounded-full border border-white/40 shadow-inner">
                      <FileCheck size={48} className="text-blue-500" />
                    </div>
                    <div>
                      <div className="text-slate-800 font-black tracking-[0.2em] text-xs uppercase mb-1">
                        Secure Behavioral Audit
                      </div>
                      <p className="text-slate-400 text-sm font-bold max-w-[250px] mx-auto leading-relaxed">
                        The ledger is currently clear. Upload a csv dataset to perform deep-link behavioral analysis.
                      </p>
                    </div>
                  </div>
                </td>
              </tr>
            )}
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
