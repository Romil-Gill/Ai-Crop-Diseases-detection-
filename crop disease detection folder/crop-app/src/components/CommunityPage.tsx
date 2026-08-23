import React, { useState, useEffect } from 'react';
import type { CommunityRadarResponse } from '../types/api';
import { getCommunityRadar } from '../services/api';
import { DataModeToggle } from './DataModeToggle';
import { RadarFilters } from './RadarFilters';
import { RadarSummaryCards } from './RadarSummaryCards';
import { RadarMap } from './RadarMap';
import { AreasToWatch } from './AreasToWatch';
import { MethodologyPanel } from './MethodologyPanel';
import { OperationsDashboard } from './OperationsDashboard';
import { Radio, Loader2, Users, Building2, Sparkles } from 'lucide-react';

export const CommunityPage: React.FC = () => {
  const [viewTab, setViewTab] = useState<'community' | 'operations'>('community');
  const [dataMode, setDataMode] = useState<'live' | 'demo'>('live');
  const [daysWindow, setDaysWindow] = useState<number>(7);
  const [cropFilter, setCropFilter] = useState<string>('All');

  const [radarData, setRadarData] = useState<CommunityRadarResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    getCommunityRadar(dataMode, daysWindow, cropFilter)
      .then((res) => {
        if (!isMounted) return;
        setRadarData(res);
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [dataMode, daysWindow, cropFilter]);

  return (
    <div className="w-full max-w-5xl mx-auto space-y-6 animate-in fade-in duration-300">
      {/* Top Header & View Switcher */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-100 text-blue-900 text-xs font-bold mb-1.5 font-mono border border-blue-200">
            <Radio className="w-3.5 h-3.5 text-blue-700 animate-pulse" />
            <span>Community Disease Radar</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold font-outfit text-slate-900">
            Regional Crop Health Telemetry
          </h2>
        </div>

        {/* View Switcher: Community View vs Agri Operations View */}
        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-2xl border border-slate-200 font-outfit self-start sm:self-auto">
          <button
            type="button"
            onClick={() => setViewTab('community')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition-all flex items-center gap-1.5 ${
              viewTab === 'community'
                ? 'bg-white text-slate-900 shadow-2xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Users className="w-3.5 h-3.5 text-emerald-600" />
            <span>COMMUNITY VIEW</span>
          </button>
          <button
            type="button"
            onClick={() => setViewTab('operations')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition-all flex items-center gap-1.5 ${
              viewTab === 'operations'
                ? 'bg-slate-900 text-white shadow-2xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Building2 className="w-3.5 h-3.5 text-blue-400" />
            <span>AGRI OPERATIONS VIEW</span>
          </button>
        </div>
      </div>

      {loading && (
        <div className="py-16 text-center space-y-2 font-outfit">
          <Loader2 className="w-7 h-7 text-blue-600 animate-spin mx-auto" />
          <p className="text-xs text-slate-500 font-medium">Loading Community Disease Radar telemetry...</p>
        </div>
      )}

      {!loading && radarData && (
        <>
          {/* View 1: COMMUNITY VIEW */}
          {viewTab === 'community' && (
            <div className="space-y-6 animate-in fade-in duration-200">
              {/* Data Mode Switcher */}
              <DataModeToggle mode={dataMode} onChangeMode={setDataMode} />

              {/* Filters */}
              <RadarFilters
                days={daysWindow}
                crop={cropFilter}
                onChangeDays={setDaysWindow}
                onChangeCrop={setCropFilter}
              />

              {/* Metric Cards */}
              <RadarSummaryCards summary={radarData.summary} />

              {/* Interactive Radar Map */}
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-extrabold font-outfit text-slate-900 uppercase tracking-wider">
                    Community Disease Radar Map
                  </h4>
                  {dataMode === 'demo' && (
                    <span className="text-xs font-bold text-amber-600 flex items-center gap-1 bg-amber-50 px-2.5 py-0.5 rounded-full border border-amber-200 font-outfit">
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Demo Mode Active</span>
                    </span>
                  )}
                </div>

                {radarData.areas.length === 0 && dataMode === 'live' ? (
                  <div className="p-10 rounded-3xl bg-white border border-slate-200 text-center space-y-3 font-outfit shadow-sm">
                    <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-slate-400">
                      <Radio className="w-6 h-6" />
                    </div>
                    <div className="space-y-1">
                      <h4 className="text-base font-bold text-slate-900">
                        No community signals in this time window yet
                      </h4>
                      <p className="text-xs text-slate-500 max-w-md mx-auto">
                        Scan your crop leaf and opt in to contribute anonymized signal telemetry for your area.
                      </p>
                    </div>
                    <div className="flex items-center justify-center gap-3 pt-1">
                      <a
                        href="/detect"
                        className="px-4 py-2 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs inline-flex items-center gap-1.5 shadow-2xs"
                      >
                        <span>Scan a Crop</span>
                      </a>
                      <button
                        type="button"
                        onClick={() => setDataMode('demo')}
                        className="px-4 py-2 rounded-2xl bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold text-xs inline-flex items-center gap-1.5 shadow-2xs"
                      >
                        <Sparkles className="w-3.5 h-3.5" />
                        <span>View Demo Data</span>
                      </button>
                    </div>
                  </div>
                ) : (
                  <RadarMap areas={radarData.areas} />
                )}
              </div>

              {/* Areas to Watch */}
              <AreasToWatch areas={radarData.areas} />

              {/* Methodology Accordion */}
              <MethodologyPanel />
            </div>
          )}

          {/* View 2: AGRI OPERATIONS VIEW */}
          {viewTab === 'operations' && (
            <OperationsDashboard
              radarData={radarData}
              mode={dataMode}
              days={daysWindow}
              crop={cropFilter}
              onChangeMode={setDataMode}
              onChangeDays={setDaysWindow}
              onChangeCrop={setCropFilter}
            />
          )}
        </>
      )}
    </div>
  );
};
