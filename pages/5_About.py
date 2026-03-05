import streamlit as st
from config.settings import settings
from config.theme import THEME
from components.layout import LayoutHelpers
from components.navigation import Navigation

st.set_page_config(**settings.PAGE_CONFIG)

st.markdown(settings.HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

with st.sidebar:
    Navigation.render(current_page="About")

st.markdown(f"""
    <style>
    .stApp {{
        background: {THEME['background_gradient']};
    }}
    .card {{
        background: white;
        padding: 18px;
        border-radius: {THEME['border_radius']};
        box-shadow: {THEME['card_shadow']};
        margin: 9px 0;
    }}
    </style>
""", unsafe_allow_html=True)

# Smaller hero section - half the height
st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px 30px; border-radius: 12px; text-align: center; 
                color: white; margin-bottom: 20px;">
        <h1 style="font-size: 1.8em; margin: 0; font-weight: 700;">About TripSmart</h1>
        <p style="font-size: 1em; margin: 5px 0 0 0; opacity: 0.95;">Intelligent Travel Planning Powered by Machine Learning</p>
    </div>
""", unsafe_allow_html=True)

# 2-column grid layout
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
        <div class="card">
            <h3 style="color: #667eea; margin-bottom: 13px;">🎯 Our Mission</h3>
            <p style="color: #555; line-height: 1.6; font-size: 1em;">
                We're revolutionizing travel planning by combining artificial intelligence with comprehensive 
                travel data to help you plan perfect trips in seconds.
            </p>
        </div>
        
        <div class="card">
            <h3 style="color: #667eea; margin-bottom: 13px;">✨ Key Features</h3>
            <div style="margin-top: 13px;">
                <div style="padding: 11px; background: #f0f7ff; border-radius: 8px; margin-bottom: 9px;">
                    <h4 style="color: #667eea; margin: 0 0 4px 0; font-size: 1em;">🤖 Smart Planning</h4>
                    <p style="color: #666; font-size: 0.9em; margin: 0;">
                        AI-powered recommendations for optimal travel choices
                    </p>
                </div>
                <div style="padding: 11px; background: #f0f7ff; border-radius: 8px; margin-bottom: 9px;">
                    <h4 style="color: #667eea; margin: 0 0 4px 0; font-size: 1em;">📊 ML Predictions</h4>
                    <p style="color: #666; font-size: 0.9em; margin: 0;">
                        Machine Learning predicts best booking times
                    </p>
                </div>
                <div style="padding: 11px; background: #f0f7ff; border-radius: 8px; margin-bottom: 9px;">
                    <h4 style="color: #667eea; margin: 0 0 4px 0; font-size: 1em;">💰 Budget Optimizer</h4>
                    <p style="color: #666; font-size: 0.9em; margin: 0;">
                        Intelligent budget calculation with categories
                    </p>
                </div>
                <div style="padding: 11px; background: #f0f7ff; border-radius: 8px;">
                    <h4 style="color: #667eea; margin: 0 0 4px 0; font-size: 1em;">🌤️ Weather Ready</h4>
                    <p style="color: #666; font-size: 0.9em; margin: 0;">
                        Real-time weather forecasts for planning
                    </p>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3 style="color: #667eea; margin-bottom: 13px;">🏙️ Supported Cities</h3>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 9px; margin-top: 13px;">
                <div style="background: #667eea; color: white; padding: 9px; border-radius: 8px; font-size: 0.9em; text-align: center; font-weight: 500;">
                    Hyderabad
                </div>
                <div style="background: #667eea; color: white; padding: 9px; border-radius: 8px; font-size: 0.9em; text-align: center; font-weight: 500;">
                    Delhi
                </div>
                <div style="background: #667eea; color: white; padding: 9px; border-radius: 8px; font-size: 0.9em; text-align: center; font-weight: 500;">
                    Mumbai
                </div>
                <div style="background: #667eea; color: white; padding: 9px; border-radius: 8px; font-size: 0.9em; text-align: center; font-weight: 500;">
                    Bangalore
                </div>
                <div style="background: #667eea; color: white; padding: 9px; border-radius: 8px; font-size: 0.9em; text-align: center; font-weight: 500;">
                    Chennai
                </div>
                <div style="background: #667eea; color: white; padding: 9px; border-radius: 8px; font-size: 0.9em; text-align: center; font-weight: 500;">
                    Kolkata
                </div>
                <div style="background: #667eea; color: white; padding: 9px; border-radius: 8px; font-size: 0.9em; text-align: center; font-weight: 500;">
                    Jaipur
                </div>
                <div style="background: #667eea; color: white; padding: 9px; border-radius: 8px; font-size: 0.9em; text-align: center; font-weight: 500;">
                    Goa
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card">
            <h3 style="color: #667eea; margin-bottom: 13px;">🛠️ Technology Stack</h3>
            <div style="margin-top: 13px;">
                <div style="margin: 11px 0; padding: 9px; background: #f8f9fa; border-radius: 6px;">
                    <strong style="color: #667eea;">Frontend:</strong>
                    <span style="color: #666; margin-left: 8px; font-size: 0.9em;">Streamlit 1.28+, Custom CSS3, Responsive Design</span>
                </div>
                <div style="margin: 11px 0; padding: 9px; background: #f8f9fa; border-radius: 6px;">
                    <strong style="color: #667eea;">Backend:</strong>
                    <span style="color: #666; margin-left: 8px; font-size: 0.9em;">Python 3.12, Pandas, NumPy, Logging</span>
                </div>
                <div style="margin: 11px 0; padding: 9px; background: #f8f9fa; border-radius: 6px;">
                    <strong style="color: #667eea;">AI/ML:</strong>
                    <span style="color: #666; margin-left: 8px; font-size: 0.9em;">Google Gemini 1.5 Flash, TensorFlow 2.13+, Scikit-learn</span>
                </div>
                <div style="margin: 11px 0; padding: 9px; background: #f8f9fa; border-radius: 6px;">
                    <strong style="color: #667eea;">Computer Vision:</strong>
                    <span style="color: #666; margin-left: 8px; font-size: 0.9em;">OpenCV, Pillow, Image Processing</span>
                </div>
                <div style="margin: 11px 0; padding: 9px; background: #f8f9fa; border-radius: 6px;">
                    <strong style="color: #667eea;">Data & Config:</strong>
                    <span style="color: #666; margin-left: 8px; font-size: 0.9em;">CSV, JSON, Python-dotenv, Session Management</span>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3 style="color: #667eea; margin-bottom: 13px;">📈 Project Stats</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 9px; margin-top: 13px;">
                <div style="text-align: center; padding: 6px; background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-radius: 10px;">
                    <h2 style="color: #10b981; margin: 0; font-size: 1.8em; font-weight: 700;">8</h2>
                    <p style="color: #666; font-size: 0.75em; margin: 1px 0 0 0; font-weight: 600;">Cities</p>
                </div>
                <div style="text-align: center; padding: 6px; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-radius: 10px;">
                    <h2 style="color: #2196f3; margin: 0; font-size: 1.8em; font-weight: 700;">5</h2>
                    <p style="color: #666; font-size: 0.75em; margin: 1px 0 0 0; font-weight: 600;">Pages</p>
                </div>
                <div style="text-align: center; padding: 6px; background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); border-radius: 10px;">
                    <h2 style="color: #ff9800; margin: 0; font-size: 1.8em; font-weight: 700;">15+</h2>
                    <p style="color: #666; font-size: 0.75em; margin: 1px 0 0 0; font-weight: 600;">Components</p>
                </div>
                <div style="text-align: center; padding: 6px; background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-radius: 10px;">
                    <h2 style="color: #9c27b0; margin: 0; font-size: 1.8em; font-weight: 700;">AI</h2>
                    <p style="color: #666; font-size: 0.75em; margin: 1px 0 0 0; font-weight: 600;">Powered</p>
                </div>
            </div>
        </div>
        
        <div class="card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <h3 style="color: white; margin-bottom: 13px;">📞 Contact Us</h3>
            <div style="margin-top: 13px;">
                <p style="margin: 9px 0; color: white; font-size: 0.95em;">
                    <strong>Email:</strong> support@tripsmart.com
                </p>
                <p style="margin: 9px 0; color: white; font-size: 0.95em;">
                    <strong>Website:</strong> www.tripsmart.com
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; padding: 20px; color: white; margin-top: 20px;">
        <p style="font-size: 0.9em; opacity: 0.9;">Version 1.0.0 | Built with ❤️ using Streamlit & Google Gemini</p>
    </div>
""", unsafe_allow_html=True)
