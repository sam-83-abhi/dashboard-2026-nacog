import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64, pathlib

def img_to_base64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()

PICS = {k: img_to_base64(f"pics/{k}.jpg") for k in ["denver_skyline","downtown","mountains","capitol","sunset","conference"]}

# --- Load background slideshow images ---
import glob
bg_files = sorted(glob.glob("pics/backgrounds/*"))
bg_base64 = [img_to_base64(f) for f in bg_files if f.lower().endswith((".jpg",".jpeg",".png"))]
# fallback to existing pics if no backgrounds uploaded yet
if not bg_base64:
    bg_base64 = [PICS[k] for k in ["downtown","mountains","capitol","sunset","conference"]]

st.set_page_config(page_title="NACOG 2026 Dashboard", layout="wide", page_icon="🎉")

# --- Password Protection ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True
    st.markdown(f"""
    <div style="display:flex;justify-content:center;align-items:center;min-height:60vh;">
        <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);padding:0;border-radius:20px;
                    text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.3);max-width:420px;width:100%;overflow:hidden;">
            <img src="data:image/jpeg;base64,{PICS['denver_skyline']}"
                 style="width:100%;height:140px;object-fit:cover;display:block;" alt="Denver"/>
            <div style="padding:30px 40px 40px;">
                <h1 style="color:#e94560;margin:0 0 5px;font-size:1.8rem;">NACOG 2026</h1>
                <p style="color:#a0a0b0;margin:0 0 5px;font-size:0.95rem;">Conference Dashboard</p>
                <p style="color:#707090;margin:0 0 25px;font-size:0.8rem;">📍 Denver, Colorado</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        pwd = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password")
        if st.button("🔓 Login", use_container_width=True):
            if pwd == st.secrets.get("password", "nacog2026"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect password")
    return False

if not check_password():
    st.stop()

# --- Custom CSS + Animations ---

# Background slideshow
if bg_base64:
    keyframes = ""
    n = len(bg_base64)
    step = 100 / n
    for i, img in enumerate(bg_base64):
        start = i * step
        mid = start + step * 0.8
        end = (i + 1) * step
        keyframes += f"""
        {start:.1f}% {{ background-image: url('data:image/jpeg;base64,{img}'); opacity:1; }}
        {mid:.1f}% {{ background-image: url('data:image/jpeg;base64,{img}'); opacity:1; }}
        {end:.1f}% {{ opacity:0.8; }}"""

    duration = n * 8  # 8 seconds per image
    st.markdown(f"""
    <style>
        .stApp::before {{
            content: "";
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-size: cover; background-position: center;
            animation: bgSlide {duration}s infinite;
            opacity: 0.03;
            z-index: 0;
            pointer-events: none;
        }}
        @keyframes bgSlide {{ {keyframes} }}
        .stApp > * {{ position: relative; z-index: 1; }}
        .block-container {{
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 1.5rem 2rem !important;
            backdrop-filter: blur(10px);
        }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 1.5rem; }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-40px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.03); }
    }
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .metric-card {
        padding: 22px 18px; border-radius: 16px; color: white; text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15); transition: transform 0.3s, box-shadow 0.3s;
        animation: fadeInUp 0.6s ease-out both;
    }
    .metric-card:nth-child(1) { animation-delay: 0.1s; }
    .metric-card:nth-child(2) { animation-delay: 0.2s; }
    .metric-card:nth-child(3) { animation-delay: 0.3s; }
    .metric-card:nth-child(4) { animation-delay: 0.4s; }
    .metric-card:nth-child(5) { animation-delay: 0.5s; }
    .metric-card:hover { transform: translateY(-6px) scale(1.02); box-shadow: 0 12px 40px rgba(0,0,0,0.25); }
    .metric-card h2 { font-size: 2.4rem; margin: 0; font-weight: 700; }
    .metric-card p { font-size: 0.85rem; margin: 5px 0 0; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }
    .mc-purple { background: linear-gradient(135deg, #667eea, #764ba2); }
    .mc-green  { background: linear-gradient(135deg, #00b09b, #96c93d); }
    .mc-blue   { background: linear-gradient(135deg, #4facfe, #00f2fe); }
    .mc-orange { background: linear-gradient(135deg, #f093fb, #f5576c); }
    .mc-pink   { background: linear-gradient(135deg, #fa709a, #fee140); }

    .dash-header {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 30px 35px; border-radius: 18px; margin-bottom: 25px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    .dash-header h1 { color: #fff; font-size: 2.2rem; margin: 0; }
    .dash-header p { color: #a0a0c0; margin: 5px 0 0; font-size: 1rem; }

    .chart-container {
        background: #ffffff; border-radius: 16px; padding: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06); margin-bottom: 10px;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e, #16213e);
    }
    div[data-testid="stSidebar"] * { color: #e0e0f0 !important; }

    .section-divider {
        height: 3px; border-radius: 2px; margin: 10px 0 20px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f5576c, #fee140, #667eea);
        background-size: 200% auto;
        animation: gradientMove 3s linear infinite;
    }

    .banner-animate {
        animation: fadeIn 1s ease-out;
    }
    .banner-animate h1 {
        animation: slideInLeft 0.8s ease-out 0.3s both;
    }
    .banner-animate p {
        animation: slideInLeft 0.8s ease-out 0.5s both;
    }

    .gallery-card {
        transition: transform 0.3s, box-shadow 0.3s;
        animation: fadeInUp 0.7s ease-out both;
    }
    .gallery-card:nth-child(1) { animation-delay: 0.1s; }
    .gallery-card:nth-child(2) { animation-delay: 0.2s; }
    .gallery-card:nth-child(3) { animation-delay: 0.3s; }
    .gallery-card:nth-child(4) { animation-delay: 0.4s; }
    .gallery-card:hover { transform: translateY(-8px) scale(1.02); box-shadow: 0 12px 35px rgba(0,0,0,0.2); }
    .gallery-card img { transition: transform 0.5s; }
    .gallery-card:hover img { transform: scale(1.08); }

    .footer-animate {
        animation: fadeIn 1s ease-out 0.5s both;
    }

    /* Plotly chart fade-in */
    .stPlotlyChart { animation: fadeInUp 0.6s ease-out both; }
</style>
""", unsafe_allow_html=True)

COLORS = ["#667eea", "#f5576c", "#00b09b", "#fa709a", "#4facfe", "#fee140", "#96c93d", "#764ba2"]

@st.cache_data(ttl=3600)
def load_data(file):
    df = pd.read_csv(file, encoding="utf-8-sig")
    df["Sold Date"] = pd.to_datetime(df["Sold Date"], errors="coerce")
    df["Ticket Price ($ Amount)"] = pd.to_numeric(df["Ticket Price ($ Amount)"], errors="coerce").fillna(0)
    df["Ticket Total ($ Amount)"] = pd.to_numeric(df["Ticket Total ($ Amount)"], errors="coerce").fillna(0)
    df["Hotel Cost"] = pd.to_numeric(df["How many hotel rooms do you need? ($ Amount)"], errors="coerce").fillna(0)
    df["Meal Cost"] = pd.to_numeric(df.get("Food: Do you wish to add a meal plan? ($ Amount)", pd.Series(dtype=float)), errors="coerce").fillna(0)
    df["Full Name"] = df["Name (First Name)"].astype(str).str.strip() + " " + df["Name (Last Name)"].astype(str).str.strip()
    return df

# --- CSV Upload ---
uploaded = st.sidebar.file_uploader("📂 Upload GeneralRegistration.csv", type="csv")
local_csv = pathlib.Path("GeneralRegistration.csv")

if uploaded:
    df = load_data(uploaded)
elif local_csv.exists():
    df = load_data(str(local_csv))
else:
    st.info("📂 Please upload your GeneralRegistration.csv file using the sidebar.")
    st.stop()
latest_entry = df["Sold Date"].max().strftime("%B %d, %Y") if pd.notna(df["Sold Date"].max()) else "Unknown"

# --- Header with Denver Banner ---
st.markdown(f"""
<div style="position:relative;border-radius:18px;overflow:hidden;margin-bottom:25px;
            box-shadow:0 10px 40px rgba(0,0,0,0.25);">
    <img src="data:image/jpeg;base64,{PICS['denver_skyline']}"
         style="width:100%;height:220px;object-fit:cover;display:block;" alt="Denver Skyline"/>
    <div style="position:absolute;top:0;left:0;width:100%;height:100%;
                background:linear-gradient(to right,rgba(15,12,41,0.85),rgba(48,43,99,0.6),rgba(36,36,62,0.4));"
         class="banner-animate">        <div style="padding:45px 35px;">
            <h1 style="color:#fff;font-size:2.4rem;margin:0;text-shadow:0 2px 10px rgba(0,0,0,0.3);">
                🎉 NACOG 2026 Conference
            </h1>
            <p style="color:#c0c0e0;margin:8px 0 0;font-size:1.05rem;">
                📍 Denver, Colorado &nbsp;•&nbsp; 📊 {len(df)} registrations &nbsp;•&nbsp; 🕐 Data as of: {latest_entry}
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown(f"""
    <div style="border-radius:12px;overflow:hidden;margin-bottom:15px;box-shadow:0 4px 15px rgba(0,0,0,0.2);">
        <img src="data:image/jpeg;base64,{bg_base64[0]}" style="width:100%;height:120px;object-fit:cover;"/>
        <div style="padding:8px 12px;background:linear-gradient(135deg,#667eea,#764ba2);text-align:center;">
            <p style="color:#fff;margin:0;font-size:0.8rem;">📍 Denver, Colorado</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("## 🎛️ Filters")
    st.markdown("---")
    statuses = st.multiselect("📌 Status", df["Status"].dropna().unique(), default=df["Status"].dropna().unique())
    ticket_levels = st.multiselect("🎫 Ticket Level", df["Ticket Level"].dropna().unique(), default=df["Ticket Level"].dropna().unique())
    genders = st.multiselect("👤 Gender", df["Gender"].dropna().unique(), default=df["Gender"].dropna().unique())
    st.markdown("---")
    st.markdown("##### 📥 Data Update")
    if st.button("Load Latest Registrations", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

mask = df["Status"].isin(statuses) & df["Ticket Level"].isin(ticket_levels) & df["Gender"].isin(genders)
fdf = df[mask]

# --- KPI Cards ---
total_reg = len(fdf)
total_revenue = fdf["Ticket Total ($ Amount)"].sum()
paid = (fdf["Status"] == "completed").sum()
pending = total_reg - paid
hotel_rooms = fdf["Hotel Cost"].gt(0).sum()

c1, c2, c3, c4, c5 = st.columns(5)
for col, cls, icon, label, val in [
    (c1, "mc-purple", "👥", "Registrations", total_reg),
    (c2, "mc-green",  "💰", "Revenue", f"${total_revenue:,.0f}"),
    (c3, "mc-blue",   "✅", "Paid", paid),
    (c4, "mc-orange", "⏳", "Pending", pending),
    (c5, "mc-pink",   "🏨", "Hotel Bookings", hotel_rooms),
]:
    col.markdown(f'<div class="metric-card {cls}"><h2>{icon} {val}</h2><p>{label}</p></div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

CHART_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#333"),
    margin=dict(l=20, r=20, t=50, b=20),
    title_font=dict(size=16, color="#333"),
)

# --- Row 1 ---
r1c1, r1c2 = st.columns(2)

with r1c1:
    daily = fdf.dropna(subset=["Sold Date"]).groupby(fdf["Sold Date"].dt.date).size().reset_index(name="Count")
    daily.columns = ["Date", "Count"]
    daily["Cumulative"] = daily["Count"].cumsum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["Date"], y=daily["Cumulative"], fill="tozeroy",
                             line=dict(color="#667eea", width=3), fillcolor="rgba(102,126,234,0.15)"))
    fig.update_layout(**CHART_LAYOUT, title="📈 Registration Growth")
    st.plotly_chart(fig, use_container_width=True)

with r1c2:
    level_counts = fdf["Ticket Level"].value_counts().reset_index()
    level_counts.columns = ["Ticket Level", "Count"]
    fig = px.pie(level_counts, names="Ticket Level", values="Count", title="🎫 Ticket Level Breakdown",
                 color_discrete_sequence=COLORS, hole=0.5)
    fig.update_traces(textinfo="percent+label", textfont_size=13,
                      marker=dict(line=dict(color="#fff", width=2)))
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

# --- Row 2 ---
r2c1, r2c2 = st.columns(2)

with r2c1:
    gender = fdf["Gender"].value_counts().reset_index()
    gender.columns = ["Gender", "Count"]
    fig = px.bar(gender, x="Gender", y="Count", title="👥 Gender Distribution",
                 color="Gender", color_discrete_sequence=COLORS, text_auto=True)
    fig.update_traces(marker_line_width=0, textposition="outside")
    fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.4)
    st.plotly_chart(fig, use_container_width=True)

with r2c2:
    age = fdf["Age Group"].value_counts().reset_index()
    age.columns = ["Age Group", "Count"]
    fig = px.bar(age, x="Count", y="Age Group", title="📊 Age Group Distribution",
                 color="Age Group", color_discrete_sequence=COLORS, text_auto=True, orientation="h")
    fig.update_traces(marker_line_width=0, textposition="outside")
    fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.35)
    st.plotly_chart(fig, use_container_width=True)

# --- Denver Photo Gallery ---
st.markdown(f"""
<div style="display:flex;gap:12px;margin-bottom:20px;">
    <div style="flex:1;border-radius:14px;overflow:hidden;box-shadow:0 6px 20px rgba(0,0,0,0.12);" class="gallery-card">
        <img src="data:image/jpeg;base64,{PICS['downtown']}"
             style="width:100%;height:180px;object-fit:cover;" alt="Denver Downtown"/>
        <div style="padding:10px 14px;background:linear-gradient(135deg,#1a1a2e,#302b63);">
            <p style="color:#fff;margin:0;font-size:0.85rem;">🏙️ Downtown Denver</p>
        </div>
    </div>
    <div style="flex:1;border-radius:14px;overflow:hidden;box-shadow:0 6px 20px rgba(0,0,0,0.12);" class="gallery-card">
        <img src="data:image/jpeg;base64,{PICS['mountains']}"
             style="width:100%;height:180px;object-fit:cover;" alt="Rocky Mountains"/>
        <div style="padding:10px 14px;background:linear-gradient(135deg,#11998e,#38ef7d);">
            <p style="color:#fff;margin:0;font-size:0.85rem;">🏔️ Rocky Mountains</p>
        </div>
    </div>
    <div style="flex:1;border-radius:14px;overflow:hidden;box-shadow:0 6px 20px rgba(0,0,0,0.12);" class="gallery-card">
        <img src="data:image/jpeg;base64,{PICS['capitol']}"
             style="width:100%;height:180px;object-fit:cover;" alt="Colorado State Capitol"/>
        <div style="padding:10px 14px;background:linear-gradient(135deg,#667eea,#764ba2);">
            <p style="color:#fff;margin:0;font-size:0.85rem;">🏛️ Colorado Capitol</p>
        </div>
    </div>
    <div style="flex:1;border-radius:14px;overflow:hidden;box-shadow:0 6px 20px rgba(0,0,0,0.12);" class="gallery-card">
        <img src="data:image/jpeg;base64,{PICS['sunset']}"
             style="width:100%;height:180px;object-fit:cover;" alt="Denver Sunset"/>
        <div style="padding:10px 14px;background:linear-gradient(135deg,#f5576c,#fa709a);">
            <p style="color:#fff;margin:0;font-size:0.85rem;">🌅 Colorado Sunset</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# --- Row 3 ---
r3c1, r3c2 = st.columns(2)

with r3c1:
    state_counts = fdf["Address (State)"].value_counts().reset_index()
    state_counts.columns = ["State", "Count"]
    fig = px.choropleth(state_counts, locations="State", locationmode="USA-states",
                        color="Count", scope="usa", title="🗺️ Registrations by State",
                        color_continuous_scale=["#e0e7ff", "#667eea", "#302b63"])
    fig.update_layout(**CHART_LAYOUT, geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, use_container_width=True)

with r3c2:
    sessions = {
        "General": fdf["Which sessions would you like to attend? (General Session)"].eq("Yes").sum(),
        "English": fdf["Which sessions would you like to attend? (English Session)"].eq("Yes").sum(),
        "Ladies": fdf["Which sessions would you like to attend? (Ladies Session)"].eq("Yes").sum(),
        "Children's": fdf["Which sessions would you like to attend? (Childrens Session)"].eq("Yes").sum(),
    }
    sess_df = pd.DataFrame(list(sessions.items()), columns=["Session", "Count"])
    fig = px.bar(sess_df, x="Session", y="Count", title="📋 Session Preferences",
                 color="Session", color_discrete_sequence=COLORS, text_auto=True)
    fig.update_traces(marker_line_width=0, textposition="outside")
    fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.4)
    st.plotly_chart(fig, use_container_width=True)

# --- Row 4 ---
r4c1, r4c2 = st.columns(2)

with r4c1:
    status_counts = fdf["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig = px.pie(status_counts, names="Status", values="Count", title="💳 Payment Status",
                 color_discrete_sequence=["#00b09b", "#f5576c", "#fee140"], hole=0.5)
    fig.update_traces(textinfo="percent+label", textfont_size=13,
                      marker=dict(line=dict(color="#fff", width=2)))
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

with r4c2:
    hotel = fdf["Do you need hotel room(s)?"].value_counts().reset_index()
    hotel.columns = ["Hotel Needed", "Count"]
    fig = px.pie(hotel, names="Hotel Needed", values="Count", title="🏨 Hotel Room Requests",
                 color_discrete_sequence=COLORS, hole=0.5)
    fig.update_traces(textinfo="percent+label", textfont_size=13,
                      marker=dict(line=dict(color="#fff", width=2)))
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# --- Row 5 ---
r5c1, r5c2 = st.columns(2)

with r5c1:
    pickup = fdf["Do you need airport pickup?"].value_counts().reset_index()
    pickup.columns = ["Pickup", "Count"]
    fig = px.bar(pickup, x="Pickup", y="Count", title="✈️ Airport Pickup Requests",
                 color="Pickup", color_discrete_sequence=COLORS, text_auto=True)
    fig.update_traces(marker_line_width=0, textposition="outside")
    fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.4)
    st.plotly_chart(fig, use_container_width=True)

with r5c2:
    dropoff = fdf["Do you need airport drop off?"].value_counts().reset_index()
    dropoff.columns = ["Drop Off", "Count"]
    fig = px.bar(dropoff, x="Drop Off", y="Count", title="🛫 Airport Drop Off Requests",
                 color="Drop Off", color_discrete_sequence=COLORS, text_auto=True)
    fig.update_traces(marker_line_width=0, textposition="outside")
    fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.4)
    st.plotly_chart(fig, use_container_width=True)

# --- Registrant Table ---
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("### 📋 Registrant Details")
display_cols = ["Full Name", "Email", "Gender", "Age Group", "Ticket Level", "Status",
                "Address (City)", "Address (State)", "Ticket Total ($ Amount)", "Sold Date"]
st.dataframe(
    fdf[display_cols].sort_values("Sold Date", ascending=False),
    use_container_width=True, height=450,
    column_config={
        "Ticket Total ($ Amount)": st.column_config.NumberColumn(format="$%.2f"),
        "Sold Date": st.column_config.DateColumn(format="MMM DD, YYYY"),
    }
)

# --- Footer ---
st.markdown(f"""
<div style="position:relative;border-radius:16px;overflow:hidden;margin-top:20px;
            box-shadow:0 6px 20px rgba(0,0,0,0.12);" class="footer-animate">
    <img src="data:image/jpeg;base64,{PICS['conference']}"
         style="width:100%;height:120px;object-fit:cover;display:block;" alt="Conference"/>
    <div style="position:absolute;top:0;left:0;width:100%;height:100%;
                background:rgba(15,12,41,0.75);display:flex;align-items:center;justify-content:center;">
        <p style="color:#c0c0e0;font-size:0.85rem;margin:0;">
            NACOG 2026 Conference Dashboard &nbsp;•&nbsp; 📍 Denver, Colorado
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
