import React from 'react';
import type { CommunityRadarResponse } from '../types/api';
import { DataModeToggle } from './DataModeToggle';
import { RadarFilters } from './RadarFilters';
import { RadarSummaryCards } from './RadarSummaryCards';
import { RadarMap } from './RadarMap';
import { AreasToWatch } from './AreasToWatch';
import { SignalActivityChart } from './SignalActivityChart';
import { CropBreakdown } from './CropBreakdown';
import { RecentSignals } from './RecentSignals';
import { MethodologyPanel } from './MethodologyPanel';
import { Sparkles, Building2 } from 'lucide-react';

interface OperationsDashboardProps {
  radarData: CommunityRadarResponse;
  mode: 'live' | 'demo';
  days: number;
  crop: string;
  onChangeMode: (mode: 'live' | 'demo') => void;
  onChangeDays: (days: number) => void;
  onChangeCrop: (crop: string) => void;
}

export const OperationsDashboard: React.FC<OperationsDashboardProps> = ({
  radarData,
  mode,
  days,
  crop,
  onChangeMode,
  onChangeDays,
  onChangeCrop,
}) => {
  return (
    <div className="space-y-6 font-outfit animate-in fade-in duration-300">
      {/* Dashboard Sub-Header */}
      <div className="p-5 rounded-3xl bg-gradient-to-r from-slate-900 to-slate-800 text-white shadow-lg space-y-2 border border-slate-700">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <Building2 className="w-5 h-5 text-emerald-400" />
            <h3 className="text-xl font-extrabold text-white uppercase tracking-wider">
              AGRI OPERATIONS VIEW
            </h3>
          </div>
          <span className="text-[11px] px-3 py-1 rounded-full bg-emerald-950 border border-emerald-500/40 font-mono font-bold text-emerald-300 w-fit">
            Regional Telemetry Intelligence
          </span>
        </div>
        <p className="text-xs text-slate-300 font-sans max-w-2xl">
          Prototype community intelligence for agricultural monitoring
        </p>
      </div>

      {/* Data Source Mode Switcher */}
      <DataModeToggle mode={mode} onChangeMode={onChangeMode} />

      {/* Filters Bar */}
      <RadarFilters
        days={days}
        crop={crop}
        onChangeDays={onChangeDays}
        onChangeCrop={onChangeCrop}
      />

      {/* Top 4 Summary Cards */}
      <RadarSummaryCards summary={radarData.summary} />

      {/* Community Disease Radar Map */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h4 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider">
            Community Disease Radar Map
          </h4>
          {mode === 'demo' && (
            <span className="text-xs font-bold text-amber-600 flex items-center gap-1 bg-amber-50 px-2.5 py-0.5 rounded-full border border-amber-200">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Demo Mode Active</span>
            </span>
          )}
        </div>
        <RadarMap areas={radarData.areas} />
      </div>

      {/* Areas to Watch Table */}
      <AreasToWatch areas={radarData.areas} />

      {/* Grid: Signal Activity Trend & Crop Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SignalActivityChart dailyTrend={radarData.daily_trend} />
        <CropBreakdown breakdown={radarData.crop_breakdown} />
      </div>

      {/* Recent Signals Feed */}
      <RecentSignals signals={radarData.recent_signals} />

      {/* Methodology & Privacy Accordion */}
      <MethodologyPanel />
    </div>
  );
};
