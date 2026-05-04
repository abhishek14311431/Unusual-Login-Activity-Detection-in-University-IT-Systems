import React from 'react';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

const StatCard = ({ title, value, icon: Icon, trend, color }) => (
  <div className="glass-card p-8 transition-transform hover:scale-[1.02] duration-500">
    <div className="flex justify-between items-start mb-6">
      <div className={`p-4 rounded-2xl ${color} bg-opacity-20 text-${color.split('-')[1]}-600`}>
        <Icon size={28} />
      </div>
      <div className={`flex items-center px-3 py-1 rounded-full text-xs font-black ${trend > 0 ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
        {trend > 0 ? <ArrowUpRight size={14} className="mr-1" /> : <ArrowDownRight size={14} className="mr-1" />}
        {Math.abs(trend)}%
      </div>
    </div>
    <div className="text-3xl font-black text-slate-800 tracking-tight">{value}</div>
    <div className="text-sm font-bold text-slate-400 mt-2 uppercase tracking-widest">{title}</div>
  </div>
);

export default StatCard;
