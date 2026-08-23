import React, { useState, useEffect } from 'react';
import type { CommunitySummaryResponse, CommunitySignalRecord } from '../types/api';
import { getCommunitySummary, getCommunitySignals } from '../services/api';
import { CommunitySummary } from './CommunitySummary';
import { Radio, Loader2, Calendar, MapPin, Shield } from 'lucide-react';

export const CommunityPage: React.FC = () => {
  const [summary, setSummary] = useState<CommunitySummaryResponse | null>(null);
  const [signals, setSignals] = useState<CommunitySignalRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    Promise.all([getCommunitySummary(), getCommunitySignals()])
      .then(([sumRes, sigRes]) => {
        if (!isMounted) return;
        setSummary(sumRes);
        setSignals(sigRes.signals || []);
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 animate-in fade-in duration-300">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-100 text-blue-900 text-xs font-bold mb-2 font-mono border border-blue-200">
            <Radio className="w-3.5 h-3.5 text-blue-700 animate-pulse" />
            <span>Anonymized Crop Health Telemetry</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold font-outfit text-slate-900">
            Community Disease Signals
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 font-medium">
            Aggregated crop health activity contributed by local farmers for early awareness.
          </p>
        </div>
      </div>

      {loading && (
        <div className="py-12 text-center space-y-2">
          <Loader2 className="w-6 h-6 text-blue-600 animate-spin mx-auto" />
          <p className="text-xs text-slate-500 font-medium">Loading community disease signals...</p>
        </div>
      )}

      {!loading && summary && (
        <div className="space-y-6">
          <CommunitySummary summary={summary} />

          {/* Signals Feed */}
          {signals.length > 0 && (
            <div className="space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 font-outfit">
                Recent Reported Disease Signals
              </h4>
              <div className="space-y-3">
                {signals.map((sig) => {
                  const formattedDate = new Date(sig.created_at).toLocaleDateString('en-GB', {
                    day: '2-digit',
                    month: 'short',
                    year: 'numeric',
                  });

                  return (
                    <div
                      key={sig.id}
                      className="p-4 rounded-2xl bg-white border border-slate-200 shadow-2xs space-y-2"
                    >
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1.5">
                        <div className="flex items-center gap-2">
                          <span className="px-2.5 py-0.5 rounded-full bg-blue-900 text-white font-extrabold text-[11px] font-outfit uppercase">
                            {sig.crop}
                          </span>
                          <span className="font-bold text-slate-900 text-sm font-outfit">
                            {sig.condition}
                          </span>
                        </div>

                        <div className="flex items-center gap-3 text-xs text-slate-500 font-medium">
                          <div className="flex items-center gap-1">
                            <MapPin className="w-3.5 h-3.5 text-slate-400" />
                            <span>{sig.area_name}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <Calendar className="w-3.5 h-3.5 text-slate-400" />
                            <span>{formattedDate}</span>
                          </div>
                        </div>
                      </div>

                      {/* Coarsened Privacy Coordinates Badge */}
                      <div className="flex items-center justify-between border-t border-slate-100 pt-2 text-[11px] text-slate-500 font-sans">
                        <div className="flex items-center gap-1">
                          <Shield className="w-3.5 h-3.5 text-emerald-600" />
                          <span>Sanitized Area Coarsening ({sig.map_lat?.toFixed(1)}°N, {sig.map_lon?.toFixed(1)}°E)</span>
                        </div>
                        <span className="font-mono text-[10px] uppercase font-bold text-slate-400">
                          {sig.status}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
