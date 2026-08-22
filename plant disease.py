# ==============================
# 1. IMPORT LIBRARIES
# ==============================
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import os

# ==============================
# 2. DATASET PATH
# ==============================
dataset_path = r"C:\Users\Lenovo\OneDrive\Desktop\OUR_DATASET"

img_size = (224, 224)
batch_size = 32

# ==============================
# 3. LOAD DATASET
# ==============================
train_data = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

val_data = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

class_names = train_data.class_names
print("Classes:", class_names)

# ==============================
# 4. NORMALIZATION
# ==============================
train_data = train_data.map(lambda x, y: (x/255.0, y))
val_data = val_data.map(lambda x, y: (x/255.0, y))

# ==============================
# 5. LOAD PRETRAINED MODEL
# ==============================
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224,224,3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False   # freeze base model

# ==============================
# 6. BUILD MODEL
# ==============================
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(class_names), activation='softmax')
])

# ==============================
# 7. COMPILE MODEL
# ==============================
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# ==============================
# 8. SAVE BEST WEIGHTS (AUTO)
# ==============================
checkpoint = tf.keras.callbacks.ModelCheckpoint(
    "best_weights.weights.h5",
    monitor='val_accuracy',
    save_best_only=True,
    save_weights_only=True,
    mode='max'
)
# ==============================
# 9. TRAIN MODEL
# ==============================
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=5,
    callbacks=[checkpoint]
)

model.fit(train_data, validation_data=val_data, epochs=5)

# ==============================
# 11. SAVE MODEL
# ==============================
model.save("crop_disease_model.keras")

print("Model saved successfully!")

# ==============================
# 12. LOAD & PREDICT NEW IMAGE
# ==============================
from tensorflow.keras.preprocessing import image

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224,224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction)]

    print("Prediction:", predicted_class)