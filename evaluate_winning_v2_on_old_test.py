import os
import csv
import json
import numpy as np
import tensorflow as tf
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset_6crop')
MANIFEST_PATH = os.path.join(BASE_DIR, 'dataset_manifest.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'crop_disease_model_v2_6crop.keras')

CLASSES = [
    'Pumpkin-Bacterial Leaf Spot', 'Pumpkin-Downy Mildew', 'Pumpkin-Healthy Leaf', 
    'Pumpkin-Mosaic Disease', 'Pumpkin-Powdery_Mildew', 'Rice-Bacterialblight', 
    'Rice-Brownspot', 'Rice-Leafsmut', 'Sugarcane-Grassy Shoot', 'Sugarcane-Healthy', 
    'Sugarcane-Mosaic', 'Sugarcane-Pokkah Boeng', 'Sugarcane-Red Leaf Spot', 
    'Sugarcane-Red Rot', 'Sugarcane-Ring Spot', 'Sugarcane-Wilt', 
    'Sugarcane-Yellow Leaf Disease', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 
    'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 
    'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy',
    'Wheat___Healthy', 'Wheat___Leaf_Rust', 'Wheat___Stripe_Rust', 'Wheat___Powdery_Mildew', 'Wheat___Septoria',
    'Maize___Healthy', 'Maize___Common_Rust', 'Maize___Northern_Leaf_Blight', 'Maize___Gray_Leaf_Spot'
]

CROPS = ['Tomato', 'Rice', 'Sugarcane', 'Pumpkin', 'Wheat', 'Maize']

def main():
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    by_class = {}
    for r in rows:
        folder = r['file'].replace('\\', '/').split('/')[0]
        if folder not in by_class:
            by_class[folder] = []
        by_class[folder].append(r)

    test_imgs, test_lbls, test_crops = [], [], []
    np.random.seed(42)

    for cname in CLASSES:
        class_rows = by_class.get(cname, [])
        if not class_rows:
            continue
        np.random.shuffle(class_rows)
        # 15% test split of full dataset (approx 1,734 total test images across full 11,560 images)
        n_tot = len(class_rows)
        n_train = int(n_tot * 0.70)
        n_val = int(n_tot * 0.15)
        test_r = class_rows[n_train + n_val:]
        c_idx = CLASSES.index(cname)
        crop_name = cname.split('-')[0].split('_')[0]
        for r in test_r:
            rel_p = r['file']
            ipath = os.path.join(DATASET_DIR, rel_p)
            if not os.path.exists(ipath):
                ipath = os.path.join(BASE_DIR, rel_p)
                if not os.path.exists(ipath):
                    continue
            img = Image.open(ipath).convert('RGB').resize((224, 224))
            arr = np.array(img, dtype=np.float32)
            test_imgs.append(arr)
            test_lbls.append(c_idx)
            test_crops.append(crop_name)

    X_test_raw = np.array(test_imgs, dtype=np.float32)
    y_test = np.array(test_lbls, dtype=np.int32)
    X_test_prep = tf.keras.applications.mobilenet_v2.preprocess_input(np.copy(X_test_raw))

    print(f"Loaded Full Dataset Test Split Size: {len(y_test)} images")
    preds_raw = model.predict(X_test_prep, batch_size=32, verbose=0)
    y_pred = np.argmax(preds_raw, axis=1)

    test_acc = float(np.mean(y_test == y_pred) * 100)
    num_c = len(CLASSES)
    cm = np.zeros((num_c, num_c), dtype=int)
    for t, p in zip(y_test, y_pred):
        cm[t, p] += 1

    precisions, recalls, f1s = [], [], []
    for i in range(num_c):
        tp = cm[i, i]
        fp = np.sum(cm[:, i]) - tp
        fn = np.sum(cm[i, :]) - tp
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        precisions.append(prec)
        recalls.append(rec)
        f1s.append(f1)

    macro_prec = float(np.mean(precisions))
    macro_rec = float(np.mean(recalls))
    macro_f1 = float(np.mean(f1s))

    cross_crop_mismatches = 0
    crop_stats = {c: {'correct': 0, 'total': 0} for c in CROPS}
    for t, p, crop_name in zip(y_test, y_pred, test_crops):
        t_crop = CLASSES[t].split('-')[0].split('_')[0]
        p_crop = CLASSES[p].split('-')[0].split('_')[0]
        if t_crop != p_crop:
            cross_crop_mismatches += 1
        if t_crop in crop_stats:
            crop_stats[t_crop]['total'] += 1
            if t == p:
                crop_stats[t_crop]['correct'] += 1

    cross_crop_alignment = float((len(y_test) - cross_crop_mismatches) / len(y_test) * 100)

    print(f"\n==================================================")
    print(f"FULL FIXED TEST SPLIT RE-EVALUATION RESULTS ({len(y_test)} Samples)")
    print(f"==================================================")
    print(f"Accuracy:             {test_acc:.2f}%")
    print(f"Macro Precision:      {macro_prec:.4f}")
    print(f"Macro Recall:         {macro_rec:.4f}")
    print(f"Macro F1-Score:       {macro_f1:.4f}")
    print(f"Cross-Crop Alignment: {cross_crop_alignment:.2f}% ({cross_crop_mismatches} errors out of {len(y_test)})")
    print("\nPer-Crop Breakdown:")
    for c in CROPS:
        st = crop_stats[c]
        c_acc = (st['correct'] / st['total'] * 100) if st['total'] > 0 else 0.0
        print(f"  {c:<10}: {c_acc:.2f}% ({st['correct']}/{st['total']})")

if __name__ == '__main__':
    main()
