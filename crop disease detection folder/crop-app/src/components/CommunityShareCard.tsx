import React, { useState } from 'react';
import type { ScanRecord, CommunitySignalRecord } from '../types/api';
import { shareCommunitySignal } from '../services/api';
import { Radio, CheckCircle2, Shield, Loader2 } from 'lucide-react';

interface CommunityShareCardProps {
  savedScan: ScanRecord;
  onShared?: (signal: CommunitySignalRecord) => void;
}

export const CommunityShareCard: React.FC<CommunityShareCardProps> = ({
  savedScan,
  onShared,
}) => {
  const [sharing, setSharing] = useState<boolean>(false);
  const [sharedSignal, setSharedSignal] = useState<CommunitySignalRecord | null>(null);
  const [error, setError] = useState<string | null>(null);

  if (savedScan.is_healthy) {
    return null; // Only disease assessments are eligible for community disease signals
  }

  const handleShare = async () => {
    if (sharedSignal || savedScan.community_shared) return;
    setSharing(true);
    setError(null);

    try {
      const res = await shareCommunitySignal(savedScan.id);
      setSharedSignal(res.signal);
      if (onShared) onShared(res.signal);
    } catch (err: any) {
      setError(err.message || 'Failed to share community signal.');
    } finally {
      setSharing(false);
    }
  };

  const isAlreadyShared = Boolean(sharedSignal || savedScan.community_shared);

  return (
    <div className="p-5 rounded-3xl bg-blue-50/80 border border-blue-200/90 space-y-3.5 shadow-2xs">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Radio className="w-5 h-5 text-blue-600 animate-pulse" />
          <h4 className="text-sm font-bold font-outfit text-slate-900">
            Help Improve Local Crop Awareness
          </h4>
        </div>
        <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-100 text-blue-900 font-mono font-bold">
          Opt-in Signal
        </span>
      </div>

      <p className="text-xs text-slate-700 leading-relaxed font-sans">
        Contribute an anonymized signal for <strong>{savedScan.condition}</strong> in <strong>{savedScan.location_name || 'your area'}</strong> to alert neighboring farmers.
      </p>

      {/* Privacy Notice */}
      <div className="p-3 rounded-2xl bg-white/90 border border-blue-200 text-[11px] text-slate-600 flex items-start gap-2 leading-relaxed">
        <Shield className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
        <span>
          <strong>Privacy Guarantee:</strong> Shares only crop condition, district area name, and date. Your leaf image, exact GPS coordinates, and personal details are <strong>NEVER</strong> shared.
        </span>
      </div>

      {isAlreadyShared ? (
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-2xl bg-emerald-600 text-white text-xs font-bold font-outfit shadow-sm">
          <CheckCircle2 className="w-4 h-4 text-emerald-200" />
          <span>Anonymized Disease Signal Shared</span>
        </div>
      ) : (
        <div>
          <button
            type="button"
            onClick={handleShare}
            disabled={sharing}
            className="w-full sm:w-auto px-5 py-2.5 rounded-2xl bg-blue-600 hover:bg-blue-700 active:scale-[0.99] text-white font-bold text-xs transition-all shadow-sm shadow-blue-600/20 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {sharing ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-blue-200" />
                <span>Sharing Signal...</span>
              </>
            ) : (
              <>
                <Radio className="w-4 h-4 text-blue-200" />
                <span>Share Anonymized Disease Signal</span>
              </>
            )}
          </button>

          {error && (
            <p className="text-xs text-rose-600 font-medium mt-1">
              {error}
            </p>
          )}
        </div>
      )}
    </div>
  );
};
