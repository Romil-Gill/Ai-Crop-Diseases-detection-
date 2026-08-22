import React from 'react';
import { AlertCircle, RefreshCw, ServerCrash } from 'lucide-react';

interface ErrorStateProps {
  errorMessage: string;
  onRetry: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ errorMessage, onRetry }) => {
  const isServerOffline = errorMessage.toLowerCase().includes('server') || errorMessage.toLowerCase().includes('unreachable');

  return (
    <div className="w-full bg-rose-50/80 border-2 border-rose-300 rounded-3xl p-6 sm:p-8 text-center shadow-sm">
      <div className="w-14 h-14 rounded-2xl bg-rose-600 text-white flex items-center justify-center mx-auto mb-4 shadow-md shadow-rose-600/20">
        {isServerOffline ? (
          <ServerCrash className="w-7 h-7" />
        ) : (
          <AlertCircle className="w-7 h-7" />
        )}
      </div>

      <h3 className="text-xl font-bold text-slate-900 font-outfit mb-2">
        {isServerOffline ? 'Backend Server Disconnected' : 'Analysis Error'}
      </h3>

      <p className="text-xs text-rose-900 font-medium max-w-md mx-auto mb-6 leading-relaxed bg-white/60 p-3.5 rounded-xl border border-rose-200">
        {errorMessage}
      </p>

      {isServerOffline && (
        <div className="text-[11px] text-slate-500 max-w-sm mx-auto mb-6 bg-slate-100 p-3 rounded-xl text-left font-mono">
          <span className="font-bold text-slate-700 block mb-1">Troubleshooting:</span>
          1. Ensure Flask backend is running on port 5000.<br/>
          2. Command: <code className="bg-slate-200 px-1 rounded text-emerald-800">python app.py</code>
        </div>
      )}

      <button
        type="button"
        onClick={onRetry}
        className="px-6 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold transition-all shadow-md shadow-rose-600/20 active:scale-95 inline-flex items-center gap-2"
      >
        <RefreshCw className="w-4 h-4" />
        Try Again
      </button>
    </div>
  );
};
