import json
import os

DATA_PATH = os.path.join("data", "expenses.json")

class ExpenseCalculator:
    def __init__(self):
        with open(DATA_PATH, "r") as f:
            self.expenses_data = json.load(f)
    
    def calculate_daily_food_cost(self, num_adults, num_children, budget_type="moderate"):
        """Calculate daily food cost for all travelers"""
        adult_exp = self.expenses_data["adult_expenses"]
        child_exp = self.expenses_data["child_expenses"]
        multiplier = self.expenses_data["budget_categories"][budget_type]["food_multiplier"]
        
        adult_daily = (
            adult_exp["food_breakfast"] + 
            adult_exp["food_lunch"] + 
            adult_exp["food_dinner"] + 
            adult_exp["food_snacks"]
        ) * multiplier
        
        child_daily = (
            child_exp["food_breakfast"] + 
            child_exp["food_lunch"] + 
            child_exp["food_dinner"] + 
            child_exp["food_snacks"]
        ) * multiplier
        
        total_daily = (adult_daily * num_adults) + (child_daily * num_children)
        
        return {
            "adult_per_day": round(adult_daily),
            "child_per_day": round(child_daily),
            "total_per_day": round(total_daily),
            "breakdown": {
                "breakfast": round((adult_exp["food_breakfast"] * num_adults + child_exp["food_breakfast"] * num_children) * multiplier),
                "lunch": round((adult_exp["food_lunch"] * num_adults + child_exp["food_lunch"] * num_children) * multiplier),
                "dinner": round((adult_exp["food_dinner"] * num_adults + child_exp["food_dinner"] * num_children) * multiplier),
                "snacks": round((adult_exp["food_snacks"] * num_adults + child_exp["food_snacks"] * num_children) * multiplier)
            }
        }
    
    def calculate_daily_activities(self, num_adults, num_children):
        """Calculate daily activity and miscellaneous costs"""
        adult_exp = self.expenses_data["adult_expenses"]
        child_exp = self.expenses_data["child_expenses"]
        
        adult_daily = (
            adult_exp["local_transport"] + 
            adult_exp["shopping"] + 
            adult_exp["activities"] + 
            adult_exp["miscellaneous"]
        )
        
        child_daily = (
            child_exp["local_transport"] + 
            child_exp["shopping"] + 
            child_exp["activities"] + 
            child_exp["miscellaneous"]
        )
        
        return {
            "adult_per_day": round(adult_daily),
            "child_per_day": round(child_daily),
            "total_per_day": round((adult_daily * num_adults) + (child_daily * num_children)),
            "breakdown": {
                "transport": round((adult_exp["local_transport"] * num_adults + child_exp["local_transport"] * num_children)),
                "shopping": round((adult_exp["shopping"] * num_adults + child_exp["shopping"] * num_children)),
                "activities": round((adult_exp["activities"] * num_adults + child_exp["activities"] * num_children)),
                "miscellaneous": round((adult_exp["miscellaneous"] * num_adults + child_exp["miscellaneous"] * num_children))
            }
        }
    
    def calculate_entry_fees(self, places, num_adults, num_children):
        """Calculate total entry fees with child discount"""
        discounts = self.expenses_data["discounts"]
        child_discount = discounts["child_entry_fee_discount"]
        
        total_adult_fees = sum([place.get('entry_fee', 0) for place in places]) * num_adults
        total_child_fees = sum([place.get('entry_fee', 0) for place in places]) * num_children * (1 - child_discount)
        
        return {
            "adult_total": round(total_adult_fees),
            "child_total": round(total_child_fees),
            "child_discount_amount": round(sum([place.get('entry_fee', 0) for place in places]) * num_children * child_discount),
            "total": round(total_adult_fees + total_child_fees),
            "per_place": [
                {
                    "name": place["name"],
                    "fee": place.get('entry_fee', 0),
                    "adult_cost": place.get('entry_fee', 0) * num_adults,
                    "child_cost": round(place.get('entry_fee', 0) * num_children * (1 - child_discount))
                }
                for place in places
            ]
        }
    
    def calculate_shared_expenses(self, num_adults, num_children, trip_days):
        """Calculate shared expenses"""
        shared = self.expenses_data["shared_expenses"]
        total_travelers = num_adults + num_children
        
        return {
            "airport_taxi": shared["taxi_airport_pickup"] + shared["taxi_airport_drop"],
            "travel_insurance": shared["travel_insurance_per_person"] * total_travelers,
            "emergency_fund": shared["emergency_fund"],
            "sim_card": shared["sim_card_data"],
            "tips_gratuity": shared["tips_gratuity_per_day"] * trip_days,
            "total": round(
                shared["taxi_airport_pickup"] + 
                shared["taxi_airport_drop"] + 
                (shared["travel_insurance_per_person"] * total_travelers) + 
                shared["emergency_fund"] + 
                shared["sim_card_data"] + 
                (shared["tips_gratuity_per_day"] * trip_days)
            )
        }
    
    def apply_group_discount(self, total_cost, num_adults, num_children):
        """Apply group discount if applicable"""
        discounts = self.expenses_data["discounts"]
        total_travelers = num_adults + num_children
        
        if total_travelers >= discounts["group_discount_threshold"]:
            discount_amount = total_cost * discounts["group_discount_percentage"]
            return {
                "applicable": True,
                "discount_percentage": discounts["group_discount_percentage"] * 100,
                "discount_amount": round(discount_amount),
                "final_cost": round(total_cost - discount_amount)
            }
        
        return {
            "applicable": False,
            "discount_percentage": 0,
            "discount_amount": 0,
            "final_cost": total_cost
        }
    
    def calculate_complete_budget(self, transport_cost, hotel_cost_per_night, places, 
                                  num_adults, num_children, trip_days, budget_type="moderate"):
        """Calculate complete trip budget"""
        
        # Daily costs
        food_costs = self.calculate_daily_food_cost(num_adults, num_children, budget_type)
        activity_costs = self.calculate_daily_activities(num_adults, num_children)
        
        # Trip costs
        total_food = food_costs["total_per_day"] * trip_days
        total_activities = activity_costs["total_per_day"] * trip_days
        total_hotel = hotel_cost_per_night * trip_days
        
        # Entry fees
        entry_fees = self.calculate_entry_fees(places, num_adults, num_children)
        
        # Shared expenses
        shared_expenses = self.calculate_shared_expenses(num_adults, num_children, trip_days)
        
        # Subtotal
        subtotal = (
            transport_cost + 
            total_hotel + 
            total_food + 
            total_activities + 
            entry_fees["total"] + 
            shared_expenses["total"]
        )
        
        # Apply group discount
        group_discount = self.apply_group_discount(subtotal, num_adults, num_children)
        
        total_travelers = num_adults + num_children
        per_person = group_discount["final_cost"] / total_travelers if total_travelers > 0 else 0
        
        return {
            "transport": transport_cost,
            "hotel": {
                "per_night": hotel_cost_per_night,
                "nights": trip_days,
                "total": total_hotel
            },
            "food": {
                "per_day": food_costs["total_per_day"],
                "days": trip_days,
                "total": total_food,
                "breakdown": food_costs["breakdown"]
            },
            "activities": {
                "per_day": activity_costs["total_per_day"],
                "days": trip_days,
                "total": total_activities,
                "breakdown": activity_costs["breakdown"]
            },
            "entry_fees": entry_fees,
            "shared_expenses": shared_expenses,
            "subtotal": subtotal,
            "group_discount": group_discount,
            "final_total": group_discount["final_cost"],
            "per_person": round(per_person),
            "per_adult": round(per_person) if num_adults > 0 else 0,
            "travelers": {
                "adults": num_adults,
                "children": num_children,
                "total": total_travelers
            }
        }
    
    def get_budget_recommendations(self, total_budget, budget_type="moderate"):
        """Get smart budget recommendations"""
        recommendations = []
        
        if budget_type == "budget":
            recommendations = [
                "🚂 Consider train travel to save 40-60% on transport",
                "🏨 Choose 2-3 star hotels for comfortable budget stays",
                "🍽️ Try local street food and small restaurants",
                "🎫 Visit free attractions and parks",
                "🚶 Use public transport and walking",
                "🛍️ Shop at local markets for better prices"
            ]
        elif budget_type == "moderate":
            recommendations = [
                "✈️ Mix of flights and trains based on distance",
                "🏨 3-4 star hotels with good amenities",
                "🍽️ Balance between restaurants and local eateries",
                "🎫 Mix of paid and free attractions",
                "🚕 Use app-based cabs for convenience",
                "🛍️ Moderate shopping at malls and markets"
            ]
        else:  # luxury
            recommendations = [
                "✈️ Premium flights with extra baggage",
                "🏨 5-star hotels with full amenities",
                "🍽️ Fine dining and premium restaurants",
                "🎫 VIP access to attractions",
                "🚗 Private car rentals",
                "🛍️ Premium shopping experiences"
            ]
        
        return recommendations


# Test the calculator
if __name__ == "__main__":
    calc = ExpenseCalculator()
    
    # Sample calculation
    result = calc.calculate_complete_budget(
        transport_cost=5000,
        hotel_cost_per_night=3000,
        places=[
            {"name": "Fort", "entry_fee": 100},
            {"name": "Museum", "entry_fee": 75},
            {"name": "Temple", "entry_fee": 0}
        ],
        num_adults=2,
        num_children=1,
        trip_days=3,
        budget_type="moderate"
    )
    
    print(f"Total Budget: ₹{result['final_total']:,}")
    print(f"Per Person: ₹{result['per_person']:,}")
