import json
from config.settings import settings

class BudgetCalculator:
    def __init__(self):
        self.expenses = self._load_expenses()
    
    def calculate_trip_budget(self, days, adults, children, transport_cost, hotel_cost, budget_type='moderate'):
        adult_exp = self.expenses['adult_expenses']
        child_exp = self.expenses['child_expenses']
        budget_mult = self.expenses['budget_categories'][budget_type]['food_multiplier']
        
        daily_food_adult = (
            adult_exp['food_breakfast'] + 
            adult_exp['food_lunch'] + 
            adult_exp['food_dinner'] + 
            adult_exp['food_snacks']
        ) * budget_mult
        
        daily_food_child = (
            child_exp['food_breakfast'] + 
            child_exp['food_lunch'] + 
            child_exp['food_dinner'] + 
            child_exp['food_snacks']
        ) * budget_mult
        
        daily_other_adult = (
            adult_exp['local_transport_per_day'] +
            adult_exp['shopping_per_day'] +
            adult_exp['activities_per_day'] +
            adult_exp['miscellaneous_per_day']
        )
        
        daily_other_child = (
            child_exp['shopping_per_day'] +
            child_exp['activities_per_day'] +
            child_exp['miscellaneous_per_day']
        )
        
        total_food = (daily_food_adult * adults + daily_food_child * children) * days
        total_activities = (daily_other_adult * adults + daily_other_child * children) * days
        
        shared = self.expenses['shared_expenses']
        shared_costs = (
            shared['taxi_airport_pickup'] +
            shared['taxi_airport_drop'] +
            shared['emergency_fund_per_trip'] +
            (shared['sim_card_data_per_person'] * (adults + children)) +
            (shared['tips_gratuity_per_day'] * days)
        )
        
        total_cost = transport_cost + hotel_cost + total_food + total_activities + shared_costs
        
        return {
            'total_cost': round(total_cost),
            'cost_per_day': round(total_cost / days),
            'transport_cost': transport_cost,
            'hotel_cost': hotel_cost,
            'food_cost': round(total_food),
            'activities_cost': round(total_activities),
            'shared_cost': round(shared_costs),
            'breakdown': {
                'Transport': transport_cost,
                'Accommodation': hotel_cost,
                'Food & Dining': round(total_food),
                'Activities & Shopping': round(total_activities),
                'Other Expenses': round(shared_costs)
            }
        }
    
    def _load_expenses(self):
        try:
            with open(settings.EXPENSES_JSON, 'r') as f:
                return json.load(f)
        except:
            return {
                'adult_expenses': {
                    'food_breakfast': 200,
                    'food_lunch': 400,
                    'food_dinner': 500,
                    'food_snacks': 150,
                    'local_transport_per_day': 300,
                    'shopping_per_day': 500,
                    'activities_per_day': 300,
                    'miscellaneous_per_day': 200
                },
                'child_expenses': {
                    'food_breakfast': 100,
                    'food_lunch': 200,
                    'food_dinner': 250,
                    'food_snacks': 100,
                    'shopping_per_day': 200,
                    'activities_per_day': 150,
                    'miscellaneous_per_day': 100
                },
                'shared_expenses': {
                    'taxi_airport_pickup': 600,
                    'taxi_airport_drop': 600,
                    'emergency_fund_per_trip': 2000,
                    'sim_card_data_per_person': 400,
                    'tips_gratuity_per_day': 150
                },
                'budget_categories': {
                    'budget': {'food_multiplier': 0.8},
                    'moderate': {'food_multiplier': 1.2},
                    'luxury': {'food_multiplier': 2.0},
                    'ultra_luxury': {'food_multiplier': 3.0}
                }
            }
