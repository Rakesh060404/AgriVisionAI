# 🌱 Plant Disease Detection System

A full-stack web application that uses machine learning to detect plant diseases from leaf images and provides treatment recommendations. The system includes a chatbot for agricultural advice and a modern React frontend.

## 🚀 Features

- **🔍 Disease Detection**: Upload plant leaf images and get instant disease predictions
- **🤖 AI Chatbot**: Ask questions about crops, fertilizers, pests, and farming practices
- **💊 Treatment Recommendations**: Get specific treatment, remedy, and prevention advice
- **📊 Confidence Scoring**: See how confident the model is in its predictions
- **🎨 Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- **⚡ Real-time Processing**: Fast image analysis and chatbot responses

## 🏗️ Architecture

- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Backend**: Flask + Python
- **AI Model**: TensorFlow/Keras CNN for plant disease classification
- **Chatbot**: Smart keyword-based responses with API integration

## 📋 Supported Plant Diseases

The model can detect 38 different plant diseases including:

### Fruits
- **Apple**: Apple scab, Black rot, Cedar apple rust
- **Cherry**: Powdery mildew
- **Grape**: Black rot, Esca, Leaf blight
- **Orange**: Huanglongbing (Citrus greening)
- **Peach**: Bacterial spot
- **Strawberry**: Leaf scorch

### Vegetables
- **Corn**: Cercospora leaf spot, Common rust, Northern Leaf Blight
- **Pepper**: Bacterial spot
- **Potato**: Early blight, Late blight
- **Tomato**: Bacterial spot, Early blight, Late blight, Leaf Mold, Septoria leaf spot, Spider mites, Target Spot, Yellow Leaf Curl Virus, Mosaic virus
- **Squash**: Powdery mildew

### Others
- **Blueberry**, **Raspberry**, **Soybean** (healthy detection)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/plant-disease-detection.git
   cd plant-disease-detection
   ```

2. **Navigate to backend directory**
   ```bash
   cd backend
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the `backend/` directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   FLASK_DEBUG=True
   FLASK_HOST=0.0.0.0
   FLASK_PORT=5000
   ```
   > **Note:** For production, set `FLASK_DEBUG=False`. See [ENV_SETUP.md](ENV_SETUP.md) for details.

5. **Verify model files**
   - Ensure `plant_disease_model.keras` and `plant_disease_model_fixed.keras` are in `backend/models/` directory
   - Or use the mock backend for testing

6. **Start the Flask backend**
   ```bash
   python backend_mock.py  # For testing
   # OR
   python backend.py       # With real model
   ```

   The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables (optional for development)**
   Create a `.env` file in the `frontend/` directory:
   ```env
   VITE_API_BASE_URL=http://localhost:5000
   ```
   > **Note:** For production, set this to your deployed backend URL. See [ENV_SETUP.md](ENV_SETUP.md) for details.

4. **Start the development server**
   ```bash
   npm run dev
   ```

   The frontend will run on `http://localhost:5173` (or port 8080 as configured)

### Quick Start (Windows)

Run the batch file to start both servers:
```bash
start_system.bat
```

## 🔧 API Endpoints

### POST /api/predict
Predicts plant disease from an uploaded image.

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

**Response:**
```json
{
  "disease": "Tomato Early Blight",
  "confidence": 87.5,
  "isHealthy": false,
  "treatment": {
    "treatments": ["Apply chlorothalonil fungicide"],
    "remedies": ["Compost tea application"],
    "prevention": ["Use certified disease-free seeds"],
    "severity": "medium"
  }
}
```

### POST /api/chat
Chatbot endpoint for agricultural questions.

**Request Body:**
```json
{
  "message": "How do I fertilize my tomatoes?"
}
```

**Response:**
```json
{
  "response": "Tomatoes need full sun (6-8 hours), well-draining soil...",
  "timestamp": "2025-09-28 23:43:55.715884"
}
```

### GET /api/health
Health check endpoint.

## 🤖 Chatbot Features

The integrated chatbot can help with:

- **Fertilizer advice**: NPK ratios, application timing
- **Watering schedules**: Optimal irrigation practices
- **Pest control**: Organic and chemical methods
- **Soil health**: pH, compost, drainage
- **Crop rotation**: Planning and benefits
- **Plant-specific care**: Tomatoes, potatoes, apples
- **Disease prevention**: Early detection and treatment

## 🧪 Testing

### Test the API
```bash
python test_chatbot.py
```

### Test Disease Detection
1. Upload a plant leaf image
2. Click "Predict Disease"
3. View results and treatment recommendations

### Test Chatbot
1. Navigate to the Chatbot section
2. Ask questions like:
   - "How do I fertilize my tomatoes?"
   - "What's wrong with my apple tree?"
   - "Tell me about organic pest control"

## 📁 Project Structure

```
plant-disease-detection/
├── backend/                  # Backend Python application
│   ├── backend.py            # Main Flask backend with TensorFlow
│   ├── backend_mock.py       # Mock backend for testing
│   ├── app.py                # Streamlit app (optional)
│   ├── diagnose_chatbot.py  # Chatbot diagnostics
│   ├── test_chatbot.py      # Chatbot tests
│   ├── load_model_test.py   # Model loading tests
│   ├── requirements.txt     # Python dependencies
│   └── models/              # ML model files
│       ├── plant_disease_model.keras
│       └── plant_disease_model_fixed.keras
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/
│   │   │   ├── DiseaseDetection.tsx
│   │   │   ├── Chatbot.tsx
│   │   │   ├── Home.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── ui/          # UI components (shadcn/ui)
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── lib/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── start_system.bat          # Windows startup script
├── README.md                 # This file
└── .gitignore               # Git ignore rules
```

## 🔧 Development

### Adding New Diseases
1. Update the `class_names` list in `backend/backend.py`
2. Add treatment data to the `treatment_data` dictionary
3. Retrain the model with the new classes
4. Place the new model file in `backend/models/`

### Customizing the UI
The frontend uses Tailwind CSS for styling. Modify components in `src/components/` to customize the appearance.

### Extending the Chatbot
Add new response patterns in the `responses` dictionary in `backend/backend.py` or `backend/backend_mock.py`.

## 🚀 Deployment

### Backend Deployment
- Use a production WSGI server like Gunicorn
- Set up environment variables (see [ENV_SETUP.md](ENV_SETUP.md))
  - Set `GEMINI_API_KEY` for chatbot functionality
  - Set `FLASK_DEBUG=False` for production
- Use a reverse proxy like Nginx
- Ensure model files are accessible in `backend/models/` directory

### Frontend Deployment
- Set `VITE_API_BASE_URL` environment variable to your production backend URL
- Build the production version: `npm run build`
- Deploy the `dist/` folder to Vercel, Netlify, or any static hosting service
- Ensure CORS is properly configured on the backend

> **Important:** See [ENV_SETUP.md](ENV_SETUP.md) for detailed deployment instructions and environment variable configuration.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- PlantVillage dataset for disease classification
- TensorFlow/Keras for machine learning framework
- React and Tailwind CSS for frontend development
- Flask for backend API development

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/plant-disease-detection/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

---

**Made with ❤️ for farmers and plant enthusiasts**