import React from 'react';

interface HistoryFiltersProps {
  activeCrop: string;
  onSelectCrop: (crop: string) => void;
}

const CROPS = ['All', 'Tomato', 'Rice', 'Sugarcane', 'Pumpkin', 'Wheat', 'Maize'];

export const HistoryFilters: React.FC<HistoryFiltersProps> = ({ activeCrop, onSelectCrop }) => {
  return (
    <div className="flex items-center gap-2 overflow-x-auto pb-1 no-scrollbar">
      {CROPS.map((crop) => (
        <button
          key={crop}
          type="button"
          onClick={() => onSelectCrop(crop)}
          className={`px-4 py-2 rounded-2xl text-xs font-extrabold font-outfit transition-all ${
            activeCrop.toLowerCase() === crop.toLowerCase()
              ? 'bg-slate-900 text-white shadow-sm scale-[1.02]'
              : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100 hover:text-slate-900'
          }`}
        >
          {crop}
        </button>
      ))}
    </div>
  );
};
