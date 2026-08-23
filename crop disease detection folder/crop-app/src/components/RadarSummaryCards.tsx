import React from 'react';
import type { CommunityRadarSummary } from '../types/api';
import { Radio, MapPin, Sprout, ShieldAlert } from 'lucide-react';

interface RadarSummaryCardsProps {
  summary: CommunityRadarSummary;
}

export const RadarSummaryCards: React.FC<RadarSummaryCardsProps> = ({ summary }) => {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3.5 font-outfit">
      <div className="p-4 rounded-3xl bg-slate-900 text-white border border-slate-800 space-y-1 shadow-sm">
        <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-300 uppercase tracking-wider">
          <Radio className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
          <span>Reported Signals</span>
        </div>
        <div className="text-2xl font-extrabold font-mono text-emerald-300">
          {summary.total_signals}
        </div>
        <p className="text-[10px] text-slate-400 font-sans">Anonymized signals</p>
      </div>

      <div className="p-4 rounded-3xl bg-slate-900 text-white border border-slate-800 space-y-1 shadow-sm">
        <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-300 uppercase tracking-wider">
          <MapPin className="w-3.5 h-3.5 text-blue-400" />
          <span>Active Areas</span>
        </div>
        <div className="text-2xl font-extrabold font-mono text-blue-300">
          {summary.active_areas}
        </div>
        <p className="text-[10px] text-slate-400 font-sans">District clusters</p>
      </div>

      <div className="p-4 rounded-3xl bg-slate-900 text-white border border-slate-800 space-y-1 shadow-sm">
        <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-300 uppercase tracking-wider">
          <Sprout className="w-3.5 h-3.5 text-lime-400" />
          <span>Top Crop</span>
        </div>
        <div className="text-lg font-extrabold text-lime-300 truncate">
          {!summary.most_reported_crop || summary.most_reported_crop === 'None' ? '—' : summary.most_reported_crop}
        </div>
        <p className="text-[10px] text-slate-400 font-sans">Highest signals</p>
      </div>

      <div className="p-4 rounded-3xl bg-slate-900 text-white border border-slate-800 space-y-1 shadow-sm">
        <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-300 uppercase tracking-wider">
          <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
          <span>Top Condition</span>
        </div>
        <div className="text-base font-extrabold text-amber-300 truncate">
          {!summary.most_reported_condition || summary.most_reported_condition === 'None' ? '—' : summary.most_reported_condition}
        </div>
        <p className="text-[10px] text-slate-400 font-sans">Most active signal</p>
      </div>
    </div>
  );
};
