import React from 'react';
import type { SymptomVerifyResponse } from '../types/api';
import { ShieldCheck, AlertCircle, AlertTriangle, Cpu, CheckCircle2, Activity, CloudSun } from 'lucide-react';

interface EvidenceSummaryProps {
  confidence: number;
  verificationResult: SymptomVerifyResponse;
  weatherFavorability?: string; // 'LOW' | 'MODERATE' | 'HIGH' | 'NEUTRAL' | 'UNAVAILABLE'
}

export const EvidenceSummary: React.FC<EvidenceSummaryProps> = ({
  confidence,
  verificationResult,
  weatherFavorability = 'MODERATE',
}) => {
  const { symptom_verification, field_assessment, disclaimer } = verificationResult;
  const { agreement, agreement_label } = symptom_verification;
  const { concern_level, reason } = field_assessment;

  // Concern level color badges
  const concernBadgeStyle = {
    LOW: 'bg-emerald-100 text-emerald-900 border-emerald-300',
    MODERATE: 'bg-amber-100 text-amber-950 border-amber-300',
    HIGH: 'bg-rose-100 text-rose-950 border-rose-300 font-extrabold',
  }[concern_level] || 'bg-slate-100 text-slate-800 border-slate-200';

  const concernDotColor = {
    LOW: 'bg-emerald-600',
    MODERATE: 'bg-amber-600',
    HIGH: 'bg-rose-600 animate-pulse',
  }[concern_level] || 'bg-slate-500';

  const weatherBadgeStyle = {
    HIGH: 'bg-rose-100 text-rose-950 border-rose-300 font-extrabold',
    MODERATE: 'bg-amber-100 text-amber-950 border-amber-300',
    LOW: 'bg-emerald-100 text-emerald-950 border-emerald-300',
    NEUTRAL: 'bg-blue-100 text-blue-950 border-blue-300',
    UNAVAILABLE: 'bg-slate-700 text-slate-300 border-slate-600',
  }[weatherFavorability] || 'bg-slate-100 text-slate-800 border-slate-200';

  return (
    <div className="p-6 rounded-3xl bg-slate-900 text-white space-y-5 shadow-lg border border-slate-800">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Activity className="w-5 h-5 text-emerald-400" />
          <h4 className="text-base font-extrabold font-outfit text-white">
            Combined Evidence Summary
          </h4>
        </div>
        <span className="text-[11px] text-slate-400 font-mono">
          Independent Multi-Layer Decision Support
        </span>
      </div>

      {/* 4-Pill Evidence Breakdown */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {/* Pill 1: CNN Model Confidence */}
        <div className="p-3.5 rounded-2xl bg-slate-800/90 border border-slate-700/80 space-y-1">
          <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-300 font-outfit uppercase tracking-wider">
            <Cpu className="w-3.5 h-3.5 text-blue-400" />
            <span>1. AI Image Assessment</span>
          </div>
          <div className="text-base font-extrabold font-mono text-blue-300">
            {confidence.toFixed(1)}% <span className="text-xs font-normal text-slate-400">Confidence</span>
          </div>
        </div>

        {/* Pill 2: Symptom Check Agreement */}
        <div className="p-3.5 rounded-2xl bg-slate-800/90 border border-slate-700/80 space-y-1">
          <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-300 font-outfit uppercase tracking-wider">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            <span>2. Symptom Check</span>
          </div>
          <div className="text-sm font-extrabold font-outfit text-emerald-300 capitalize">
            {agreement_label}
          </div>
        </div>

        {/* Pill 3: Field Concern Level */}
        <div className="p-3.5 rounded-2xl bg-slate-800/90 border border-slate-700/80 space-y-1">
          <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-300 font-outfit uppercase tracking-wider">
            <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
            <span>3. Field Concern</span>
          </div>
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${concernDotColor}`} />
            <span className={`text-xs px-2 py-0.5 rounded-full border font-bold font-mono ${concernBadgeStyle}`}>
              {concern_level} CONCERN
            </span>
          </div>
        </div>

        {/* Pill 4: Weather Favorability */}
        <div className="p-3.5 rounded-2xl bg-slate-800/90 border border-slate-700/80 space-y-1">
          <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-300 font-outfit uppercase tracking-wider">
            <CloudSun className="w-3.5 h-3.5 text-indigo-400" />
            <span>4. Weather Favorability</span>
          </div>
          <div className="flex items-center gap-2">
            <span className={`text-xs px-2 py-0.5 rounded-full border font-bold font-mono ${weatherBadgeStyle}`}>
              {weatherFavorability} RISK
            </span>
          </div>
        </div>
      </div>

      {/* Field Concern Reason */}
      {reason && (
        <p className="text-xs text-slate-300 leading-relaxed font-sans bg-slate-800/50 p-3 rounded-xl border border-slate-700/50">
          <strong className="text-white">Field Triage Note:</strong> {reason}
        </p>
      )}

      {/* Disagreement Warning Card (Triggered when symptom agreement is LOW) */}
      {agreement === 'low' && (
        <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs space-y-2">
          <div className="flex items-center gap-2 font-bold font-outfit text-amber-300">
            <AlertCircle className="w-4 h-4 text-amber-400 shrink-0" />
            <span>Additional verification recommended</span>
          </div>
          <p className="leading-relaxed text-slate-300">
            Symptoms do not strongly match the AI assessment. We recommend inspecting another affected leaf on the same plant, rescanning, or consulting an extension officer before applying intensive management.
          </p>
        </div>
      )}

      {/* High-Concern Escalation Alert Card (Triggered when concern level is HIGH) */}
      {concern_level === 'HIGH' && (
        <div className="p-4 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-200 text-xs space-y-2">
          <div className="flex items-center gap-2 font-bold font-outfit text-rose-300">
            <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
            <span>Symptoms May Be Spreading</span>
          </div>
          <p className="leading-relaxed text-slate-300">
            Field reports indicate symptoms are appearing across multiple leaves or nearby plants. Inspect surrounding rows promptly and avoid moving infected plant material unnecessarily.
          </p>
        </div>
      )}

      {/* Triage Disclaimer */}
      <div className="text-[11px] text-slate-400 italic border-t border-slate-800 pt-3">
        * {disclaimer}
      </div>
    </div>
  );
};
