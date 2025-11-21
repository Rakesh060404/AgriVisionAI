from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import base64
import io
from PIL import Image
import os
import requests
import re
from datetime import datetime
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

app = Flask(__name__)

# === FIXED CORS CONFIG ===
CORS(app, resources={
    r"/api/*": {
        "origins": "http://localhost:8080",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# === IMPORTANT: Fix preflight OPTIONS ===
@app.before_request
def handle_options_request():
    if request.method == "OPTIONS":
        return jsonify({"status": "OK"}), 200


# === Gemini API Setup ===
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    API_KEY = API_KEY.strip('"\'')
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

if API_KEY:
    print("✅ Gemini API key loaded successfully.")
else:
    print("⚠️ No Gemini API key found. Using local fallback for treatments only.")

# === Model Setup ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
model_path = os.path.join(MODEL_DIR, "plant_disease_model_38class_finetuned_v2.keras")

print(f"📂 Loading model from: {model_path}")
model = load_model(model_path, compile=False)
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
print("✅ Model loaded successfully!")

# === Class Names (38 Classes) ===
class_names = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry___healthy', 'Cherry___Powdery_mildew',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight',
    'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# === Local Treatment Data ===
treatment_data = {
    "tomato early blight": {
        "treatments": [
            "Spray copper-based fungicides weekly.",
            "Remove infected leaves regularly."
        ],
        "remedies": [
            "Use garlic or neem oil spray twice a week."
        ],
        "prevention": [
            "Rotate crops and avoid overhead irrigation.",
            "Mulch around plants to prevent soil splash."
        ],
        "severity": "medium"
    },
    "potato late blight": {
        "treatments": [
            "Spray mancozeb or chlorothalonil every 7 days.",
            "Destroy heavily infected plants."
        ],
        "remedies": [
            "Neem oil and baking soda mixture weekly."
        ],
        "prevention": [
            "Ensure good air circulation.",
            "Avoid watering late in the evening."
        ],
        "severity": "high"
    }
}

# === Image Preprocessing ===
def preprocess_image(image_data):
    if "," in image_data:
        image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array)

# === Normalize Text ===
def normalize_text(text):
    return (
        text.lower()
        .replace("___", " ")
        .replace("_", " ")
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .replace("-", " ")
        .strip()
    )

# === Improved Gemini Treatment Parser ===
def parse_gemini_treatment(text):
    sections = {"treatments": [], "remedies": [], "prevention": []}
    text = text.replace("**", "").replace("###", "").strip()

    pattern = re.split(
        r"(?:^|\n)\s*(?:\d+\.\s*)?(Treatments?|Natural Remedies?|Remedies?|Prevention)[:\-]?\s*",
        text,
        flags=re.IGNORECASE
    )

    current_section = None

    for part in pattern:
        if not part.strip():
            continue
        
        lower = part.lower()

        if "treatment" in lower:
            current_section = "treatments"
            continue
        elif "remed" in lower:
            current_section = "remedies"
            continue
        elif "prevent" in lower:
            current_section = "prevention"
            continue

        if current_section:
            bullets = re.split(r"[\n•\-\*\u2022]+", part)
            for bullet in bullets:
                bullet = bullet.strip()
                if len(bullet) > 3:
                    sections[current_section].append(bullet)

    if not any(sections.values()):
        sections["treatments"].append(text.strip())

    return sections

# === Gemini Treatment Generator ===
def gemini_generate_treatment(disease_name):
    if not API_KEY:
        return None
    try:
        print(f"🤖 Fetching Gemini treatment for: {disease_name}")
        prompt = (
            f"Provide short, clear, structured plant treatment advice for '{disease_name}'. "
            f"Use this format:\n"
            f"Treatments: (2 steps)\n"
            f"Natural Remedies: (1-2 organic solutions)\n"
            f"Prevention: (2 prevention tips)\n"
            f"Keep under 100 words."
        )

        resp = requests.post(
            GEMINI_URL,
            params={"key": API_KEY},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=25
        )

        if resp.status_code != 200:
            print(f"❌ Gemini Error: {resp.text}")
            return None

        text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        print(f"✅ Gemini response received for {disease_name}")
        return parse_gemini_treatment(text)

    except Exception as e:
        print(f"⚠️ Gemini API failed: {e}")
        return None

# === Treatment Finder ===
def find_treatment(predicted_class):
    normalized = normalize_text(predicted_class)
    print(f"🔍 Normalized class: {normalized}")

    for key in treatment_data.keys():
        if key in normalized or normalized in key:
            print(f"✅ Found local treatment for {key}")
            return treatment_data[key]

    print(f"🌐 Using Gemini API for treatment: {normalized}")
    gemini_structured = gemini_generate_treatment(predicted_class)

    if gemini_structured:
        return {**gemini_structured, "severity": "auto"}

    return {
        "treatments": ["Consult a local agricultural officer for guidance."],
        "remedies": ["Use neem oil or mild organic fungicide."],
        "prevention": ["Ensure crop rotation and good soil drainage."],
        "severity": "medium"
    }

# ============================================
#        🚀 ADDING YOUR MISSING CHAT API
# ============================================
@app.route("/api/chat", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()
        user_msg = data.get("message")

        if not user_msg:
            return jsonify({"error": "No message provided"}), 400

        if not API_KEY:
            return jsonify({"reply": "Gemini API key missing in backend."}), 200

        prompt = user_msg

        resp = requests.post(
            GEMINI_URL,
            params={"key": API_KEY},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=20
        )

        if resp.status_code != 200:
            return jsonify({"error": resp.text}), 500

        reply = resp.json()["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === Prediction Endpoint ===
@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if "image" not in data:
            return jsonify({"error": "No image provided"}), 400

        processed_image = preprocess_image(data["image"])
        predictions = model.predict(processed_image)
        idx = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]) * 100)
        predicted_class = class_names[idx]

        is_healthy = "healthy" in predicted_class.lower()
        treatment = None if is_healthy else find_treatment(predicted_class)

        return jsonify({
            "disease": predicted_class.replace("_", " ").replace("  ", " "),
            "confidence": round(confidence, 2),
            "isHealthy": is_healthy,
            "treatment": treatment
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Health Check ===
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "Plant Disease Detection API is running."})

# === Run Server ===
if __name__ == "__main__":
    print("🌱 Starting Plant Disease Detection API...")
    app.run(debug=True, host="0.0.0.0", port=5000)
