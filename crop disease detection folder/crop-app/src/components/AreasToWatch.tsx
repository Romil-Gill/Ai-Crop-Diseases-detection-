import React from 'react';
import type { RadarAreaItem } from '../types/api';
import { Eye, MapPin } from 'lucide-react';

interface AreasToWatchProps {
  areas: RadarAreaItem[];
}

export const AreasToWatch: React.FC<AreasToWatchProps> = ({ areas }) => {
  if (areas.length === 0) {
    return (
      <div className="p-6 rounded-3xl bg-white border border-slate-200 text-center space-y-2">
        <p className="text-xs text-slate-500 font-medium">No area signals recorded for the selected filter window.</p>
      </div>
    );
  }

  const getActivityBadge = (level: string) => {
    switch (level) {
      case 'ELEVATED':
        return 'bg-rose-100 text-rose-800 border-rose-200';
      case 'MODERATE':
        return 'bg-amber-100 text-amber-800 border-amber-200';
      default:
        return 'bg-emerald-100 text-emerald-800 border-emerald-200';
    }
  };

  return (
    <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-sm space-y-4 font-outfit">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Eye className="w-5 h-5 text-emerald-600" />
          <h4 className="text-base font-extrabold text-slate-900">
            Areas to Watch (Priority Aggregation)
          </h4>
        </div>
        <span className="text-[11px] font-bold text-slate-500">
          Ranked by Signal Volume
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-slate-200 text-slate-400 font-bold uppercase tracking-wider text-[10px]">
              <th className="pb-2.5">District Area</th>
              <th className="pb-2.5">Primary Reported Condition</th>
              <th className="pb-2.5 text-center">Signals</th>
              <th className="pb-2.5 text-center">Activity Level</th>
              <th className="pb-2.5 text-right">Last Signal</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {areas.map((area, idx) => {
              const topCond = area.conditions[0] || { crop: 'Crop', condition: 'Condition', count: 0 };
              const formattedTime = new Date(area.last_signal_at).toLocaleDateString('en-GB', {
                day: '2-digit',
                month: 'short',
              });

              return (
                <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3 font-extrabold text-slate-900 flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5 text-blue-600 shrink-0" />
                    <span>{area.area_name}</span>
                  </td>
                  <td className="py-3 font-medium text-slate-700">
                    <span className="font-bold text-slate-900">{topCond.crop}</span> • {topCond.condition}
                  </td>
                  <td className="py-3 text-center font-extrabold font-mono text-slate-900">
                    {area.signal_count}
                  </td>
                  <td className="py-3 text-center">
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold font-mono border ${getActivityBadge(area.activity_level)}`}>
                      {area.activity_level}
                    </span>
                  </td>
                  <td className="py-3 text-right text-slate-500 font-medium">
                    {formattedTime}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
