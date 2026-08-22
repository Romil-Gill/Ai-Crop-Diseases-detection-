import React, { useState } from 'react';
import type { PredictResponse, SupportedCrop } from '../types/api';
import { AlertTriangle, RefreshCw, ChevronDown, ChevronUp, Sliders, Info } from 'lucide-react';
import { TopPredictions } from './TopPredictions';

interface UncertainStateProps {
  result: PredictResponse;
  selectedCrop: SupportedCrop | null;
  onResetUpload: () => void;
  onChangeCrop: () => void;
}

export const UncertainState: React.FC<UncertainStateProps> = ({
  result,
  selectedCrop,
  onResetUpload,
  onChangeCrop,
}) => {
  const [showTechnicalDetails, setShowTechnicalDetails] = useState(false);

  return (
    <div className="w-full bg-gradient-to-b from-amber-50/90 via-white to-amber-50/30 rounded-3xl p-6 sm:p-8 border-2 border-amber-300 shadow-md">
      
      {/* Alert Header */}
      <div className="flex items-start gap-4 mb-6">
        <div className="w-12 h-12 rounded-2xl bg-amber-600 text-white flex items-center justify-center shrink-0 shadow-md shadow-amber-600/20">
          <AlertTriangle className="w-6 h-6" />
        </div>

        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 border border-amber-300 text-xs font-bold uppercase tracking-wider mb-1">
            Safe Diagnosis Gate Alert
          </div>
          <h3 className="text-2xl font-extrabold text-slate-900 font-outfit">
            Diagnosis Uncertain
          </h3>
          <p className="text-xs text-amber-950 font-medium mt-1">
            The AI model cannot issue a reliable diagnosis for this leaf upload.
          </p>
        </div>
      </div>

      {/* Uncertainty Reason Box */}
      <div className="bg-amber-100/70 border border-amber-300/80 rounded-2xl p-4 mb-6">
        <div className="flex items-center gap-2 text-amber-900 font-bold text-xs mb-1">
          <Info className="w-4 h-4 text-amber-700" />
          <span>Reason for Uncertainty:</span>
        </div>
        <p className="text-xs text-amber-950 font-medium leading-relaxed">
          {result.uncertainty_reason || 'Low prediction confidence or crop mismatch detected.'}
        </p>

        {selectedCrop && result.prediction && (
          <div className="mt-3 pt-3 border-t border-amber-200/80 grid grid-cols-2 gap-2 text-[11px]">
            <div>
              <span className="text-amber-800 font-medium">Your Selected Crop:</span>
              <span className="font-bold text-slate-900 ml-1">{selectedCrop}</span>
            </div>
            <div>
              <span className="text-amber-800 font-medium">Model Raw Prediction:</span>
              <span className="font-bold text-slate-900 ml-1">{result.prediction.crop} ({result.prediction.condition})</span>
            </div>
          </div>
        )}
      </div>

      {/* Primary User Guidance Actions */}
      <div className="flex flex-col sm:flex-row items-center gap-3 mb-6">
        <button
          type="button"
          onClick={onResetUpload}
          className="w-full sm:w-1/2 px-5 py-3 rounded-xl bg-amber-600 hover:bg-amber-700 text-white text-xs font-bold transition-all shadow-md shadow-amber-600/20 active:scale-95 flex items-center justify-center gap-2"
        >
          <RefreshCw className="w-4 h-4" />
          Upload Another Leaf Image
        </button>

        <button
          type="button"
          onClick={onChangeCrop}
          className="w-full sm:w-1/2 px-5 py-3 rounded-xl border border-amber-300 bg-white hover:bg-amber-50 text-amber-900 text-xs font-bold transition-all flex items-center justify-center gap-2"
        >
          <Sliders className="w-4 h-4 text-amber-700" />
          Change Target Crop
        </button>
      </div>

      {/* Expandable Technical Details Accordion */}
      <div className="border-t border-amber-200/60 pt-4">
        <button
          type="button"
          onClick={() => setShowTechnicalDetails(!showTechnicalDetails)}
          className="w-full flex items-center justify-between text-xs font-bold text-amber-900 hover:text-amber-950 py-1"
        >
          <span className="flex items-center gap-1.5">
            <Info className="w-3.5 h-3.5 text-amber-700" />
            Expand Raw Technical Probabilities
          </span>
          {showTechnicalDetails ? (
            <ChevronUp className="w-4 h-4 text-amber-700" />
          ) : (
            <ChevronDown className="w-4 h-4 text-amber-700" />
          )}
        </button>

        {showTechnicalDetails && (
          <div className="mt-3 transition-all duration-300">
            <p className="text-[11px] text-amber-900/80 mb-3 bg-amber-100/40 p-2.5 rounded-lg border border-amber-200">
              Note: Below raw top predictions were flagged by the Safe Diagnosis Gate as unverified.
            </p>
            <TopPredictions predictions={result.top_predictions} />
          </div>
        )}
      </div>

    </div>
  );
};
