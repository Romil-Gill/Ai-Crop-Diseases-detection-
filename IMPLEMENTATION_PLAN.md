# IMPLEMENTATION PLAN: FASALRAKSHAK AI
**Target System**: FasalRakshak AI — Explainable Crop-Health & Early-Warning Platform  
**Tagline**: Scan. Understand. Act.  
**Event**: SIH Internal Hackathon  
**Status**: Revised Technical Architecture Blueprint & Phase 1 Plan

---

## 1. Product Identity & Design Direction

* **Brand Name**: **FasalRakshak AI**
* **Tagline**: *Scan. Understand. Act.*
* **Target Users**: Farmers & Field Extension Officers (Judges demo priority).
* **Design Philosophy**:
  * Clean, modern agricultural technology product (NOT a generic college ML dashboard).
  * Mobile-first, desktop-optimized layout.
  * **Color Palette**:
    * Warm off-white / light background (`#f8faf7`)
    * Deep agricultural green primary (`#1b4332` / `#2d6a4f`)
    * Lime / fresh green secondary accent (`#52b788` / `#74c69d`)
    * Amber warnings (`#d97706` / `#f59e0b`)
    * Red / coral critical alert states (`#dc2626` / `#ef4444`)
  * **Typography**: Clean, highly readable sans-serif (Inter / Outfit).
  * **Icons & Animation**: Lucide React icons, subtle purposeful micro-interactions.

### Primary Judge Flow
```
[Home] ──> [Select Crop] ──> [Scan / Upload Leaf] ──> [AI Analysis] ──> [Diagnosis Result] ──> [Explanation / Action]
```

### Supported Crop Scope (Strict Closed-Set)
The underlying model natively supports exactly **4 crops** across **27 classes**:
1. **Pumpkin** (5 classes)
2. **Rice** (3 classes)
3. **Sugarcane** (9 classes)
4. **Tomato** (10 classes)

*UI controls will explicitly restrict selection to these 4 supported crops. Unsupported crops will not be presented.*

---

## 2. Technical Architecture & Component Preservation

```
+-----------------------------------------------------------------------------------+
|                            FASALRAKSHAK AI PLATFORM                               |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                 PHASE 1B+ FRONTEND (React + Vite + Tailwind)                |  |
|  | - Crop Selector & Guided Image Uploader                                     |  |
|  | - Safe Diagnosis Result Display & Reliability Warnings                      |  |
|  | - Grad-CAM Visualizer Overlay                                               |  |
|  | - Verified Non-Chemical Advisory Cards                                      |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
|                                  REST API (JSON)                                  |
|                                        |                                          |
|  +-------------------------------------v---------------------------------------+  |
|  |                     FLASK REST API BACKEND (app.py)                         |  |
|  |                                                                             |  |
|  |  [GET /api/health]         - Server & Model Health Check                    |  |
|  |  [GET /api/classes]        - Supported 27 Classes & Crop Metadata           |  |
|  |  [POST /api/predict]       - Image Validation, Top-3 Softmax, Safe Gate    |  |
|  |  [POST /api/explain]       - Model-Inspected Grad-CAM Visualizer (Phase 2)  |  |
|  |                                                                             |  |
|  |  * Legacy HTML routes (/, /detect, /history, /contact) preserved untouched  |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
|  +-------------------------------------v---------------------------------------+  |
|  |                 UNTOUCHED CORE ML ASSETS (Preserved 100%)                   |  |
|  |  - crop_disease_model.keras (MobileNetV2 base +GAP + Dense 128 + Dense 27)    |  |
|  |  - Preprocessing Contract: (224, 224, 3) RGB float array, / 255.0 scaling     |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

### Safety & Preservation Commitments
- **Core Model**: `crop_disease_model.keras` will be used completely UNCHANGED. No re-training or modification.
- **Legacy Flask App**: Existing server-rendered HTML routes (`/`, `/detect`, `/history`, `/contact`, `/predict`) will be preserved so the current application remains 100% functional while new REST APIs are added.
- **Legacy Static Files**: HTML templates and static JS/CSS will NOT be deleted until full system verification in Phase 3.
- **Training Code**: `plant disease.py` will remain untouched as a reference document.

---

## 3. Mandatory Engineering Guards & Architectural Clarifications

### A. Safe Diagnosis Gate (Uncertainty & OOD Guard)
* **Clarification**: Softmax probabilities and top-1 vs top-2 margins do **NOT** constitute true Out-of-Distribution (OOD) detection. A closed-set 27-class model can still output high confidence on non-leaf or unsupported images.
* **MVP Protection Mechanism (Safe Diagnosis Gate)**:
  1. Mandatory user crop selection (`selected_crop`) prior to upload.
  2. Input file validation (MIME type check, image decode validation, size sanity check).
  3. Crop alignment check: Predicted class crop **must match** `selected_crop`.
  4. Minimum Top-1 confidence threshold (e.g. 60.0%).
  5. Minimum Top-1 vs Top-2 margin threshold (e.g. 15.0%).
  6. If any check fails, response returns `"diagnosis_reliable": false` and `"status": "uncertain"` with a specific human-readable reason (e.g., `"Predicted crop (Tomato) does not match selected crop (Rice)"`).
* **Future Enhancement**: True OOD leaf/non-leaf and unsupported-crop detection requires a separate binary validation model or embedding-distance estimator (documented for post-hackathon).

### B. Disease Severity Policy
* **Rule**: Disease severity MUST NOT be calculated from classifier confidence. Confidence represents classification certainty, NOT damage degree.
* **MVP Strategy**:
  - Keep confidence completely separate from severity.
  - Do NOT fabricate or output severity in `/api/predict`.
  - Severity will later be estimated via optional symptom verification or experimental lesion-area contour estimation, explicitly labeled as an **"Estimate"**.

### C. Agricultural Advisory Safety Policy
* **Rule**: Do NOT invent or hardcode arbitrary chemical pesticide names, dosages, or chemical application intervals.
* **MVP Architecture**:
  - Focus strictly on verified non-chemical advisory content: Disease Overview, Visual Symptoms, Immediate Non-Chemical Actions, Prevention, and Expert Escalation.
  - Chemical treatment fields will either be omitted or explicitly marked: `"requires_verified_agri_expert_data": true`.

### D. Grad-CAM Layer Inspection Policy
* Prior to implementing `/api/explain`, the backend code will programmatically inspect `model.layers` to identify the true name of the final 4D convolutional layer of `MobileNetV2` (e.g., `Conv_1` or `out_relu`) rather than hardcoding arbitrary layer names.

---

## 4. Phased Implementation Roadmap

### Phase 1A: Flask API Engine & Safety Verification (CURRENT FOCUS)
- [x] Refactor `app.py` to add CORS support.
- [x] Implement `GET /api/health` endpoint.
- [x] Implement `GET /api/classes` endpoint (returns 27 classes grouped by crop).
- [x] Implement `POST /api/predict` with Safe Diagnosis Gate:
  - Validates image file & MIME header.
  - Applies 224x224 RGB `/ 255.0` preprocessing.
  - Obtains real Top-3 predictions with exact class names and confidence percentages.
  - Evaluates selected crop vs predicted crop, top-1 threshold (60%), and top-1/top-2 margin (15%).
  - Returns structured JSON response (`diagnosis_reliable`, `status`, `uncertainty_reason`).
- [x] Create comprehensive automated test script (`test_api.py`) verifying all edge cases.
- [x] Confirm existing Jinja HTML routes remain fully operational.

### Phase 1B: Stable Vertical Slice Frontend (React + Vite)
- Build clean React single-page app (Crop Selector, Guided Image Upload, AI Analysis loading state, Safe Result Card).
- Connect React UI to `/api/predict`.
- Validate full end-to-end user flow.

### Phase 2: Grad-CAM Explainable AI Visualization
- Programmatically inspect model layers.
- Implement `POST /api/explain` generating Grad-CAM heatmaps overlaid on the leaf photo.
- Add opacity slider & highlight visualizer in React UI.

### Phase 3: Safe Non-Chemical Advisory & Diagnostic Polish
- Add structured advisory drawer (Symptoms, Non-chemical immediate care, Prevention, Expert escalation).
- Polish UI animations, typography, and theme styling for judge presentation.

### Deferred / Future Ecosystem Features (Post-MVP)
- Real-time weather risk API integration.
- Community disease radar map.
- Agri-Officer aggregate analytics dashboard.
- Five-language translation toggle.

---

## 5. Phase 1A API Specifications (`app.py`)

### `GET /api/health`
```json
{
  "status": "ok",
  "model_loaded": true,
  "supported_crops": ["Pumpkin", "Rice", "Sugarcane", "Tomato"],
  "total_classes": 27
}
```

### `GET /api/classes`
```json
{
  "crops": {
    "Pumpkin": ["Pumpkin-Bacterial Leaf Spot", "Pumpkin-Downy Mildew", ...],
    "Rice": ["Rice-Bacterialblight", "Rice-Brownspot", ...],
    "Sugarcane": ["Sugarcane-Grassy Shoot", ...],
    "Tomato": ["Tomato___Bacterial_spot", ...]
  },
  "total_classes": 27
}
```

### `POST /api/predict`
* **Form Parameters**: `file` (image binary), `selected_crop` (string, e.g. `"Tomato"`).
* **Success Response (`diagnosis_reliable`: true)**:
```json
{
  "status": "success",
  "selected_crop": "Tomato",
  "prediction": {
    "class_name": "Tomato___Early_blight",
    "crop": "Tomato",
    "condition": "Early Blight",
    "confidence": 94.52
  },
  "top_predictions": [
    { "class_name": "Tomato___Early_blight", "crop": "Tomato", "condition": "Early Blight", "confidence": 94.52 },
    { "class_name": "Tomato___Late_blight", "crop": "Tomato", "condition": "Late Blight", "confidence": 3.21 },
    { "class_name": "Tomato___Leaf_Mold", "crop": "Tomato", "condition": "Leaf Mold", "confidence": 1.10 }
  ],
  "diagnosis_reliable": true,
  "uncertainty_reason": null,
  "is_healthy": false
}
```

* **Uncertain Response (`diagnosis_reliable`: false)**:
```json
{
  "status": "uncertain",
  "selected_crop": "Rice",
  "prediction": {
    "class_name": "Tomato___Early_blight",
    "crop": "Tomato",
    "condition": "Early Blight",
    "confidence": 88.10
  },
  "top_predictions": [ ... ],
  "diagnosis_reliable": false,
  "uncertainty_reason": "Predicted crop (Tomato) does not match user-selected crop (Rice).",
  "is_healthy": false
}
```
