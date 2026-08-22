import { useState } from "react";
import { Upload, CheckCircle2 } from "lucide-react";

const DetectionPage = () => {
  const [image, setImage] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFiles = (files: FileList | null) => {
    if (files && files[0]) {
      const reader = new FileReader();
      reader.onload = (e) => setImage(e.target?.result as string);
      reader.readAsDataURL(files[0]);
    }
  };

  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <h1 className="text-3xl font-bold mb-8 text-center">Disease Detection</h1>
      
      <div 
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(e) => { e.preventDefault(); setIsDragging(false); handleFiles(e.dataTransfer.files); }}
        className={`border-4 border-dashed rounded-3xl p-12 text-center transition-all ${
          isDragging ? "border-emerald-500 bg-emerald-50" : "border-slate-200 bg-white"
        }`}
      >
        {!image ? (
          <div className="flex flex-col items-center">
            <div className="w-20 h-20 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mb-4">
              <Upload size={40} />
            </div>
            <p className="text-xl font-medium">Drag and drop your crop photo here</p>
            <input 
              type="file" 
              className="hidden" 
              id="file-upload" 
              onChange={(e) => handleFiles(e.target.files)} 
            />
            <label htmlFor="file-upload" className="mt-4 px-6 py-2 bg-emerald-600 text-white rounded-lg cursor-pointer hover:bg-emerald-700">
              Browse Files
            </label>
          </div>
        ) : (
          <div className="space-y-6">
            <img src={image} alt="Preview" className="max-h-80 mx-auto rounded-lg shadow-lg" />
            <div className="flex justify-center gap-4">
              <button onClick={() => setImage(null)} className="px-6 py-2 border rounded-lg hover:bg-slate-50">Remove</button>
              <button className="px-6 py-2 bg-emerald-600 text-white rounded-lg flex items-center gap-2">
                <CheckCircle2 size={18} /> Analyze Image
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DetectionPage;