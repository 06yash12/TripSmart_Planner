import streamlit as st
from datetime import datetime, timedelta
from config.constants import CITIES, FLIGHT_CLASSES, TRAIN_CLASSES, BUDGET_TYPES, TRANSPORT_MODES

class FormComponents:
    @staticmethod
    def route_selector():
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        
        with col1:
            source = st.selectbox("From", options=CITIES, key="source_city", label_visibility="collapsed")
            st.caption("From (Source City)")
        
        with col2:
            destination = st.selectbox("To", options=CITIES, index=1, key="dest_city", label_visibility="collapsed")
            st.caption("To (Destination City)")
        
        with col3:
            from_date = st.date_input("From Date", value=datetime.now(), key="from_date", label_visibility="collapsed")
            st.caption("From Date")
        
        with col4:
            to_date = st.date_input("To Date", value=datetime.now() + timedelta(days=3), key="to_date", label_visibility="collapsed")
            st.caption("To Date")
        
        # Calculate days
        if to_date >= from_date:
            days = (to_date - from_date).days + 1
        else:
            days = 1
            st.warning("To Date must be after From Date")
        
        return source, destination, days, from_date, to_date
    
    @staticmethod
    def traveler_config():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            adults = st.number_input("Adults", min_value=1, max_value=10, value=2, key="num_adults", label_visibility="collapsed")
            st.caption("Adults")
        
        with col2:
            children = st.number_input("Children", min_value=0, max_value=10, value=0, key="num_children", label_visibility="collapsed")
            st.caption("Children")
        
        with col3:
            transport = st.selectbox("Transport", TRANSPORT_MODES, key="transport_mode", label_visibility="collapsed")
            st.caption("Travel Mode")
        
        return adults, children, transport
    
    @staticmethod
    def traveler_and_class_config():
        """Combined traveler config with flight/train class in one row"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            adults = st.number_input("Adults", min_value=1, max_value=10, value=2, key="num_adults", label_visibility="collapsed")
            st.caption("Adults")
        
        with col2:
            children = st.number_input("Children", min_value=0, max_value=10, value=0, key="num_children", label_visibility="collapsed")
            st.caption("Children")
        
        with col3:
            transport = st.selectbox("Transport", TRANSPORT_MODES, key="transport_mode", label_visibility="collapsed")
            st.caption("Travel Mode")
        
        with col4:
            if transport == "Flight":
                flight_class = st.selectbox("Flight Class", FLIGHT_CLASSES, key="flight_class", label_visibility="collapsed")
                st.caption("Flight Class")
                train_class = "3AC"
            elif transport == "Train":
                train_class = st.selectbox("Train Class", TRAIN_CLASSES, index=1, key="train_class", label_visibility="collapsed")
                st.caption("Train Class")
                flight_class = "Economy"
            else:  # Compare Both
                flight_class = st.selectbox("Flight Class", FLIGHT_CLASSES, key="flight_class", label_visibility="collapsed")
                st.caption("Flight Class")
                train_class = "3AC"
        
        return adults, children, transport, flight_class, train_class
    
    @staticmethod
    def class_selector(transport_mode):
        flight_class = None
        train_class = None
        
        if transport_mode in ["Flight", "Compare Both"]:
            cols = []
            if transport_mode in ["Flight", "Compare Both"]:
                cols.append(1)
            if transport_mode in ["Train", "Compare Both"]:
                cols.append(1)
            
            col_widgets = st.columns(len(cols))
            col_idx = 0
            
            if transport_mode in ["Flight", "Compare Both"]:
                with col_widgets[col_idx]:
                    flight_class = st.selectbox("Flight Class", FLIGHT_CLASSES, key="flight_class", label_visibility="collapsed")
                    st.caption("Flight Class")
                col_idx += 1
            
            if transport_mode in ["Train", "Compare Both"]:
                with col_widgets[col_idx]:
                    train_class = st.selectbox("Train Class", TRAIN_CLASSES, index=1, key="train_class", label_visibility="collapsed")
                    st.caption("Train Class")
        
        return flight_class or "Economy", train_class or "3AC"
