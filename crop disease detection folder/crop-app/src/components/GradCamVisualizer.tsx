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
  const [viewMode, setViewMode] = useState<'overlay' | 'original' | 'sideBySide'>('overlay');
  const [showDetails, setShowDetails] = useState<boolean>(false);

  return (
    <div className="glass-panel p-6 rounded-2xl border border-[var(--color-primary)]/20 shadow-xl bg-white/90 backdrop-blur-md transition-all duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-emerald-900/10">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100/80 text-[var(--color-primary-dark)] text-xs font-semibold tracking-wide mb-2">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600 animate-pulse" />
            <span>Grad-CAM Explainability</span>
          </div>
          <h3 className="text-xl font-bold font-heading text-slate-900">
            Why did the AI choose this?
          </h3>
          <p className="text-sm text-slate-600 mt-1">
            Highlighted regions had the strongest influence on the AI's diagnosis.
          </p>
        </div>

        {/* View mode toggle */}
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-100/90 border border-slate-200 self-start sm:self-center">
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
            Overlay
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
            Compare
          </button>
        </div>
      </div>

      {/* Main Image Frame Container */}
      <div className="mt-6">
        {viewMode === 'sideBySide' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Original Image Card */}
            <div className="flex flex-col items-center bg-slate-50 p-4 rounded-xl border border-slate-200">
              <span className="text-xs font-semibold text-slate-600 uppercase tracking-wider mb-2">
                Original Uploaded Leaf
              </span>
              <div className="relative aspect-square w-full max-w-[280px] rounded-lg overflow-hidden border border-slate-300 shadow-sm bg-black/5">
                <img
                  src={originalImageUrl}
                  alt="Original Leaf"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>

            {/* AI Attention Heatmap Overlay Card */}
            <div className="flex flex-col items-center bg-slate-50 p-4 rounded-xl border border-slate-200">
              <span className="text-xs font-semibold text-[var(--color-primary-dark)] uppercase tracking-wider mb-2">
                AI Attention Heatmap
              </span>
              <div className="relative aspect-square w-full max-w-[280px] rounded-lg overflow-hidden border border-slate-300 shadow-sm bg-black">
                <img
                  src={explanation.overlay}
                  alt="AI Attention Overlay"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            {/* Interactive Single Overlay Viewer */}
            <div className="relative aspect-square w-full max-w-[340px] rounded-2xl overflow-hidden border-2 border-emerald-900/20 shadow-lg bg-black group">
              {/* Base Image */}
              <img
                src={originalImageUrl}
                alt="Base Leaf"
                className="absolute inset-0 w-full h-full object-cover"
              />
              {/* Heatmap Overlay with dynamic opacity */}
              <img
                src={explanation.overlay}
                alt="Grad-CAM Overlay"
                className="absolute inset-0 w-full h-full object-cover transition-opacity duration-150 ease-out"
                style={{ opacity: opacity }}
              />
            </div>

            {/* Opacity Control Slider */}
            <div className="w-full max-w-[340px] mt-4 p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center gap-3">
              <Sliders className="w-4 h-4 text-emerald-700 shrink-0" />
              <span className="text-xs font-medium text-slate-700 shrink-0">
                Heatmap Opacity:
              </span>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={opacity}
                onChange={(e) => setOpacity(parseFloat(e.target.value))}
                className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[var(--color-primary)]"
              />
              <span className="text-xs font-mono font-semibold text-slate-900 w-9 text-right shrink-0">
                {Math.round(opacity * 100)}%
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Color Legend */}
      <div className="mt-5 p-3 rounded-xl bg-emerald-50/60 border border-emerald-200/60 flex items-center justify-between text-xs text-slate-700">
        <span className="font-semibold text-emerald-900">Attention Spectrum:</span>
        <div className="flex items-center gap-2">
          <span className="text-[11px] text-slate-500">Low</span>
          <div className="h-3.5 w-32 rounded-full bg-gradient-to-r from-blue-600 via-cyan-400 via-yellow-400 to-red-600 shadow-inner" />
          <span className="text-[11px] font-bold text-red-600">High Influence</span>
        </div>
      </div>

      {/* Expandable Technical Explainer for Judges */}
      <div className="mt-4 border-t border-slate-200/80 pt-3">
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
          <div className="mt-2 p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-600 space-y-2 leading-relaxed font-sans">
            <p>
              <strong>Gradient-weighted Class Activation Mapping (Grad-CAM)</strong> computes the gradients of the model's top predicted class score with respect to the final convolutional feature maps of the MobileNetV2 backbone (layer: <code className="font-mono text-emerald-800 bg-emerald-100/80 px-1 py-0.5 rounded">{explanation.target_layer}</code>).
            </p>
            <p>
              Spatial regions highlighted in warm colors (red/orange) represent specific leaf areas where visual features (spots, discoloration, pustules) most strongly influenced the neural network's classification decision.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
