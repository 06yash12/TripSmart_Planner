import streamlit as st

class Navigation:
    @staticmethod
    def render(current_page="Home"):
        """Render professional navigation with active page highlighting"""
        
        # Add custom CSS for consistent button styling
        st.markdown("""
            <style>
            /* Lock button container position */
            div[data-testid="stButton"] {
                transform: none !important;
                position: relative !important;
                margin: 5px 0 !important;
            }
            
            /* Remove ALL button animations and movements */
            div[data-testid="stButton"] > button {
                width: 100%;
                border-radius: 8px;
                padding: 12px !important;
                font-size: 1em;
                font-weight: 500;
                background: transparent !important;
                color: #e0e0e0 !important;
                border: 1px solid #444 !important;
                transition: background 0.2s ease, border-color 0.2s ease !important;
                transform: translate(0, 0) !important;
                position: relative !important;
                top: 0 !important;
                left: 0 !important;
                bottom: 0 !important;
                right: 0 !important;
                box-shadow: none !important;
                margin: 0 !important;
                vertical-align: middle !important;
            }
            
            div[data-testid="stButton"] > button:hover {
                background: rgba(102, 126, 234, 0.15) !important;
                border-color: #667eea !important;
                transform: translate(0, 0) !important;
                top: 0 !important;
                box-shadow: none !important;
                padding: 12px !important;
            }
            
            div[data-testid="stButton"] > button:active {
                transform: translate(0, 0) !important;
                top: 0 !important;
                box-shadow: none !important;
                background: rgba(102, 126, 234, 0.25) !important;
                padding: 12px !important;
            }
            
            div[data-testid="stButton"] > button:focus {
                box-shadow: none !important;
                transform: translate(0, 0) !important;
                top: 0 !important;
                outline: none !important;
                padding: 12px !important;
            }
            
            div[data-testid="stButton"] > button:focus:not(:focus-visible) {
                box-shadow: none !important;
                outline: none !important;
            }
            
            /* Active page styling with consistent spacing */
            .nav-active {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px;
                border-radius: 8px;
                text-align: center;
                font-weight: 600;
                font-size: 1em;
                margin: 5px 0;
                border: none;
                display: block;
            }
            </style>
        """, unsafe_allow_html=True)
        
        pages = {
            "Home": "app.py",
            "Plan Trip": "pages/2_Plan_Trip.py",
            "Landmark Finder": "pages/3_Landmark_Finder.py",
            "AI Assistant": "pages/4_AI_Assistant.py",
            "About": "pages/5_About.py"
        }
        
        st.markdown("### Navigation")
        
        for page_name, page_path in pages.items():
            is_active = (current_page == page_name)
            
            if is_active:
                # Show active page as styled div (not clickable)
                st.markdown(f"""
                    <div class="nav-active">
                        {page_name}
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Show inactive page as button
                if st.button(
                    page_name, 
                    use_container_width=True, 
                    key=f"nav_{page_name.lower().replace(' ', '_')}"
                ):
                    st.switch_page(page_path)
        
        st.markdown("---")
        
        # User Info
        st.markdown("### User Profile")
        st.markdown("""
            <div style="background: #1e1e1e; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
                <p style="color: #e0e0e0; margin: 0; font-size: 0.9em;">
                    <strong>Demo User</strong><br>
                    <span style="color: #999;">demo@travel.com</span>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Pro Tips
        st.markdown("### Pro Tips")
        st.info("Compare transport options")
        st.success("Book early for savings")
        st.warning("Check weather forecasts")


