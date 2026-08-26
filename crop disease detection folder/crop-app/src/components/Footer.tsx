import React from 'react';
import { ShieldCheck, Sparkles } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="w-full bg-slate-900 text-slate-400 py-8 border-t border-slate-800 mt-auto">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 flex flex-col md:flex-row items-center justify-between gap-4 text-xs">
        
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-md bg-emerald-600 flex items-center justify-center text-white">
            <ShieldCheck className="w-3.5 h-3.5" />
          </div>
          <span className="font-semibold text-slate-200">FasalRakshak AI</span>
          <span className="text-slate-500">• SIH Hackathon Platform</span>
        </div>

        <div className="flex items-center gap-4 text-slate-400">
          <span className="flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-amber-400" /> MobileNetV2 Architecture
          </span>
          <span>•</span>
          <span>4 Crops (27 Classes)</span>
          <span>•</span>
          <span>Safe Diagnosis Engine</span>
        </div>

        <p className="text-slate-500 text-center md:text-right">
          Explainable Crop-Health & Early-Warning System
        </p>
      </div>
    </footer>
  );
};
