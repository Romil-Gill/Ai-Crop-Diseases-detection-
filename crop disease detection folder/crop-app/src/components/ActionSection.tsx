import React from 'react';
import { CheckCircle2, Eye, ShieldCheck, Search } from 'lucide-react';
import type { AdvisoryContent } from '../types/api';

interface ActionSectionProps {
  advisory: AdvisoryContent;
}

export const ActionSection: React.FC<ActionSectionProps> = ({ advisory }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
      {/* 1. TODAY: Immediate Actions */}
      <div className="bg-emerald-900/5 border border-emerald-800/20 p-5 rounded-2xl space-y-3">
        <div className="flex items-center gap-2 text-emerald-950 font-extrabold text-sm font-outfit uppercase tracking-wider">
          <span className="bg-emerald-800 text-white text-[10px] px-2 py-0.5 rounded font-mono">
            TODAY
          </span>
          <CheckCircle2 className="w-4 h-4 text-emerald-700" />
          <span>Immediate Non-Chemical Actions</span>
        </div>
        <ul className="space-y-2 text-xs text-slate-700 leading-relaxed font-sans">
          {advisory.immediate_actions.map((action, idx) => (
            <li key={idx} className="flex items-start gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 shrink-0 mt-1.5" />
              <span>{action}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* 2. MONITOR: Next Few Days */}
      <div className="bg-amber-500/10 border border-amber-500/25 p-5 rounded-2xl space-y-3">
        <div className="flex items-center gap-2 text-amber-950 font-extrabold text-sm font-outfit uppercase tracking-wider">
          <span className="bg-amber-700 text-white text-[10px] px-2 py-0.5 rounded font-mono">
            MONITOR
          </span>
          <Eye className="w-4 h-4 text-amber-700" />
          <span>Next Few Days Checklist</span>
        </div>
        <ul className="space-y-2 text-xs text-slate-700 leading-relaxed font-sans">
          {advisory.monitoring.map((item, idx) => (
            <li key={idx} className="flex items-start gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-600 shrink-0 mt-1.5" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* 3. PREVENT: Reduce Future Risk */}
      <div className="bg-blue-500/5 border border-blue-500/20 p-5 rounded-2xl space-y-3">
        <div className="flex items-center gap-2 text-blue-950 font-extrabold text-sm font-outfit uppercase tracking-wider">
          <span className="bg-blue-700 text-white text-[10px] px-2 py-0.5 rounded font-mono">
            PREVENT
          </span>
          <ShieldCheck className="w-4 h-4 text-blue-700" />
          <span>Future Crop Protection</span>
        </div>
        <ul className="space-y-2 text-xs text-slate-700 leading-relaxed font-sans">
          {advisory.prevention.map((item, idx) => (
            <li key={idx} className="flex items-start gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0 mt-1.5" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* 4. WATCH FOR: Common Symptoms */}
      <div className="bg-slate-100/80 border border-slate-200/90 p-5 rounded-2xl space-y-3">
        <div className="flex items-center gap-2 text-slate-900 font-extrabold text-sm font-outfit uppercase tracking-wider">
          <span className="bg-slate-700 text-white text-[10px] px-2 py-0.5 rounded font-mono">
            WATCH FOR
          </span>
          <Search className="w-4 h-4 text-slate-700" />
          <span>Common Symptoms to Confirm</span>
        </div>
        <ul className="space-y-2 text-xs text-slate-700 leading-relaxed font-sans">
          {advisory.common_symptoms.map((symptom, idx) => (
            <li key={idx} className="flex items-start gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-slate-500 shrink-0 mt-1.5" />
              <span>{symptom}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
