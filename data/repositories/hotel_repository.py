import pandas as pd
from config.settings import settings

class HotelRepository:
    def __init__(self):
        self.data_path = settings.HOTEL_CSV
        self._cache = None
    
    def get_all(self):
        if self._cache is None:
            self._load_data()
        return self._cache
    
    def find_by_city(self, city, adults, children, days, top_n=5):
        df = self.get_all()
        hotels = df[df['city'].str.lower() == city.lower()]
        
        if hotels.empty:
            return []
        
        # Sort by rating
        hotels = hotels.sort_values('rating', ascending=False).head(top_n)
        
        result = []
        for _, hotel in hotels.iterrows():
            total_people = adults + children
            # Use base_2p_rate_inr as the price per night
            price_per_night = int(hotel['base_2p_rate_inr'])
            num_rooms = (total_people + 1) // 2
            total_price = price_per_night * num_rooms * days
            
            result.append({
                "name": hotel['hotel_name'],
                "rating": hotel['rating'],
                "nearest_landmark": hotel['nearest_landmark'],
                "amenities": hotel['amenities'],
                "price_per_night": price_per_night,
                "total_price": total_price,
                "num_rooms": num_rooms,
                "num_days": days
            })
        
        return result
    
    def _load_data(self):
        self._cache = pd.read_csv(self.data_path)
