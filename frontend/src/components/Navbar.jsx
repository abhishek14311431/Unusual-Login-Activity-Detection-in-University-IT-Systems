import React from 'react';
import { ShieldCheck, Layout, List, ScanLine, Settings } from 'lucide-react';

const Navbar = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Layout },
    { id: 'logs', label: 'Anomaly Logs', icon: List },
    { id: 'checker', label: 'Risk Checker', icon: ScanLine },
  ];

  return (
    <div className="w-64 glass-sidebar flex flex-col h-screen fixed left-0 top-0 z-50">
      <div className="p-8 flex items-center space-x-3 text-blue-600">
        <div className="p-2 bg-blue-600 text-white rounded-xl shadow-lg shadow-blue-200">
          <ShieldCheck size={28} />
        </div>
        <span className="text-2xl font-black text-slate-800 tracking-tighter">UniGuard</span>
      </div>
      
      <nav className="flex-1 p-6 space-y-2 mt-4">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center space-x-3 px-5 py-4 rounded-2xl transition-all duration-300 ${
                activeTab === item.id 
                  ? 'glass-button' 
                  : 'text-slate-500 hover:bg-white/50 hover:text-slate-900'
              }`}
            >
              <Icon size={20} />
              <span className="font-bold">{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="p-6 border-t border-white/20">
        <button className="w-full flex items-center space-x-3 px-5 py-4 rounded-2xl text-slate-400 hover:bg-white/50 transition-all duration-300">
          <Settings size={20} />
          <span className="font-bold">Settings</span>
        </button>
      </div>
    </div>
  );
};

export default Navbar;
