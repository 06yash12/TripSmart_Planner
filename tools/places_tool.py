import csv
import os

DATA_PATH = os.path.join("data", "Landmark.csv")

def get_top_places(city, top_n=8):
    """
    Get top-rated tourist places for a given city from CSV.
    """
    try:
        city_places = []
        with open(DATA_PATH, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["city"].lower() == city.lower():
                    city_places.append({
                        "name": row["landmark"],
                        "rating": float(row["rating"]),
                        "entry_fee": int(row["entry_fee_inr"]),
                        "description": row["description"],
                        "why_visit": row["why_visit"],
                        "city": row["city"]
                    })
        
        if not city_places:
            return {"message": "No places found"}
        
        # Sort by rating (high to low)
        top_places = sorted(
            city_places,
            key=lambda x: x["rating"],
            reverse=True
        )[:top_n]
        
        return top_places
    
    except Exception as e:
        print(f"Error loading places: {e}")
        return {"message": "Error loading places"}


# Test the tool
if __name__ == "__main__":
    result = get_top_places("Mumbai")
    for p in result:
        print(p)
