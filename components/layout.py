import streamlit as st
from contextlib import contextmanager

class LayoutHelpers:
    @staticmethod
    @contextmanager
    def show_loading(message="Processing..."):
        with st.spinner(message):
            yield
    
    @staticmethod
    def show_success(message):
        st.success(message)
    
    @staticmethod
    def show_error(message):
        st.error(message)
    
    @staticmethod
    def show_info(message):
        st.info(message)
    
    @staticmethod
    def show_warning(message):
        st.warning(message)
    
    @staticmethod
    def section_header(title):
        st.markdown(f"""
            <h2 style="color: #1a1a1a; font-size: 1.5em; font-weight: 700; margin: 20px 0 15px 0; 
                       padding: 12px 15px; background: rgba(255,255,255,0.95); border-radius: 8px; 
                       border-left: 5px solid #667eea; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                {title}
            </h2>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def hero_section(title, subtitle, show_button=False):
        st.markdown(f"""
            <div class="main-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 12px; text-align: center; color: white; margin-bottom: 20px;">
                <h1 style="font-size: 2.5em; margin: 0; font-weight: 700;">{title}</h1>
                <p style="font-size: 1.1em; margin: 10px 0 0 0; opacity: 0.95;">{subtitle}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if show_button:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Plan My Trip", use_container_width=True, type="primary"):
                    st.switch_page("pages/2_Plan_Trip.py")
