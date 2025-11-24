import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import os
import numpy as np

# --- 1. Define Constants ---
DATA_DIR = 'Processed Dataset'
# MobileNetV2 requires a specific input size
IMG_SIZE = (224, 224) 
BATCH_SIZE = 32
EPOCHS = 15 

# --- 2. Load and Preprocess Data ---
print(f"Loading and preprocessing data from: {DATA_DIR}")

if not os.path.exists(DATA_DIR):
    print(f"Error: Dataset directory not found at '{DATA_DIR}'")
    exit()

try:
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE
    )
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

# Get class names
class_names = train_ds.class_names
num_classes = len(class_names)
print(f"Found {num_classes} classes: {class_names}")

# --- 3. Save Class Names ---
print("Saving class names...")
if not os.path.exists('model'):
    os.makedirs('model')
with open('model/class_names.txt', 'w') as f:
    for item in class_names:
        f.write("%s\n" % item)

# --- 4. Configure for Performance ---
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# --- 5. Build the Transfer Learning Model ---
print("Building the transfer learning model...")

# Load the Pretrained "Base Model" (MobileNetV2)
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
    include_top=False,  # Don't include the final ImageNet classifier layer
    weights='imagenet'  # Use weights pre-trained on ImageNet
)

# Freeze the Base Model (we don't want to re-train it)
base_model.trainable = False

# --- 6. Add Our Own New "Head" (Classifier) ---
inputs = tf.keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))

# Add data augmentation layers
data_augmentation = models.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
    ]
)
x = data_augmentation(inputs)

# Normalize inputs for MobileNetV2
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

# Pass augmented inputs to the base model
x = base_model(x, training=False) # training=False is important

# Add our new classifier layers on top
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
x = layers.Dense(128, activation='relu')(x)
outputs = layers.Dense(num_classes, activation='softmax')(x) # Our final output

# Create the new model
model = models.Model(inputs, outputs)

# --- 7. Compile the Model ---
print("Compiling the model...")
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

# Print a summary
model.summary()

# --- 8. Train the Model ---
print("Starting training...")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)
print("Training finished.")

# --- 9. Save the Model ---
print("Saving the trained model...")
model.save('model/fruit_disease_model.keras')
print("Model saved successfully in 'model' folder.")

# --- 10. Plot Training History ---
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs_range = range(EPOCHS)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.savefig('training_history.png')
print("Training history plot saved as 'training_history.png'")