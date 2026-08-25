import React, { useState } from 'react';
import type { TreatmentOptions } from '../types/api';
import { ShieldCheck, Sprout, Bug, FlaskConical, AlertTriangle, Building2, ExternalLink, HelpCircle, CheckCircle2 } from 'lucide-react';

interface TreatmentOptionsCardProps {
  treatmentOptions?: TreatmentOptions | null;
  isReliable: boolean;
}

export const TreatmentOptionsCard: React.FC<TreatmentOptionsCardProps> = ({ treatmentOptions, isReliable }) => {
  const [activeTab, setActiveTab] = useState<'cultural' | 'biological' | 'chemical' | 'expert'>('cultural');

  if (!isReliable || !treatmentOptions || !treatmentOptions.available) {
    return null;
  }

  // If crop is healthy or no treatment required
  if (treatmentOptions.treatment_required === false) {
    return (
      <div className="bg-emerald-50/80 border border-emerald-200 rounded-2xl p-5 mb-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-9 h-9 rounded-xl bg-emerald-100 flex items-center justify-center text-emerald-700 font-bold">
            <CheckCircle2 className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-emerald-950 font-outfit">Treatment Options: Not Required</h3>
            <p className="text-xs text-emerald-700">Healthy crop foliage. No disease treatment is necessary.</p>
          </div>
        </div>
        <p className="text-xs text-emerald-800 mt-2 bg-white/70 p-3 rounded-xl border border-emerald-100">
          {treatmentOptions.message || 'Continue regular good agricultural management, balanced fertilization, and crop monitoring.'}
        </p>
      </div>
    );
  }

  const cultural = treatmentOptions.cultural_controls || [];
  const biological = treatmentOptions.biological_controls || [];
  const chemical = treatmentOptions.chemical_options || [];
  const expert = treatmentOptions.expert_escalation || [];
  const sources = treatmentOptions.sources || [];
  const immediate = treatmentOptions.immediate_actions || [];

  return (
    <div id="treatment-options-section" className="bg-white border border-slate-200/80 rounded-2xl p-5 md:p-6 shadow-sm mb-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 mb-5 border-b border-slate-100">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 font-bold shadow-xs">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-lg font-bold text-slate-900 font-outfit">Treatment & Protection Options</h3>
              <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-700 bg-indigo-50 border border-indigo-200 px-2 py-0.5 rounded-md">
                Source-Backed
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Possible crop-protection approaches for <span className="font-semibold text-slate-700">{treatmentOptions.disease || treatmentOptions.crop}</span>
            </p>
          </div>
        </div>
      </div>

      {/* Mandatory Regional Safety Disclaimer Banner */}
      <div className="mb-5 bg-amber-50/90 border border-amber-200/90 rounded-xl p-3.5 flex items-start gap-3 text-xs text-amber-900">
        <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <span className="font-bold text-amber-950">Official Agricultural Notice: </span>
          {treatmentOptions.safety_notice || "Use only products registered for this crop and disease in your region. Follow official product labels and local agricultural guidance."}
        </div>
      </div>

      {/* Immediate Actions Summary */}
      {immediate.length > 0 && (
        <div className="mb-5 bg-slate-50 rounded-xl p-3.5 border border-slate-200/60">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <Sprout className="w-3.5 h-3.5 text-emerald-600" />
            Immediate Field Actions
          </h4>
          <ul className="space-y-1.5 text-xs text-slate-700">
            {immediate.map((act, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
                <span>{act}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Tab Navigation */}
      <div className="flex border-b border-slate-200 mb-5 overflow-x-auto no-scrollbar gap-2">
        <button
          onClick={() => setActiveTab('cultural')}
          className={`flex items-center gap-2 px-3.5 py-2 text-xs font-bold border-b-2 transition-colors whitespace-nowrap cursor-pointer ${
            activeTab === 'cultural'
              ? 'border-emerald-600 text-emerald-700 bg-emerald-50/50 rounded-t-lg'
              : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <Sprout className="w-3.5 h-3.5" />
          Cultural ({cultural.length})
        </button>

        <button
          onClick={() => setActiveTab('biological')}
          className={`flex items-center gap-2 px-3.5 py-2 text-xs font-bold border-b-2 transition-colors whitespace-nowrap cursor-pointer ${
            activeTab === 'biological'
              ? 'border-teal-600 text-teal-700 bg-teal-50/50 rounded-t-lg'
              : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <Bug className="w-3.5 h-3.5" />
          Biological ({biological.length})
        </button>

        <button
          onClick={() => setActiveTab('chemical')}
          className={`flex items-center gap-2 px-3.5 py-2 text-xs font-bold border-b-2 transition-colors whitespace-nowrap cursor-pointer ${
            activeTab === 'chemical'
              ? 'border-indigo-600 text-indigo-700 bg-indigo-50/50 rounded-t-lg'
              : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <FlaskConical className="w-3.5 h-3.5" />
          Chemical Active Ingredients ({chemical.length})
        </button>

        <button
          onClick={() => setActiveTab('expert')}
          className={`flex items-center gap-2 px-3.5 py-2 text-xs font-bold border-b-2 transition-colors whitespace-nowrap cursor-pointer ${
            activeTab === 'expert'
              ? 'border-rose-600 text-rose-700 bg-rose-50/50 rounded-t-lg'
              : 'border-transparent text-slate-600 hover:text-slate-900'
          }`}
        >
          <HelpCircle className="w-3.5 h-3.5" />
          Expert Escalation
        </button>
      </div>

      {/* Tab Content */}
      <div className="min-h-[160px]">
        {/* Cultural Controls Tab */}
        {activeTab === 'cultural' && (
          <div className="space-y-3">
            <p className="text-xs text-slate-600 mb-3">
              Non-chemical field sanitation, crop rotation, and soil management practices:
            </p>
            {cultural.length > 0 ? (
              <ul className="space-y-2 text-xs text-slate-800">
                {cultural.map((item, i) => (
                  <li key={i} className="flex items-start gap-2.5 bg-slate-50 p-3 rounded-xl border border-slate-100">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-xs text-slate-400 italic">No specific cultural control options listed.</p>
            )}
          </div>
        )}

        {/* Biological Controls Tab */}
        {activeTab === 'biological' && (
          <div className="space-y-3">
            <p className="text-xs text-slate-600 mb-3">
              Verified bio-fungicides and bio-control agent options:
            </p>
            {biological.length > 0 ? (
              <ul className="space-y-2 text-xs text-slate-800">
                {biological.map((item, i) => (
                  <li key={i} className="flex items-start gap-2.5 bg-teal-50/60 p-3 rounded-xl border border-teal-100 text-teal-950">
                    <Bug className="w-4 h-4 text-teal-600 shrink-0 mt-0.5" />
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="bg-slate-50 p-4 rounded-xl text-xs text-slate-500 text-center border border-slate-100">
                No specific biological control agents are currently cataloged for this disease in the verified database.
              </div>
            )}
          </div>
        )}

        {/* Chemical Active Ingredients Tab */}
        {activeTab === 'chemical' && (
          <div className="space-y-3">
            <div className="bg-indigo-50/70 p-3 rounded-xl border border-indigo-100 text-xs text-indigo-900 mb-3">
              <span className="font-bold">Active Ingredient Categories: </span>
              Shows verified chemical compounds recommended in agricultural extension packages. Commercial brand names are excluded.
            </div>

            {chemical.length > 0 ? (
              <div className="space-y-3">
                {chemical.map((chem, i) => (
                  <div key={i} className="bg-slate-50 p-4 rounded-xl border border-slate-200/80 space-y-2">
                    <div className="flex items-center justify-between">
                      <h5 className="font-bold text-sm text-slate-900 font-outfit flex items-center gap-2">
                        <FlaskConical className="w-4 h-4 text-indigo-600" />
                        {chem.active_ingredient}
                      </h5>
                      <span className="text-[10px] font-semibold text-slate-500 bg-white px-2 py-0.5 rounded border border-slate-200">
                        Active Ingredient
                      </span>
                    </div>

                    <p className="text-xs text-slate-700">
                      <span className="font-semibold text-slate-900">Purpose: </span>
                      {chem.purpose}
                    </p>

                    <p className="text-xs text-slate-600 bg-white p-2.5 rounded-lg border border-slate-100 leading-relaxed">
                      <span className="font-semibold text-amber-800">Usage Note: </span>
                      {chem.restrictions_or_notes}
                    </p>

                    {chem.source && (
                      <div className="text-[11px] text-slate-400 flex items-center gap-1.5 pt-1">
                        <Building2 className="w-3 h-3 text-slate-400" />
                        <span>Source: {chem.source}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-slate-50 p-4 rounded-xl text-xs text-slate-500 text-center border border-slate-100">
                No chemical active ingredients specified for this condition.
              </div>
            )}
          </div>
        )}

        {/* Expert Escalation Tab */}
        {activeTab === 'expert' && (
          <div className="space-y-3">
            <p className="text-xs text-slate-600 mb-3">
              When to seek escalation from local agricultural officers or KVK specialists:
            </p>
            {expert.length > 0 ? (
              <ul className="space-y-2 text-xs text-slate-800">
                {expert.map((exp, i) => (
                  <li key={i} className="flex items-start gap-2.5 bg-rose-50/70 p-3 rounded-xl border border-rose-100 text-rose-950">
                    <HelpCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                    <span className="leading-relaxed">{exp}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-xs text-slate-500">Consult your local Krishi Vigyan Kendra (KVK) if disease spreads rapidly across field blocks.</p>
            )}
          </div>
        )}
      </div>

      {/* Verified Sources Footer */}
      {sources.length > 0 && (
        <div className="mt-6 pt-4 border-t border-slate-100 flex flex-col gap-2">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
            <Building2 className="w-3.5 h-3.5 text-slate-400" />
            Verified Source Authorities
          </span>
          <div className="flex flex-wrap gap-2">
            {sources.map((src, i) => (
              <a
                key={i}
                href={src.url || '#'}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 text-[11px] font-medium text-slate-700 bg-slate-100/80 hover:bg-slate-200/80 px-2.5 py-1 rounded-lg transition-colors"
              >
                <span>{src.organization}</span>
                <ExternalLink className="w-3 h-3 text-slate-400" />
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
