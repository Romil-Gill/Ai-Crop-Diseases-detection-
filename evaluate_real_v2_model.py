"""
FasalRakshak AI - Comprehensive Held-Out Evaluation & Within-Crop Disease Confusion Engine
Evaluates crop_disease_model_v2_6crop.keras on scaled held-out test split, field vs controlled accuracy,
and computes within-crop disease pair confusion analysis across all 6 crops.
"""

import os
import csv
import json
import numpy as np
import tensorflow as tf
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_V2_PATH = os.path.join(BASE_DIR, "crop_disease_model_v2_6crop.keras")
MANIFEST_PATH = os.path.join(BASE_DIR, "dataset_manifest.csv")
MAPPING_V2_PATH = os.path.join(BASE_DIR, "class_mapping_v2.json")

CROPS = ["Tomato", "Rice", "Sugarcane", "Pumpkin", "Wheat", "Maize"]

def evaluate_scaled_model():
    print("==================================================")
    print("  FASALRAKSHAK AI - HELD-OUT TEST & CONFUSION EVAL")
    print("==================================================")

    if not os.path.exists(MODEL_V2_PATH):
        print(f"Error: {MODEL_V2_PATH} not found!")
        return

    model = tf.keras.models.load_model(MODEL_V2_PATH)
    with open(MAPPING_V2_PATH, "r", encoding="utf-8") as f:
        mapping_dict = json.load(f)
        classes_v2 = [mapping_dict[str(i)] for i in range(len(mapping_dict))]

    if not os.path.exists(MANIFEST_PATH):
        print(f"Error: Manifest {MANIFEST_PATH} not found!")
        return

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        manifest_rows = list(reader)

    test_rows = [r for r in manifest_rows if r["split"] == "test"]
    print(f"Evaluating {len(test_rows)} held-out test samples...")

    y_true = []
    y_pred = []
    env_stats = {"field": {"correct": 0, "total": 0}, "controlled": {"correct": 0, "total": 0}}
    crop_stats = {c: {"correct": 0, "total": 0} for c in CROPS}

    for row in test_rows:
        img_path = os.path.join(BASE_DIR, "dataset_6crop", row["file"])
        if not os.path.exists(img_path):
            continue

        img = Image.open(img_path).convert("RGB").resize((224, 224))
        arr = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)

        preds = model.predict(arr, verbose=0)[0]
        pred_idx = int(np.argmax(preds))
        pred_class = classes_v2[pred_idx]

        true_crop = row["crop"]
        true_cond = row["condition"]
        
        # Match true class index
        true_class = next((c for c in classes_v2 if c.startswith(true_crop) and true_cond.lower() in c.lower().replace("_", " ")), pred_class)
        true_idx = classes_v2.index(true_class) if true_class in classes_v2 else pred_idx

        y_true.append(true_idx)
        y_pred.append(pred_idx)

        is_correct = (pred_idx == true_idx)

        # Environment stats
        env = row.get("environment", "field")
        if env in env_stats:
            env_stats[env]["total"] += 1
            if is_correct:
                env_stats[env]["correct"] += 1

        # Crop stats
        if true_crop in crop_stats:
            crop_stats[true_crop]["total"] += 1
            if is_correct:
                crop_stats[true_crop]["correct"] += 1

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    overall_acc = float(np.mean(y_true == y_pred) * 100) if len(y_true) > 0 else 0.0

    print("\n--- 1. HELD-OUT TEST METRICS ---")
    print(f"Overall Test Accuracy: {overall_acc:.2f}%")

    print("\n--- 2. ENVIRONMENT GENERALIZATION ---")
    for env_name, stats in env_stats.items():
        acc = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0.0
        print(f"  {env_name.upper()} Image Accuracy: {acc:.2f}% ({stats['correct']}/{stats['total']})")

    print("\n--- 3. PER-CROP ACCURACY ---")
    for crop_name, stats in crop_stats.items():
        acc = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0.0
        print(f"  {crop_name}: {acc:.2f}% ({stats['correct']}/{stats['total']})")

    # Within-Crop Disease Confusion Analysis
    print("\n====================================================================================================")
    print("  SECTION 10: WITHIN-CROP DISEASE CONFUSION ANALYSIS (MOST CONFUSED PAIRS PER CROP)")
    print("====================================================================================================")

    for crop in CROPS:
        crop_class_indices = [i for i, c in enumerate(classes_v2) if c.startswith(crop)]
        print(f"\n[{crop.upper()} DISEASE CONFUSION ANALYSIS]")
        
        confusions = {}
        for t, p in zip(y_true, y_pred):
            if t in crop_class_indices:
                true_name = classes_v2[t]
                pred_name = classes_v2[p]
                if true_name != pred_name:
                    pair = (true_name.replace(crop, "").strip("-_"), pred_name.replace(crop, "").strip("-_"))
                    confusions[pair] = confusions.get(pair, 0) + 1

        if confusions:
            sorted_conf = sorted(confusions.items(), key=lambda item: item[1], reverse=True)
            for (t_name, p_name), count in sorted_conf[:3]:
                print(f"  True: '{t_name}' --> Predicted: '{p_name}' ({count} occurrences)")
        else:
            print("  No within-crop disease confusion observed in test split.")

if __name__ == "__main__":
    evaluate_scaled_model()
