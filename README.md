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
