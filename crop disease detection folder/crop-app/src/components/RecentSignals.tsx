import React from 'react';
import type { CommunitySignalRecord } from '../types/api';
import { Calendar, MapPin, Radio } from 'lucide-react';

interface RecentSignalsProps {
  signals: CommunitySignalRecord[];
}

export const RecentSignals: React.FC<RecentSignalsProps> = ({ signals }) => {
  if (signals.length === 0) return null;

  return (
    <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-sm space-y-4 font-outfit">
      <div className="flex items-center gap-2">
        <Radio className="w-5 h-5 text-blue-600 animate-pulse" />
        <h4 className="text-base font-extrabold text-slate-900">
          Recent Community Signal Activity
        </h4>
      </div>

      <div className="space-y-2.5">
        {signals.map((sig) => {
          const formattedDate = new Date(sig.created_at).toLocaleDateString('en-GB', {
            day: '2-digit',
            month: 'short',
            hour: '2-digit',
            minute: '2-digit',
          });

          return (
            <div
              key={sig.id}
              className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs"
            >
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded-full bg-slate-900 text-white font-extrabold text-[10px] uppercase font-mono">
                  {sig.crop}
                </span>
                <span className="font-bold text-slate-900">
                  {sig.condition}
                </span>
              </div>

              <div className="flex items-center gap-3 text-slate-500 font-medium">
                <div className="flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" />
                  <span>{sig.area_name}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Calendar className="w-3.5 h-3.5 text-slate-400" />
                  <span>{formattedDate}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
