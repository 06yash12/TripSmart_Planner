import csv
import os
import math

DATA_PATH = os.path.join("data", "Hotel.csv")

def calculate_hotel_price(hotel, num_adults, num_children, num_days):
    """
    Calculate hotel price based on number of people and days
    
    Logic:
    - 1 person: use price_1p_inr
    - 2 people: use price_2p_inr
    - 3 people: use price_3p_inr
    - 4 people: use price_4p_inr
    - 5+ people: combine rooms (e.g., 6 people = 4p room + 2p room)
    """
    total_people = num_adults + num_children
    
    # Get prices from hotel
    price_1p = int(hotel['price_1p_inr'])
    price_2p = int(hotel['price_2p_inr'])
    price_3p = int(hotel['price_3p_inr'])
    price_4p = int(hotel['price_4p_inr'])
    
    rooms_breakdown = []
    total_price_per_night = 0
    
    if total_people <= 4:
        # Single room
        if total_people == 1:
            total_price_per_night = price_1p
            rooms_breakdown.append({"type": "Single Room", "people": 1, "price": price_1p})
        elif total_people == 2:
            total_price_per_night = price_2p
            rooms_breakdown.append({"type": "Double Room", "people": 2, "price": price_2p})
        elif total_people == 3:
            total_price_per_night = price_3p
            rooms_breakdown.append({"type": "Triple Room", "people": 3, "price": price_3p})
        else:  # 4 people
            total_price_per_night = price_4p
            rooms_breakdown.append({"type": "Quad Room", "people": 4, "price": price_4p})
    else:
        # Multiple rooms needed
        remaining_people = total_people
        
        # Use 4-person rooms first
        while remaining_people >= 4:
            total_price_per_night += price_4p
            rooms_breakdown.append({"type": "Quad Room", "people": 4, "price": price_4p})
            remaining_people -= 4
        
        # Handle remaining people
        if remaining_people == 3:
            total_price_per_night += price_3p
            rooms_breakdown.append({"type": "Triple Room", "people": 3, "price": price_3p})
        elif remaining_people == 2:
            total_price_per_night += price_2p
            rooms_breakdown.append({"type": "Double Room", "people": 2, "price": price_2p})
        elif remaining_people == 1:
            total_price_per_night += price_1p
            rooms_breakdown.append({"type": "Single Room", "people": 1, "price": price_1p})
    
    total_price = total_price_per_night * num_days
    
    return {
        'price_per_night': total_price_per_night,
        'total_price': total_price,
        'rooms_breakdown': rooms_breakdown,
        'num_rooms': len(rooms_breakdown),
        'total_people': total_people
    }

def get_hotels_from_csv(city, num_adults=2, num_children=0, num_days=3, top_n=5):
    """
    Get hotels from CSV file with calculated prices based on occupancy
    """
    try:
        city_hotels = []
        with open(DATA_PATH, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["city"].lower() == city.lower():
                    # Calculate price for this hotel
                    pricing = calculate_hotel_price(row, num_adults, num_children, num_days)
                    
                    city_hotels.append({
                        "name": row["hotel_name"],
                        "rating": float(row["rating"]),
                        "city": row["city"],
                        "amenities": row["amenities"],
                        "nearest_landmark": row["nearest_landmark"],
                        "price_per_night": pricing['price_per_night'],
                        "total_price": pricing['total_price'],
                        "rooms_breakdown": pricing['rooms_breakdown'],
                        "num_rooms": pricing['num_rooms'],
                        "total_people": pricing['total_people'],
                        "num_days": num_days,
                        "base_2p_rate": int(row["base_2p_rate_inr"])
                    })
        
        if not city_hotels:
            return []
        
        # Sort by rating (desc) then price (asc)
        sorted_hotels = sorted(
            city_hotels,
            key=lambda x: (-x["rating"], x["price_per_night"])
        )[:top_n]
        
        return sorted_hotels
    
    except Exception as e:
        print(f"Error loading hotels: {e}")
        return []

def recommend_hotel(city, num_adults=2, num_children=0, num_days=3):
    """
    Recommend the best hotel for a given city
    based on rating (higher is better) and price (lower is better).
    """
    hotels = get_hotels_from_csv(city, num_adults, num_children, num_days, top_n=1)
    
    if not hotels:
        return {"message": "No hotels found"}
    
    return hotels[0]


# Test the tool
if __name__ == "__main__":
    result = recommend_hotel("Mumbai", num_adults=3, num_children=2, num_days=3)
    print(result)
    print(f"\nRooms breakdown:")
    for room in result['rooms_breakdown']:
        print(f"  {room['type']}: {room['people']} people - ₹{room['price']}/night")
    print(f"\nTotal: {result['num_rooms']} room(s) for {result['total_people']} people")
    print(f"Price: ₹{result['price_per_night']}/night × {result['num_days']} days = ₹{result['total_price']}")
