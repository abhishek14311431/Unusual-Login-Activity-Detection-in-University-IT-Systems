import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import RiskChecker from './pages/RiskChecker';
import AnomalyLog from './pages/AnomalyLog';
import { ShieldCheck } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="flex min-h-screen bg-slate-50 font-sans text-slate-900">
      {/* Sidebar Navigation */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <main className="flex-1 ml-64 p-12 transition-all duration-500 overflow-y-auto h-screen">
        <header className="mb-12 flex justify-between items-center animate-in fade-in slide-in-from-top-4 duration-1000">
          <div>
            <div className="flex items-center space-x-2 text-xs font-black text-blue-500 uppercase tracking-[0.3em] mb-2">
              <span className="w-8 h-[2px] bg-blue-500"></span>
              <span>Secure Intelligence</span>
            </div>
            <h1 className="text-4xl font-black tracking-tighter text-slate-800">
              UniGuard <span className="text-blue-600">AI</span>
            </h1>
            <p className="text-slate-400 font-bold mt-1">Institutional Behavioral Analytics Platform</p>
          </div>
          <div className="flex items-center space-x-6 glass-card p-3 pr-6 border-white/40">
             <div className="w-12 h-12 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-2xl shadow-lg shadow-blue-200 flex items-center justify-center text-white ring-4 ring-white">
                <ShieldCheck size={24} />
             </div>
             <div className="text-right">
                <div className="text-sm font-black text-slate-700 uppercase tracking-tight">System Administrator</div>
                <div className="text-[10px] text-green-500 font-black flex items-center justify-end uppercase tracking-widest mt-1">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-2 shadow-[0_0_8px_rgba(34,197,94,0.6)] animate-pulse"></span>
                  Node-01 Active
                </div>
             </div>
          </div>
        </header>

        {/* Dynamic Route Content */}
        <div className="relative">
          {activeTab === 'dashboard' && <Dashboard />}
          {activeTab === 'checker' && <RiskChecker />}
          {activeTab === 'logs' && <AnomalyLog />}
        </div>
      </main>
    </div>
  );
}

export default App;
