import React, { useState } from 'react';
import { BookOpen, ExternalLink, ChevronDown, ChevronUp, ShieldCheck } from 'lucide-react';
import type { AdvisorySource } from '../types/api';

interface SourceReferencesProps {
  sources: AdvisorySource[];
}

export const SourceReferences: React.FC<SourceReferencesProps> = ({ sources }) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-4 border-t border-slate-200/80 pt-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-700">
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-100/90 text-emerald-900 text-[11px] font-bold border border-emerald-300/80">
            <ShieldCheck className="w-3 h-3 text-emerald-700" />
            Source-backed guidance
          </span>
          <span className="text-slate-500 text-[11px] hidden sm:inline">
            Verified agricultural extension sources
          </span>
        </div>

        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-1 text-xs font-semibold text-slate-600 hover:text-emerald-800 transition-colors py-1"
        >
          <BookOpen className="w-3.5 h-3.5 text-emerald-700" />
          <span>Advisory sources ({sources.length})</span>
          {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {isOpen && (
        <div className="mt-3 space-y-2 p-3.5 rounded-2xl bg-slate-50 border border-slate-200 text-xs font-sans">
          {sources.map((src, idx) => (
            <div key={idx} className="flex items-start justify-between gap-3 p-2.5 rounded-xl bg-white border border-slate-200/80">
              <div>
                <span className="font-bold text-slate-900 block font-outfit">
                  {src.organization}
                </span>
                <span className="text-slate-600 text-[11px] block mt-0.5">
                  {src.title}
                </span>
              </div>
              {src.url && (
                <a
                  href={src.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 hover:text-emerald-900 hover:underline shrink-0 pt-0.5"
                >
                  <span>Verify</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
