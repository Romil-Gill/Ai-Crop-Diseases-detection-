import React from 'react';
import type { AdvisoryContent } from '../types/api';
import { ActionSection } from './ActionSection';
import { HealthyGuidance } from './HealthyGuidance';
import { SourceReferences } from './SourceReferences';
import { Sprout, PhoneCall, CheckCircle2 } from 'lucide-react';

interface AdvisoryPanelProps {
  advisory: AdvisoryContent;
  crop: string;
  condition: string;
  isHealthy: boolean;
}

export const AdvisoryPanel: React.FC<AdvisoryPanelProps> = ({
  advisory,
  crop,
  condition,
  isHealthy,
}) => {
  if (!advisory) return null;

  return (
    <div className="w-full bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6 transition-all">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-100">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100/90 text-emerald-900 text-xs font-bold mb-2 border border-emerald-300/80">
            <Sprout className="w-3.5 h-3.5 text-emerald-700" />
            <span>Farmer Action Plan</span>
          </div>
          <h3 className="text-xl sm:text-2xl font-extrabold font-outfit text-slate-900">
            What should you do now?
          </h3>
          <p className="text-sm text-slate-600 mt-1 font-medium">
            Non-chemical agricultural practices and field management for {crop} ({condition}).
          </p>
        </div>

        <div className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-xl bg-slate-100 text-slate-700 border border-slate-200 self-start sm:self-center shrink-0">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>Non-Chemical First</span>
        </div>
      </div>

      {/* Condition Overview Summary */}
      <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 text-xs sm:text-sm text-slate-700 leading-relaxed font-sans">
        <p>
          <strong className="text-slate-900 font-outfit">Overview:</strong> {advisory.overview}
        </p>
      </div>

      {/* Main Guidance Render */}
      {isHealthy ? (
        <HealthyGuidance crop={crop} advisory={advisory} />
      ) : (
        <ActionSection advisory={advisory} />
      )}

      {/* Expert Escalation Box */}
      {advisory.expert_escalation && (
        <div className="p-5 rounded-2xl bg-gradient-to-r from-emerald-900 to-green-900 text-white space-y-3 shadow-md">
          <div className="flex items-center justify-between gap-3">
            <h4 className="text-sm font-extrabold font-outfit uppercase tracking-wider flex items-center gap-2 text-emerald-200">
              <PhoneCall className="w-4 h-4 text-emerald-400" />
              When should you contact an expert?
            </h4>
          </div>
          <p className="text-xs text-emerald-100 leading-relaxed font-sans">
            {advisory.expert_escalation}
          </p>
          <div className="pt-1 flex items-center justify-between">
            <span className="text-[11px] text-emerald-300 font-medium">
              Krishi Vigyan Kendra (KVK) & Agricultural Extension Support
            </span>
            <button
              type="button"
              className="px-4 py-2 rounded-xl bg-white text-emerald-950 font-bold text-xs hover:bg-emerald-50 transition-colors shadow-xs"
              onClick={() => alert("Consult your local Krishi Vigyan Kendra (KVK) or Block Agriculture Development Officer for field inspection.")}
            >
              Consult Agricultural Expert
            </button>
          </div>
        </div>
      )}

      {/* Source References Accordion */}
      <SourceReferences sources={advisory.sources} />
    </div>
  );
};
