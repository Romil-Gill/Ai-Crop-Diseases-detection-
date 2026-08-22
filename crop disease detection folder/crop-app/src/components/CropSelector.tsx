import React from 'react';
import type { SupportedCrop } from '../types/api';
import { CheckCircle2, Sprout } from 'lucide-react';

interface CropSelectorProps {
  selectedCrop: SupportedCrop | null;
  onSelectCrop: (crop: SupportedCrop) => void;
}

interface CropOption {
  id: SupportedCrop;
  name: string;
  hindiName: string;
  classesCount: number;
  description: string;
  colorTheme: string;
  iconSvg: React.ReactNode;
}

const CROP_OPTIONS: CropOption[] = [
  {
    id: 'Tomato',
    name: 'Tomato',
    hindiName: 'टमाटर',
    classesCount: 10,
    description: 'Bacterial spot, Blights, Leaf Mold, Mites, Curl Virus',
    colorTheme: 'from-rose-500/10 to-red-500/5 border-rose-200 hover:border-rose-400 text-rose-700',
    iconSvg: (
      <svg className="w-8 h-8 text-rose-600" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C8.5 2 5.5 4 4.5 7C3.5 10 3.5 14 5.5 17.5C7.5 21 11 22 12 22C13 22 16.5 21 18.5 17.5C20.5 14 20.5 10 19.5 7C18.5 4 15.5 2 12 2ZM12 4C13 4 14.5 4.5 15 5.5C14 5.5 13 6 12 6.5C11 6 10 5.5 9 5.5C9.5 4.5 11 4 12 4Z"/>
      </svg>
    ),
  },
  {
    id: 'Rice',
    name: 'Rice',
    hindiName: 'चावल',
    classesCount: 3,
    description: 'Bacterial Blight, Brown Spot, Leaf Smut',
    colorTheme: 'from-amber-500/10 to-yellow-500/5 border-amber-200 hover:border-amber-400 text-amber-800',
    iconSvg: (
      <svg className="w-8 h-8 text-amber-600" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2L10 6L12 10L14 6L12 2ZM6 8L4 12L6 16L8 12L6 8ZM18 8L16 12L18 16L20 12L18 8ZM12 12L10 16L12 20L14 16L12 12Z"/>
      </svg>
    ),
  },
  {
    id: 'Sugarcane',
    name: 'Sugarcane',
    hindiName: 'गन्ना',
    classesCount: 9,
    description: 'Grassy Shoot, Mosaic, Red Rot, Wilt, Yellow Leaf',
    colorTheme: 'from-emerald-500/10 to-green-500/5 border-emerald-200 hover:border-emerald-400 text-emerald-800',
    iconSvg: (
      <svg className="w-8 h-8 text-emerald-600" viewBox="0 0 24 24" fill="currentColor">
        <path d="M17 2H7V4H9V20H7V22H17V20H15V4H17V2ZM11 6H13V10H11V6ZM11 12H13V16H11V12Z"/>
      </svg>
    ),
  },
  {
    id: 'Pumpkin',
    name: 'Pumpkin',
    hindiName: 'कद्दू',
    classesCount: 5,
    description: 'Bacterial Spot, Downy & Powdery Mildew, Mosaic',
    colorTheme: 'from-orange-500/10 to-amber-500/5 border-orange-200 hover:border-orange-400 text-orange-800',
    iconSvg: (
      <svg className="w-8 h-8 text-orange-600" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 3C10 3 9 4 9 4C9 4 7 3 5 4C3 5 3 7 3 8C3 13 6 21 12 21C18 21 21 13 21 8C21 7 21 5 19 4C17 3 15 4 15 4C15 4 14 3 12 3Z"/>
      </svg>
    ),
  },
];

export const CropSelector: React.FC<CropSelectorProps> = ({ selectedCrop, onSelectCrop }) => {
  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Sprout className="w-5 h-5 text-emerald-600" />
            Step 1: Select Target Crop
          </h3>
          <p className="text-xs text-slate-500">
            Choose the crop species for leaf diagnosis. Must match the uploaded image.
          </p>
        </div>

        {selectedCrop && (
          <span className="text-xs font-semibold text-emerald-700 bg-emerald-100/80 px-2.5 py-1 rounded-full flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
            Selection Confirmed
          </span>
        )}
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3.5">
        {CROP_OPTIONS.map((crop) => {
          const isSelected = selectedCrop === crop.id;
          return (
            <div
              key={crop.id}
              onClick={() => onSelectCrop(crop.id)}
              className={`relative cursor-pointer rounded-2xl p-4 transition-all duration-200 border-2 ${
                isSelected
                  ? 'bg-gradient-to-b from-emerald-50/90 to-white border-emerald-600 shadow-md shadow-emerald-700/10 ring-2 ring-emerald-500/20 scale-[1.02]'
                  : 'bg-white/80 border-slate-200 hover:border-slate-300 hover:bg-slate-50/50 hover:shadow-xs'
              }`}
            >
              {/* Selected badge icon */}
              {isSelected && (
                <div className="absolute top-3 right-3 text-emerald-600 bg-emerald-100 rounded-full p-0.5">
                  <CheckCircle2 className="w-4 h-4" />
                </div>
              )}

              <div className="flex flex-col h-full justify-between">
                <div>
                  <div className="mb-3">{crop.iconSvg}</div>
                  <div className="flex items-baseline justify-between">
                    <h4 className="font-extrabold text-base text-slate-900 font-outfit">
                      {crop.name}
                    </h4>
                    <span className="text-xs text-slate-400 font-medium">{crop.hindiName}</span>
                  </div>
                  <p className="text-[11px] text-slate-500 mt-1 line-clamp-2 leading-relaxed">
                    {crop.description}
                  </p>
                </div>

                <div className="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-[11px]">
                  <span className="font-semibold text-slate-600">Supported AI Classes</span>
                  <span className="font-bold bg-slate-100 text-slate-700 px-2 py-0.5 rounded-md">
                    {crop.classesCount}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
