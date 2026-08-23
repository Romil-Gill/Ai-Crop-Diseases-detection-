import React from 'react';
import type { CommunitySummaryResponse } from '../types/api';
import { Radio, Calendar, ShieldCheck, MapPin } from 'lucide-react';

interface CommunitySummaryProps {
  summary: CommunitySummaryResponse;
}

export const CommunitySummary: React.FC<CommunitySummaryProps> = ({ summary }) => {
  return (
    <div className="space-y-6">
      {/* 3 Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-5 rounded-3xl bg-slate-900 text-white border border-slate-800 space-y-1">
          <div className="flex items-center gap-1.5 text-xs font-bold text-slate-300 font-outfit uppercase tracking-wider">
            <Radio className="w-4 h-4 text-emerald-400" />
            <span>Total Signals</span>
          </div>
          <div className="text-2xl font-extrabold font-mono text-emerald-300">
            {summary.total_reported_signals}
          </div>
          <p className="text-[11px] text-slate-400">Anonymized disease reports</p>
        </div>

        <div className="p-5 rounded-3xl bg-slate-900 text-white border border-slate-800 space-y-1">
          <div className="flex items-center gap-1.5 text-xs font-bold text-slate-300 font-outfit uppercase tracking-wider">
            <Calendar className="w-4 h-4 text-blue-400" />
            <span>Last 7 Days</span>
          </div>
          <div className="text-2xl font-extrabold font-mono text-blue-300">
            {summary.signals_last_7_days}
          </div>
          <p className="text-[11px] text-slate-400">Recent active signals</p>
        </div>

        <div className="p-5 rounded-3xl bg-slate-900 text-white border border-slate-800 space-y-1">
          <div className="flex items-center gap-1.5 text-xs font-bold text-slate-300 font-outfit uppercase tracking-wider">
            <ShieldCheck className="w-4 h-4 text-amber-400" />
            <span>Top Reported</span>
          </div>
          <div className="text-base font-extrabold font-outfit text-amber-300 truncate">
            {summary.most_reported_condition}
          </div>
          <p className="text-[11px] text-slate-400">Most active disease signal</p>
        </div>
      </div>

      {/* Regional Area Breakdown List */}
      {summary.area_breakdown.length > 0 && (
        <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center gap-2">
            <MapPin className="w-5 h-5 text-blue-600" />
            <h4 className="text-base font-extrabold font-outfit text-slate-900">
              Regional Crop-Health Activity (District Level)
            </h4>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {summary.area_breakdown.map((item, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-between"
              >
                <div>
                  <div className="font-bold text-xs text-slate-900 font-outfit">
                    {item.area_name}
                  </div>
                  <div className="text-xs text-slate-600 font-medium">
                    {item.condition}
                  </div>
                </div>
                <div className="px-3 py-1 rounded-full bg-blue-100 text-blue-900 font-extrabold font-mono text-xs">
                  {item.reported_signals} signals
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Disclaimer */}
      <div className="text-xs text-slate-500 italic p-3 rounded-2xl bg-slate-100 border border-slate-200">
        * {summary.disclaimer}
      </div>
    </div>
  );
};
