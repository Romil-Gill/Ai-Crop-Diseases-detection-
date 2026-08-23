import React from 'react';
import type { CropBreakdownItem } from '../types/api';
import { Sprout } from 'lucide-react';

interface CropBreakdownProps {
  breakdown: CropBreakdownItem[];
}

export const CropBreakdown: React.FC<CropBreakdownProps> = ({ breakdown }) => {
  if (breakdown.length === 0) return null;

  const total = breakdown.reduce((acc, curr) => acc + curr.signals, 0);

  const getCropColor = (crop: string) => {
    switch (crop.toLowerCase()) {
      case 'tomato':
        return 'bg-rose-500 text-rose-100';
      case 'rice':
        return 'bg-blue-600 text-blue-100';
      case 'sugarcane':
        return 'bg-emerald-600 text-emerald-100';
      case 'pumpkin':
        return 'bg-amber-500 text-amber-100';
      default:
        return 'bg-slate-700 text-slate-100';
    }
  };

  return (
    <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-sm space-y-4 font-outfit">
      <div className="flex items-center gap-2">
        <Sprout className="w-5 h-5 text-emerald-600" />
        <h4 className="text-base font-extrabold text-slate-900">
          Crop Distribution Breakdown
        </h4>
      </div>

      <div className="space-y-3">
        {breakdown.map((item) => {
          const percent = total > 0 ? Math.round((item.signals / total) * 100) : 0;

          return (
            <div key={item.crop} className="space-y-1">
              <div className="flex items-center justify-between text-xs font-bold">
                <span className="text-slate-900">{item.crop}</span>
                <span className="text-slate-600 font-mono">{item.signals} signals ({percent}%)</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all ${getCropColor(item.crop)}`}
                  style={{ width: `${percent}%` }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
