import React from 'react';
import { Database, Sparkles } from 'lucide-react';

interface DataModeToggleProps {
  mode: 'live' | 'demo';
  onChangeMode: (mode: 'live' | 'demo') => void;
}

export const DataModeToggle: React.FC<DataModeToggleProps> = ({ mode, onChangeMode }) => {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 rounded-3xl bg-slate-900 text-white shadow-md border border-slate-800 font-outfit">
      <div className="flex items-center gap-2.5">
        <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-emerald-400">
          <Database className="w-4 h-4" />
        </div>
        <div>
          <div className="text-xs font-bold text-slate-200">
            Telemetry Data Source Mode
          </div>
          <p className="text-[11px] text-slate-400 font-sans">
            {mode === 'demo'
              ? 'Displaying synthetic regional demo signals for SIH presentation.'
              : 'Displaying real local SQLite community signals.'}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-1.5 bg-slate-800/90 p-1 rounded-2xl border border-slate-700">
        <button
          type="button"
          onClick={() => onChangeMode('live')}
          className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
            mode === 'live'
              ? 'bg-emerald-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          LIVE LOCAL DATA
        </button>

        <button
          type="button"
          onClick={() => onChangeMode('demo')}
          className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
            mode === 'demo'
              ? 'bg-amber-500 text-slate-950 font-black shadow-sm'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>DEMO DATA</span>
        </button>
      </div>
    </div>
  );
};
