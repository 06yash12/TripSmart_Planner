import streamlit as st

class SessionManager:
    @staticmethod
    def init_session():
        if 'trip_data' not in st.session_state:
            st.session_state.trip_data = {}
        if 'user_id' not in st.session_state:
            st.session_state.user_id = 'demo_user'
        if 'trip_planned' not in st.session_state:
            st.session_state.trip_planned = False
    
    @staticmethod
    def save_trip(trip_data):
        st.session_state.trip_data = trip_data
        st.session_state.trip_planned = True
    
    @staticmethod
    def clear_trip():
        st.session_state.trip_data = {}
        st.session_state.trip_planned = False
    
    @staticmethod
    def get_trip():
        return st.session_state.get('trip_data', {})
