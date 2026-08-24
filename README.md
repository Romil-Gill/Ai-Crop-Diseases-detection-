# FasalRakshak AI — Explainable Crop-Health & Early-Warning Platform

**Tagline**: *Scan. Understand. Act.*  
**Event**: SIH Internal Hackathon

---

## Quick Start Guide

### 1. Backend Setup (Flask ML Server)

```bash
# Create and activate Python virtual environment
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start Flask backend API
python app.py
```
*Backend API server runs at `http://127.0.0.1:5000`.*

---

### 2. Frontend Setup (React + Vite App)

```bash
# Navigate to React app directory
cd "crop disease detection folder/crop-app"

# Install Node dependencies
npm install

# Start Vite dev server
npm run dev
```
*React frontend runs at `http://localhost:5173`.*

---

## Supported Crops (27 Classes Total)

- **Tomato** (10 classes): Bacterial spot, Early blight, Late blight, Leaf mold, Septoria leaf spot, Spider mites, Target spot, Yellow leaf curl virus, Mosaic virus, Healthy
- **Rice** (3 classes): Bacterial blight, Brown spot, Leaf smut
- **Sugarcane** (9 classes): Grassy shoot, Healthy, Mosaic, Pokkah boeng, Red leaf spot, Red rot, Ring spot, Wilt, Yellow leaf disease
- **Pumpkin** (5 classes): Bacterial leaf spot, Downy mildew, Healthy, Mosaic disease, Powdery mildew

---

## Production Deployment

This project is configured for a split-stack deployment for optimal performance and compatibility:

- **Frontend**: React + Vite (Recommended host: **Vercel**)
- **Backend**: Flask API + TensorFlow (Recommended host: **Render**, **Railway**, or **Google Cloud Run**)

> **Note**: Vercel's serverless functions have a 250 MB size limit, which the `tensorflow` package exceeds. This is why a separate backend host is required.

### 1. Backend Deployment

1. The `crop_disease_model.keras` file is fully tracked in Git and is the only artifact required for inference. The original 30,000+ image training dataset is **NOT** required at runtime and should not be uploaded.
2. The `requirements.txt` is updated to use `opencv-python-headless` for headless Linux environments.
3. Deploy the root directory to your chosen Python host (e.g., Render Web Service). 
4. Ensure the start command is `gunicorn app:app`.

### 2. Frontend Deployment (Vercel)

1. Deploy the `crop disease detection folder/crop-app/` directory to Vercel.
2. In the Vercel project settings, set the **Environment Variable**:
   - `VITE_API_BASE_URL` = `<your-backend-live-url>`
3. A `vercel.json` is already provided to handle React Router SPA rewrites correctly.
