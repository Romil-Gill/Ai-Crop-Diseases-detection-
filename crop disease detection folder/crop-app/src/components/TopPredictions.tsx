import React from 'react';
import type { PredictionItem } from '../types/api';
import { Layers } from 'lucide-react';

interface TopPredictionsProps {
  predictions: PredictionItem[];
}

export const TopPredictions: React.FC<TopPredictionsProps> = ({ predictions }) => {
  if (!predictions || predictions.length === 0) return null;

  return (
    <div className="w-full bg-white rounded-3xl p-6 border border-slate-200 shadow-xs">
      <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
        <Layers className="w-4 h-4 text-emerald-600" />
        <h4 className="text-sm font-bold text-slate-900 font-outfit">
          Top-3 Softmax Probability Distribution
        </h4>
      </div>

      <div className="space-y-3">
        {predictions.map((pred, index) => {
          const isTop1 = index === 0;
          return (
            <div 
              key={index} 
              className={`p-3.5 rounded-2xl border transition-all ${
                isTop1 
                  ? 'bg-emerald-50/50 border-emerald-200' 
                  : 'bg-slate-50/60 border-slate-100'
              }`}
            >
              <div className="flex items-center justify-between text-xs font-semibold mb-1.5">
                <div className="flex items-center gap-2">
                  <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                    isTop1 ? 'bg-emerald-700 text-white' : 'bg-slate-200 text-slate-700'
                  }`}>
                    #{index + 1}
                  </span>
                  <span className="text-slate-900 font-bold">{pred.condition}</span>
                  <span className="text-slate-400 font-medium">({pred.crop})</span>
                </div>

                <span className={`font-mono font-bold ${
                  isTop1 ? 'text-emerald-700' : 'text-slate-600'
                }`}>
                  {pred.confidence.toFixed(2)}%
                </span>
              </div>

              <div className="w-full bg-slate-200/80 h-2 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    isTop1 ? 'bg-emerald-600' : 'bg-slate-400'
                  }`}
                  style={{ width: `${Math.max(2, pred.confidence)}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
