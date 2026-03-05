import os
from pathlib import Path

class Settings:
    APP_NAME = "TripSmart"
    VERSION = "1.0.0"
    DEBUG = False
    
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    
    FLIGHT_CSV = RAW_DATA_DIR / "Flight.csv"
    TRAIN_CSV = RAW_DATA_DIR / "Train.csv"
    HOTEL_CSV = RAW_DATA_DIR / "Hotel.csv"
    LANDMARK_CSV = RAW_DATA_DIR / "Landmark.csv"
    
    USER_TRIPS_JSON = PROCESSED_DATA_DIR / "user_trips.json"
    EXPENSES_JSON = PROCESSED_DATA_DIR / "expenses.json"
    
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    
    CACHE_TTL = 3600
    
    PAGE_CONFIG = {
        "page_title": "TripSmart",
        "page_icon": "🛫",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
    
    HIDE_STREAMLIT_STYLE = """
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        </style>
    """

settings = Settings()
