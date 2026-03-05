import streamlit as st
from config.settings import settings
from config.theme import THEME
from components.layout import LayoutHelpers
from components.cards import CardComponents
from components.navigation import Navigation
from utils.session import SessionManager

st.set_page_config(**settings.PAGE_CONFIG)
SessionManager.init_session()

st.markdown(settings.HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

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
        transition: transform 0.3s ease;
        color: #333;
    }}
    
    .card h1, .card h2, .card h3, .card h4, .card h5, .card h6 {{
        color: #333;
    }}
    
    .card p, .card li, .card span {{
        color: #333;
    }}
    
    .card:hover {{
        transform: translateY(-3px);
        box-shadow: {THEME['hover_shadow']};
    }}
    
    .main-header {{
        background: {THEME['background_gradient']};
        padding: 30px;
        border-radius: {THEME['border_radius']};
        text-align: center;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }}
    
    .main-header h1, .main-header h2, .main-header p {{
        color: white !important;
    }}
    
    .metric-card {{
        background: {THEME['background_gradient']};
        color: white;
        padding: 15px;
        border-radius: {THEME['border_radius_sm']};
        text-align: center;
        margin: 8px 0;
    }}
    
    .metric-card * {{
        color: white !important;
    }}
    
    .info-box {{
        background: #ffffff;
        padding: 15px;
        border-radius: {THEME['border_radius_sm']};
        border-left: 4px solid {THEME['info_color']};
        margin: 10px 0;
        box-shadow: {THEME['card_shadow']};
    }}
    
    .info-box h1, .info-box h2, .info-box h3, .info-box h4, .info-box h5, .info-box h6 {{
        color: #333 !important;
    }}
    
    .info-box p, .info-box li, .info-box span {{
        color: #333 !important;
    }}
    
    .stButton>button {{
        background: {THEME['background_gradient']};
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 1.1em;
        font-weight: 600;
        border-radius: {THEME['border_radius_sm']};
        width: 100%;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: {THEME['hover_shadow']};
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    Navigation.render(current_page="Home")

# Welcome Header - Compact and at the top
st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px 30px; border-radius: 12px; text-align: center; 
                color: white; margin-bottom: 20px;">
        <h1 style="font-size: 1.8em; margin: 0; font-weight: 700; color: white !important;">Welcome To TripSmart</h1>
        <p style="font-size: 1em; margin: 5px 0 0 0; opacity: 0.95; color: white !important;">Your Intelligent Travel Companion - Plan Perfect Trips in Seconds</p>
    </div>
""", unsafe_allow_html=True)

# Features Section - Centered
st.markdown("""
    <div style="text-align: center; margin: 20px 0 15px 0;">
        <h2 style="color: white; font-size: 1.8em; font-weight: 600;">Features</h2>
    </div>
""", unsafe_allow_html=True)

# First row of features
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
        <div class="card" style="height: 130px; display: flex; flex-direction: column; justify-content: center; padding: 18px; text-align: center;">
            <h3 style="color: #667eea; font-weight: 600; font-size: 1.05em; margin: 0 0 8px 0;">Smart Planning</h3>
            <p style="color: #555; font-size: 0.88em; line-height: 1.4; margin: 0;">TensorFlow-powered recommendations with optimal selection</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card" style="height: 130px; display: flex; flex-direction: column; justify-content: center; padding: 18px; text-align: center;">
            <h3 style="color: #667eea; font-weight: 600; font-size: 1.05em; margin: 0 0 8px 0;">ML Predictions</h3>
            <p style="color: #555; font-size: 0.88em; line-height: 1.4; margin: 0;">Machine Learning predicts best booking time and trends</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="card" style="height: 130px; display: flex; flex-direction: column; justify-content: center; padding: 18px; text-align: center;">
            <h3 style="color: #667eea; font-weight: 600; font-size: 1.05em; margin: 0 0 8px 0;">Weather Ready</h3>
            <p style="color: #555; font-size: 0.88em; line-height: 1.4; margin: 0;">Real-time weather forecasts to help you pack right</p>
        </div>
    """, unsafe_allow_html=True)

# Second row of features
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
        <div class="card" style="height: 130px; display: flex; flex-direction: column; justify-content: center; padding: 18px; text-align: center;">
            <h3 style="color: #667eea; font-weight: 600; font-size: 1.05em; margin: 0 0 8px 0;">Price Comparison</h3>
            <p style="color: #555; font-size: 0.88em; line-height: 1.4; margin: 0;">Compare flights, hotels, and trains to find best deals</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card" style="height: 130px; display: flex; flex-direction: column; justify-content: center; padding: 18px; text-align: center;">
            <h3 style="color: #667eea; font-weight: 600; font-size: 1.05em; margin: 0 0 8px 0;">Landmark Discovery</h3>
            <p style="color: #555; font-size: 0.88em; line-height: 1.4; margin: 0;">Explore top attractions and hidden gems at your destination</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="card" style="height: 130px; display: flex; flex-direction: column; justify-content: center; padding: 18px; text-align: center;">
            <h3 style="color: #667eea; font-weight: 600; font-size: 1.05em; margin: 0 0 8px 0;">24/7 AI Assistant</h3>
            <p style="color: #555; font-size: 0.88em; line-height: 1.4; margin: 0;">Get instant answers to all your travel questions anytime</p>
        </div>
    """, unsafe_allow_html=True)

# How It Works Section - Centered
st.markdown("""
    <div style="text-align: center; margin: 20px 0 15px 0;">
        <h2 style="color: white; font-size: 1.8em; font-weight: 600;">How It Works</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown("""
        <div class="card" style="padding: 12px 18px; text-align: center; min-height: 70px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 1.8em; color: #667eea; margin-bottom: 5px; font-weight: 700;">1</div>
            <p style="color: #333; font-size: 0.85em; line-height: 1.3; margin: 0;">Select source and destination cities</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card" style="padding: 12px 18px; text-align: center; min-height: 70px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 1.8em; color: #667eea; margin-bottom: 5px; font-weight: 700;">2</div>
            <p style="color: #333; font-size: 0.85em; line-height: 1.3; margin: 0;">Choose your travel dates and preferences</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="card" style="padding: 12px 18px; text-align: center; min-height: 70px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 1.8em; color: #667eea; margin-bottom: 5px; font-weight: 700;">3</div>
            <p style="color: #333; font-size: 0.85em; line-height: 1.3; margin: 0;">Get instant AI-generated itinerary</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="card" style="padding: 12px 18px; text-align: center; min-height: 70px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 1.8em; color: #667eea; margin-bottom: 5px; font-weight: 700;">4</div>
            <p style="color: #333; font-size: 0.85em; line-height: 1.3; margin: 0;">View flights, hotels, places and weather</p>
        </div>
    """, unsafe_allow_html=True)

# Recommended Destinations Section - Centered
st.markdown("""
    <div style="text-align: center; margin: 20px 0 15px 0;">
        <h2 style="color: white; font-size: 1.8em; font-weight: 600;">Recommended Destinations</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

destinations = [
    {
        "name": "Goa",
        "type": "Beach Paradise",
        "vibe": "Relaxed & Fun",
        "best_for": "Beach lovers, Nightlife, Water sports",
        "match": 95
    },
    {
        "name": "Jaipur",
        "type": "Heritage City",
        "vibe": "Cultural & Historic",
        "best_for": "History buffs, Architecture, Shopping",
        "match": 88
    },
    {
        "name": "Mumbai",
        "type": "Metropolitan",
        "vibe": "Fast-paced & Vibrant",
        "best_for": "Food lovers, Business, Entertainment",
        "match": 82
    }
]

for col, dest in zip([col1, col2, col3], destinations):
    with col:
        # Header with city name
        st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 15px;">
                <h3 style="color: white; font-weight: 700; font-size: 1.3em; margin: 0;">{dest["name"]}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Type and vibe - side by side
        st.markdown(f"""
            <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; margin-bottom: 12px; border-left: 4px solid #667eea;">
                <span style="color: #667eea; font-size: 0.85em; font-weight: 600;">{dest["type"]}</span>
                <span style="color: #888; font-size: 0.85em; font-style: italic;"> • {dest["vibe"]}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Best for - inline
        st.markdown(f"""
            <div style="background: #fff; padding: 12px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 12px;">
                <span style="color: #667eea; font-size: 0.85em; font-weight: 600;">Best for:</span>
                <span style="color: #555; font-size: 0.85em; margin-left: 6px;">{dest["best_for"]}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Match badge
        st.markdown(f"""
            <div style="text-align: center; margin-top: 15px;">
                <div style="display: inline-block; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 8px 20px; border-radius: 20px; font-size: 0.95em; font-weight: 700; box-shadow: 0 2px 6px rgba(16, 185, 129, 0.3);">
                    ✓ Match: {dest["match"]}%
                </div>
            </div>
        """, unsafe_allow_html=True)


