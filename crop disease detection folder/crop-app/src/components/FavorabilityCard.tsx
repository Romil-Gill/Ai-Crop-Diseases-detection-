import React from 'react';
import type { DiseaseWeatherContext } from '../types/api';
import { ShieldAlert, CheckCircle2, XCircle, Info } from 'lucide-react';

interface FavorabilityCardProps {
  diseaseContext: DiseaseWeatherContext;
}

export const FavorabilityCard: React.FC<FavorabilityCardProps> = ({ diseaseContext }) => {
  const { favorability, favorability_label, matched_factors, unmatched_factors, explanation, disclaimer, sources } = diseaseContext;

  const badgeStyle = {
    HIGH: 'bg-rose-100 text-rose-950 border-rose-300 font-extrabold',
    MODERATE: 'bg-amber-100 text-amber-950 border-amber-300 font-bold',
    LOW: 'bg-emerald-100 text-emerald-950 border-emerald-300 font-bold',
    NEUTRAL: 'bg-slate-100 text-slate-800 border-slate-200',
    UNAVAILABLE: 'bg-slate-100 text-slate-600 border-slate-200',
  }[favorability] || 'bg-slate-100 text-slate-800 border-slate-200';

  const dotColor = {
    HIGH: 'bg-rose-600 animate-pulse',
    MODERATE: 'bg-amber-600',
    LOW: 'bg-emerald-600',
    NEUTRAL: 'bg-blue-500',
    UNAVAILABLE: 'bg-slate-400',
  }[favorability] || 'bg-slate-400';

  return (
    <div className="p-5 rounded-2xl bg-white border border-slate-200 space-y-4 shadow-2xs">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-slate-700" />
          <h4 className="text-sm font-bold font-outfit text-slate-900">
            Disease Environmental Favorability
          </h4>
        </div>
        <div className="flex items-center gap-1.5">
          <span className={`w-2 h-2 rounded-full ${dotColor}`} />
          <span className={`text-xs px-2.5 py-0.5 rounded-full border font-mono ${badgeStyle}`}>
            {favorability_label}
          </span>
        </div>
      </div>

      <p className="text-xs text-slate-700 leading-relaxed font-sans">
        {explanation}
      </p>

      {/* Matched Factors */}
      {matched_factors.length > 0 && (
        <div className="space-y-2">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 font-outfit block">
            Environmental Match Factors
          </span>
          <div className="flex flex-wrap gap-2">
            {matched_factors.map((factor, idx) => (
              <div
                key={idx}
                className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-950 text-xs font-semibold"
              >
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                <span>{factor}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Unmatched Factors */}
      {unmatched_factors.length > 0 && (
        <div className="space-y-2">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 font-outfit block">
            Unmatched Factors
          </span>
          <div className="flex flex-wrap gap-2">
            {unmatched_factors.map((factor, idx) => (
              <div
                key={idx}
                className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-slate-50 border border-slate-200 text-slate-700 text-xs font-medium"
              >
                <XCircle className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                <span>{factor}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Citations */}
      {sources.length > 0 && (
        <div className="text-[11px] text-slate-500 font-sans border-t border-slate-100 pt-2.5">
          <strong className="text-slate-700">Source Basis:</strong> {sources.join('; ')}
        </div>
      )}

      {/* Disclaimer */}
      <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-[11px] text-slate-600 flex items-start gap-2 leading-relaxed">
        <Info className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
        <span>{disclaimer}</span>
      </div>
    </div>
  );
};
