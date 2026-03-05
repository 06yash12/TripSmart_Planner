import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import json
import os
from datetime import datetime, timedelta
import calendar

class PricePredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.label_encoders = {}
        self.is_trained = False
        
        # Indian holidays (approximate dates)
        self.holiday_periods = [
            (1, 1),   # New Year
            (1, 26),  # Republic Day
            (3, 8),   # Holi (varies)
            (4, 14),  # Ambedkar Jayanti
            (5, 1),   # May Day
            (8, 15),  # Independence Day
            (10, 2),  # Gandhi Jayanti
            (10, 24), # Dussehra (varies)
            (11, 12), # Diwali (varies)
            (12, 25), # Christmas
        ]
        
        # Summer vacation months
        self.summer_months = [4, 5, 6]  # April, May, June
        # Winter vacation months
        self.winter_months = [12, 1]  # December, January
    
    def is_weekend(self, date):
        """Check if date is weekend (Saturday=5, Sunday=6)"""
        return date.weekday() in [5, 6]
    
    def is_holiday_period(self, date):
        """Check if date is near a holiday (within 3 days)"""
        for month, day in self.holiday_periods:
            if date.month == month and abs(date.day - day) <= 3:
                return True
        return False
    
    def is_vacation_season(self, date):
        """Check if date is in vacation season"""
        return date.month in self.summer_months or date.month in self.winter_months
    
    def calculate_price_multiplier(self, travel_date):
        """Calculate price multiplier based on date characteristics"""
        multiplier = 1.0
        
        # Weekend pricing (1.4x)
        if self.is_weekend(travel_date):
            multiplier *= 1.4
        
        # Holiday period pricing (1.4x)
        if self.is_holiday_period(travel_date):
            multiplier *= 1.4
        
        # Vacation season pricing (1.2x)
        if self.is_vacation_season(travel_date):
            multiplier *= 1.2
        
        return multiplier
        
    def generate_training_data(self):
        """Generate synthetic training data based on real patterns"""
        # Load actual flight data from CSV
        import csv
        flights = []
        with open(os.path.join("data", "Flight.csv"), "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                flights.append({
                    'from': row['from_city'],
                    'to': row['to_city'],
                    'airline': row['airline_name'],
                    'price': int(row['economy_price_inr'])
                })
        
        training_data = []
        
        # Generate historical data with price variations
        for flight in flights:
            base_price = flight['price']
            
            # Simulate 90 days of historical data
            for days_before in range(1, 91):
                # Price factors
                advance_booking_factor = 1.0 - (days_before / 200)  # Cheaper when booked early
                weekend_factor = 1.1 if days_before % 7 in [5, 6] else 1.0
                holiday_factor = 1.3 if days_before % 30 < 5 else 1.0  # Holiday season
                demand_factor = np.random.uniform(0.9, 1.2)
                
                # Calculate price with variations
                price = base_price * advance_booking_factor * weekend_factor * holiday_factor * demand_factor
                
                training_data.append({
                    'from': flight['from'],
                    'to': flight['to'],
                    'airline': flight['airline'],
                    'days_before_travel': days_before,
                    'is_weekend': 1 if days_before % 7 in [5, 6] else 0,
                    'is_holiday_season': 1 if days_before % 30 < 5 else 0,
                    'price': price
                })
        
        return training_data
    
    def train(self):
        """Train the price prediction model"""
        training_data = self.generate_training_data()
        
        # Prepare features
        X = []
        y = []
        
        # Encode categorical variables
        self.label_encoders['from'] = LabelEncoder()
        self.label_encoders['to'] = LabelEncoder()
        self.label_encoders['airline'] = LabelEncoder()
        
        from_cities = [d['from'] for d in training_data]
        to_cities = [d['to'] for d in training_data]
        airlines = [d['airline'] for d in training_data]
        
        self.label_encoders['from'].fit(from_cities)
        self.label_encoders['to'].fit(to_cities)
        self.label_encoders['airline'].fit(airlines)
        
        for data in training_data:
            features = [
                self.label_encoders['from'].transform([data['from']])[0],
                self.label_encoders['to'].transform([data['to']])[0],
                self.label_encoders['airline'].transform([data['airline']])[0],
                data['days_before_travel'],
                data['is_weekend'],
                data['is_holiday_season']
            ]
            X.append(features)
            y.append(data['price'])
        
        # Train model
        self.model.fit(X, y)
        self.is_trained = True
        
        return True
    
    def predict_price_for_date(self, from_city, to_city, airline, base_price, travel_date):
        """Predict price for a specific travel date"""
        # Calculate multiplier based on date characteristics
        multiplier = self.calculate_price_multiplier(travel_date)
        
        # Apply multiplier to base price
        predicted_price = base_price * multiplier
        
        return predicted_price
    
    def get_price_trend_with_dates(self, from_city, to_city, airline, base_price, start_date=None):
        """Get price trend for next 30 days with actual dates"""
        if start_date is None:
            start_date = datetime.now()
        
        predictions = []
        days_to_check = [1, 3, 7, 14, 21, 30]
        
        for days in days_to_check:
            travel_date = start_date + timedelta(days=days)
            predicted_price = self.predict_price_for_date(
                from_city, to_city, airline, base_price, travel_date
            )
            
            change = ((predicted_price - base_price) / base_price) * 100
            
            predictions.append({
                'days': days,
                'date': travel_date.strftime('%d %b %Y'),
                'day_name': travel_date.strftime('%A'),
                'price': round(predicted_price, 2),
                'change_percent': round(change, 1),
                'is_weekend': self.is_weekend(travel_date),
                'is_holiday': self.is_holiday_period(travel_date),
                'is_vacation': self.is_vacation_season(travel_date)
            })
        
        return predictions
        return predictions
    
    def get_best_booking_time(self, from_city, to_city, airline):
        """Recommend best time to book within 30 days"""
        if not self.is_trained:
            self.train()
        
        # Check prices for next 30 days only
        prices = []
        for days in range(1, 31):
            price = self.predict_price(from_city, to_city, airline, days)
            if price:
                prices.append({'days': days, 'price': price})
        
        if not prices:
            return None
        
        # Find minimum price within 30 days
        min_price_day = min(prices, key=lambda x: x['price'])
        current_price = prices[0]['price']
        
        savings = current_price - min_price_day['price']
        savings_percent = (savings / current_price) * 100
        
        # Calculate the actual date
        best_date = datetime.now() + timedelta(days=min_price_day['days'])
        current_date = datetime.now() + timedelta(days=1)
        
        return {
            'best_day': min_price_day['days'],
            'best_date': best_date.strftime('%d %B %Y'),
            'current_date': current_date.strftime('%d %B %Y'),
            'best_price': round(min_price_day['price'], 2),
            'current_price': round(current_price, 2),
            'savings': round(savings, 2),
            'savings_percent': round(savings_percent, 1),
            'recommendation': self._get_recommendation(min_price_day['days'], savings_percent, best_date)
        }
    
    def _get_recommendation(self, best_day, savings_percent, best_date):
        """Generate booking recommendation with date"""
        date_str = best_date.strftime('%d %B')
        
        if best_day <= 3 and savings_percent < 5:
            return "📌 Book now! Prices are stable and unlikely to drop significantly."
        elif best_day <= 7 and savings_percent < 10:
            return f"⏰ Consider booking by {date_str}. Small savings possible."
        elif savings_percent >= 15:
            return f"💰 Wait until {date_str} to save {savings_percent:.1f}%! Set a price alert."
        elif savings_percent >= 10:
            return f"💡 Booking on {date_str} could save you {savings_percent:.1f}%."
        else:
            return "📊 Prices are relatively stable. Book when convenient."

# Global predictor instance
_predictor = None

def get_predictor():
    """Get or create predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = PricePredictor()
        _predictor.train()
    return _predictor

    def get_best_booking_time_v2(self, from_city, to_city, airline, base_price, start_date=None):
        """Recommend best time to book within 30 days with actual dates and improved algorithm"""
        if start_date is None:
            start_date = datetime.now()
        
        # Check prices for next 30 days
        prices = []
        for days in range(1, 31):
            travel_date = start_date + timedelta(days=days)
            price = self.predict_price_for_date(from_city, to_city, airline, base_price, travel_date)
            prices.append({
                'days': days,
                'date': travel_date,
                'price': price
            })
        
        if not prices:
            return None
        
        # Find minimum price within 30 days
        min_price_day = min(prices, key=lambda x: x['price'])
        current_price = prices[0]['price']
        
        savings = current_price - min_price_day['price']
        savings_percent = (savings / current_price) * 100
        
        # Calculate the actual dates
        best_date = min_price_day['date']
        current_date = prices[0]['date']
        
        return {
            'best_day': min_price_day['days'],
            'best_date': best_date.strftime('%d %B %Y'),
            'best_day_name': best_date.strftime('%A'),
            'current_date': current_date.strftime('%d %B %Y'),
            'best_price': round(min_price_day['price'], 2),
            'current_price': round(current_price, 2),
            'savings': round(savings, 2),
            'savings_percent': round(savings_percent, 1),
            'is_weekend': self.is_weekend(best_date),
            'is_holiday': self.is_holiday_period(best_date),
            'recommendation': self._get_recommendation_v2(min_price_day['days'], savings_percent, best_date)
        }
    
    def _get_recommendation_v2(self, best_day, savings_percent, best_date):
        """Generate booking recommendation with date and day name"""
        date_str = best_date.strftime('%d %B')
        day_name = best_date.strftime('%A')
        
        if best_day <= 3 and savings_percent < 5:
            return "📌 Book now! Prices are stable and unlikely to drop significantly."
        elif best_day <= 7 and savings_percent < 10:
            return f"⏰ Consider booking by {date_str} ({day_name}). Small savings possible."
        elif savings_percent >= 15:
            return f"💰 Wait until {date_str} ({day_name}) to save {savings_percent:.1f}%! Set a price alert."
        elif savings_percent >= 10:
            return f"💡 Booking on {date_str} ({day_name}) could save you {savings_percent:.1f}%."
        else:
            return "📊 Prices are relatively stable. Book when convenient."
