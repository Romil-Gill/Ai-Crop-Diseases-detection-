import React from 'react';
import type { PredictResponse } from '../types/api';
import { CheckCircle2, ShieldCheck, AlertCircle, Sparkles } from 'lucide-react';

interface DiagnosisCardProps {
  result: PredictResponse;
}

export const DiagnosisCard: React.FC<DiagnosisCardProps> = ({ result }) => {
  const { prediction, selected_crop, is_healthy } = result;

  return (
    <div className={`w-full rounded-3xl p-6 sm:p-8 border-2 shadow-sm transition-all ${is_healthy
      ? 'bg-gradient-to-br from-emerald-50 via-white to-green-50/50 border-emerald-300'
      : 'bg-gradient-to-br from-amber-50/60 via-white to-orange-50/30 border-amber-300'
      }`}>

      {/* Header Banner */}
      <div className="flex items-center justify-between gap-2 mb-6 border-b border-slate-200/60 pb-4">
        <div className="flex items-center gap-2">
          {is_healthy ? (
            <div className="w-9 h-9 rounded-xl bg-emerald-600 text-white flex items-center justify-center shadow-xs">
              <ShieldCheck className="w-5 h-5" />
            </div>
          ) : (
            <div className="w-9 h-9 rounded-xl bg-amber-600 text-white flex items-center justify-center shadow-xs">
              <AlertCircle className="w-5 h-5" />
            </div>
          )}
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
              AI Crop Assessment
            </span>
            <h3 className="text-sm font-extrabold text-slate-900 font-outfit">
              {prediction.crop} Leaf Assessment
            </h3>
          </div>
        </div>

        <div className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1 rounded-full bg-emerald-100/80 text-emerald-800 border border-emerald-300">
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
          <span>Crop Confirmed: {selected_crop || prediction.crop}</span>
        </div>
      </div>

      {/* Primary Diagnosis Display */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">
            Detected Condition
          </div>

          <h2 className={`text-2xl sm:text-3xl font-extrabold font-outfit tracking-tight ${is_healthy ? 'text-emerald-700' : 'text-slate-900'
            }`}>
            {prediction.condition}
          </h2>

          <p className="text-xs text-slate-500 mt-1 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            <span>AI model matched prediction with user-selected crop ({prediction.crop}).</span>
          </p>
        </div>

        {/* Confidence Percentage Badge */}
        <div className="flex flex-col items-start md:items-end justify-center bg-white border border-slate-200/80 rounded-2xl p-4 shadow-xs min-w-[160px]">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
            Model Confidence
          </span>
          <div className="flex items-baseline gap-1 mt-0.5">
            <span className="text-3xl font-extrabold font-outfit text-emerald-700">
              {prediction.confidence.toFixed(1)}
            </span>
            <span className="text-lg font-bold text-emerald-600">%</span>
          </div>
          <div className="w-full bg-slate-100 h-1.5 rounded-full mt-2 overflow-hidden">
            <div
              className="bg-emerald-600 h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, prediction.confidence)}%` }}
            />
          </div>
        </div>
      </div>

      {/* Healthy Notice Banner if healthy */}
      {is_healthy && (
        <div className="mt-6 p-3.5 bg-emerald-600/10 border border-emerald-300/60 rounded-xl flex items-center gap-3 text-xs text-emerald-900 font-medium">
          <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0" />
          <span>
            No symptoms of disease detected. Your {prediction.crop} leaf displays normal healthy tissue features.
          </span>
        </div>
      )}
    </div>
  );
};
