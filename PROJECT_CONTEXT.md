# PROJECT CONTEXT & COMPREHENSIVE SYSTEM ANALYSIS
**Project**: FasalRakshak AI (Upgraded from LeafGuard AI / Crop Disease Detection)  
**Date**: August 22, 2026  
**Phase**: Phase 1 - Read-Only Analysis & Technical Assessment

---

## 1. Functional Assessment & Current Status

### Which application is functional right now?
* **Working Application**: **Flask + Jinja2 Monolithic App** located at the root directory (`app.py`, `templates/`, `static/`).
  * Running `python app.py` launches a Flask server on `http://127.0.0.1:5000`.
  * Renders server-side HTML templates (`index.html`, `detect.html`, `history.html`, `contact.html`).
  * Accepts file uploads via `POST /predict`, processes the leaf image through `crop_disease_model.keras`, and returns JSON predictions (`prediction`, `confidence`, `status`).
* **Broken / Non-functional Application**: **React + Vite Frontend** located inside `crop disease detection folder/crop-app`.
  * The React project setup is broken and incomplete.
  * `src/` directory is missing critical entry points: `index.html`, `main.tsx`, `App.tsx`, and `index.css`.
  * Page components (`ContactPage.tsx`, `DetectionPage.tsx`, `HistoryPage.tsx`) are misplaced inside `src/assets/pages/`.
  * `DetectionPage.tsx` contains dummy UI state with no `fetch` / `axios` integration to the Flask backend.

---

## 2. Architecture & Technical Stack

### Current Architecture Diagram
```
+-----------------------------------------------------------------------+
|                      FLASK MONOLITH (Port 5000)                       |
|                                                                       |
|   +-------------------+       +-------------------------------+       |
|   | Jinja2 Templates  |       | Static Assets                 |       |
|   | (index, detect,   |       | (styles.css, script.js,       |       |
|   |  history, contact)|       |  detect.js, hero-farm.jpg)    |       |
|   +---------+---------+       +---------------+---------------+       |
|             |                                 |                       |
|             +-----------------+---------------+                       |
|                               |                                       |
|                               v                                       |
|                  +--------------------------+                         |
|                  | Flask Routes (app.py)    |                         |
|                  | GET /                    |                         |
|                  | GET /detect              |                         |
|                  | GET /history             |                         |
|                  | GET /contact             |                         |
|                  | POST /predict            |                         |
|                  +------------+-------------+                         |
|                               |                                       |
|                               v                                       |
|                  +--------------------------+                         |
|                  | TensorFlow Keras Model   |                         |
|                  | crop_disease_model.keras |                         |
|                  +--------------------------+                         |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
|                ABANDONED REACT FRONTEND (Non-functional)              |
|   crop disease detection folder/crop-app                              |
|   - Missing index.html, main.tsx, App.tsx                             |
|   - Misplaced components in src/assets/pages/                         |
|   - No API connection to Flask backend                                |
+-----------------------------------------------------------------------+
```

### Technology Stack Table
| Component | Technology | Version / Details | Status |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | Python / Flask | Flask 3.x, Flask-CORS | Functional |
| **ML Engine** | TensorFlow / Keras | Keras 3.x (`.keras` format) | Functional |
| **Base Model Architecture** | MobileNetV2 | Transfer Learning (ImageNet weights, frozen) | Functional |
| **Server-Side UI** | Jinja2 HTML / CSS / JS | FontAwesome 6.0, Inter Font | Functional |
| **Client-Side UI** | React / Vite / TypeScript | React 19, Vite 8, Tailwind CSS, Lucide React | Broken / Disconnected |
| **Data Storage** | Browser `localStorage` | Storage key: `leafHistory` | Client-only, unpersisted |

---

## 3. ML Model Deep-Dive (`crop_disease_model.keras`)

### Model Specifications
* **File Name**: `crop_disease_model.keras`
* **File Size**: ~11.6 MB
* **Base Network**: `MobileNetV2` (input shape: `224x224x3`, `include_top=False`, weights: `'imagenet'`, `trainable=False`)
* **Classifier Head**:
  * `GlobalAveragePooling2D()`
  * `Dense(128, activation='relu')`
  * `Dense(27, activation='softmax')`
* **Loss Function**: `sparse_categorical_crossentropy`
* **Optimizer**: `adam`

### Input Dimensions & Preprocessing Contract
* **Target Input Resolution**: `224 x 224` pixels, 3 channels (RGB).
* **Preprocessing Workflow**:
  1. Image loaded/resized: `image.load_img(img_path, target_size=(224, 224))`
  2. Array conversion: `image.img_to_array(img)`
  3. Scaling & Batching: `np.expand_dims(img_array, axis=0) / 255.0`
  4. Pass tensor shape `(1, 224, 224, 3)` to `model.predict()`.

### Supported Crops & 27 Prediction Classes

```
+-------------------------------------------------------------------------------------+
| SUPPORTED CROPS & CLASSES (27 TOTAL)                                                |
+-------------------+-----------------------------------------------------------------+
| Crop (4 Categories)| Supported Disease / Healthy Classes                            |
+-------------------+-----------------------------------------------------------------+
| 1. Pumpkin        | - Pumpkin-Bacterial Leaf Spot                                   |
| (5 classes)       | - Pumpkin-Downy Mildew                                          |
|                   | - Pumpkin-Healthy Leaf                                          |
|                   | - Pumpkin-Mosaic Disease                                        |
|                   | - Pumpkin-Powdery_Mildew                                        |
+-------------------+-----------------------------------------------------------------+
| 2. Rice           | - Rice-Bacterialblight                                          |
| (3 classes)       | - Rice-Brownspot                                                |
|                   | - Rice-Leafsmut                                                 |
+-------------------+-----------------------------------------------------------------+
| 3. Sugarcane      | - Sugarcane-Grassy Shoot                                        |
| (9 classes)       | - Sugarcane-Healthy                                             |
|                   | - Sugarcane-Mosaic                                              |
|                   | - Sugarcane-Pokkah Boeng                                        |
|                   | - Sugarcane-Red Leaf Spot                                       |
|                   | - Sugarcane-Red Rot                                             |
|                   | - Sugarcane-Ring Spot                                           |
|                   | - Sugarcane-Wilt                                                |
|                   | - Sugarcane-Yellow Leaf Disease                                 |
+-------------------+-----------------------------------------------------------------+
| 4. Tomato         | - Tomato___Bacterial_spot                                       |
| (10 classes)      | - Tomato___Early_blight                                         |
|                   | - Tomato___Late_blight                                          |
|                   | - Tomato___Leaf_Mold                                            |
|                   | - Tomato___Septoria_leaf_spot                                   |
|                   | - Tomato___Spider_mites Two-spotted_spider_mite                |
|                   | - Tomato___Target_Spot                                          |
|                   | - Tomato___Tomato_Yellow_Leaf_Curl_Virus                        |
|                   | - Tomato___Tomato_mosaic_virus                                  |
|                   | - Tomato___healthy                                              |
+-------------------+-----------------------------------------------------------------+
```

---

## 4. API Endpoints & Routes Analysis

| Route Path | HTTP Method | Handler Function | Purpose | Response Type |
| :--- | :--- | :--- | :--- | :--- |
| `/` | `GET` | `home()` | Renders main landing page | `text/html` |
| `/detect` | `GET` | `detect()` | Renders leaf upload & detection view | `text/html` |
| `/history` | `GET` | `history()` | Renders scan history table | `text/html` |
| `/contact` | `GET` | `contact()` | Renders expert contact form | `text/html` |
| `/predict` | `POST` | `predict_api()` | Accepts multipart `file`, returns top class prediction & confidence | `application/json` |

---

## 5. File Inventory & Categorization

### A. Essential & Reusable Files (Keep & Refactor)
* `crop_disease_model.keras`: Trained weights and architecture for 27 crop disease classes. Must be preserved.
* `app.py`: Contains working model load logic, preprocessing code, class mapping, and Flask API integration.
* `plant disease.py`: Reference script showing how model layers were constructed (MobileNetV2 + GAP + Dense(128) + Dense(27)). Needed to construct Grad-CAM feature extractor.
* `static/hero-farm.jpg`: High-resolution background image asset.

### B. Obsolete / Duplicate / Broken Files (To Clean Up or Replace)
* `crop disease detection folder/crop-app/`: Broken Vite template with missing files and disconnected UI components. Needs to be replaced with a clean, unified modern React/Vite app connected to Flask.
* `predict.py`: Hardcoded desktop CLI test script (`C:\Users\Lenovo\OneDrive\Desktop\images.jpg`). Obsolete.
* `static/js/detect.js`: Redundant script duplicate of `static/js/script.js`.
* `package.json` & `package-lock.json` (at root): Orphaned node dependencies (`axios`, `sonner`) with no build configuration.
* Root junk files: `60`, `{`, empty `README.md`.

---

## 6. Fake, Placeholder & Inconsistent Content Audit

1. **Tech Stack Falsehood**: Landing page (`templates/index.html` line 13) claims diagnosis is powered by **TensorFlow Lite**, but backend uses full `tensorflow.keras`.
2. **Class Count Misrepresentation**: Landing page claims "25+ Classes" (it is exactly 27 classes across 4 crops).
3. **React Mock Data Inconsistency**: `HistoryPage.tsx` displays mock scans for Potato (Healthy) and Corn (Common Rust), neither of which exist in the model's 27 supported classes.
4. **Non-functional Contact Forms**: Contact page forms (both HTML & React) perform zero POST handling or mail delivery.
5. **No Out-of-Distribution Handling**: Uploading a non-leaf or non-supported crop image forces the model to pick one of the 27 classes with high confidence.
6. **No Uncertainty or Top-K Probabilities**: `/predict` only returns `prediction` and `confidence` for `argmax(prediction)`, discarding runner-up probabilities.

---

## 7. Technical Risks for Hackathon Demo

* **Risk 1: UI / Backend Disconnect**: Presenting the React app without connecting it to Flask will cause instant demo failure.
* **Risk 2: Out-of-Distribution Inputs**: If a judge uploads an arbitrary image (e.g. wheat, corn, or a non-plant), the raw model will confidently output a false label (e.g., "Tomato Early Blight 98%").
* **Risk 3: Model Cold-Start Latency**: Loading `tensorflow` inside Flask during startup takes 3-5 seconds.
* **Risk 4: Browser Caching & Storage**: Scan history is currently saved in browser `localStorage`. Refreshing or changing browsers clears history.
* **Risk 5: Folder Naming Spaces**: Path `crop disease detection folder` contains spaces, causing execution path issues in command line tooling.
