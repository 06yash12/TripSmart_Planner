import streamlit as st
from config.theme import COLORS

class MetricComponents:
    @staticmethod
    def metric_row(metrics_list):
        cols = st.columns(len(metrics_list))
        for col, metric in zip(cols, metrics_list):
            with col:
                st.metric(
                    label=metric.get('label', ''),
                    value=metric.get('value', ''),
                    delta=metric.get('delta', None)
                )
    
    @staticmethod
    def savings_badge(amount, percentage):
        return f'<span style="background: {COLORS["success"]["main"]}; color: white; padding: 5px 12px; border-radius: 15px; font-size: 0.9em;">Save Rs. {amount:,} ({percentage:.1f}%)</span>'
    
    @staticmethod
    def rating_badge(rating):
        return f'<span style="background: {COLORS["warning"]["main"]}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.85em;">Rating: {rating}</span>'
    
    @staticmethod
    def match_badge(percentage):
        return f'<span style="background: linear-gradient(135deg, {COLORS["primary"]["main"]} 0%, {COLORS["secondary"]["main"]} 100%); color: white; padding: 5px 12px; border-radius: 15px; font-size: 0.85em;">Match: {percentage:.0f}%</span>'
