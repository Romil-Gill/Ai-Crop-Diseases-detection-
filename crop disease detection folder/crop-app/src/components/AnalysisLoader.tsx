import React, { useEffect, useState } from 'react';
import { Cpu, CheckCircle2, Loader2 } from 'lucide-react';
import type { SupportedCrop } from '../types/api';

interface AnalysisLoaderProps {
  imageSrc: string;
  selectedCrop: SupportedCrop;
}

const STEPS = [
  'Preprocessing image array to 224x224 RGB float32...',
  'Normalizing pixel values (MobileNetV2 preprocess_input)...',
  'MobileNetV2 feature extractor forward pass...',
  'Evaluating 36-class softmax probabilities...',
  'Running Safe Diagnosis Gate evaluation...',
];

export const AnalysisLoader: React.FC<AnalysisLoaderProps> = ({ imageSrc, selectedCrop }) => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStepIndex((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 600);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full bg-white rounded-3xl p-8 border border-slate-200 shadow-sm text-center">
      <div className="max-w-md mx-auto">
        
        {/* Animated Scanner Preview */}
        <div className="relative max-w-xs mx-auto aspect-square rounded-2xl overflow-hidden bg-slate-950 border-4 border-emerald-600 shadow-lg mb-6">
          <img
            src={imageSrc}
            alt="Scanning Leaf"
            className="w-full h-full object-cover opacity-75"
          />

          {/* Scanning Laser Animation Overlay */}
          <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-lime-400 to-transparent shadow-[0_0_15px_#a3e635] animate-scan-laser" />

          {/* Grid Lines Overlay */}
          <div 
            className="absolute inset-0 opacity-20 pointer-events-none"
            style={{
              backgroundImage: 'radial-gradient(#10b981 1px, transparent 1px)',
              backgroundSize: '16px 16px'
            }}
          />

          <div className="absolute bottom-3 left-1/2 -translate-x-1/2 bg-black/80 backdrop-blur-md text-lime-400 text-xs font-mono px-3 py-1 rounded-full border border-lime-500/30 flex items-center gap-1.5">
            <Loader2 className="w-3.5 h-3.5 animate-spin" />
            <span>AI SCANNING ({selectedCrop})</span>
          </div>
        </div>

        <h3 className="text-xl font-bold text-slate-900 font-outfit mb-2 flex items-center justify-center gap-2">
          <Cpu className="w-5 h-5 text-emerald-600 animate-pulse" />
          Analyzing Leaf Patterns
        </h3>

        {/* Dynamic Progress Steps */}
        <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 mb-4 text-left space-y-2">
          {STEPS.map((step, idx) => {
            const isDone = idx < currentStepIndex;
            const isCurrent = idx === currentStepIndex;
            return (
              <div
                key={idx}
                className={`flex items-center gap-2.5 text-xs transition-opacity duration-300 ${
                  isDone
                    ? 'text-emerald-700 font-medium opacity-90'
                    : isCurrent
                    ? 'text-slate-900 font-bold opacity-100'
                    : 'text-slate-400 opacity-50'
                }`}
              >
                {isDone ? (
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                ) : isCurrent ? (
                  <Loader2 className="w-3.5 h-3.5 text-emerald-600 animate-spin shrink-0" />
                ) : (
                  <div className="w-3.5 h-3.5 rounded-full border border-slate-300 shrink-0" />
                )}
                <span>{step}</span>
              </div>
            );
          })}
        </div>

        <p className="text-xs text-slate-500">
          Running real TensorFlow Keras inference on Flask server...
        </p>
      </div>
    </div>
  );
};
