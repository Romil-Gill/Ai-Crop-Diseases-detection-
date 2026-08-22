import React from 'react';
import { RefreshCw, Trash2, Microscope, Scan, CheckCircle } from 'lucide-react';
import type { SupportedCrop } from '../types/api';

interface ScanPreviewProps {
  imageSrc: string;
  selectedCrop: SupportedCrop;
  onAnalyze: () => void;
  onReplace: () => void;
  onRemove: () => void;
  isLoading: boolean;
}

export const ScanPreview: React.FC<ScanPreviewProps> = ({
  imageSrc,
  selectedCrop,
  onAnalyze,
  onReplace,
  onRemove,
  isLoading,
}) => {
  return (
    <div className="w-full bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Scan className="w-5 h-5 text-emerald-600" />
          <h3 className="text-base font-bold text-slate-900 font-outfit">
            Scan Reticle Preview
          </h3>
        </div>
        <span className="text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 px-2.5 py-1 rounded-full flex items-center gap-1">
          <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
          Target: {selectedCrop}
        </span>
      </div>

      {/* Visual Scanner Frame / Reticle */}
      <div className="relative max-w-md mx-auto aspect-square rounded-2xl overflow-hidden bg-slate-950 border-4 border-slate-900 shadow-inner group">
        <img
          src={imageSrc}
          alt="Crop Leaf Preview"
          className="w-full h-full object-cover"
        />

        {/* Reticle Corner Guides */}
        <div className="absolute top-3 left-3 w-8 h-8 border-t-2 border-l-2 border-emerald-400 rounded-tl-lg pointer-events-none" />
        <div className="absolute top-3 right-3 w-8 h-8 border-t-2 border-r-2 border-emerald-400 rounded-tr-lg pointer-events-none" />
        <div className="absolute bottom-3 left-3 w-8 h-8 border-b-2 border-l-2 border-emerald-400 rounded-bl-lg pointer-events-none" />
        <div className="absolute bottom-3 right-3 w-8 h-8 border-b-2 border-r-2 border-emerald-400 rounded-br-lg pointer-events-none" />

        {/* Center Alignment Reticle Crosshair */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-40">
          <div className="w-16 h-16 border border-emerald-400/60 rounded-full flex items-center justify-center">
            <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full" />
          </div>
        </div>

        {/* Target Badge */}
        <div className="absolute bottom-3 left-1/2 -translate-x-1/2 bg-black/60 backdrop-blur-md text-emerald-300 text-[11px] font-mono font-medium px-3 py-1 rounded-full border border-emerald-500/30">
          224x224 RGB Frame
        </div>
      </div>

      {/* Control Buttons */}
      <div className="mt-6 flex flex-col sm:flex-row items-center justify-center gap-3">
        <button
          type="button"
          onClick={onRemove}
          disabled={isLoading}
          className="w-full sm:w-auto px-4 py-2.5 rounded-xl border border-slate-200 hover:bg-rose-50 hover:border-rose-200 hover:text-rose-700 text-slate-600 text-xs font-semibold transition-all flex items-center justify-center gap-1.5"
        >
          <Trash2 className="w-4 h-4" />
          Remove Image
        </button>

        <button
          type="button"
          onClick={onReplace}
          disabled={isLoading}
          className="w-full sm:w-auto px-4 py-2.5 rounded-xl border border-slate-200 hover:bg-slate-100 text-slate-700 text-xs font-semibold transition-all flex items-center justify-center gap-1.5"
        >
          <RefreshCw className="w-4 h-4" />
          Choose Different Image
        </button>

        <button
          type="button"
          onClick={onAnalyze}
          disabled={isLoading}
          className="w-full sm:w-auto px-6 py-3 rounded-xl bg-gradient-to-r from-emerald-700 to-green-600 hover:from-emerald-800 hover:to-green-700 text-white text-sm font-bold shadow-md shadow-emerald-700/20 active:scale-95 transition-all flex items-center justify-center gap-2"
        >
          <Microscope className="w-4 h-4" />
          Analyze Crop Leaf
        </button>
      </div>
    </div>
  );
};
