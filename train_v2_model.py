"""
FasalRakshak AI - Phase 8 Model Retraining Script
Expands crop model from 4 crops (27 classes) to 6 crops (36 classes: +5 Wheat, +4 Maize).
Generates class_mapping_v2.json and validates crop_disease_model_v2_6crop.keras.
"""

import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset_6crop")
MODEL_V1_PATH = os.path.join(BASE_DIR, "crop_disease_model.keras")
MODEL_V2_PATH = os.path.join(BASE_DIR, "crop_disease_model_v2_6crop.keras")
MAPPING_V2_PATH = os.path.join(BASE_DIR, "class_mapping_v2.json")

# 36 Exact Classes
CLASSES = [
    # 27 Existing Classes
    'Pumpkin-Bacterial Leaf Spot', 'Pumpkin-Downy Mildew', 'Pumpkin-Healthy Leaf', 
    'Pumpkin-Mosaic Disease', 'Pumpkin-Powdery_Mildew', 'Rice-Bacterialblight', 
    'Rice-Brownspot', 'Rice-Leafsmut', 'Sugarcane-Grassy Shoot', 'Sugarcane-Healthy', 
    'Sugarcane-Mosaic', 'Sugarcane-Pokkah Boeng', 'Sugarcane-Red Leaf Spot', 
    'Sugarcane-Red Rot', 'Sugarcane-Ring Spot', 'Sugarcane-Wilt', 
    'Sugarcane-Yellow Leaf Disease', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 
    'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 
    'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy',
    # 5 Wheat Classes
    'Wheat___Healthy', 'Wheat___Leaf_Rust', 'Wheat___Stripe_Rust', 'Wheat___Powdery_Mildew', 'Wheat___Septoria',
    # 4 Maize Classes
    'Maize___Healthy', 'Maize___Common_Rust', 'Maize___Northern_Leaf_Blight', 'Maize___Gray_Leaf_Spot'
]

def validate_real_dataset():
    """Validates that a genuine labelled image dataset exists before training."""
    if not os.path.exists(DATASET_DIR):
        raise RuntimeError(
            f"Dataset directory '{DATASET_DIR}' not found. "
            "Real labelled crop disease dataset is required. Synthetic fallback is strictly disabled."
        )
    
    missing_or_insufficient = []
    for cname in CLASSES:
        cdir = os.path.join(DATASET_DIR, cname)
        if not os.path.exists(cdir) or len([f for f in os.listdir(cdir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]) < 10:
            missing_or_insufficient.append(cname)
            
    if missing_or_insufficient:
        raise RuntimeError(
            f"Real labelled dataset is incomplete or missing for {len(missing_or_insufficient)} classes: "
            f"{missing_or_insufficient[:5]}... Synthetic fallback is strictly disabled."
        )
    print(f"[DATASET CHECK] Verified real labelled image dataset across all {len(CLASSES)} classes.")

def train_and_evaluate():
    validate_real_dataset()
    
    # Save Machine-Readable Class Mapping (8.14)
    class_mapping = {str(i): cname for i, cname in enumerate(CLASSES)}
    with open(MAPPING_V2_PATH, "w", encoding="utf-8") as f:
        json.dump(class_mapping, f, indent=2)
    print(f"[CLASS MAPPING] Saved machine-readable mapping to {MAPPING_V2_PATH}")
    
    # Load dataset with deterministic split
    img_size = (224, 224)
    batch_size = 16
    
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=img_size,
        batch_size=batch_size,
        class_names=CLASSES
    )
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=img_size,
        batch_size=batch_size,
        class_names=CLASSES
    )
    
    train_ds = train_ds.map(lambda x, y: (x / 255.0, y))
    val_ds = val_ds.map(lambda x, y: (x / 255.0, y))
    
    # Load pre-trained backbone
    print("[MODEL BUILD] Constructing MobileNetV2 36-Class Model...")
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(name="global_average_pooling2d"),
        layers.Dense(128, activation='relu', name="dense"),
        layers.Dense(len(CLASSES), activation='softmax', name="dense_1")
    ])
    
    # STAGE A: Train classifier head
    print("[TRAINING STAGE A] Training classifier head (frozen backbone)...")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=1
    )
    
    model.save(MODEL_V2_PATH)
    print(f"[MODEL CHECKPOINT] Saved v2 candidate model to {MODEL_V2_PATH}")
    
    # STAGE B: Fine-tune upper backbone layers
    print("[TRAINING STAGE B] Fine-tuning upper MobileNetV2 backbone...")
    base_model.trainable = True
    for layer in base_model.layers[:140]:
        layer.trainable = False
        
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=1
    )
    
    model.save(MODEL_V2_PATH)
    print(f"[MODEL SAVED] Saved final candidate v2 model to {MODEL_V2_PATH}")
    
    # Evaluate using numpy
    print("\n==================================================")
    print("  MODEL EVALUATION & METRICS REPORT")
    print("==================================================")
    
    y_true = []
    y_pred = []
    for x_batch, y_batch in val_ds:
        preds = model.predict(x_batch, verbose=0)
        y_pred.extend(np.argmax(preds, axis=1))
        y_true.extend(y_batch.numpy())
        
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    print(f"Total Validation Samples Evaluated: {len(y_true)}")
    acc = np.mean(y_true == y_pred) * 100
    print(f"Overall Accuracy: {acc:.2f}%")
    
    num_classes = len(CLASSES)
    cm = np.zeros((num_classes, num_classes), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1
        
    print(f"Confusion Matrix Shape: {cm.shape}")
    return True

if __name__ == "__main__":
    train_and_evaluate()
