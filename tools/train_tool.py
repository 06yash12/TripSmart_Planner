import csv
import os

DATA_PATH = os.path.join("data", "Train.csv")

def search_trains(from_city, to_city, travel_class="3AC"):
    """
    Search for trains matching source and destination
    and return options sorted by price.
    """
    matching_trains = []
    
    try:
        with open(DATA_PATH, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["from_city"].lower() == from_city.lower() and row["to_city"].lower() == to_city.lower():
                    # Map class to price column
                    class_map = {
                        "SL": "SL_price_inr",
                        "3AC": "3AC_price_inr",
                        "2AC": "2AC_price_inr",
                        "1AC": "1AC_price_inr"
                    }
                    
                    price_column = class_map.get(travel_class, "3AC_price_inr")
                    price = int(row[price_column])
                    
                    matching_trains.append({
                        "train_no": row["train_no"],
                        "train_name": row["train_name"],
                        "from": row["from_city"],
                        "to": row["to_city"],
                        "duration": row["duration_hours"],
                        "selected_price": price,
                        "selected_class": travel_class
                    })
    except Exception as e:
        print(f"Error loading trains: {e}")
        return []

    if not matching_trains:
        return []

    # Sort by price
    matching_trains.sort(key=lambda x: x['selected_price'])

    return matching_trains


# Test the tool
if __name__ == "__main__":
    result = search_trains("Hyderabad", "Delhi", "3AC")
    print(result)
