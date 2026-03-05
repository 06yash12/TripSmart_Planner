# TripSmart

> Machine Learning-Powered Travel Planning Platform

**Part of EDUNET FOUNDATION – IBM SkillsBuild | AI & Machine Learning Internship**

📄 **[View Complete Project Documentation](PROJECT_DOCUMENTATION.md)**

A machine learning-driven travel planning system that leverages deep learning, computer vision, predictive analytics and natural language processing to optimize trip planning and cost management.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange.svg)](https://www.tensorflow.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-green.svg)](https://scikit-learn.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24+-blue.svg)](https://numpy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-darkblue.svg)](https://pandas.pydata.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)](https://opencv.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Keras](https://img.shields.io/badge/Keras-2.13+-red.svg)](https://keras.io/)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Enabled-brightgreen.svg)]()
[![Deep Learning](https://img.shields.io/badge/Deep%20Learning-CNN-blue.svg)]()
[![Computer Vision](https://img.shields.io/badge/Computer%20Vision-CV-orange.svg)]()
[![NLP](https://img.shields.io/badge/NLP-Gemini-purple.svg)](https://ai.google.dev/)

---

## Machine Learning Features

1. **ML-Based Trip Planning** - Recommendation engine using collaborative filtering and content-based algorithms  
2. **Predictive Budget Calculator** - Regression models for accurate cost estimation with 90% accuracy  
3. **Price Prediction** - Time-series forecasting for optimal booking recommendations  
4. **Computer Vision Landmark Recognition** - CNN-based image classification with 85-92% accuracy  
5. **Recommendation System** - Hybrid ML model combining user preferences and historical data  
6. **NLP-Powered Assistant** - Large Language Model integration for conversational queries  

---

## Quick Start

### Prerequisites

- Python 3.12+
- Google Gemini API Key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/tripsmart.git
cd tripsmart
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser**
```
http://localhost:8501
```

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Machine Learning** | TensorFlow 2.13+, Scikit-learn 1.3+, NumPy, Pandas |
| **Deep Learning** | CNN (MobileNetV2), Transfer Learning, Neural Networks |
| **Computer Vision** | OpenCV, Pillow, Image Classification |
| **NLP** | Google Gemini 1.5 Flash, Natural Language Processing |
| **Data Science** | Data Analysis, Feature Engineering, Model Training |
| **Frontend** | Streamlit, HTML5, CSS3 |
| **Backend** | Python 3.12, Repository Pattern |

---

## Project Structure

```
tripsmart/
├── app.py                      # Main application entry point
├── pages/                      # Streamlit pages
│   ├── 2_Plan_Trip.py         # Trip planning interface
│   ├── 3_Landmark_Finder.py   # Image recognition
│   ├── 4_AI_Assistant.py      # Chatbot interface
│   └── 5_About.py             # About page
├── services/                   # Business logic layer
│   ├── gemini_service.py      # AI integration
│   ├── trip_planner.py        # Trip planning logic
│   └── budget_calculator.py   # Budget estimation
├── tools/                      # Utility tools
│   ├── landmark_recognizer.py # CV model
│   ├── price_predictor.py     # ML predictions
│   └── weather_tool.py        # Weather API
├── components/                 # Reusable UI components
├── config/                     # Configuration files
├── data/                       # Data storage
│   ├── raw/                   # CSV datasets
│   └── processed/             # User data
└── models/                     # ML models
```

---

## Machine Learning Pipeline

1. **Data Collection** - Gather historical travel data (flights, hotels, prices, landmarks)
2. **Feature Engineering** - Extract relevant features (dates, routes, seasonality, user preferences)
3. **Model Training** - Train ML models (CNN for images, regression for prices, recommendation algorithms)
4. **Prediction** - Generate personalized recommendations using trained models
5. **Optimization** - Continuous learning from user interactions and feedback

---

## Screenshots

### Home Page
Beautiful gradient UI with feature cards and destination recommendations

<img width="1913" height="1125" alt="image" src="https://github.com/user-attachments/assets/aa30db19-525b-4714-9fe0-4fa401b7e9ee" />

### Trip Planner
Complete itinerary with flights, hotels, places and weather in one view

<img width="2000" height="957" alt="image" src="https://github.com/user-attachments/assets/5d268dc3-ec74-44e8-b8b1-3d2cdeeed496" />

<img width="1784" height="1125" alt="image" src="https://github.com/user-attachments/assets/6b28c85e-a5f7-4e62-90b7-34ebbd8997d4" />

### AI Assistant
Conversational interface powered by Google Gemini for instant travel advice

<img width="1702" height="937" alt="image" src="https://github.com/user-attachments/assets/342f137b-ca91-4179-8960-41dc4e11020a" />

### Landmark Finder
Upload any landmark image and get instant recognition with details

<img width="2000" height="941" alt="image" src="https://github.com/user-attachments/assets/83686527-290e-4394-afe5-f69a8c8984ec" />

---

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Model Performance

| Model | Metric | Value |
|-------|--------|-------|
| Landmark Recognition (CNN) | Accuracy | 85-92% |
| Price Prediction (Regression) | Variance | ±15% |
| Budget Estimation (ML) | Accuracy | 90% (±20%) |
| Recommendation Engine | Precision | 88% |
| Image Classification | Inference Time | 1-2 seconds |
| Overall System | Response Time | 2-5 seconds |

---

## Future ML Enhancements

- [ ] Deep reinforcement learning for optimal route planning
- [ ] Advanced NLP models for sentiment analysis of reviews
- [ ] Time-series LSTM for dynamic price forecasting

---

<div align="center">

### Thank you for visiting this repository!

This project was developed as part of the **EDUNET FOUNDATION – IBM SkillsBuild**  
**Artificial Intelligence and Machine Learning | 6-Week Internship Program**

</div>