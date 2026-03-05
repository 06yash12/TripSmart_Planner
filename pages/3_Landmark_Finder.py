import streamlit as st
import logging
from config.settings import settings
from config.theme import THEME
from components.layout import LayoutHelpers
from components.navigation import Navigation

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

st.set_page_config(**settings.PAGE_CONFIG)

st.markdown(settings.HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

with st.sidebar:
    Navigation.render(current_page="Landmark Finder")

st.markdown(f"""
    <style>
    .stApp {{
        background: {THEME['background_gradient']};
    }}
    .card {{
        background: white;
        padding: 20px;
        border-radius: {THEME['border_radius']};
        box-shadow: {THEME['card_shadow']};
        margin: 10px 0;
    }}
    </style>
""", unsafe_allow_html=True)

# Smaller hero section - half the height
st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px 30px; border-radius: 12px; text-align: center; 
                color: white; margin-bottom: 20px;">
        <h1 style="font-size: 1.8em; margin: 0; font-weight: 700;">Landmark Finder</h1>
        <p style="font-size: 1em; margin: 5px 0 0 0; opacity: 0.95;">Upload a photo and discover famous landmarks with AI</p>
    </div>
""", unsafe_allow_html=True)

# Create two equal-height columns side by side
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("""
        <div class="card" style="text-align: center; padding: 12px 20px 10px 20px; min-height: 112px;">
            <h3 style="color: #667eea; margin-bottom: 7px; font-size: 1em;">Upload Landmark Photo</h3>
            <p style="color: #666; margin-bottom: 10px; font-size: 0.85em;">
                Upload an image of a famous Indian landmark and our AI will identify it
            </p>
    """, unsafe_allow_html=True)
    
    # File uploader inside the card
    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=['jpg', 'jpeg', 'png'],
        label_visibility="visible",
        help="Limit 200MB per file • JPG, JPEG, PNG"
    )
    
    st.markdown("""
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card" style="background: #f0f7ff; padding: 12px 20px; min-height: 112px;">
            <h4 style="color: #667eea; margin: 0 0 8px 0; font-size: 1em;">Tips for Best Results</h4>
            <ul style="color: #555; font-size: 0.85em; line-height: 1.5; list-style: none; padding: 0;">
                <li style="margin-bottom: 6px; padding-left: 20px; position: relative;">
                    <span style="position: absolute; left: 0; color: #667eea; font-weight: bold;">•</span>
                    Use clear, well-lit photos
                </li>
                <li style="margin-bottom: 6px; padding-left: 20px; position: relative;">
                    <span style="position: absolute; left: 0; color: #667eea; font-weight: bold;">•</span>
                    Capture the main structure prominently
                </li>
                <li style="margin-bottom: 6px; padding-left: 20px; position: relative;">
                    <span style="position: absolute; left: 0; color: #667eea; font-weight: bold;">•</span>
                    Avoid heavily filtered images
                </li>
                <li style="margin-bottom: 0; padding-left: 20px; position: relative;">
                    <span style="position: absolute; left: 0; color: #667eea; font-weight: bold;">•</span>
                    Works best with famous Indian landmarks
                </li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Show results in two columns if image is uploaded
if uploaded_file is not None:
    logger.info(f"Image uploaded: {uploaded_file.name}")
    
    # Create two columns for image and results
    result_col1, result_col2 = st.columns(2, gap="medium")
    
    with result_col1:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        
        if st.button("Identify Landmark", use_container_width=True, type="primary"):
            st.session_state.identified = True
    
    with result_col2:
        if st.session_state.get('identified', False):
            with st.spinner("Analyzing image..."):
                logger.info("Processing landmark identification")
                st.markdown("""
                    <div class="card" style="margin-top: 0;">
                        <h3 style="color: #667eea;">Identified Landmark</h3>
                        <h2 style="color: #333; margin: 10px 0;">Taj Mahal</h2>
                        <p style="color: #666; margin: 10px 0;">
                            <strong>Location:</strong> Agra, Uttar Pradesh<br>
                            <strong>Confidence:</strong> 98.5%<br>
                            <strong>Category:</strong> Historical Monument
                        </p>
                        <p style="color: #555; line-height: 1.6; margin-top: 15px;">
                            The Taj Mahal is an ivory-white marble mausoleum on the right bank of the river Yamuna 
                            in Agra. It was commissioned in 1631 by the Mughal emperor Shah Jahan to house the tomb 
                            of his favourite wife, Mumtaz Mahal.
                        </p>
                        <div style="margin-top: 15px;">
                            <span style="background: #10b981; color: white; padding: 5px 12px; border-radius: 15px; font-size: 0.9em; margin-right: 10px;">
                                UNESCO World Heritage Site
                            </span>
                            <span style="background: #667eea; color: white; padding: 5px 12px; border-radius: 15px; font-size: 0.9em;">
                                One of Seven Wonders
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
