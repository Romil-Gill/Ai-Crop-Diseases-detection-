import React from 'react';
import type { ScanRecord } from '../types/api';
import { Calendar, MapPin, Trash2, Cpu, CheckCircle2, ShieldCheck, CloudSun } from 'lucide-react';

interface ScanHistoryCardProps {
  scan: ScanRecord;
  onDelete?: (id: number) => void;
}

export const ScanHistoryCard: React.FC<ScanHistoryCardProps> = ({ scan, onDelete }) => {
  const formattedDate = new Date(scan.created_at).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });

  return (
    <div className="p-5 rounded-3xl bg-white border border-slate-200 shadow-sm space-y-4 transition-all hover:border-slate-300">
      {/* Header Info */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          <span className="px-3 py-1 rounded-full bg-slate-900 text-white font-extrabold text-xs font-outfit uppercase tracking-wider">
            {scan.crop}
          </span>
          <h4 className="text-base font-extrabold font-outfit text-slate-900">
            {scan.condition}
          </h4>
        </div>

        <div className="flex items-center gap-3 text-xs text-slate-500 font-medium">
          <div className="flex items-center gap-1">
            <Calendar className="w-3.5 h-3.5 text-slate-400" />
            <span>{formattedDate}</span>
          </div>
          {scan.location_name && (
            <div className="flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5 text-slate-400" />
              <span>{scan.location_name}</span>
            </div>
          )}
          {onDelete && (
            <button
              type="button"
              onClick={() => onDelete(scan.id)}
              className="p-1 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors ml-1"
              title="Delete scan record"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* 4-Pill Evidence Badges */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
        {/* Pill 1: CNN Model Confidence */}
        <div className="p-2.5 rounded-2xl bg-blue-50 border border-blue-200 space-y-0.5">
          <div className="flex items-center gap-1 text-[10px] font-bold text-blue-800 font-outfit uppercase">
            <Cpu className="w-3 h-3 text-blue-600" />
            <span>AI Model</span>
          </div>
          <div className="font-extrabold font-mono text-blue-900">
            {scan.model_confidence.toFixed(1)}%
          </div>
        </div>

        {/* Pill 2: Symptom Check */}
        <div className="p-2.5 rounded-2xl bg-emerald-50 border border-emerald-200 space-y-0.5">
          <div className="flex items-center gap-1 text-[10px] font-bold text-emerald-800 font-outfit uppercase">
            <CheckCircle2 className="w-3 h-3 text-emerald-600" />
            <span>Symptom Check</span>
          </div>
          <div className="font-bold text-emerald-900 capitalize">
            {scan.symptom_agreement || 'Skipped'}
          </div>
        </div>

        {/* Pill 3: Field Concern */}
        <div className="p-2.5 rounded-2xl bg-amber-50 border border-amber-200 space-y-0.5">
          <div className="flex items-center gap-1 text-[10px] font-bold text-amber-800 font-outfit uppercase">
            <ShieldCheck className="w-3 h-3 text-amber-600" />
            <span>Field Concern</span>
          </div>
          <div className="font-bold text-amber-900 font-mono">
            {scan.field_concern ? `${scan.field_concern}` : 'Not Evaluated'}
          </div>
        </div>

        {/* Pill 4: Weather Favorability */}
        <div className="p-2.5 rounded-2xl bg-indigo-50 border border-indigo-200 space-y-0.5">
          <div className="flex items-center gap-1 text-[10px] font-bold text-indigo-800 font-outfit uppercase">
            <CloudSun className="w-3 h-3 text-indigo-600" />
            <span>Weather Risk</span>
          </div>
          <div className="font-bold text-indigo-900 font-mono">
            {scan.weather_favorability ? `${scan.weather_favorability}` : 'Neutral'}
          </div>
        </div>
      </div>
    </div>
  );
};
