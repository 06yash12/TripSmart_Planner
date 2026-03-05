import streamlit as st
from config.theme import COLORS

class CardComponents:
    @staticmethod
    def feature_card(title, description, height="110px"):
        st.markdown(f"""
            <div class="card" style="height: {height}; display: flex; flex-direction: column; justify-content: center; padding: 15px;">
                <div>
                    <h3 style="color: {COLORS['primary']['main']}; font-weight: 600; font-size: 1em; margin: 0 0 8px 0;">{title}</h3>
                    <p style="color: #000; font-size: 0.85em; line-height: 1.4; margin: 0;">{description}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def metric_card(label, value, delta=None, color="primary"):
        color_value = COLORS.get(color, COLORS['primary'])['main']
        delta_html = f'<p style="color: {COLORS["success"]["main"]}; font-size: 0.9em; margin: 5px 0 0 0;">{delta}</p>' if delta else ''
        
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, {COLORS['primary']['main']} 0%, {COLORS['secondary']['main']} 100%); color: white; padding: 15px; border-radius: 10px; text-align: center;">
                <p style="font-size: 0.9em; margin: 0; opacity: 0.9;">{label}</p>
                <p style="font-size: 1.8em; font-weight: 700; margin: 8px 0;">{value}</p>
                {delta_html}
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def hotel_card(hotel, selectable=False, hotel_index=None):
        amenities_list = hotel['amenities'].split(';')[:3]
        amenities_html = ' • '.join([f'<span style="color: #000; font-size: 0.85em;">{a.strip()}</span>' for a in amenities_list])
        
        st.markdown(f"""
            <div class="card" style="padding: 15px; margin: 10px 0;">
                <h4 style="color: {COLORS['primary']['main']}; margin: 0 0 8px 0;">{hotel['name']}</h4>
                <p style="color: #000; font-size: 0.9em; margin: 5px 0;">
                    Rating: {hotel['rating']} | Location: {hotel['nearest_landmark']}
                </p>
                <p style="color: #000; font-size: 0.85em; margin: 8px 0;">
                    {amenities_html}
                </p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                    <div>
                        <p style="color: {COLORS['primary']['main']}; font-size: 1.3em; font-weight: 700; margin: 0;">
                            Rs. {hotel['price_per_night']:,}
                        </p>
                        <p style="color: #000; font-size: 0.8em; margin: 0;">per night</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="color: #000; font-size: 0.9em; margin: 0;">
                            Total: Rs. {hotel['total_price']:,}
                        </p>
                        <p style="color: #000; font-size: 0.8em; margin: 0;">
                            {hotel['num_rooms']} room(s) • {hotel['num_days']} days
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if selectable and hotel_index is not None:
            return st.checkbox(f"Select {hotel['name']}", key=f"hotel_select_{hotel_index}", value=False)
    
    @staticmethod
    def attraction_card(place):
        st.markdown(f"""
            <div class="card" style="padding: 15px; margin: 8px 0; text-align: center;">
                <h4 style="color: {COLORS['primary']['main']}; font-size: 1.1em; margin: 0 0 8px 0; font-weight: 600;">{place['name']}</h4>
                <p style="color: #000; font-size: 0.9em; margin: 6px 0; font-weight: 500;">
                    Rating: {place['rating']} | Entry: Rs. {place['entry_fee']}
                </p>
                <p style="color: #000; font-size: 0.85em; margin: 8px 0; line-height: 1.5;">
                    {place['description']}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    
    @staticmethod
    def transport_comparison_card(flight, train):
        savings = (flight['class_price'] - train['selected_price']) if flight and train else 0
        
        html = f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0;">
        """
        
        if flight:
            html += f"""
            <div class="card" style="padding: 15px; border: 2px solid {COLORS['primary']['main']};">
                <h3 style="color: {COLORS['primary']['main']}; font-size: 1.1em; margin: 0 0 10px 0;">Flight</h3>
                <p style="color: #000; font-size: 0.95em; margin: 5px 0;">
                    <strong>{flight['airline']}</strong><br>
                    Duration: {flight['duration']}<br>
                    Class: {flight['selected_class']}<br>
                    Baggage: {flight['baggage']}
                </p>
                <p style="color: {COLORS['primary']['main']}; font-size: 1.5em; font-weight: 700; margin: 10px 0 0 0;">
                    Rs. {flight['class_price']:,}
                </p>
            </div>
            """
        
        if train:
            savings_badge = f'<span style="background: {COLORS["success"]["main"]}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8em;">Save Rs. {savings:,}</span>' if savings > 0 else ''
            html += f"""
            <div class="card" style="padding: 15px; border: 2px solid {COLORS['info']['main']};">
                <h3 style="color: {COLORS['info']['main']}; font-size: 1.1em; margin: 0 0 10px 0;">Train</h3>
                {savings_badge}
                <p style="color: #000; font-size: 0.95em; margin: 5px 0;">
                    <strong>{train['train_name']}</strong><br>
                    Duration: {train['duration']} hrs<br>
                    Class: {train['selected_class']}<br>
                    Train No: {train['train_no']}
                </p>
                <p style="color: {COLORS['info']['main']}; font-size: 1.5em; font-weight: 700; margin: 10px 0 0 0;">
                    Rs. {train['selected_price']:,}
                </p>
            </div>
            """
        
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
