import React, { useState } from 'react';
import { ShieldAlert, Fingerprint, MapPin, Monitor } from 'lucide-react';
import { checkLogin } from '../services/api';
import RiskBadge from '../components/RiskBadge';

const RiskChecker = () => {
  const [formData, setFormData] = useState({
    user_id: '',
    ip_address: '',
    browser: 'Chrome',
    os: 'Windows',
    hour_of_day: 12,
    day_of_week: 0
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await checkLogin(formData);
      setResult(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-10">
      <div className="glass-card p-10 animate-in fade-in zoom-in duration-500">
        <div className="flex items-center space-x-4 mb-10">
          <div className="p-3 bg-blue-600/10 text-blue-600 rounded-2xl">
            <ShieldAlert size={32} />
          </div>
          <div>
            <h2 className="text-2xl font-black text-slate-800 tracking-tight">Real-time Risk Assessment</h2>
            <p className="text-sm font-bold text-slate-400 mt-1 uppercase tracking-widest">Manual Behavioral Audit</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-8">
          <div className="space-y-3">
            <label className="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center">
              <Fingerprint size={16} className="mr-2 text-blue-500" /> User Identification
            </label>
            <input 
              type="text" 
              className="w-full p-4 glass-input font-bold text-slate-700"
              placeholder="e.g. user_123"
              value={formData.user_id}
              onChange={(e) => setFormData({...formData, user_id: e.target.value})}
              required
            />
          </div>

          <div className="space-y-3">
            <label className="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center">
              <MapPin size={16} className="mr-2 text-blue-500" /> Source IP Address
            </label>
            <input 
              type="text" 
              className="w-full p-4 glass-input font-bold text-slate-700"
              placeholder="e.g. 192.168.1.1"
              value={formData.ip_address}
              onChange={(e) => setFormData({...formData, ip_address: e.target.value})}
              required
            />
          </div>

          <div className="space-y-3">
            <label className="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center">
              <Monitor size={16} className="mr-2 text-blue-500" /> Client Environment
            </label>
            <div className="grid grid-cols-2 gap-4">
              <select className="p-4 glass-input font-bold text-slate-600 border-none appearance-none" value={formData.os} onChange={(e) => setFormData({...formData, os: e.target.value})}>
                <option>Windows</option><option>MacOS</option><option>Linux</option><option>Android</option>
              </select>
              <select className="p-4 glass-input font-bold text-slate-600 border-none appearance-none" value={formData.browser} onChange={(e) => setFormData({...formData, browser: e.target.value})}>
                <option>Chrome</option><option>Firefox</option><option>Safari</option><option>Edge</option>
              </select>
            </div>
          </div>

          <div className="space-y-3">
            <label className="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center text-slate-600">
               Temporal Context (0-23)
            </label>
            <input 
              type="number" min="0" max="23"
              className="w-full p-4 glass-input font-bold text-slate-700"
              value={formData.hour_of_day}
              onChange={(e) => setFormData({...formData, hour_of_day: parseInt(e.target.value)})}
            />
          </div>

          <div className="md:col-span-2 pt-4">
            <button type="submit" disabled={loading} className="w-full glass-button py-5 text-lg font-black tracking-tight rounded-[1.5rem]">
              {loading ? 'Analyzing Behavior...' : 'Initialize AI Security Scan'}
            </button>
          </div>
        </form>
      </div>

      {result && (
        <div className={`p-10 glass-card transition-all duration-700 animate-in slide-in-from-top-10 ${
          result.risk_level === 'High' ? 'bg-red-50/50 border-red-200/50' : 'bg-green-50/50 border-green-200/50'
        }`}>
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-xl font-black text-slate-800 mb-2 tracking-tight">Intelligence Quotient Result</h3>
              <p className="text-slate-500 font-bold text-sm mb-6">Assigned by UniGuard Ensemble ML V2.1</p>
              <RiskBadge level={result.risk_level} />
            </div>
            <div className="text-right">
              <div className={`text-6xl font-black ${result.risk_level === 'High' ? 'text-red-600' : 'text-green-600'} tracking-tighter`}>{result.risk_score}<span className="text-2xl text-slate-300">/10</span></div>
              <div className="text-xs font-black text-slate-400 uppercase tracking-[0.2em] mt-2">Final Risk Index</div>
            </div>
          </div>
          
          <div className="mt-10 grid grid-cols-1 md:grid-cols-2 gap-4">
            {result.factors.map((factor, i) => (
              <div key={i} className="flex items-center space-x-4 glass-card bg-white/50 p-4 border-none">
                <div className={`w-3 h-3 rounded-full animate-pulse ${result.risk_level === 'High' ? 'bg-red-400' : 'bg-blue-400'}`} />
                <span className="text-sm font-bold text-slate-700 whitespace-nowrap">{factor}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default RiskChecker;
