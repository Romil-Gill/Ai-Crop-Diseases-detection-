import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, AlertTriangle } from 'lucide-react';
import type { SupportedCrop } from '../types/api';

interface ImageUploaderProps {
  selectedCrop: SupportedCrop | null;
  onFileSelect: (file: File) => void;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({ selectedCrop, onFileSelect }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (selectedCrop) setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    if (!selectedCrop) return;

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (validateFile(file)) {
        onFileSelect(file);
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      if (validateFile(file)) {
        onFileSelect(file);
      }
    }
  };

  const validateFile = (file: File): boolean => {
    if (!file.type.startsWith('image/')) {
      alert('Please upload a valid image file (.jpg, .png, .webp)');
      return false;
    }
    return true;
  };

  return (
    <div className="w-full">
      {!selectedCrop && (
        <div className="mb-3 p-3 bg-amber-50 border border-amber-200 rounded-xl flex items-center gap-2.5 text-xs text-amber-800 font-medium">
          <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
          <span>Please select a target crop above before uploading the leaf photo.</span>
        </div>
      )}

      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => selectedCrop && fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-3xl p-8 sm:p-12 text-center transition-all duration-200 ${
          !selectedCrop
            ? 'border-slate-200 bg-slate-50/70 cursor-not-allowed opacity-75'
            : isDragOver
            ? 'border-emerald-500 bg-emerald-50/80 shadow-inner scale-[0.99] cursor-pointer'
            : 'border-emerald-300/80 bg-white hover:border-emerald-500 hover:bg-emerald-50/30 cursor-pointer shadow-xs'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp,image/bmp"
          onChange={handleFileChange}
          disabled={!selectedCrop}
          className="hidden"
        />

        <div className="flex flex-col items-center justify-center max-w-sm mx-auto">
          <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-4 transition-transform ${
            selectedCrop ? 'bg-emerald-100 text-emerald-600 shadow-sm' : 'bg-slate-200 text-slate-400'
          }`}>
            <UploadCloud className="w-8 h-8" />
          </div>

          <h4 className="text-base font-bold text-slate-900 font-outfit mb-1">
            {selectedCrop ? `Upload ${selectedCrop} Leaf Photo` : 'Select a crop first'}
          </h4>

          <p className="text-xs text-slate-500 mb-4 leading-relaxed">
            Drag and drop a clear photo of the leaf or click to browse files from your device.
          </p>

          <div className="flex items-center gap-2">
            <button
              type="button"
              disabled={!selectedCrop}
              className={`px-5 py-2.5 rounded-xl text-xs font-bold transition-all shadow-xs flex items-center gap-2 ${
                selectedCrop
                  ? 'bg-emerald-700 hover:bg-emerald-800 text-white shadow-emerald-700/20 active:scale-95'
                  : 'bg-slate-200 text-slate-400 cursor-not-allowed'
              }`}
            >
              <ImageIcon className="w-4 h-4" />
              Browse Image
            </button>
          </div>

          <p className="text-[11px] text-slate-400 mt-4">
            Supports JPG, PNG, WEBP • Max 10MB • Auto 224x224 RGB preprocessing
          </p>
        </div>
      </div>

      {selectedCrop && (
        <div className="mt-4 p-4 bg-white border border-slate-200 rounded-2xl shadow-sm text-left">
          <h5 className="text-xs font-bold text-slate-700 mb-2 font-outfit">For best results:</h5>
          <ul className="text-xs text-slate-600 space-y-1.5 list-disc pl-4">
            <li>Use one clearly visible leaf</li>
            <li>Capture the leaf close-up</li>
            <li>Use good natural lighting</li>
            <li>Avoid heavy blur</li>
            <li>Avoid screenshots with text/watermarks</li>
            <li>Avoid multiple overlapping leaves</li>
            <li>Keep the leaf as the main object</li>
          </ul>
        </div>
      )}
    </div>
  );
};
