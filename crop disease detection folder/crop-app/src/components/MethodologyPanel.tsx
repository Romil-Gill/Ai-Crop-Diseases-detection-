import React, { useState } from 'react';
import { ChevronDown, ShieldCheck, Info, FileText } from 'lucide-react';

export const MethodologyPanel: React.FC = () => {
  const [open, setOpen] = useState<boolean>(false);

  return (
    <div className="rounded-3xl bg-white border border-slate-200 shadow-sm overflow-hidden font-outfit">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="w-full p-5 flex items-center justify-between hover:bg-slate-50 transition-colors text-left"
      >
        <div className="flex items-center gap-2">
          <Info className="w-5 h-5 text-blue-600" />
          <div>
            <h4 className="text-sm font-extrabold text-slate-900">
              Methodology & Privacy Framework
            </h4>
            <p className="text-xs text-slate-500 font-sans">
              How the Community Disease Radar protects farmer identity while aggregating regional signals.
            </p>
          </div>
        </div>
        <ChevronDown className={`w-5 h-5 text-slate-400 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>

      {open && (
        <div className="p-5 pt-0 border-t border-slate-100 space-y-4 text-xs text-slate-700 leading-relaxed font-sans">
          <div className="space-y-1.5">
            <h5 className="font-bold font-outfit text-slate-900 flex items-center gap-1.5">
              <FileText className="w-4 h-4 text-blue-600" />
              <span>1. Signal Origin & Validation</span>
            </h5>
            <p>
              Signals originate strictly from user-submitted assessments where FasalRakshak AI confirms a <strong>reliable diagnosis</strong>. Crop mismatches, low-confidence predictions, and healthy baseline assessments are automatically excluded from disease signal counts.
            </p>
          </div>

          <div className="space-y-1.5">
            <h5 className="font-bold font-outfit text-slate-900 flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>2. Privacy by Design</span>
            </h5>
            <p>
              Public map coordinates are intentionally coarsened to 1 decimal place (~11km regional grid). Farm locations, leaf images, base64 payloads, exact GPS coordinates, and personal user identifiers are <strong>NEVER</strong> stored in community databases or transmitted in public API responses.
            </p>
          </div>

          <div className="space-y-1.5">
            <h5 className="font-bold font-outfit text-slate-900 flex items-center gap-1.5">
              <Info className="w-4 h-4 text-amber-600" />
              <span>3. Activity Level Interpretation</span>
            </h5>
            <p>
              Activity levels (<code>LOW</code>, <code>MODERATE</code>, <code>ELEVATED</code>) measure report volume and recency within an area cluster. They represent community-reported signals and do <strong>NOT</strong> constitute laboratory-confirmed cases or official government outbreak declarations.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
