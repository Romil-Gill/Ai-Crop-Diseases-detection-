import React from 'react';
import type { ScanRecord } from '../types/api';
import { Activity, ArrowRight } from 'lucide-react';

interface CropTimelineProps {
  scans: ScanRecord[];
}

export const CropTimeline: React.FC<CropTimelineProps> = ({ scans }) => {
  if (scans.length < 2) return null;

  // Group by crop & condition
  const groups: Record<string, ScanRecord[]> = {};
  scans.forEach((s) => {
    const key = `${s.crop} - ${s.condition}`;
    if (!groups[key]) groups[key] = [];
    groups[key].push(s);
  });

  const timelineItems = Object.entries(groups).filter(([_, list]) => list.length >= 2);
  if (timelineItems.length === 0) return null;

  return (
    <div className="p-5 rounded-3xl bg-slate-900 text-white space-y-4 shadow-lg border border-slate-800">
      <div className="flex items-center gap-2">
        <Activity className="w-5 h-5 text-emerald-400" />
        <h4 className="text-sm font-extrabold font-outfit text-white">
          Crop Health Field Progression Timeline
        </h4>
      </div>

      <div className="space-y-3">
        {timelineItems.map(([label, list]) => {
          // Sorted chronologically (oldest to newest)
          const sorted = [...list].sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
          const oldest = sorted[0];
          const newest = sorted[sorted.length - 1];

          const prevConcern = oldest.field_concern || 'Unrated';
          const newConcern = newest.field_concern || 'Unrated';

          return (
            <div key={label} className="p-3.5 rounded-2xl bg-slate-800/90 border border-slate-700/80 space-y-1.5 text-xs">
              <div className="font-bold text-emerald-300 font-outfit">
                {label} ({list.length} scans)
              </div>
              <div className="flex items-center gap-2 text-slate-300">
                <span>Field concern changed:</span>
                <span className="px-2 py-0.5 rounded bg-slate-700 font-mono font-bold">{prevConcern}</span>
                <ArrowRight className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span className="px-2 py-0.5 rounded bg-emerald-950 border border-emerald-500/50 font-mono font-bold text-emerald-200">
                  {newConcern}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
