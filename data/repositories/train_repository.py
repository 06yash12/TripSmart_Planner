import pandas as pd
from config.settings import settings

class TrainRepository:
    def __init__(self):
        self.data_path = settings.TRAIN_CSV
        self._cache = None
    
    def get_all(self):
        if self._cache is None:
            self._load_data()
        return self._cache
    
    def find_by_route(self, source, destination, train_class="3AC"):
        df = self.get_all()
        trains = df[(df['from_city'].str.lower() == source.lower()) & 
                    (df['to_city'].str.lower() == destination.lower())]
        
        if trains.empty:
            return []
        
        class_map = {
            "Sleeper": "SL_price_inr",
            "3AC": "3AC_price_inr",
            "2AC": "2AC_price_inr",
            "1AC": "1AC_price_inr"
        }
        
        price_column = class_map.get(train_class, "3AC_price_inr")
        
        result = []
        for _, train in trains.iterrows():
            result.append({
                "from": train['from_city'],
                "to": train['to_city'],
                "train_name": train['train_name'],
                "train_no": train['train_no'],
                "duration": train['duration_hours'],
                "selected_price": int(train[price_column]),
                "selected_class": train_class
            })
        
        result.sort(key=lambda x: x['selected_price'])
        return result
    
    def _load_data(self):
        self._cache = pd.read_csv(self.data_path)
