import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class NeuralCollaborativeFiltering:
    """Neural Collaborative Filtering model using TensorFlow/Keras"""
    
    def __init__(self, embedding_dim=32):
        self.embedding_dim = embedding_dim
        self.model = None
        self.user_encoder = LabelEncoder()
        self.destination_encoder = LabelEncoder()
        self.is_trained = False
        
    def build_model(self, num_users, num_destinations):
        """Build NCF model architecture"""
        # User input
        user_input = layers.Input(shape=(1,), name='user_input')
        user_embedding = layers.Embedding(
            num_users, 
            self.embedding_dim, 
            name='user_embedding'
        )(user_input)
        user_vec = layers.Flatten(name='user_flatten')(user_embedding)
        
        # Destination input
        dest_input = layers.Input(shape=(1,), name='dest_input')
        dest_embedding = layers.Embedding(
            num_destinations, 
            self.embedding_dim, 
            name='dest_embedding'
        )(dest_input)
        dest_vec = layers.Flatten(name='dest_flatten')(dest_embedding)
        
        # Concatenate embeddings
        concat = layers.Concatenate()([user_vec, dest_vec])
        
        # Deep neural network layers
        dense1 = layers.Dense(128, activation='relu', name='dense1')(concat)
        dropout1 = layers.Dropout(0.3)(dense1)
        dense2 = layers.Dense(64, activation='relu', name='dense2')(dropout1)
        dropout2 = layers.Dropout(0.3)(dense2)
        dense3 = layers.Dense(32, activation='relu', name='dense3')(dropout2)
        
        # Output layer (rating prediction)
        output = layers.Dense(1, activation='sigmoid', name='output')(dense3)
        
        # Create model
        model = Model(inputs=[user_input, dest_input], outputs=output)
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def train(self, user_trips_data):
        """Train the NCF model"""
        if len(user_trips_data) < 3:
            return False
        
        # Prepare data
        users = [trip['user_id'] for trip in user_trips_data]
        destinations = [trip['destination'] for trip in user_trips_data]
        ratings = np.array([trip['rating'] / 5.0 for trip in user_trips_data])  # Normalize to 0-1
        
        # Encode users and destinations
        self.user_encoder.fit(users)
        self.destination_encoder.fit(destinations)
        
        user_encoded = self.user_encoder.transform(users)
        dest_encoded = self.destination_encoder.transform(destinations)
        
        # Build model
        num_users = len(self.user_encoder.classes_)
        num_destinations = len(self.destination_encoder.classes_)
        
        self.model = self.build_model(num_users, num_destinations)
        
        # Train model
        self.model.fit(
            [user_encoded, dest_encoded],
            ratings,
            epochs=50,
            batch_size=32,
            verbose=0,
            validation_split=0.2
        )
        
        self.is_trained = True
        return True
    
    def predict(self, user_id, destination):
        """Predict rating for user-destination pair"""
        if not self.is_trained:
            return None
        
        try:
            user_encoded = self.user_encoder.transform([user_id])[0]
            dest_encoded = self.destination_encoder.transform([destination])[0]
            
            prediction = self.model.predict(
                [np.array([user_encoded]), np.array([dest_encoded])],
                verbose=0
            )[0][0]
            
            return prediction * 5.0  # Denormalize to 1-5 scale
        except:
            return None
    
    def get_user_recommendations(self, user_id, all_destinations, n=3):
        """Get top N recommendations for a user"""
        if not self.is_trained:
            return []
        
        predictions = []
        for dest in all_destinations:
            pred = self.predict(user_id, dest)
            if pred is not None:
                predictions.append({
                    'destination': dest,
                    'predicted_rating': pred
                })
        
        # Sort by predicted rating
        predictions.sort(key=lambda x: x['predicted_rating'], reverse=True)
        return predictions[:n]


class TravelRecommender:
    def __init__(self):
        self.user_data_file = "data/user_trips.json"
        self.ncf_model = NeuralCollaborativeFiltering(embedding_dim=32)
        
        # Destination features for content-based filtering
        self.destination_features = {
            "Goa": {
                "type": "beach",
                "vibe": "relaxed", 
                "budget_level": 2,  # 1=budget, 2=moderate, 3=luxury
                "activities": ["water_sports", "nightlife", "beaches"],
                "best_for": ["couples", "friends"],
                "climate": "tropical"
            },
            "Jaipur": {
                "type": "heritage",
                "vibe": "cultural",
                "budget_level": 2,
                "activities": ["monuments", "shopping", "history"],
                "best_for": ["family", "solo"],
                "climate": "desert"
            },
            "Kerala": {
                "type": "nature",
                "vibe": "relaxed",
                "budget_level": 2,
                "activities": ["backwaters", "nature", "ayurveda"],
                "best_for": ["couples", "family"],
                "climate": "tropical"
            },
            "Manali": {
                "type": "mountain",
                "vibe": "adventure",
                "budget_level": 2,
                "activities": ["trekking", "skiing", "nature"],
                "best_for": ["friends", "couples"],
                "climate": "cold"
            },
            "Udaipur": {
                "type": "heritage",
                "vibe": "romantic",
                "budget_level": 3,
                "activities": ["palaces", "lakes", "culture"],
                "best_for": ["couples", "family"],
                "climate": "desert"
            },
            "Mumbai": {
                "type": "city",
                "vibe": "energetic",
                "budget_level": 3,
                "activities": ["shopping", "nightlife", "food"],
                "best_for": ["friends", "solo"],
                "climate": "tropical"
            },
            "Delhi": {
                "type": "city",
                "vibe": "cultural",
                "budget_level": 2,
                "activities": ["monuments", "food", "shopping"],
                "best_for": ["family", "solo"],
                "climate": "continental"
            },
            "Bangalore": {
                "type": "city",
                "vibe": "modern",
                "budget_level": 2,
                "activities": ["tech", "pubs", "gardens"],
                "best_for": ["friends", "solo"],
                "climate": "pleasant"
            },
            "Chennai": {
                "type": "city",
                "vibe": "cultural",
                "budget_level": 2,
                "activities": ["temples", "beaches", "food"],
                "best_for": ["family", "solo"],
                "climate": "tropical"
            },
            "Kolkata": {
                "type": "city",
                "vibe": "cultural",
                "budget_level": 1,
                "activities": ["culture", "food", "history"],
                "best_for": ["family", "solo"],
                "climate": "tropical"
            }
        }
        
        # Initialize user-item matrix for collaborative filtering
        self.user_item_matrix = {}
        self.load_user_data()
    
    def load_user_data(self):
        """Load existing user trip data"""
        if os.path.exists(self.user_data_file):
            try:
                with open(self.user_data_file, 'r') as f:
                    data = json.load(f)
                    
                # Build user-item matrix
                for trip in data:
                    user_id = trip.get('user_id', 'guest')
                    destination = trip.get('destination')
                    rating = trip.get('rating', 3)
                    
                    if user_id not in self.user_item_matrix:
                        self.user_item_matrix[user_id] = {}
                    
                    self.user_item_matrix[user_id][destination] = rating
            except:
                pass
    
    def save_user_trip(self, user_id, destination, rating, budget_type, trip_details):
        """Save user trip for future recommendations"""
        trip_data = {
            'user_id': user_id,
            'destination': destination,
            'rating': rating,
            'budget_type': budget_type,
            'timestamp': str(datetime.now()),
            'details': trip_details
        }
        
        # Load existing data
        if os.path.exists(self.user_data_file):
            try:
                with open(self.user_data_file, 'r') as f:
                    data = json.load(f)
            except:
                data = []
        else:
            data = []
        
        data.append(trip_data)
        
        # Save updated data
        os.makedirs(os.path.dirname(self.user_data_file), exist_ok=True)
        with open(self.user_data_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Update in-memory matrix
        if user_id not in self.user_item_matrix:
            self.user_item_matrix[user_id] = {}
        self.user_item_matrix[user_id][destination] = rating
    
    def get_user_preferences(self, user_id):
        """Extract user preferences from trip history"""
        if user_id not in self.user_item_matrix:
            return None
        
        user_trips = self.user_item_matrix[user_id]
        
        # Analyze preferences
        preferences = {
            'visited': list(user_trips.keys()),
            'liked_types': [],
            'liked_vibes': [],
            'budget_level': 2,
            'liked_activities': []
        }
        
        # Extract patterns from highly rated destinations
        for dest, rating in user_trips.items():
            if rating >= 4 and dest in self.destination_features:
                features = self.destination_features[dest]
                preferences['liked_types'].append(features['type'])
                preferences['liked_vibes'].append(features['vibe'])
                preferences['liked_activities'].extend(features['activities'])
        
        return preferences
    
    def content_based_recommendations(self, user_id, n=3):
        """Get recommendations based on destination similarity"""
        preferences = self.get_user_preferences(user_id)
        
        if not preferences or not preferences['visited']:
            # Cold start: return popular destinations
            return self._get_popular_destinations(n)
        
        scores = {}
        visited = set(preferences['visited'])
        
        for dest, features in self.destination_features.items():
            if dest in visited:
                continue
            
            score = 0
            
            # Match destination type
            if features['type'] in preferences['liked_types']:
                score += 3
            
            # Match vibe
            if features['vibe'] in preferences['liked_vibes']:
                score += 2
            
            # Match activities
            for activity in preferences['liked_activities']:
                if activity in features['activities']:
                    score += 1
            
            scores[dest] = score
        
        # Sort by score
        sorted_destinations = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for dest, score in sorted_destinations[:n]:
            recommendations.append({
                'destination': dest,
                'score': score,
                'reason': self._generate_reason(dest, preferences),
                'features': self.destination_features[dest]
            })
        
        return recommendations
    
    def collaborative_filtering_recommendations(self, user_id, n=3):
        """Get recommendations using Neural Collaborative Filtering (TensorFlow)"""
        # Load all trip data for training
        if os.path.exists(self.user_data_file):
            try:
                with open(self.user_data_file, 'r') as f:
                    all_trips = json.load(f)
                
                # Train NCF model if not already trained or needs update
                if not self.ncf_model.is_trained and len(all_trips) >= 3:
                    self.ncf_model.train(all_trips)
                
                # Get recommendations using neural network
                if self.ncf_model.is_trained:
                    all_destinations = list(self.destination_features.keys())
                    user_visited = set(self.user_item_matrix.get(user_id, {}).keys())
                    
                    # Filter out already visited destinations
                    unvisited = [d for d in all_destinations if d not in user_visited]
                    
                    # Get neural network predictions
                    ncf_recs = self.ncf_model.get_user_recommendations(
                        user_id, 
                        unvisited, 
                        n=n
                    )
                    
                    result = []
                    for rec in ncf_recs:
                        result.append({
                            'destination': rec['destination'],
                            'score': rec['predicted_rating'],
                            'reason': f"Deep Learning predicts you'll rate this {rec['predicted_rating']:.1f}/5.0",
                            'features': self.destination_features.get(rec['destination'], {})
                        })
                    
                    return result
            except Exception as e:
                pass
        
        # Fallback to traditional collaborative filtering
        if user_id not in self.user_item_matrix:
            return self._get_popular_destinations(n)
        
        # Find similar users using cosine similarity
        similar_users = self._find_similar_users(user_id)
        
        if not similar_users:
            return self._get_popular_destinations(n)
        
        # Get destinations liked by similar users
        recommendations = {}
        user_visited = set(self.user_item_matrix[user_id].keys())
        
        for similar_user, similarity in similar_users[:5]:
            for dest, rating in self.user_item_matrix[similar_user].items():
                if dest not in user_visited and rating >= 4:
                    if dest not in recommendations:
                        recommendations[dest] = 0
                    recommendations[dest] += similarity * rating
        
        # Sort by score
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        
        result = []
        for dest, score in sorted_recs[:n]:
            result.append({
                'destination': dest,
                'score': score,
                'reason': f"Travelers with similar preferences loved {dest}",
                'features': self.destination_features.get(dest, {})
            })
        
        return result
    
    def hybrid_recommendations(self, user_id, n=3):
        """Combine content-based and collaborative filtering"""
        content_recs = self.content_based_recommendations(user_id, n=5)
        collab_recs = self.collaborative_filtering_recommendations(user_id, n=5)
        
        # Merge scores
        combined = {}
        
        for rec in content_recs:
            dest = rec['destination']
            combined[dest] = {
                'score': rec['score'] * 0.6,  # 60% weight to content
                'reason': rec['reason'],
                'features': rec['features']
            }
        
        for rec in collab_recs:
            dest = rec['destination']
            if dest in combined:
                combined[dest]['score'] += rec['score'] * 0.4  # 40% weight to collaborative
            else:
                combined[dest] = {
                    'score': rec['score'] * 0.4,
                    'reason': rec['reason'],
                    'features': rec['features']
                }
        
        # Sort and return top N
        sorted_recs = sorted(combined.items(), key=lambda x: x[1]['score'], reverse=True)
        
        recommendations = []
        for dest, data in sorted_recs[:n]:
            recommendations.append({
                'destination': dest,
                'score': round(data['score'], 2),
                'reason': data['reason'],
                'features': data['features']
            })
        
        return recommendations
    
    def _find_similar_users(self, user_id):
        """Find users with similar travel preferences using cosine similarity"""
        if user_id not in self.user_item_matrix:
            return []
        
        # Create user vectors
        all_destinations = set()
        for user_trips in self.user_item_matrix.values():
            all_destinations.update(user_trips.keys())
        
        all_destinations = sorted(list(all_destinations))
        
        # Build vectors
        user_vector = []
        for dest in all_destinations:
            user_vector.append(self.user_item_matrix[user_id].get(dest, 0))
        
        similarities = []
        for other_user, trips in self.user_item_matrix.items():
            if other_user == user_id:
                continue
            
            other_vector = []
            for dest in all_destinations:
                other_vector.append(trips.get(dest, 0))
            
            # Calculate cosine similarity
            similarity = cosine_similarity([user_vector], [other_vector])[0][0]
            
            if similarity > 0:
                similarities.append((other_user, similarity))
        
        return sorted(similarities, key=lambda x: x[1], reverse=True)
    
    def _get_popular_destinations(self, n=3):
        """Get popular destinations for cold start"""
        popular = [
            {
                'destination': 'Goa',
                'score': 5.0,
                'reason': 'Popular beach destination loved by travelers',
                'features': self.destination_features['Goa']
            },
            {
                'destination': 'Jaipur',
                'score': 4.8,
                'reason': 'Rich heritage and cultural experience',
                'features': self.destination_features['Jaipur']
            },
            {
                'destination': 'Kerala',
                'score': 4.7,
                'reason': 'Serene backwaters and natural beauty',
                'features': self.destination_features['Kerala']
            }
        ]
        return popular[:n]
    
    def _generate_reason(self, destination, preferences):
        """Generate personalized reason for recommendation"""
        features = self.destination_features.get(destination, {})
        
        if features['type'] in preferences['liked_types']:
            return f"You enjoyed {features['type']} destinations before"
        elif features['vibe'] in preferences['liked_vibes']:
            return f"Matches your preference for {features['vibe']} vibes"
        else:
            return f"Based on your travel history"

# Global recommender instance
_recommender = None

def get_recommender():
    """Get or create recommender instance"""
    global _recommender
    if _recommender is None:
        _recommender = TravelRecommender()
    return _recommender
