import pandas as pd
from config.settings import settings

class LandmarkRepository:
    def __init__(self):
        self.data_path = settings.LANDMARK_CSV
        self._cache = None
    
    def get_all(self):
        if self._cache is None:
            self._load_data()
        return self._cache
    
    def find_by_city(self, city, top_n=8):
        df = self.get_all()
        landmarks = df[df['city'].str.lower() == city.lower()]
        
        if landmarks.empty:
            return []
        
        # Sort by rating
        landmarks = landmarks.sort_values('rating', ascending=False).head(top_n)
        
        result = []
        for _, landmark in landmarks.iterrows():
            result.append({
                "name": landmark['landmark'],
                "rating": landmark['rating'],
                "entry_fee": int(landmark['entry_fee_inr']),
                "description": landmark['description']
            })
        
        return result
    
    def _load_data(self):
        self._cache = pd.read_csv(self.data_path)
