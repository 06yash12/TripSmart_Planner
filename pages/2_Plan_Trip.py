import streamlit as st
import logging
from config.settings import settings
from config.theme import THEME
from components.layout import LayoutHelpers
from components.forms import FormComponents
from components.cards import CardComponents
from components.navigation import Navigation
from services.trip_planner import TripPlannerService
from utils.session import SessionManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

st.set_page_config(**settings.PAGE_CONFIG)
SessionManager.init_session()

st.markdown(settings.HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

with st.sidebar:
    Navigation.render(current_page="Plan Trip")

st.markdown(f"""
    <style>
    .stApp {{
        background: {THEME['background_gradient']};
    }}
    .card {{
        background: white;
        padding: 15px;
        border-radius: {THEME['border_radius']};
        box-shadow: {THEME['card_shadow']};
        margin: 10px 0;
    }}
    .info-box {{
        background: #ffffff;
        padding: 15px;
        border-radius: {THEME['border_radius_sm']};
        border-left: 4px solid {THEME['info_color']};
        margin: 10px 0;
        box-shadow: {THEME['card_shadow']};
    }}
    </style>
""", unsafe_allow_html=True)

# Smaller hero section - half the height
st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px 30px; border-radius: 12px; text-align: center; 
                color: white; margin-bottom: 20px;">
        <h1 style="font-size: 1.8em; margin: 0; font-weight: 700;">Plan Your Trip</h1>
        <p style="font-size: 1em; margin: 5px 0 0 0; opacity: 0.95;">Customize your travel details and let AI create the perfect itinerary</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('<p style="color: #1a1a1a; font-weight: 700; font-size: 1.2em; margin: 10px 0 8px 0; background: rgba(255,255,255,0.9); padding: 8px 12px; border-radius: 5px; border-left: 4px solid #667eea;">Route & Duration</p>', unsafe_allow_html=True)
source, destination, days, from_date, to_date = FormComponents.route_selector()

st.markdown('<p style="color: #1a1a1a; font-weight: 700; font-size: 1.2em; margin: 10px 0 8px 0; background: rgba(255,255,255,0.9); padding: 8px 12px; border-radius: 5px; border-left: 4px solid #667eea;">Travelers & Travel Class</p>', unsafe_allow_html=True)
adults, children, transport_mode, flight_class, train_class = FormComponents.traveler_and_class_config()

col1, col2 = st.columns([3, 1])

with col1:
    plan_button = st.button("Plan My Trip", use_container_width=True, type="primary")

with col2:
    if st.button("Reset", use_container_width=True):
        SessionManager.clear_trip()
        logger.info("Trip data cleared")
        st.rerun()

if plan_button or st.session_state.trip_planned:
    with LayoutHelpers.show_loading("AI is crafting your perfect itinerary..."):
        try:
            logger.info(f"Planning trip from {source} to {destination}")
            planner = TripPlannerService()
            
            config = {
                'source': source,
                'destination': destination,
                'days': days,
                'adults': adults,
                'children': children,
                'transport_mode': transport_mode,
                'flight_class': flight_class,
                'train_class': train_class,
                'budget_type': 'moderate'
            }
            
            result = planner.plan_trip(config)
            SessionManager.save_trip(result)
            logger.info("Trip planning completed successfully")
        except Exception as e:
            logger.error(f"Error planning trip: {str(e)}")
            st.error("An error occurred while planning your trip. Please try again.")
            st.stop()
    
    LayoutHelpers.show_success("Your itinerary is ready!")
    
    st.markdown(f"""
        <div class="card" style="background: #e8f5e9; border-left: 4px solid #4caf50;">
            <h4 style="color: #2e7d32; margin: 0;">Current Selections</h4>
            <p style="color: #000000; margin: 8px 0; font-size: 0.95em;">
                <strong>Route:</strong> {source} to {destination} | 
                <strong>Travel Dates:</strong> {from_date.strftime('%d %b %Y')} to {to_date.strftime('%d %b %Y')} ({days} days) | 
                <strong>Travelers:</strong> {adults} Adults + {children} Children
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Transport Selection Section
    if transport_mode in ["Flight", "Compare Both"] and result['flights']:
        LayoutHelpers.section_header("Select Your Flight")
        
        # Create flight options for dropdown with column-aligned formatting
        flight_options = []
        for idx, flight in enumerate(result['flights']):
            total_price = flight['class_price'] * (adults + children)
            # Format with fixed widths for alignment
            airline = f"{flight['airline']:<12}"
            duration = f"{flight['duration']:<6}"
            flight_class = f"{flight['selected_class']:<15}"
            baggage = f"{flight['baggage']:<5}"
            price_per = f"Rs. {flight['class_price']:>6,}"
            total = f"Rs. {total_price:>7,}"
            
            flight_options.append(
                f"{airline} | {duration} | {flight_class} | {baggage} | {price_per} | {total} ({adults + children} persons)"
            )
        
        selected_flight_idx = st.selectbox(
            "Choose your preferred flight",
            range(len(flight_options)),
            format_func=lambda x: flight_options[x],
            key="selected_flight"
        )
        
        # Display selected flight details in table
        selected_flight = result['flights'][selected_flight_idx]
        st.markdown("""
            <style>
            .flight-table {
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }
            .flight-table th {
                background: #667eea;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }
            .flight-table td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
                color: #000;
            }
            .flight-table tr:hover {
                background: #f5f5f5;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="card">
                <table class="flight-table">
                    <tr>
                        <th>Airline</th>
                        <th>Duration</th>
                        <th>Class</th>
                        <th>Baggage</th>
                        <th>Price per Person</th>
                        <th>Total Price</th>
                    </tr>
                    <tr>
                        <td><strong>{selected_flight['airline']}</strong></td>
                        <td>{selected_flight['duration']}</td>
                        <td>{selected_flight['selected_class']}</td>
                        <td>{selected_flight['baggage']}</td>
                        <td>Rs. {selected_flight['class_price']:,}</td>
                        <td><strong style="color: #667eea; font-size: 1.2em;">Rs. {selected_flight['class_price'] * (adults + children):,}</strong></td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
    
    if transport_mode in ["Train", "Compare Both"] and result['trains']:
        LayoutHelpers.section_header("Select Your Train")
        
        # Create train options for dropdown with column-aligned formatting
        train_options = []
        for idx, train in enumerate(result['trains']):
            total_price = train['selected_price'] * (adults + children)
            # Format with fixed widths for alignment
            train_name = f"{train['train_name']:<30}"
            train_no = f"({train['train_no']})"
            duration = f"{train['duration']:>2} hrs"
            train_class = f"{train['selected_class']:<5}"
            price_per = f"Rs. {train['selected_price']:>6,}"
            total = f"Rs. {total_price:>7,}"
            
            train_options.append(
                f"{train_name} {train_no} | {duration} | {train_class} | {price_per} | {total} ({adults + children} persons)"
            )
        
        selected_train_idx = st.selectbox(
            "Choose your preferred train",
            range(len(train_options)),
            format_func=lambda x: train_options[x],
            key="selected_train"
        )
        
        # Display selected train details in table
        selected_train = result['trains'][selected_train_idx]
        st.markdown("""
            <style>
            .train-table {
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }
            .train-table th {
                background: #3b82f6;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }
            .train-table td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
                color: #000;
            }
            .train-table tr:hover {
                background: #f5f5f5;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="card">
                <table class="train-table">
                    <tr>
                        <th>Train Name</th>
                        <th>Train No</th>
                        <th>Duration</th>
                        <th>Class</th>
                        <th>Price per Person</th>
                        <th>Total Price</th>
                    </tr>
                    <tr>
                        <td><strong>{selected_train['train_name']}</strong></td>
                        <td>{selected_train['train_no']}</td>
                        <td>{selected_train['duration']} hrs</td>
                        <td>{selected_train['selected_class']}</td>
                        <td>Rs. {selected_train['selected_price']:,}</td>
                        <td><strong style="color: #3b82f6; font-size: 1.2em;">Rs. {selected_train['selected_price'] * (adults + children):,}</strong></td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
    
    if result['hotels']:
        LayoutHelpers.section_header("Recommended Hotels")
        
        # Create hotel options for dropdown with column-aligned formatting
        hotel_options = []
        for idx, hotel in enumerate(result['hotels']):
            # Format with fixed widths for better alignment
            hotel_name = f"{hotel['name']:<30}"
            rating = f"★{hotel['rating']:<4}"
            location = f"{hotel['nearest_landmark']:<18}"
            price_per_night = f"Rs. {hotel['price_per_night']:>7,}"
            total = f"Rs. {hotel['total_price']:>8,}"
            rooms_days = f"({hotel['num_rooms']} room × {hotel['num_days']} days)"
            
            hotel_options.append(
                f"{hotel_name} | {rating} | {location} | {price_per_night}/night | {total} {rooms_days}"
            )
        
        selected_hotel_idx = st.selectbox(
            "Choose your preferred hotel",
            range(len(hotel_options)),
            format_func=lambda x: hotel_options[x],
            key="selected_hotel"
        )
        
        # Display selected hotel details in card
        selected_hotel = result['hotels'][selected_hotel_idx]
        amenities_list = selected_hotel['amenities'].split(';')[:4]
        amenities_html = '<br>'.join([f'✓ {a.strip()}' for a in amenities_list])
        
        st.markdown(f"""
            <div class="card" style="padding: 20px; margin: 15px 0; border: 2px solid #667eea;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <h3 style="color: #667eea; margin: 0 0 10px 0;">{selected_hotel['name']}</h3>
                        <p style="color: #000; font-size: 0.95em; margin: 5px 0;">
                            <strong>Rating:</strong> ★ {selected_hotel['rating']} | 
                            <strong>Location:</strong> {selected_hotel['nearest_landmark']}
                        </p>
                        <div style="margin: 15px 0; color: #000; font-size: 0.9em;">
                            <strong>Amenities:</strong><br>
                            {amenities_html}
                        </div>
                    </div>
                    <div style="text-align: right; min-width: 200px;">
                        <p style="color: #667eea; font-size: 1.5em; font-weight: 700; margin: 0;">
                            Rs. {selected_hotel['price_per_night']:,}
                        </p>
                        <p style="color: #000; font-size: 0.85em; margin: 5px 0;">per night</p>
                        <div style="margin-top: 15px; padding-top: 15px; border-top: 2px solid #eee;">
                            <p style="color: #000; font-size: 1em; margin: 5px 0;">
                                <strong>Total Cost:</strong>
                            </p>
                            <p style="color: #667eea; font-size: 1.3em; font-weight: 700; margin: 0;">
                                Rs. {selected_hotel['total_price']:,}
                            </p>
                            <p style="color: #000; font-size: 0.8em; margin: 5px 0;">
                                {selected_hotel['num_rooms']} room(s) × {selected_hotel['num_days']} days
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    if result['attractions']:
        # Colored section header for Top Attractions
        st.markdown("""
            <div style="text-align: center; margin: 20px 0 15px 0; background: rgba(255,255,255,0.95); padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h2 style="color: #1a1a1a; font-size: 1.8em; font-weight: 700; margin-bottom: 5px;">
                    🎯 Top Attractions
                </h2>
                <p style="color: #555; font-size: 0.9em; margin: 0;">Explore the best places to visit</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Display attractions in 3x3 grid
        for row in range(3):
            cols = st.columns(3)
            for col_idx in range(3):
                attraction_idx = row * 3 + col_idx
                if attraction_idx < len(result['attractions']):
                    with cols[col_idx]:
                        CardComponents.attraction_card(result['attractions'][attraction_idx])
    
    if result['budget']:
        LayoutHelpers.section_header("Budget Breakdown")
        budget = result['budget']
        
        # Create two-column layout: Detailed breakdown on left, Summary on right
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.markdown("""
                <h3 style="color: #1a1a1a; margin-bottom: 15px; font-weight: 700; background: rgba(255,255,255,0.9); padding: 10px; border-radius: 5px; border-left: 4px solid #667eea;">Detailed Breakdown</h3>
            """, unsafe_allow_html=True)
            
            # Detailed breakdown table
            for category, amount in budget['breakdown'].items():
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; padding: 12px; 
                                border-bottom: 1px solid #ddd; background: white; margin: 2px 0; border-radius: 5px;">
                        <span style="color: #000; font-weight: 500;">{category}</span>
                        <strong style="color: #000;">Rs. {amount:,}</strong>
                    </div>
                """, unsafe_allow_html=True)
        
        with col_right:
            st.markdown("""
                <h3 style="color: #1a1a1a; margin-bottom: 15px; font-weight: 700; background: rgba(255,255,255,0.9); padding: 10px; border-radius: 5px; border-left: 4px solid #667eea;">Summary</h3>
            """, unsafe_allow_html=True)
            
            # Summary metrics with dark text
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                    <p style="color: #000; font-size: 0.9em; margin: 0; font-weight: 600;">Total Cost</p>
                    <p style="color: #000; font-size: 2em; font-weight: 700; margin: 5px 0;">Rs. {budget['total_cost']:,}</p>
                </div>
                
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 20px; border-radius: 10px;">
                    <p style="color: #000; font-size: 0.9em; margin: 0; font-weight: 600;">Per Day</p>
                    <p style="color: #000; font-size: 2em; font-weight: 700; margin: 5px 0;">Rs. {budget['cost_per_day']:,}</p>
                </div>
            """, unsafe_allow_html=True)
