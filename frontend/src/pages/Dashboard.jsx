import React, { useEffect, useState } from 'react';
import { 
  Activity, 
  ShieldCheck, 
  AlertTriangle, 
  Users, 
  TrendingUp 
} from 'lucide-react';
import { getStats } from '../services/api';
import StatCard from '../components/StatCard'
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  AreaChart,
  Area 
} from 'recharts';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getStats().then(res => {
      setStats(res.data);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="text-slate-400 font-medium">Loading Intelligence Dashboard...</div>;

  const chartData = [
    { name: 'Mon', value: 400, anomalies: 24 },
    { name: 'Tue', value: 300, anomalies: 13 },
    { name: 'Wed', value: 600, anomalies: 38 },
    { name: 'Thu', value: 800, anomalies: 41 },
    { name: 'Fri', value: 500, anomalies: 30 },
    { name: 'Sat', value: 900, anomalies: 55 },
    { name: 'Sun', value: 700, anomalies: 40 },
  ];

  return (
    <div className="space-y-8">
      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Total Login Attempts" 
          value={stats?.total_logins?.toLocaleString() || "6.4M"} 
          icon={Users} 
          trend={12.5} 
          color="bg-blue-500"
        />
        <StatCard 
          title="Flagged Anomalies" 
          value={stats?.anomalies?.toLocaleString() || "142"} 
          icon={AlertTriangle} 
          trend={-2.4} 
          color="bg-orange-500"
        />
        <StatCard 
          title="Active Sessions" 
          value="842" 
          icon={Activity} 
          trend={5.1} 
          color="bg-emerald-500"
        />
        <StatCard 
          title="System Health" 
          value="99.9%" 
          icon={ShieldCheck} 
          trend={0.1} 
          color="bg-purple-500"
        />
      </div>

      {/* Analysis Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 glass-card p-10">
          <div className="flex justify-between items-center mb-10">
            <div>
              <h3 className="text-xl font-black text-slate-800 tracking-tight">Anomaly Trend Analysis</h3>
              <p className="text-sm font-bold text-slate-400 mt-1">Behavioral clustering over time</p>
            </div>
            <select className="glass-input text-xs font-bold px-4 py-2 cursor-pointer border-none bg-white font-sans text-slate-600">
              <option>Last 7 Days</option>
              <option>Last 30 Days</option>
            </select>
          </div>
          <div className="h-80 w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.2}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12, fontWeight: 700}} dy={15} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12, fontWeight: 700}} />
                <Tooltip 
                  contentStyle={{borderRadius: '24px', border: 'none', boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.1)', padding: '16px'}}
                />
                <Area type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={4} fillOpacity={1} fill="url(#colorValue)" dot={{r: 4, strokeWidth: 2, fill: '#fff'}} activeDot={{r: 6, strokeWidth: 0}} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-900/95 backdrop-blur-xl p-10 rounded-[2.5rem] shadow-2xl text-white border border-white/10">
          <h3 className="text-lg font-bold mb-6 flex items-center">
            <TrendingUp size={20} className="mr-2 text-blue-400" />
            Clustering Distribution
          </h3>
          <div className="space-y-6">
            <div className="relative pt-1">
              <div className="flex mb-2 items-center justify-between">
                <div><span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blue-200 bg-blue-900/50">Safe Clusters</span></div>
                <div className="text-right"><span className="text-xs font-semibold inline-block">92%</span></div>
              </div>
              <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-slate-800">
                <div style={{ width: "92%" }} className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-blue-500"></div>
              </div>
            </div>
            
            <div className="relative pt-1">
              <div className="flex mb-2 items-center justify-between">
                <div><span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-orange-200 bg-orange-900/50">Heuristic Flags</span></div>
                <div className="text-right"><span className="text-xs font-semibold inline-block">5%</span></div>
              </div>
              <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-slate-800">
                <div style={{ width: "5%" }} className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-orange-500"></div>
              </div>
            </div>

            <div className="relative pt-1">
              <div className="flex mb-2 items-center justify-between">
                <div><span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-red-200 bg-red-900/50">DBSCAN Noise</span></div>
                <div className="text-right"><span className="text-xs font-semibold inline-block">3%</span></div>
              </div>
              <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-slate-800">
                <div style={{ width: "3%" }} className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-red-500"></div>
              </div>
            </div>
          </div>
          
          <div className="mt-10 p-4 bg-slate-800 rounded-2xl border border-slate-700">
            <div className="text-xs text-slate-400 mb-1">Model Version</div>
            <div className="text-sm font-bold">UniGuard-v2.1 (PCA+KMeans)</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
