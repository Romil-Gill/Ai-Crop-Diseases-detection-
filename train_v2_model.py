"""
FasalRakshak AI - Single 36-Class MobileNetV2 Model Retraining Engine
Trains MobileNetV2 architecture from clean ImageNet weights on real dataset with data augmentation,
staged fine-tuning, and early stopping.
"""

import os
import json
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset_6crop")
MODEL_V2_PATH = os.path.join(BASE_DIR, "crop_disease_model_v2_6crop.keras")
BEST_WEIGHTS_PATH = os.path.join(BASE_DIR, "best_v2_weights.keras")
MAPPING_V2_PATH = os.path.join(BASE_DIR, "class_mapping_v2.json")
METADATA_V2_PATH = os.path.join(BASE_DIR, "model_metadata_v2.json")

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

def retrain_single_model():
    print("==================================================")
    print("  RETRAINING SINGLE 36-CLASS MOBILENETV2 MODEL")
    print("==================================================")

    # Save mapping
    class_mapping = {str(i): cname for i, cname in enumerate(CLASSES)}
    with open(MAPPING_V2_PATH, "w", encoding="utf-8") as f:
        json.dump(class_mapping, f, indent=2)

    img_size = (224, 224)
    batch_size = 16

    # Load Train/Val datasets
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=img_size,
        batch_size=batch_size,
        class_names=CLASSES
    )
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=img_size,
        batch_size=batch_size,
        class_names=CLASSES
    )

    # Preprocessing / 255.0
    train_ds = train_ds.map(lambda x, y: (x / 255.0, y))
    val_ds = val_ds.map(lambda x, y: (x / 255.0, y))

    # Data Augmentation pipeline
    data_aug = tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        layers.RandomTranslation(0.05, 0.05),
    ], name="data_augmentation")

    # Build Clean MobileNetV2 Model
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False

    inputs = layers.Input(shape=(224, 224, 3))
    x = data_aug(inputs)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(len(CLASSES), activation='softmax')(x)

    model = models.Model(inputs, outputs, name="Single_36Class_MobileNetV2")

    checkpoint_cb = callbacks.ModelCheckpoint(
        BEST_WEIGHTS_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    early_stop_cb = callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    reduce_lr_cb = callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=2,
        verbose=1
    )

    # STAGE A: Train Classifier Head
    print("\n[STAGE A] Training classifier head (frozen backbone)...")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    model.fit(train_ds, validation_data=val_ds, epochs=8, callbacks=[checkpoint_cb, early_stop_cb])

    # STAGE B: Fine-tune Upper Backbone Blocks (layers 130+)
    print("\n[STAGE B] Fine-tuning upper MobileNetV2 backbone...")
    base_model.trainable = True
    for layer in base_model.layers[:130]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    model.fit(train_ds, validation_data=val_ds, epochs=10, callbacks=[checkpoint_cb, early_stop_cb, reduce_lr_cb])

    # Save best model to candidate path
    model.save(MODEL_V2_PATH)
    print(f"\n[MODEL SAVED] Saved retrained Single 36-Class model to '{MODEL_V2_PATH}'")

if __name__ == "__main__":
    retrain_single_model()
