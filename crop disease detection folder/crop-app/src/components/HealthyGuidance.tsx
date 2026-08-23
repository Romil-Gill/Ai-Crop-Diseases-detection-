import React from 'react';
import { ShieldCheck, CheckCircle2, AlertTriangle } from 'lucide-react';
import type { AdvisoryContent } from '../types/api';

interface HealthyGuidanceProps {
  crop: string;
  advisory: AdvisoryContent;
}

export const HealthyGuidance: React.FC<HealthyGuidanceProps> = ({ crop, advisory }) => {
  return (
    <div className="space-y-5">
      {/* Primary Healthy Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-emerald-50 via-green-50/50 to-white border-2 border-emerald-300 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-emerald-600 text-white flex items-center justify-center shrink-0 shadow-md">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h4 className="text-lg font-bold font-outfit text-emerald-950">
              Leaf Appears Healthy
            </h4>
            <p className="text-xs text-emerald-800 mt-0.5 font-medium">
              No visible symptoms of fungal, bacterial, or viral disease detected on this leaf sample.
            </p>
          </div>
        </div>
      </div>

      {/* Recommended Care Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-5 rounded-2xl bg-white border border-slate-200 space-y-2">
          <h5 className="text-xs font-bold uppercase tracking-wider text-slate-800 flex items-center gap-1.5 font-outfit">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            Routine Crop Maintenance
          </h5>
          <ul className="space-y-1.5 text-xs text-slate-600 font-sans">
            {advisory.immediate_actions.map((act, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0 mt-1.5" />
                <span>{act}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="p-5 rounded-2xl bg-white border border-slate-200 space-y-2">
          <h5 className="text-xs font-bold uppercase tracking-wider text-slate-800 flex items-center gap-1.5 font-outfit">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            Preventive Field Hygiene
          </h5>
          <ul className="space-y-1.5 text-xs text-slate-600 font-sans">
            {advisory.prevention.map((prev, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0 mt-1.5" />
                <span>{prev}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Scope Disclaimer */}
      <div className="p-3.5 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-900 flex items-center gap-2.5 font-sans">
        <AlertTriangle className="w-4 h-4 text-amber-700 shrink-0" />
        <span>
          <strong>Important Note:</strong> This assessment applies strictly to the uploaded leaf image. Inspect surrounding {crop} plants and roots periodically for uninspected symptoms.
        </span>
      </div>
    </div>
  );
};
