import React, { useState } from 'react';
import type { PredictionItem } from '../types/api';
import { Layers, Info, ChevronDown, ChevronUp } from 'lucide-react';

interface TopPredictionsProps {
  predictions: PredictionItem[];
  selectedCrop?: string | null;
}

export const TopPredictions: React.FC<TopPredictionsProps> = ({ predictions, selectedCrop }) => {
  const [showTechnicalDetails, setShowTechnicalDetails] = useState<boolean>(false);

  if (!predictions || predictions.length === 0) return null;

  const top1Crop = predictions[0]?.crop;
  const activeCrop = selectedCrop || top1Crop;

  // Filter main user-facing alternative predictions to the selected crop only
  const cropMatches = predictions.filter(
    (p) => p.crop.toLowerCase() === activeCrop.toLowerCase()
  );

  // Fallback to top predictions if filtering returns empty
  const displayMatches = cropMatches.length > 0 ? cropMatches : predictions;

  return (
    <div className="w-full bg-white rounded-3xl p-6 border border-slate-200 shadow-xs">
      {/* Title */}
      <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
        <Layers className="w-4 h-4 text-emerald-600" />
        <h4 className="text-sm font-bold text-slate-900 font-outfit">
          Other possible matches ({activeCrop})
        </h4>
      </div>

      {/* Main User-Facing Crop-Specific Prediction Bars */}
      <div className="space-y-3">
        {displayMatches.map((pred, index) => {
          const isTop1 = index === 0;
          return (
            <div
              key={index}
              className={`p-3.5 rounded-2xl border transition-all ${
                isTop1
                  ? 'bg-emerald-50/50 border-emerald-200'
                  : 'bg-slate-50/60 border-slate-100'
              }`}
            >
              <div className="flex items-center justify-between text-xs font-semibold mb-1.5">
                <div className="flex items-center gap-2">
                  <span
                    className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                      isTop1 ? 'bg-emerald-700 text-white' : 'bg-slate-200 text-slate-700'
                    }`}
                  >
                    #{index + 1}
                  </span>
                  <span className="text-slate-900 font-bold">{pred.condition}</span>
                </div>

                <span
                  className={`font-mono font-bold ${
                    isTop1 ? 'text-emerald-700' : 'text-slate-600'
                  }`}
                >
                  {pred.confidence.toFixed(2)}%
                </span>
              </div>

              <div className="w-full bg-slate-200/80 h-2 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    isTop1 ? 'bg-emerald-600' : 'bg-slate-400'
                  }`}
                  style={{ width: `${Math.max(2, pred.confidence)}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Optional Judge Technical Accordion */}
      <div className="mt-4 border-t border-slate-100 pt-3">
        <button
          type="button"
          onClick={() => setShowTechnicalDetails(!showTechnicalDetails)}
          className="w-full flex items-center justify-between text-xs font-medium text-slate-500 hover:text-emerald-700 transition-colors py-1"
        >
          <span className="flex items-center gap-1.5 font-semibold">
            <Info className="w-3.5 h-3.5 text-emerald-600" />
            Technical Model Details (Raw Top-3 Softmax Distribution)
          </span>
          {showTechnicalDetails ? (
            <ChevronUp className="w-4 h-4" />
          ) : (
            <ChevronDown className="w-4 h-4" />
          )}
        </button>

        {showTechnicalDetails && (
          <div className="mt-2 p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-600 space-y-2">
            <p className="font-semibold text-slate-700">Raw Global 36-Class Softmax Output:</p>
            <div className="space-y-1.5 font-mono text-[11px]">
              {predictions.map((p, idx) => (
                <div key={idx} className="flex justify-between items-center bg-white p-2 rounded border border-slate-200">
                  <span>#{idx + 1} {p.crop} — {p.condition}</span>
                  <span className="font-bold text-emerald-800">{p.confidence.toFixed(2)}%</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
