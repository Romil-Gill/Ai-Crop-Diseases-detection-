import React, { useState } from 'react';
import { Eye, Sparkles, Sliders, Info, ChevronDown, ChevronUp, Layers } from 'lucide-react';
import type { GradCamExplanation } from '../types/api';

interface GradCamVisualizerProps {
  explanation: GradCamExplanation;
  originalImageUrl: string;
}

export const GradCamVisualizer: React.FC<GradCamVisualizerProps> = ({
  explanation,
  originalImageUrl,
}) => {
  const [opacity, setOpacity] = useState<number>(0.65);
  const [viewMode, setViewMode] = useState<'overlay' | 'sideBySide'>('overlay');
  const [showDetails, setShowDetails] = useState<boolean>(false);

  return (
    <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-[var(--color-primary)]/20 shadow-xl bg-white/95 backdrop-blur-md transition-all duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-emerald-900/10">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100/80 text-[var(--color-primary-dark)] text-xs font-semibold tracking-wide mb-2">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600 animate-pulse" />
            <span>Grad-CAM Explainability</span>
          </div>
          <h3 className="text-xl sm:text-2xl font-bold font-heading text-slate-900">
            Why did the AI choose this?
          </h3>
          <p className="text-sm text-slate-600 mt-1">
            Highlighted regions had the strongest influence on the AI's prediction.
          </p>
        </div>

        {/* View mode toggle */}
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-100/90 border border-slate-200 self-start sm:self-center shrink-0">
          <button
            type="button"
            onClick={() => setViewMode('overlay')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 flex items-center gap-1.5 ${
              viewMode === 'overlay'
                ? 'bg-white text-[var(--color-primary-dark)] shadow-sm font-semibold'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            Overlay View
          </button>
          <button
            type="button"
            onClick={() => setViewMode('sideBySide')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 flex items-center gap-1.5 ${
              viewMode === 'sideBySide'
                ? 'bg-white text-[var(--color-primary-dark)] shadow-sm font-semibold'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Eye className="w-3.5 h-3.5" />
            Side-by-Side
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="mt-6">
        {viewMode === 'sideBySide' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Original Image Card */}
            <div className="flex flex-col items-center bg-slate-50 p-5 rounded-2xl border border-slate-200">
              <span className="text-xs font-bold text-slate-600 uppercase tracking-wider mb-3">
                Original Uploaded Leaf
              </span>
              <div className="relative aspect-square w-full max-w-[320px] rounded-xl overflow-hidden border border-slate-300 shadow-sm bg-black/5">
                <img
                  src={originalImageUrl}
                  alt="Original Leaf"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>

            {/* AI Attention Heatmap Overlay Card */}
            <div className="flex flex-col items-center bg-slate-50 p-5 rounded-2xl border border-slate-200">
              <span className="text-xs font-bold text-[var(--color-primary-dark)] uppercase tracking-wider mb-3">
                AI Attention Heatmap Overlay
              </span>
              <div className="relative aspect-square w-full max-w-[320px] rounded-xl overflow-hidden border border-slate-300 shadow-sm bg-black">
                <img
                  src={explanation.overlay}
                  alt="AI Attention Overlay"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
            {/* Left: Interactive Canvas Frame */}
            <div className="md:col-span-6 flex justify-center">
              <div className="relative aspect-square w-full max-w-[340px] rounded-2xl overflow-hidden border-2 border-emerald-900/20 shadow-lg bg-black">
                <img
                  src={originalImageUrl}
                  alt="Base Leaf"
                  className="absolute inset-0 w-full h-full object-cover"
                />
                <img
                  src={explanation.overlay}
                  alt="Grad-CAM Overlay"
                  className="absolute inset-0 w-full h-full object-cover transition-opacity duration-150 ease-out"
                  style={{ opacity: opacity }}
                />
              </div>
            </div>

            {/* Right: Controls & Spectrum Legend */}
            <div className="md:col-span-6 space-y-5">
              {/* Opacity Control Slider */}
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                    <Sliders className="w-4 h-4 text-emerald-700" />
                    Heatmap Blend Opacity
                  </span>
                  <span className="text-xs font-mono font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-md">
                    {Math.round(opacity * 100)}%
                  </span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={opacity}
                  onChange={(e) => setOpacity(parseFloat(e.target.value))}
                  className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[var(--color-primary)]"
                />
                <div className="flex justify-between text-[10px] text-slate-500 font-medium">
                  <span>0% (Original Leaf)</span>
                  <span>100% (Full AI Overlay)</span>
                </div>
              </div>

              {/* Spectrum Legend */}
              <div className="p-4 rounded-2xl bg-emerald-50/60 border border-emerald-200/60 space-y-2">
                <div className="flex justify-between items-center text-xs font-bold text-emerald-950">
                  <span>Attention Spectrum:</span>
                  <span className="text-[11px] font-normal text-slate-600">Model Feature Weight</span>
                </div>
                <div className="h-4 w-full rounded-full bg-gradient-to-r from-blue-600 via-cyan-400 via-yellow-400 to-red-600 shadow-inner" />
                <div className="flex justify-between text-[10px] font-semibold text-slate-600">
                  <span className="text-blue-700">Low Contribution</span>
                  <span className="text-red-700">High Model Focus</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Expandable Technical Explainer for Judges */}
      <div className="mt-6 border-t border-slate-200/80 pt-4">
        <button
          type="button"
          onClick={() => setShowDetails(!showDetails)}
          className="w-full flex items-center justify-between text-xs font-medium text-slate-600 hover:text-[var(--color-primary-dark)] transition-colors py-1"
        >
          <span className="flex items-center gap-1.5 font-semibold">
            <Info className="w-3.5 h-3.5 text-emerald-600" />
            How Grad-CAM Works (Judge Technical Note)
          </span>
          {showDetails ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>

        {showDetails && (
          <div className="mt-2.5 p-4 rounded-2xl bg-slate-50 border border-slate-200 text-xs text-slate-600 space-y-2 leading-relaxed font-sans">
            <p>
              <strong>Gradient-weighted Class Activation Mapping (Grad-CAM)</strong> computes the gradients of the top predicted class score with respect to the final convolutional feature maps of the MobileNetV2 backbone.
            </p>
            <p>
              Warm regions (red/orange) highlight specific leaf areas where spatial visual features (spots, lesions, pustules) most strongly influenced the neural network's classification.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
