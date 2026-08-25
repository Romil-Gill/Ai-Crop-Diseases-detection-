import React from 'react';
import { Calendar, Filter } from 'lucide-react';

interface RadarFiltersProps {
  days: number;
  crop: string;
  onChangeDays: (days: number) => void;
  onChangeCrop: (crop: string) => void;
}

const TIME_WINDOWS = [
  { label: '24 Hours', value: 1 },
  { label: '7 Days', value: 7 },
  { label: '30 Days', value: 30 },
  { label: 'All Time', value: 0 },
];

const CROPS = ['All', 'Tomato', 'Rice', 'Sugarcane', 'Pumpkin', 'Wheat', 'Maize'];

export const RadarFilters: React.FC<RadarFiltersProps> = ({
  days,
  crop,
  onChangeDays,
  onChangeCrop,
}) => {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-3xl bg-white border border-slate-200 shadow-2xs font-outfit">
      {/* Time Window Buttons */}
      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1 text-slate-400 text-xs font-bold mr-1">
          <Calendar className="w-3.5 h-3.5" />
          <span>Window:</span>
        </div>
        <div className="flex items-center gap-1 overflow-x-auto no-scrollbar">
          {TIME_WINDOWS.map((tw) => (
            <button
              key={tw.value}
              type="button"
              onClick={() => onChangeDays(tw.value)}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                days === tw.value
                  ? 'bg-slate-900 text-white shadow-2xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {tw.label}
            </button>
          ))}
        </div>
      </div>

      {/* Crop Filter Tabs */}
      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1 text-slate-400 text-xs font-bold mr-1">
          <Filter className="w-3.5 h-3.5" />
          <span>Crop:</span>
        </div>
        <div className="flex items-center gap-1 overflow-x-auto no-scrollbar">
          {CROPS.map((c) => (
            <button
              key={c}
              type="button"
              onClick={() => onChangeCrop(c)}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                crop.toLowerCase() === c.toLowerCase()
                  ? 'bg-emerald-700 text-white shadow-2xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {c}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
