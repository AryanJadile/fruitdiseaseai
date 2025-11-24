import tensorflow as tf
import numpy as np
import cv2 # OpenCV for image processing
import sys
import os

# --- 1. Load Model and Class Names ---
IMG_SIZE = (224, 224) 

try:
    # Load the trained model
    model = tf.keras.models.load_model('model/fruit_disease_model.keras')
    
    # Load the class names
    with open('model/class_names.txt', 'r') as f:
        class_names = [line.strip() for line in f.readlines()]
except IOError:
    print("Error: Model or class_names.txt not found.")
    print("Please run train.py first to train and save the model.")
    sys.exit(1)

def preprocess_image(image_path):
    """Loads and preprocesses an image for prediction."""
    try:
        # Load image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not read image from {image_path}")
            return None
        
        # Resize to the model's expected input size
        img = cv2.resize(img, IMG_SIZE)
        
        # Convert from BGR (OpenCV default) to RGB (TensorFlow default)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert to a batch of 1
        img_array = tf.expand_dims(img, 0) 
        
        #
        #   *** THIS IS THE FIX ***
        #   Cast to float32, but DO NOT preprocess.
        #   The model itself will do the preprocessing.
        #
        img_array = tf.cast(img_array, tf.float32)
        
        #   *** REMOVED THIS LINE ***
        #   img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def predict_disease(image_path):
    """Predicts the disease for a given image."""
    
    # Preprocess the image
    processed_image = preprocess_image(image_path)
    if processed_image is None:
        return
    
    # Make prediction
    # The model will now receive the [0, 255] float image 
    # and perform its internal preprocessing.
    predictions = model.predict(processed_image)
    
    # 'predictions' is an array of probabilities for each class
    # We find the one with the highest probability
    score = tf.nn.softmax(predictions[0])
    predicted_class_index = np.argmax(score)
    predicted_class_name = class_names[predicted_class_index]
    confidence = 100 * np.max(score)
    
    print("\n--- Prediction Result ---")
    print(f"Image: {os.path.basename(image_path)}")
    print(f"Disease: {predicted_class_name}")
    print(f"Confidence: {confidence:.2f}%")
    print("-------------------------\n")

# --- Main execution ---
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python predict.py <path_to_image>")
        sys.exit(1)
        
    image_path = sys.argv[1]
    predict_disease(image_path)