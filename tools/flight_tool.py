import csv
import os

DATA_PATH = os.path.join("data", "Flight.csv")

def search_flights(from_city, to_city, flight_class="Economy"):
    """
    Search for flights matching source and destination
    and return the cheapest option for the selected class.
    """
    matching_flights = []
    
    try:
        with open(DATA_PATH, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["from_city"].lower() == from_city.lower() and row["to_city"].lower() == to_city.lower():
                    # Map class to price column
                    if flight_class == "Economy":
                        price = int(row["economy_price_inr"])
                        baggage = "15kg"
                    elif flight_class == "Premium Economy":
                        price = int(row["premium_economy_price_inr"])
                        baggage = "20kg"
                    elif flight_class == "Business":
                        price = int(row["business_price_inr"])
                        baggage = "30kg"
                    elif flight_class == "First Class":
                        price = int(row["first_class_price_inr"])
                        baggage = "40kg"
                    else:
                        price = int(row["economy_price_inr"])
                        baggage = "15kg"
                    
                    matching_flights.append({
                        "from": row["from_city"],
                        "to": row["to_city"],
                        "airline": row["airline_name"],
                        "duration": row["duration_hours_avg"],
                        "class_price": price,
                        "selected_class": flight_class,
                        "baggage": baggage
                    })
    except Exception as e:
        print(f"Error loading flights: {e}")
        return {"message": "Error loading flights"}

    if not matching_flights:
        return {"message": "No flights found"}

    # Choose cheapest flight for the selected class
    cheapest_flight = min(matching_flights, key=lambda x: x["class_price"])

    return cheapest_flight


# Test the tool
if __name__ == "__main__":
    result = search_flights("Hyderabad", "Delhi", "Business")
    print(result)

