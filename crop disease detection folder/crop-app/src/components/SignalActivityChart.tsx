import React from 'react';
import type { DailyTrendItem } from '../types/api';
import { TrendingUp } from 'lucide-react';

interface SignalActivityChartProps {
  dailyTrend: DailyTrendItem[];
}

export const SignalActivityChart: React.FC<SignalActivityChartProps> = ({ dailyTrend }) => {
  if (dailyTrend.length === 0) {
    return (
      <div className="p-6 rounded-3xl bg-white border border-slate-200 text-center space-y-2 font-outfit">
        <p className="text-xs text-slate-500 font-medium">No trend data points for the selected filter window.</p>
      </div>
    );
  }

  const maxVal = Math.max(...dailyTrend.map((d) => d.signals), 1);

  return (
    <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-sm space-y-4 font-outfit">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-blue-600" />
          <h4 className="text-base font-extrabold text-slate-900">
            Reported Signal Activity
          </h4>
        </div>
        <span className="text-[11px] font-bold text-slate-500">
          Daily Community Reports
        </span>
      </div>

      <div className="pt-2 flex items-end gap-3 h-32 border-b border-slate-200 pb-2">
        {dailyTrend.map((item, idx) => {
          const heightPercent = Math.max((item.signals / maxVal) * 100, 12);
          const formattedDate = item.date.slice(5); // MM-DD

          return (
            <div key={idx} className="flex-1 flex flex-col items-center gap-1 group h-full justify-end">
              <span className="text-[10px] font-bold font-mono text-slate-600 opacity-0 group-hover:opacity-100 transition-opacity">
                {item.signals}
              </span>
              <div
                className="w-full bg-gradient-to-t from-blue-600 to-indigo-500 rounded-t-xl group-hover:from-blue-700 group-hover:to-indigo-600 transition-all"
                style={{ height: `${heightPercent}%` }}
              ></div>
              <span className="text-[10px] font-medium text-slate-500 font-mono">
                {formattedDate}
              </span>
            </div>
          );
        })}
      </div>

      <p className="text-[11px] text-slate-500 italic">
        * Daily signal count reflects community report submissions in the selected time window.
      </p>
    </div>
  );
};
