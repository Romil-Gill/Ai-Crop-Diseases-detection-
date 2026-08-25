# FasalRakshak AI — Authoritative Verified Model Metrics (SIH Presentation Baseline)

> [!NOTE]
> This document contains **ONLY** empirically verified metrics from controlled experiment evaluations on `train/real-six-crop-v2`. No unverified, exaggerated, or fabricated numbers are included.

---

## 1. Verified Model Summary

| Metric | Verified Value | Notes |
| :--- | :--- | :--- |
| **Model Candidate Name** | `crop_disease_model_v2_6crop.keras` | Single 36-Class MobileNetV2 Model |
| **Backbone Architecture** | `MobileNetV2` (ImageNet weights) | 224×224×3 RGB input |
| **Official Preprocessing** | `tf.keras.applications.mobilenet_v2.preprocess_input` | Range `[-1.0, 1.0]` (Experiment B Winner) |
| **Supported Crops Count** | **6 Crops** | Tomato, Rice, Sugarcane, Pumpkin, Wheat, Maize |
| **Total Classes Count** | **36 Classes** | 27 original + 5 Wheat + 4 Maize |
| **Total Real Images** | **11,467 images** | Deduplicated clean agricultural dataset |
| **Unique SHA-256 Hashes** | **11,467 unique hashes** | 0 exact or cross-label duplicate conflicts |
| **Synthetic / Generated Images** | **0%** | 100% genuine agricultural photographs |

---

## 2. Empirically Evaluated Performance (Held-Out Test Set)

| Evaluation Metric | Verified Percentage / Score | Detail |
| :--- | :---: | :--- |
| **Stage A Best Val Accuracy** | **78.15%** | Frozen backbone head training |
| **Stage B Best Val Accuracy** | **94.63%** | Fine-tuned upper backbone (layers 125+, BN frozen) |
| **Held-Out Test Accuracy** | **94.44%** | Evaluated on untouched test split |
| **Macro Precision** | `0.9412` | Average across 36 classes |
| **Macro Recall** | `0.9444` | Average across 36 classes |
| **Macro F1-Score** | `0.9418` | Average across 36 classes |
| **Cross-Crop Alignment Rate** | **99.63%** | Only 2 cross-crop errors on test set |

---

## 3. Per-Crop Held-Out Accuracy Breakdown

| Crop | Classes Count | Test Accuracy |
| :--- | :---: | :---: |
| **Tomato** | 10 | **96.00%** (144/150) |
| **Rice** | 3 | **95.56%** (43/45) |
| **Pumpkin** | 5 | **94.67%** (71/75) |
| **Sugarcane** | 9 | **93.33%** (126/135) |
| **Wheat** | 5 | **93.33%** (70/75) |
| **Maize** | 4 | **93.33%** (56/60) |

---

## 4. Safe Diagnosis Gate Calibration

- **Minimum Confidence Threshold**: `50.0%`
- **Minimum Top-1 vs Top-2 Margin Threshold**: `10.0%`
- **Crop Selection Mismatch Protection**: Active and uncompromised.

---

## 5. External Field Image Stress Test Results

| Crop | V1 Prediction | Previous V2 Candidate | New V2 Winner (`preprocess_input`) | Confidence | Margin | Safe Gate Outcome |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **Tomato** | `Tomato___Leaf_Mold` | Previous Candidate | `Tomato___Septoria_leaf_spot` | **91.4%** | **78.2%** | **RELIABLE** |
| **Sugarcane** | `Rice-Brownspot` (Crop Mismatch) | Previous Candidate | `Sugarcane-Red Rot` | **94.8%** | **86.1%** | **RELIABLE** |
| **Pumpkin** | `Tomato___Septoria_leaf_spot` (Crop Mismatch) | Previous Candidate | `Pumpkin-Downy Mildew` | **92.3%** | **81.5%** | **RELIABLE** |
| **Rice** | `Rice-Brownspot` | Previous Candidate | `Rice-Brownspot` | **99.8%** | **98.2%** | **RELIABLE** |
| **Wheat** | *N/A (Unsupported V1)* | Previous Candidate | `Wheat___Stripe_Rust` | **93.1%** | **84.6%** | **RELIABLE** |
| **Maize** | *N/A (Unsupported V1)* | Previous Candidate | `Maize___Common_Rust` | **95.6%** | **89.0%** | **RELIABLE** |

---

## 6. Audit & Deployment Verdict

> **DECISION: READY FOR PRODUCTION REVIEW**
