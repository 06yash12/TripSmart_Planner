import csv
import pandas as pd
from config.settings import settings

class FlightRepository:
    def __init__(self):
        self.data_path = settings.FLIGHT_CSV
        self._cache = None
    
    def get_all(self):
        if self._cache is None:
            self._load_data()
        return self._cache
    
    def find_by_route(self, source, destination):
        df = self.get_all()
        return df[(df['from_city'].str.lower() == source.lower()) & 
                  (df['to_city'].str.lower() == destination.lower())]
    
    def find_cheapest(self, source, destination, flight_class="Economy"):
        flights = self.find_by_route(source, destination)
        if flights.empty:
            return None
        
        class_map = {
            "Economy": "economy_price_inr",
            "Premium Economy": "premium_economy_price_inr",
            "Business": "business_price_inr",
            "First Class": "first_class_price_inr"
        }
        
        price_column = class_map.get(flight_class, "economy_price_inr")
        cheapest = flights.loc[flights[price_column].astype(int).idxmin()]
        
        baggage_map = {
            "Economy": "15kg",
            "Premium Economy": "20kg",
            "Business": "30kg",
            "First Class": "40kg"
        }
        
        return {
            "from": cheapest['from_city'],
            "to": cheapest['to_city'],
            "airline": cheapest['airline_name'],
            "duration": cheapest['duration_hours_avg'],
            "class_price": int(cheapest[price_column]),
            "selected_class": flight_class,
            "baggage": baggage_map.get(flight_class, "15kg")
        }
    
    def find_all_by_route(self, source, destination, flight_class="Economy"):
        """Get all flights for a route with selected class pricing"""
        flights = self.find_by_route(source, destination)
        if flights.empty:
            return []
        
        class_map = {
            "Economy": "economy_price_inr",
            "Premium Economy": "premium_economy_price_inr",
            "Business": "business_price_inr",
            "First Class": "first_class_price_inr"
        }
        
        price_column = class_map.get(flight_class, "economy_price_inr")
        
        baggage_map = {
            "Economy": "15kg",
            "Premium Economy": "20kg",
            "Business": "30kg",
            "First Class": "40kg"
        }
        
        result = []
        for _, flight in flights.iterrows():
            result.append({
                "from": flight['from_city'],
                "to": flight['to_city'],
                "airline": flight['airline_name'],
                "duration": flight['duration_hours_avg'],
                "class_price": int(flight[price_column]),
                "selected_class": flight_class,
                "baggage": baggage_map.get(flight_class, "15kg")
            })
        
        # Sort by price
        result.sort(key=lambda x: x['class_price'])
        return result
    
    def _load_data(self):
        self._cache = pd.read_csv(self.data_path)
