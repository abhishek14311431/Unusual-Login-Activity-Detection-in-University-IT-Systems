import React from 'react';

const RiskBadge = ({ level }) => {
  const styles = {
    Low: 'bg-green-100 text-green-700 border-green-200',
    Medium: 'bg-orange-100 text-orange-700 border-orange-200',
    High: 'bg-red-100 text-red-700 border-red-200'
  };

  return (
    <span className={`px-2.5 py-1 rounded-full text-xs font-bold border ${styles[level] || 'bg-slate-100 text-slate-600'}`}>
      {level.toUpperCase()}
    </span>
  );
};

export default RiskBadge;
