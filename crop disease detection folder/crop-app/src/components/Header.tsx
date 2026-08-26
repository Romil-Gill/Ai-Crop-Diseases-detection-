import React from 'react';
import { Leaf, Activity, AlertCircle } from 'lucide-react';
import type { SupportedCrop } from '../types/api';

interface HeaderProps {
  serverOnline: boolean | null;
  selectedCrop: SupportedCrop | null;
  activeView?: 'home' | 'history' | 'community';
  onNavigateView?: (view: 'home' | 'history' | 'community') => void;
  onReset: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  serverOnline,
  selectedCrop,
  activeView = 'home',
  onNavigateView,
  onReset,
}) => {
  return (
    <header className="sticky top-0 z-40 w-full glass-panel border-b border-slate-200/80 shadow-xs">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        
        {/* Brand Logo & Name */}
        <div 
          onClick={() => {
            if (onNavigateView) onNavigateView('home');
            onReset();
          }}
          className="flex items-center gap-3 cursor-pointer group transition-all"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-700 to-green-600 flex items-center justify-center text-white shadow-md shadow-emerald-700/20 group-hover:scale-105 transition-transform">
            <Leaf className="w-5 h-5 text-lime-300" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-xl tracking-tight text-emerald-950 font-outfit">
                Fasal<span className="text-emerald-600">Rakshak</span>
              </span>
              <span className="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-1.5 py-0.5 rounded-md uppercase tracking-wider">
                AI
              </span>
            </div>
            <p className="text-[11px] font-medium text-slate-500 hidden sm:block">
              Scan. Understand. Act.
            </p>
          </div>
        </div>

        {/* Center Navigation Tabs */}
        {onNavigateView && (
          <nav className="flex items-center gap-1 bg-slate-100/90 p-1 rounded-2xl border border-slate-200/80 font-outfit">
            <button
              type="button"
              onClick={() => onNavigateView('home')}
              className={`px-3 py-1.5 rounded-xl text-xs font-extrabold transition-all ${
                activeView === 'home'
                  ? 'bg-white text-slate-900 shadow-2xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Home
            </button>
            <button
              type="button"
              onClick={() => onNavigateView('history')}
              className={`px-3 py-1.5 rounded-xl text-xs font-extrabold transition-all ${
                activeView === 'history'
                  ? 'bg-white text-slate-900 shadow-2xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Saved Assessments
            </button>
            <button
              type="button"
              onClick={() => onNavigateView('community')}
              className={`px-3 py-1.5 rounded-xl text-xs font-extrabold transition-all ${
                activeView === 'community'
                  ? 'bg-white text-slate-900 shadow-2xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Community
            </button>
          </nav>
        )}

        {/* Status Indicators & Selected Crop Badge */}
        <div className="flex items-center gap-3">
          {selectedCrop && (
            <div className="hidden md:flex items-center gap-1.5 bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-semibold px-3 py-1.5 rounded-full">
              <span className="text-slate-400">Crop:</span>
              <span className="font-bold text-emerald-900">{selectedCrop}</span>
            </div>
          )}

          {/* Backend Health Badge */}
          <div 
            className={`flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full border ${
              serverOnline === true
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                : serverOnline === false
                ? 'bg-rose-50 text-rose-700 border-rose-200'
                : 'bg-slate-50 text-slate-500 border-slate-200'
            }`}
            title={serverOnline ? "Backend Flask ML Server Connected" : "Flask Server Disconnected"}
          >
            {serverOnline === true ? (
              <>
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span className="hidden sm:inline">Backend API</span>
                <span className="font-semibold">Online</span>
              </>
            ) : serverOnline === false ? (
              <>
                <AlertCircle className="w-3.5 h-3.5 text-rose-500" />
                <span className="font-semibold">Backend Offline</span>
              </>
            ) : (
              <>
                <Activity className="w-3.5 h-3.5 text-slate-400 animate-spin" />
                <span>Checking...</span>
              </>
            )}
          </div>
        </div>

      </div>
    </header>
  );
};
