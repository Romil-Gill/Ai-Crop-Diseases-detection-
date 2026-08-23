import React from 'react';
import type { FieldSpreadOption } from '../types/api';
import { Layers } from 'lucide-react';

interface FieldSpreadSelectorProps {
  options: FieldSpreadOption[];
  selectedOption: string;
  onSelect: (id: string) => void;
}

export const FieldSpreadSelector: React.FC<FieldSpreadSelectorProps> = ({
  options,
  selectedOption,
  onSelect,
}) => {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-800 font-outfit">
        <Layers className="w-4 h-4 text-emerald-600" />
        <span>How widely are similar symptoms appearing?</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        {options.map((opt) => {
          const isSelected = selectedOption === opt.id;
          return (
            <button
              key={opt.id}
              type="button"
              onClick={() => onSelect(opt.id)}
              className={`p-3 rounded-2xl text-left border transition-all ${
                isSelected
                  ? 'bg-emerald-50 border-emerald-500 shadow-2xs ring-1 ring-emerald-500/50'
                  : 'bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50'
              }`}
            >
              <div className="font-bold text-xs text-slate-900 font-outfit">
                {opt.label}
              </div>
              <div className="text-[11px] text-slate-500 mt-0.5 leading-snug">
                {opt.description}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
