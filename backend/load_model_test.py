import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import cv2
import os

# --- CONFIG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'plant_disease_model.keras')
IMAGE_PATH = os.path.join(BASE_DIR, 'sample_leaf.jpg')  # Replace with your image path
IMG_SIZE = (224, 224)  # Use the size your model expects

# --- LOAD MODEL ---
model = load_model(MODEL_PATH, compile=False)
print("Model loaded successfully!")
print("Model inputs:", model.inputs)
print("Model outputs:", model.outputs)

# --- LOAD AND PREPROCESS IMAGE ---
def load_and_preprocess(img_path, img_size):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, img_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # MobileNetV2 preprocessing
    return img_array

x1 = load_and_preprocess(IMAGE_PATH, IMG_SIZE)
x2 = load_and_preprocess(IMAGE_PATH, IMG_SIZE)  # If second input is same, else load differently

# --- PREDICT ---
prediction = model.predict([x1, x2])
print("Prediction:", prediction)
