from data.repositories import FlightRepository, TrainRepository, HotelRepository, LandmarkRepository
from .budget_calculator import BudgetCalculator

class TripPlannerService:
    def __init__(self):
        self.flight_repo = FlightRepository()
        self.train_repo = TrainRepository()
        self.hotel_repo = HotelRepository()
        self.landmark_repo = LandmarkRepository()
        self.budget_calc = BudgetCalculator()
    
    def plan_trip(self, config):
        source = config['source']
        destination = config['destination']
        days = config['days']
        adults = config['adults']
        children = config['children']
        transport_mode = config['transport_mode']
        flight_class = config.get('flight_class', 'Economy')
        train_class = config.get('train_class', '3AC')
        budget_type = config.get('budget_type', 'moderate')
        
        result = {
            'flights': [],
            'trains': [],
            'hotels': [],
            'attractions': [],
            'budget': None
        }
        
        if transport_mode in ["Flight", "Compare Both"]:
            flights = self.flight_repo.find_all_by_route(source, destination, flight_class)
            result['flights'] = flights
        
        if transport_mode in ["Train", "Compare Both"]:
            trains = self.train_repo.find_by_route(source, destination, train_class)
            result['trains'] = trains
        
        hotels = self.hotel_repo.find_by_city(destination, adults, children, days, top_n=10)
        result['hotels'] = hotels
        
        attractions = self.landmark_repo.find_by_city(destination, top_n=9)
        result['attractions'] = attractions
        
        if result['flights'] or result['trains']:
            transport_cost = 0
            if result['flights']:
                transport_cost = result['flights'][0]['class_price'] * (adults + children)
            elif result['trains']:
                transport_cost = result['trains'][0]['selected_price'] * (adults + children)
            
            hotel_cost = hotels[0]['total_price'] if hotels else 0
            
            budget = self.budget_calc.calculate_trip_budget(
                days=days,
                adults=adults,
                children=children,
                transport_cost=transport_cost,
                hotel_cost=hotel_cost,
                budget_type=budget_type
            )
            result['budget'] = budget
        
        return result
    
    def compare_transport(self, source, dest, flight_class, train_class, num_people):
        flight = self.flight_repo.find_cheapest(source, dest, flight_class)
        trains = self.train_repo.find_by_route(source, dest, train_class)
        
        comparison = {
            'flight': flight,
            'train': trains[0] if trains else None,
            'savings': 0
        }
        
        if flight and trains:
            flight_total = flight['class_price'] * num_people
            train_total = trains[0]['selected_price'] * num_people
            comparison['savings'] = flight_total - train_total
        
        return comparison
