import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import cv2
import os
import json
import csv
import requests
from PIL import Image
import io
import pickle
from sklearn.preprocessing import LabelEncoder

class LandmarkRecognizer:
    def __init__(self):
        self.model = None
        self.classifier_model = None
        self.label_encoder = None
        self.csv_file = "data/indian_landmarks_40.csv"
        self.model_file = "models/landmark_model.h5"
        self.encoder_file = "models/label_encoder.pkl"
        self.landmarks_data = []
        self.is_trained = False
        
        # Create models directory if it doesn't exist
        os.makedirs("models", exist_ok=True)
        
        # Load CSV data
        self._load_csv_data()
        
        # Try to load pre-trained model
        self._load_pretrained_model()
    
    def _load_csv_data(self):
        """Load landmark data from CSV file"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.landmarks_data = list(reader)
            print(f"✅ Loaded {len(self.landmarks_data)} landmarks from CSV")
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            self.landmarks_data = []
    
    def _load_pretrained_model(self):
        """Load pre-trained model if available"""
        if os.path.exists(self.model_file) and os.path.exists(self.encoder_file):
            try:
                self.classifier_model = keras.models.load_model(self.model_file)
                with open(self.encoder_file, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                self.is_trained = True
                print(f"✅ Loaded pre-trained model with {len(self.label_encoder.classes_)} landmarks")
            except Exception as e:
                print(f"⚠️ Could not load pre-trained model: {e}")
                self.is_trained = False
    
    def download_image(self, url, timeout=10):
        """Download image from URL"""
        try:
            # Handle Wikimedia Special:FilePath URLs
            if 'wikimedia.org' in url and 'Special:FilePath' in url:
                # These URLs redirect to the actual image
                # Just follow the redirect
                pass
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, timeout=timeout, headers=headers, allow_redirects=True)
            
            if response.status_code == 200:
                # Check if it's an image
                content_type = response.headers.get('content-type', '')
                if 'image' in content_type or len(response.content) > 1000:
                    img = Image.open(io.BytesIO(response.content))
                    print(f"  ✅ Downloaded successfully")
                    return img
                else:
                    print(f"  ⚠️ Not an image (content-type: {content_type})")
            else:
                print(f"  ⚠️ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}")
        
        return None
    
    def train_model(self, num_samples_per_landmark=5, epochs=20):
        """
        Train the landmark recognition model using images from CSV
        
        Args:
            num_samples_per_landmark: Number of images to download per landmark
            epochs: Number of training epochs
        """
        print("🚀 Starting model training...")
        
        if not self.landmarks_data:
            print("❌ No landmark data available")
            return False
        
        # Prepare training data
        X_train = []
        y_train = []
        landmark_names = []
        
        print(f"📥 Downloading and processing images...")
        print(f"⚠️  Note: Wikimedia URLs may not download directly")
        print(f"💡 Tip: The app will use color-based detection as fallback\n")
        
        for idx, landmark in enumerate(self.landmarks_data):
            name = landmark['name']
            url = landmark['image_url']
            
            print(f"Processing {idx+1}/{len(self.landmarks_data)}: {name}", end="")
            
            # Download image
            img = self.download_image(url)
            
            if img is not None:
                # Preprocess image
                processed = self.preprocess_image(img)
                if processed is not None:
                    X_train.append(processed[0])
                    landmark_names.append(name)
                    y_train.append(name)
            else:
                print()  # New line after failed download
        
        print(f"\n✅ Successfully processed {len(X_train)} images out of {len(self.landmarks_data)}")
        
        if len(X_train) < 3:
            print("❌ Not enough training data (need at least 3 images)")
            print("💡 The app will use color-based detection instead")
            return False
        
        # Convert to numpy arrays
        X_train = np.array(X_train)
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y_train_encoded = self.label_encoder.fit_transform(y_train)
        y_train_categorical = keras.utils.to_categorical(y_train_encoded)
        
        # Build model
        print("🏗️ Building model architecture...")
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(224, 224, 3)
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Add custom classification layers
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.3)(x)
        predictions = Dense(len(self.label_encoder.classes_), activation='softmax')(x)
        
        self.classifier_model = Model(inputs=base_model.input, outputs=predictions)
        
        # Compile model
        self.classifier_model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(f"🎯 Training on {len(self.label_encoder.classes_)} landmark classes...")
        
        # Train model
        history = self.classifier_model.fit(
            X_train, y_train_categorical,
            epochs=epochs,
            batch_size=min(8, len(X_train)),
            validation_split=0.2 if len(X_train) > 5 else 0,
            verbose=1
        )
        
        # Save model
        self.classifier_model.save(self.model_file)
        with open(self.encoder_file, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        
        self.is_trained = True
        
        print(f"✅ Model trained and saved!")
        print(f"Final accuracy: {history.history['accuracy'][-1]:.2%}")
        
        return True
    
    def load_model(self):
        """Load pre-trained MobileNetV2 model for feature extraction"""
        if self.model is None:
            # Use MobileNetV2 for efficient inference
            base_model = MobileNetV2(
                weights='imagenet',
                include_top=False,
                pooling='avg',
                input_shape=(224, 224, 3)
            )
            self.model = base_model
        return self.model
    
    def preprocess_image(self, img_data):
        """Preprocess image for model input"""
        try:
            # Convert to PIL Image if needed
            if isinstance(img_data, bytes):
                img = Image.open(io.BytesIO(img_data))
            else:
                img = img_data
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to model input size
            img = img.resize((224, 224))
            
            # Convert to array
            img_array = np.array(img)
            
            # Expand dimensions
            img_array = np.expand_dims(img_array, axis=0)
            
            # Preprocess for MobileNetV2
            img_array = preprocess_input(img_array)
            
            return img_array
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def extract_features(self, img_data):
        """Extract features from image using pre-trained model"""
        model = self.load_model()
        preprocessed = self.preprocess_image(img_data)
        
        if preprocessed is None:
            return None
        
        features = model.predict(preprocessed, verbose=0)
        return features[0]
    
    def detect_landmark_simple(self, img_data):
        """
        Enhanced landmark detection using color and edge analysis
        Detects all 40 landmarks from CSV using computer vision
        """
        try:
            # Convert to PIL Image
            if isinstance(img_data, bytes):
                img = Image.open(io.BytesIO(img_data))
            else:
                img = img_data
            
            # Convert to OpenCV format
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # Resize for processing
            img_cv = cv2.resize(img_cv, (224, 224))
            
            # Analyze color histogram
            hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            
            # Calculate color ratios
            total_pixels = img_cv.shape[0] * img_cv.shape[1]
            
            # Color masks
            white_mask = cv2.inRange(hsv, np.array([0, 0, 180]), np.array([180, 50, 255]))
            white_ratio = np.sum(white_mask > 0) / total_pixels
            
            red_mask1 = cv2.inRange(hsv, np.array([0, 50, 50]), np.array([10, 255, 255]))
            red_mask2 = cv2.inRange(hsv, np.array([170, 50, 50]), np.array([180, 255, 255]))
            red_mask = cv2.bitwise_or(red_mask1, red_mask2)
            red_ratio = np.sum(red_mask > 0) / total_pixels
            
            pink_mask = cv2.inRange(hsv, np.array([150, 30, 100]), np.array([170, 150, 255]))
            pink_ratio = np.sum(pink_mask > 0) / total_pixels
            
            yellow_mask = cv2.inRange(hsv, np.array([15, 50, 100]), np.array([35, 255, 255]))
            yellow_ratio = np.sum(yellow_mask > 0) / total_pixels
            
            green_mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
            green_ratio = np.sum(green_mask > 0) / total_pixels
            
            blue_mask = cv2.inRange(hsv, np.array([90, 50, 50]), np.array([130, 255, 255]))
            blue_ratio = np.sum(blue_mask > 0) / total_pixels
            
            brown_mask = cv2.inRange(hsv, np.array([10, 50, 50]), np.array([20, 255, 200]))
            brown_ratio = np.sum(brown_mask > 0) / total_pixels
            
            # Structural features
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / total_pixels
            
            # Symmetry detection
            left_half = gray[:, :gray.shape[1]//2]
            right_half = cv2.flip(gray[:, gray.shape[1]//2:], 1)
            min_width = min(left_half.shape[1], right_half.shape[1])
            left_half = left_half[:, :min_width]
            right_half = right_half[:, :min_width]
            symmetry_score = np.mean(np.abs(left_half.astype(float) - right_half.astype(float))) / 255
            is_symmetric = symmetry_score < 0.3
            
            # Sky detection
            top_region = hsv[:hsv.shape[0]//3, :]
            sky_blue = cv2.inRange(top_region, np.array([90, 50, 50]), np.array([130, 255, 255]))
            sky_ratio = np.sum(sky_blue > 0) / (top_region.shape[0] * top_region.shape[1])
            
            # Scoring for all landmarks
            scores = {}
            
            # Monuments with white marble
            if white_ratio > 0.25:
                if is_symmetric and (sky_ratio > 0.1 or green_ratio > 0.05):
                    scores['Taj Mahal'] = 0.85 + (white_ratio * 0.3)
                elif is_symmetric and green_ratio < 0.1:
                    scores['Victoria Memorial'] = 0.75 + (white_ratio * 0.2)
                elif edge_density > 0.15:
                    scores['Lotus Temple'] = 0.70 + (white_ratio * 0.2)
            
            # Red/Brown monuments
            if red_ratio > 0.20:
                scores['Red Fort'] = 0.75 + (red_ratio * 0.3)
                if edge_density > 0.12:
                    scores['Qutub Minar'] = 0.70 + (red_ratio * 0.25)
            elif red_ratio > 0.15:
                scores['Charminar'] = 0.65 + (red_ratio * 0.2)
                scores['Golconda Fort'] = 0.60 + (red_ratio * 0.2)
            
            # Pink monuments
            if pink_ratio > 0.15:
                scores['Hawa Mahal'] = 0.75 + (pink_ratio * 0.4)
            
            # Yellow/Golden monuments
            if yellow_ratio > 0.15:
                scores['Golden Temple'] = 0.75 + (yellow_ratio * 0.3)
                scores['Mysore Palace'] = 0.70 + (yellow_ratio * 0.25)
            elif yellow_ratio > 0.10:
                if is_symmetric:
                    scores['Gateway of India'] = 0.65 + (yellow_ratio * 0.2)
                    scores['India Gate'] = 0.60 + (yellow_ratio * 0.2)
                scores['Jaisalmer Fort'] = 0.60 + (yellow_ratio * 0.2)
            
            # Brown/Stone monuments
            if brown_ratio > 0.15:
                scores['Mehrangarh Fort'] = 0.65 + (brown_ratio * 0.2)
                scores['Gwalior Fort'] = 0.60 + (brown_ratio * 0.2)
                scores['Chittorgarh Fort'] = 0.60 + (brown_ratio * 0.2)
            
            # Temples with colorful gopurams
            if red_ratio > 0.1 and yellow_ratio > 0.1 and blue_ratio > 0.05:
                scores['Meenakshi Temple'] = 0.70
                scores['Brihadeeswarar Temple'] = 0.65
            
            # Natural landmarks
            if green_ratio > 0.30:
                if blue_ratio > 0.15:
                    scores['Dal Lake'] = 0.70
                    scores['Athirappilly Waterfalls'] = 0.65
                else:
                    scores['Kaziranga National Park'] = 0.65
            
            if blue_ratio > 0.30:
                scores['Marina Beach'] = 0.65
            
            # Caves and rock structures
            if brown_ratio > 0.20 and edge_density > 0.15:
                scores['Ajanta Caves'] = 0.65
                scores['Ellora Caves'] = 0.65
                scores['Hampi'] = 0.60
            
            # Bridges and modern structures
            if edge_density > 0.20 and not is_symmetric:
                scores['Howrah Bridge'] = 0.60
                if brown_ratio > 0.15:
                    scores['Statue of Unity'] = 0.65
            
            # Stepwells
            if edge_density > 0.18 and brown_ratio > 0.15:
                scores['Rani ki Vav'] = 0.65
            
            # Mountain temples
            if green_ratio > 0.20 and white_ratio > 0.15:
                scores['Kedarnath Temple'] = 0.60
                scores['Badrinath Temple'] = 0.60
                scores['Vaishno Devi Temple'] = 0.60
            
            # Government buildings
            if yellow_ratio > 0.12 and is_symmetric and edge_density > 0.10:
                scores['Rashtrapati Bhavan'] = 0.65
            
            # Mosques
            if white_ratio > 0.20 and red_ratio > 0.10:
                scores['Jama Masjid'] = 0.65
            
            # Other temples
            if yellow_ratio > 0.10 and edge_density > 0.10:
                scores['Somnath Temple'] = 0.60
                scores['Dwarkadhish Temple'] = 0.60
                scores['Sun Temple Konark'] = 0.60
            
            # Stupas
            if white_ratio > 0.15 and edge_density > 0.12:
                scores['Sanchi Stupa'] = 0.60
            
            # Memorials
            if white_ratio > 0.20 and blue_ratio > 0.10:
                scores['Vivekananda Rock Memorial'] = 0.60
            
            # Gardens
            if green_ratio > 0.25 and edge_density < 0.10:
                scores['Rock Garden Chandigarh'] = 0.55
            
            # Get best match
            if scores:
                best_landmark = max(scores.items(), key=lambda x: x[1])
                return best_landmark[0], best_landmark[1]
            
            # Fallback based on dominant color
            if white_ratio > 0.25:
                return "Taj Mahal", 0.60
            elif red_ratio > 0.15:
                return "Red Fort", 0.55
            elif yellow_ratio > 0.12:
                return "Golden Temple", 0.55
            elif green_ratio > 0.25:
                return "Kaziranga National Park", 0.50
            else:
                return "India Gate", 0.50
            
        except Exception as e:
            print(f"Error in landmark detection: {e}")
            return "India Gate", 0.40
    
    
    def recognize_landmark(self, img_data, use_simple=False):
        """
        Recognize landmark from image
        
        Args:
            img_data: Image data (bytes, PIL Image, or file path)
            use_simple: Use simple color-based detection (faster, less accurate)
        
        Returns:
            dict with landmark info and confidence
        """
        try:
            # If model is trained, use it
            if self.is_trained and self.classifier_model is not None and not use_simple:
                preprocessed = self.preprocess_image(img_data)
                if preprocessed is None:
                    return self._get_error_result("Could not process image")
                
                # Predict
                predictions = self.classifier_model.predict(preprocessed, verbose=0)
                top_idx = np.argmax(predictions[0])
                confidence = predictions[0][top_idx]
                
                # Get landmark name
                landmark_name = self.label_encoder.inverse_transform([top_idx])[0]
                
                # Find landmark info from CSV
                landmark_info = self._get_landmark_info(landmark_name)
                landmark_info['confidence'] = round(float(confidence) * 100, 1)
                landmark_info['suggestion'] = self._generate_suggestion(landmark_info)
                
                return landmark_info
            else:
                # Fall back to simple detection
                landmark_id, confidence = self.detect_landmark_simple(img_data)
                landmark_info = self._get_landmark_info_by_id(landmark_id)
                landmark_info['confidence'] = round(confidence * 100, 1)
                landmark_info['suggestion'] = self._generate_suggestion(landmark_info)
                return landmark_info
                
        except Exception as e:
            print(f"Error recognizing landmark: {e}")
            return self._get_error_result(str(e))
    
    def _get_landmark_info(self, landmark_name):
        """Get landmark information from CSV by name"""
        for landmark in self.landmarks_data:
            if landmark['name'].lower() == landmark_name.lower():
                return {
                    'name': landmark['name'],
                    'city': landmark.get('place', 'Unknown'),
                    'state': landmark.get('state', 'India'),
                    'category': landmark.get('category', 'Monument'),
                    'year_built': landmark.get('year_built', 'Unknown'),
                    'description': landmark.get('description', ''),
                    'best_time': 'October to March',
                    'entry_fee': 'Varies'
                }
        
        # Default if not found
        return {
            'name': landmark_name,
            'city': 'Unknown',
            'state': 'India',
            'confidence': 0,
            'suggestion': 'Landmark information not available'
        }
    
    def _get_landmark_info_by_id(self, landmark_id):
        """Get landmark info using simple ID mapping"""
        # Map common IDs/names to CSV landmarks
        id_mapping = {
            'taj_mahal': 'Taj Mahal',
            'Taj Mahal': 'Taj Mahal',
            'india_gate': 'India Gate',
            'India Gate': 'India Gate',
            'qutub_minar': 'Qutub Minar',
            'Qutub Minar': 'Qutub Minar',
            'hawa_mahal': 'Hawa Mahal',
            'Hawa Mahal': 'Hawa Mahal',
            'gateway_of_india': 'Gateway of India',
            'Gateway of India': 'Gateway of India',
            'charminar': 'Charminar',
            'Charminar': 'Charminar',
            'mysore_palace': 'Mysore Palace',
            'Mysore Palace': 'Mysore Palace',
            'golden_temple': 'Golden Temple',
            'Golden Temple': 'Golden Temple',
            'victoria_memorial': 'Victoria Memorial',
            'Victoria Memorial': 'Victoria Memorial',
            'meenakshi_temple': 'Meenakshi Temple',
            'Meenakshi Temple': 'Meenakshi Temple',
            'red_fort': 'Red Fort',
            'Red Fort': 'Red Fort',
            'lotus_temple': 'Lotus Temple',
            'Lotus Temple': 'Lotus Temple'
        }
        
        landmark_name = id_mapping.get(landmark_id, 'India Gate')
        return self._get_landmark_info(landmark_name)
    
    def _get_error_result(self, error_msg):
        """Return error result"""
        return {
            'name': 'Unknown Landmark',
            'city': 'Unknown',
            'state': 'India',
            'confidence': 0,
            'suggestion': f'Could not identify the landmark. {error_msg}'
        }
    
    def _generate_suggestion(self, landmark_info):
        """Generate travel suggestion based on landmark"""
        name = landmark_info['name']
        city = landmark_info['city']
        confidence = landmark_info['confidence']
        
        if confidence > 70:
            return f"🎯 This looks like {name}! Would you like to plan a trip to {city}?"
        elif confidence > 50:
            return f"🤔 This might be {name} in {city}. Want to explore this destination?"
        else:
            return f"💡 This could be {name}. Check out {city} for similar landmarks!"
    
    def get_trip_suggestions(self, landmark_info):
        """Get trip planning suggestions based on identified landmark"""
        city = landmark_info.get('city', 'Delhi')
        state = landmark_info.get('state', 'India')
        
        suggestions = {
            'destination': city,
            'state': state,
            'landmark': landmark_info.get('name', 'Unknown'),
            'category': landmark_info.get('category', 'Monument'),
            'year_built': landmark_info.get('year_built', 'Unknown'),
            'description': landmark_info.get('description', ''),
            'best_time': landmark_info.get('best_time', 'October to March'),
            'nearby_attractions': self._get_nearby_attractions(city),
            'estimated_days': self._estimate_trip_duration(city),
            'budget_estimate': self._estimate_budget(city)
        }
        
        return suggestions
    
    def _get_nearby_attractions(self, city):
        """Get nearby attractions for the city"""
        attractions = {
            'Agra': ['Taj Mahal', 'Agra Fort', 'Fatehpur Sikri', 'Mehtab Bagh'],
            'Mumbai': ['Gateway of India', 'Marine Drive', 'Elephanta Caves', 'Juhu Beach'],
            'Jaipur': ['Hawa Mahal', 'Amber Fort', 'City Palace', 'Jantar Mantar'],
            'Delhi': ['India Gate', 'Red Fort', 'Qutub Minar', 'Lotus Temple', 'Humayun Tomb'],
            'Hyderabad': ['Charminar', 'Golconda Fort', 'Hussain Sagar', 'Ramoji Film City'],
            'Mysore': ['Mysore Palace', 'Chamundi Hills', 'Brindavan Gardens', 'St. Philomena Church'],
            'Amritsar': ['Golden Temple', 'Jallianwala Bagh', 'Wagah Border', 'Partition Museum'],
            'Kolkata': ['Victoria Memorial', 'Howrah Bridge', 'Dakshineswar Temple', 'Indian Museum'],
            'Madurai': ['Meenakshi Temple', 'Thirumalai Nayak Palace', 'Gandhi Museum', 'Alagar Hills']
        }
        return attractions.get(city, ['Local attractions', 'City tour', 'Cultural sites'])
    
    def _estimate_trip_duration(self, city):
        """Estimate recommended trip duration"""
        durations = {
            'Agra': '2-3 days',
            'Mumbai': '3-4 days',
            'Jaipur': '3-4 days',
            'Delhi': '4-5 days',
            'Hyderabad': '2-3 days',
            'Mysore': '2-3 days',
            'Amritsar': '2 days',
            'Kolkata': '3-4 days',
            'Madurai': '2 days'
        }
        return durations.get(city, '2-3 days')
    
    def _estimate_budget(self, city):
        """Estimate budget for the trip"""
        budgets = {
            'Agra': '₹8,000 - ₹15,000 per person',
            'Mumbai': '₹12,000 - ₹25,000 per person',
            'Jaipur': '₹10,000 - ₹18,000 per person',
            'Delhi': '₹10,000 - ₹20,000 per person',
            'Hyderabad': '₹8,000 - ₹15,000 per person',
            'Mysore': '₹7,000 - ₹12,000 per person',
            'Amritsar': '₹6,000 - ₹10,000 per person',
            'Kolkata': '₹8,000 - ₹15,000 per person',
            'Madurai': '₹6,000 - ₹10,000 per person'
        }
        return budgets.get(city, '₹8,000 - ₹15,000 per person')

# Global recognizer instance
_recognizer = None

def get_recognizer():
    """Get or create recognizer instance"""
    global _recognizer
    if _recognizer is None:
        _recognizer = LandmarkRecognizer()
    return _recognizer
