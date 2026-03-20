import streamlit as st
import pandas as pd
from auth import check_password
from styles import apply_styles
from data_loader import get_data
from charts import (render_kpis, render_registration, render_demographics, render_payment,
                    render_hotel, render_travel, render_airport,
                    render_food, render_community, render_table)

st.set_page_config(page_title="NACOG 2026 Dashboard", layout="wide", page_icon="🎉")

# --- Login ---
if not check_password():
    st.stop()

# --- Dashboard ---
apply_styles()
df = get_data()
latest_entry = df["Sold Date"].max().strftime("%B %d, %Y") if pd.notna(df["Sold Date"].max()) else "Unknown"

# Header
st.markdown(f"""
<div style="background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
            padding:30px;border-radius:18px;margin-bottom:25px;box-shadow:0 10px 40px rgba(0,0,0,0.25);
            text-align:center;border:1px solid rgba(102,126,234,0.15);">
    <h1 style="color:#fff;font-size:2rem;margin:0;font-weight:800;letter-spacing:1px;
               background:linear-gradient(90deg,#667eea,#f5576c,#fee140,#667eea);background-size:300% auto;
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               animation:shimmer 5s linear infinite;">NACOG 2026 Conference Dashboard</h1>
    <p style="color:#c0c0e0;margin:10px 0 0;font-size:0.95rem;">
        📍 Denver, Colorado &nbsp;•&nbsp; 📊 {len(df)} registrations &nbsp;•&nbsp; 🕐 Data as of: {latest_entry}
    </p>
</div>
<style>@keyframes shimmer {{ 0% {{ background-position:200% center; }} 100% {{ background-position:-200% center; }} }}</style>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.markdown("---")
    statuses = st.multiselect("📌 Status", df["Status"].dropna().unique(), default=df["Status"].dropna().unique())
    ticket_levels = st.multiselect("🎫 Ticket Level", df["Ticket Level"].dropna().unique(), default=df["Ticket Level"].dropna().unique())
    genders = st.multiselect("👤 Gender", df["Gender"].dropna().unique(), default=df["Gender"].dropna().unique())
    st.markdown("---")
    st.markdown("##### 📥 Data Update")
    if st.button("🔄 Load Latest Registrations", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

fdf = df[df["Status"].isin(statuses) & df["Ticket Level"].isin(ticket_levels) & df["Gender"].isin(genders)]

# Render dashboard
section = '''<div style="margin:20px 0 10px;padding:10px 16px;border-radius:12px;
    background:linear-gradient(135deg,rgba(102,126,234,0.15),rgba(118,75,162,0.1));
    border-left:4px solid #667eea;display:flex;align-items:center;gap:8px;">
    <span style="font-size:1.1rem;color:#ffffff;font-weight:600;letter-spacing:0.5px;">{}</span>
</div>'''
divider = '<div class="section-divider"></div>'

render_kpis(fdf)

st.markdown(section.format("📊 Registration Overview"), unsafe_allow_html=True)
render_registration(fdf)

st.markdown(divider, unsafe_allow_html=True)
st.markdown(section.format("👥 Demographics"), unsafe_allow_html=True)
render_demographics(fdf)

st.markdown(divider, unsafe_allow_html=True)
st.markdown(section.format("🏨 Hotel & Accommodation"), unsafe_allow_html=True)
render_hotel(fdf)

st.markdown(divider, unsafe_allow_html=True)
st.markdown(section.format("✈️ Travel & Airport"), unsafe_allow_html=True)
render_travel(fdf)
render_airport(fdf)

st.markdown(divider, unsafe_allow_html=True)
st.markdown(section.format("🍽️ Food & Meals"), unsafe_allow_html=True)
render_food(fdf)

st.markdown(divider, unsafe_allow_html=True)
st.markdown(section.format("⛪ Community"), unsafe_allow_html=True)
render_community(fdf)

st.markdown(divider, unsafe_allow_html=True)
st.markdown(section.format("💳 Payment"), unsafe_allow_html=True)
render_payment(fdf)

st.markdown(divider, unsafe_allow_html=True)
st.markdown(section.format("📋 Registrant Details"), unsafe_allow_html=True)
render_table(fdf)

# Footer
st.markdown("""
<div style="background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
            border-radius:16px;margin-top:20px;padding:20px;text-align:center;box-shadow:0 6px 20px rgba(0,0,0,0.12);">
    <p style="color:#c0c0e0;font-size:0.85rem;margin:0;">NACOG 2026 Conference Dashboard &nbsp;•&nbsp; 📍 Denver, Colorado</p>
</div>
""", unsafe_allow_html=True)
