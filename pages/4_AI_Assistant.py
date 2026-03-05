import streamlit as st
import logging
from config.settings import settings
from config.theme import THEME
from components.layout import LayoutHelpers
from components.navigation import Navigation
from services.gemini_service import GeminiService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

st.set_page_config(**settings.PAGE_CONFIG)

# Initialize Gemini service
if 'gemini_service' not in st.session_state:
    st.session_state.gemini_service = GeminiService()

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI travel assistant powered by Google Gemini. How can I help you plan your perfect trip today?"}
    ]

st.markdown(settings.HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

with st.sidebar:
    Navigation.render(current_page="AI Assistant")

st.markdown(f"""
    <style>
    .stApp {{
        background: {THEME['background_gradient']};
    }}
    .chat-message {{
        background: white;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #333;
    }}
    .user-message {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }}
    .user-message strong {{
        color: white;
    }}
    .ai-message {{
        background: white;
        margin-right: 20%;
        color: #333;
    }}
    .ai-message strong {{
        color: #333;
    }}
    /* Make all buttons same height */
    .stButton > button {{
        height: 38px !important;
        padding: 0 16px !important;
        min-height: 38px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Smaller custom hero section
st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px 30px; border-radius: 12px; text-align: center; 
                color: white; margin-bottom: 20px;">
        <h1 style="font-size: 1.8em; margin: 0; font-weight: 700;">AI Travel Assistant</h1>
        <p style="font-size: 1em; margin: 5px 0 0 0; opacity: 0.95;">Ask me anything about your travel plans</p>
    </div>
""", unsafe_allow_html=True)

col_title, col_spacer, col_status = st.columns([1, 3, 2])

with col_title:
    st.markdown("""
        <div style="margin-top: 8px;">
            <h3 style="margin: 0; color: white;">Chat with AI</h3>
        </div>
    """, unsafe_allow_html=True)

with col_spacer:
    pass

with col_status:
    # Show API status on extreme right with Gemini logo
    if st.session_state.gemini_service.is_available():
        st.markdown("""
            <div style="background: #d4edda; color: #155724; padding: 8px 16px; border-radius: 8px; 
                        margin-top: 8px; font-size: 0.9em; display: flex; align-items: center; 
                        justify-content: flex-end; gap: 8px; float: right;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" fill="url(#gemini-gradient)"/>
                    <path d="M12 6L8 12L12 18L16 12L12 6Z" fill="white"/>
                    <defs>
                        <linearGradient id="gemini-gradient" x1="0" y1="0" x2="24" y2="24">
                            <stop offset="0%" stop-color="#4285f4"/>
                            <stop offset="50%" stop-color="#9b72cb"/>
                            <stop offset="100%" stop-color="#d96570"/>
                        </linearGradient>
                    </defs>
                </svg>
                <span style="font-weight: 600;">Gemini AI Connected</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: #f8d7da; color: #721c24; padding: 8px 16px; border-radius: 8px; 
                        margin-top: 8px; font-size: 0.9em; display: flex; align-items: center; 
                        justify-content: flex-end; gap: 8px; float: right;">
                <span>⚠️</span>
                <span style="font-weight: 600;">Not Connected</span>
            </div>
        """, unsafe_allow_html=True)

col_label, col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 2, 2])

with col_label:
    st.markdown("""
        <div style="background: white; padding: 8px 16px; border-radius: 6px; 
                    border: 1px solid rgba(49, 51, 63, 0.2); height: 38px; 
                    display: flex; align-items: center; justify-content: center;
                    font-size: 0.875rem; font-weight: 600; color: #333;
                    margin-top: 6px;">
            Quick Questions:
        </div>
    """, unsafe_allow_html=True)

with col_btn1:
    if st.button("Best time to visit Goa?", use_container_width=True):
        logger.info("Quick question: Best time to visit Goa")
        user_msg = "What's the best time to visit Goa?"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        
        with st.spinner("Thinking..."):
            response = st.session_state.gemini_service.get_travel_response(
                user_msg, 
                st.session_state.messages[:-1]
            )
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col_btn2:
    if st.button("What to pack for Jaipur?", use_container_width=True):
        logger.info("Quick question: What to pack for Jaipur")
        user_msg = "What should I pack for Jaipur?"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        
        with st.spinner("Thinking..."):
            response = st.session_state.gemini_service.get_travel_response(
                user_msg, 
                st.session_state.messages[:-1]
            )
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col_btn3:
    if st.button("Budget tips for Delhi?", use_container_width=True):
        logger.info("Quick question: Budget tips for Delhi")
        user_msg = "Give me budget tips for Delhi"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        
        with st.spinner("Thinking..."):
            response = st.session_state.gemini_service.get_travel_response(
                user_msg, 
                st.session_state.messages[:-1]
            )
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Display chat messages directly below
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <strong style="color: white;">You:</strong><br>
                <span style="color: white;">{message["content"]}</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message ai-message">
                <strong style="color: #333;">✨ Gemini AI:</strong><br>
                <span style="color: #333;">{message["content"]}</span>
            </div>
        """, unsafe_allow_html=True)

# Gemini badge and Clear Chat button in one row
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin: 20px 0 10px 0;">
            <div style="background: linear-gradient(135deg, #4285f4 0%, #9b72cb 50%, #d96570 100%); 
                        padding: 8px 16px; border-radius: 20px; display: inline-flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.2em;">✨</span>
                <span style="color: white; font-weight: 600; font-size: 0.9em;">Powered by Google Gemini</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    if len(st.session_state.messages) > 1:
        if st.button("Clear Chat", use_container_width=True):
            logger.info("Chat cleared")
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your AI travel assistant powered by Google Gemini. How can I help you plan your perfect trip today?"}
            ]
            st.rerun()

# Chat input at the bottom
user_input = st.chat_input("Ask me anything about travel...")

if user_input:
    logger.info(f"User query: {user_input}")
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("✨ Gemini is thinking..."):
        response = st.session_state.gemini_service.get_travel_response(
            user_input, 
            st.session_state.messages[:-1]
        )
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

