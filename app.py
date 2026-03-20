import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pathlib

st.set_page_config(page_title="NACOG 2026 Dashboard", layout="wide", page_icon="🎉")

# --- Password Protection ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True
    st.markdown("""
    <style>
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        @keyframes bgSlide {
            0%   { background-image: url('https://images.pexels.com/photos/417074/pexels-photo-417074.jpeg?auto=compress&w=1400'); }
            20%  { background-image: url('https://images.pexels.com/photos/417074/pexels-photo-417074.jpeg?auto=compress&w=1400'); }
            25%  { background-image: url('https://images.pexels.com/photos/1632790/pexels-photo-1632790.jpeg?auto=compress&w=1400'); }
            45%  { background-image: url('https://images.pexels.com/photos/1632790/pexels-photo-1632790.jpeg?auto=compress&w=1400'); }
            50%  { background-image: url('https://images.pexels.com/photos/1054218/pexels-photo-1054218.jpeg?auto=compress&w=1400'); }
            70%  { background-image: url('https://images.pexels.com/photos/1054218/pexels-photo-1054218.jpeg?auto=compress&w=1400'); }
            75%  { background-image: url('https://images.pexels.com/photos/1578750/pexels-photo-1578750.jpeg?auto=compress&w=1400'); }
            95%  { background-image: url('https://images.pexels.com/photos/1578750/pexels-photo-1578750.jpeg?auto=compress&w=1400'); }
            100% { background-image: url('https://images.pexels.com/photos/417074/pexels-photo-417074.jpeg?auto=compress&w=1400'); }
        }
        .stApp {
            background-size: cover !important;
            background-position: center !important;
            animation: bgSlide 32s infinite;
        }
        .stApp::before {
            content: "";
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(10, 10, 30, 0.55);
            z-index: 0;
        }
        .stApp > * { position: relative; z-index: 1; }
        .login-card { animation: fadeInUp 0.8s ease-out; }
        .login-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 30px 80px rgba(0,0,0,0.5) !important;
            transition: all 0.3s;
        }
        .login-emoji { animation: pulse 2s ease-in-out infinite; display: inline-block; }
    </style>
    <div style="display:flex;justify-content:center;align-items:center;min-height:70vh;">
        <div class="login-card" style="background:rgba(26,26,46,0.55);backdrop-filter:blur(8px);padding:0;border-radius:20px;
                    text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.4);max-width:420px;width:100%;overflow:hidden;">
            <div style="padding:35px 40px 30px;">
                <div class="login-emoji" style="font-size:3rem;margin-bottom:8px;">🎉</div>
                <h1 style="color:#ff4d6d;margin:0 0 5px;font-size:2rem;font-weight:700;">NACOG 2026</h1>
                <p style="color:#e0e0f0;margin:0 0 5px;font-size:1.1rem;font-weight:600;">Conference Dashboard</p>
                <p style="color:#c0c0d0;margin:0 0 20px;font-size:0.9rem;">📍 Denver, Colorado</p>
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

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 1.5rem; }

    /* Dark theme - force all text white */
    .stApp { background-color: #0a0a1a; }
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div,
    .stApp li, .stApp td, .stApp th, .stApp caption,
    .stApp input, .stApp textarea, .stApp select,
    .stMarkdown, .stMarkdown p, .stMarkdown span,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"], .stDataFrame,
    .stSelectbox label, .stMultiSelect label,
    .stFileUploader label, .stTextInput label { color: #ffffff !important; }
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    .stDataFrame td, .stDataFrame th { color: #ffffff !important; }
    [data-testid="stTable"] { color: #ffffff !important; }
    .stAlert p { color: #ffffff !important; }

    /* All input fields */
    .stTextInput input, .stTextArea textarea {
        color: #ffffff !important;
        background: #1a1a3a !important;
        border: 1px solid #667eea !important;
        caret-color: #ffffff !important;
    }
    .stTextInput input::placeholder { color: #a0a0c0 !important; }

    /* Dataframe / Table */
    [data-testid="stDataFrame"] * { color: #ffffff !important; }
    [data-testid="stDataFrame"] input { color: #ffffff !important; background: #1a1a3a !important; border: 1px solid #667eea !important; }
    [data-testid="stDataFrame"] button { color: #ffffff !important; }
    [data-testid="stDataFrame"] svg { fill: #ffffff !important; }
    [data-testid="stDataFrame"] [data-testid="glideDataEditor"] { background: #0a0a1a !important; }
    .stDataFrame th, .stDataFrame td { color: #ffffff !important; background: #12122a !important; }
    [data-testid="stDataFrame"] input::placeholder { color: #a0a0c0 !important; }

    .metric-card {
        padding: 22px 18px; border-radius: 16px; color: white; text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .metric-card h2 { font-size: 2.4rem; margin: 0; font-weight: 700; color: #fff !important; }
    .metric-card p { font-size: 0.85rem; margin: 5px 0 0; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; color: #fff !important; }
    .mc-purple { background: linear-gradient(135deg, #667eea, #764ba2); }
    .mc-green  { background: linear-gradient(135deg, #00b09b, #96c93d); }
    .mc-blue   { background: linear-gradient(135deg, #4facfe, #00f2fe); }
    .mc-orange { background: linear-gradient(135deg, #f093fb, #f5576c); }
    .mc-pink   { background: linear-gradient(135deg, #fa709a, #fee140); }
    div[data-testid="stSidebar"],
    div[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background: #0a0a1a !important;
        border-right: 1px solid #1a1a3a;
    }
    /* Sidebar - every single element white */
    div[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] *,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] button span,
    [data-testid="stSidebar"] [data-baseweb] *,
    [data-testid="stSidebar"] [role="button"],
    [data-testid="stSidebar"] svg { color: #ffffff !important; fill: #ffffff !important; }

    [data-testid="stSidebar"] button {
        background: #667eea !important; color: #ffffff !important;
        border: 2px solid #764ba2 !important; font-weight: 700 !important;
        font-size: 1rem !important; padding: 10px !important;
    }
    [data-testid="stSidebar"] button:hover { background: #764ba2 !important; }
    [data-testid="stSidebar"] button span { color: #ffffff !important; }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        background: rgba(102,126,234,0.2) !important;
        border: 2px dashed #667eea !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * { color: #ffffff !important; }
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
        background: #f5576c !important; border: none !important;
    }

    [data-testid="stSidebar"] h5 { color: #ffffff !important; font-size: 1.1rem !important; }
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] { background: #667eea !important; }
    [data-testid="stSidebar"] [data-baseweb="select"] * { color: #ffffff !important; }
    .section-divider {
        height: 3px; border-radius: 2px; margin: 10px 0 20px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f5576c, #fee140);
    }
    .chart-card {
        background: rgba(18,18,42,0.6);
        border: 1px solid rgba(102,126,234,0.15);
        border-radius: 14px;
        padding: 10px;
        margin-bottom: 10px;
    }
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

# --- Header ---
st.markdown(f"""
<div style="background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
            padding:35px;border-radius:18px;margin-bottom:25px;
            box-shadow:0 10px 40px rgba(0,0,0,0.25);">
    <h1 style="color:#fff;font-size:2.4rem;margin:0;">🎉 NACOG 2026 Conference</h1>
    <p style="color:#c0c0e0;margin:8px 0 0;font-size:1.05rem;">
        📍 Denver, Colorado &nbsp;•&nbsp; 📊 {len(df)} registrations &nbsp;•&nbsp; 🕐 Data as of: {latest_entry}
    </p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.markdown("---")
    statuses = st.multiselect("📌 Status", df["Status"].dropna().unique(), default=df["Status"].dropna().unique())
    ticket_levels = st.multiselect("🎫 Ticket Level", df["Ticket Level"].dropna().unique(), default=df["Ticket Level"].dropna().unique())
    genders = st.multiselect("👤 Gender", df["Gender"].dropna().unique(), default=df["Gender"].dropna().unique())
    st.markdown("---")
    st.markdown("##### 📥 Data Update"
               , unsafe_allow_html=False)
    if st.button("🔄 Load Latest Registrations", use_container_width=True):
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
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(18,18,42,0.5)",
    font=dict(family="Inter", color="#e0e0f0"),
    margin=dict(l=10, r=10, t=40, b=10),
    title_font=dict(size=14, color="#ffffff"),
    height=280,
)

# --- Row 1: Growth + Tickets + Gender ---
r1c1, r1c2, r1c3 = st.columns(3)

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
    fig = px.pie(level_counts, names="Ticket Level", values="Count", title="🎫 Ticket Level",
                 color_discrete_sequence=COLORS, hole=0.55)
    fig.update_traces(textinfo="percent+label", textfont_size=11,
                      marker=dict(line=dict(color="#1a1a2e", width=2)))
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

with r1c3:
    gender = fdf["Gender"].value_counts().reset_index()
    gender.columns = ["Gender", "Count"]
    fig = px.bar(gender, x="Gender", y="Count", title="👥 Gender",
                 color="Gender", color_discrete_sequence=COLORS, text_auto=True)
    fig.update_traces(marker_line_width=0, textposition="outside")
    fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.4)
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# --- Row 2: Age + Sessions + Map ---
r2c1, r2c2, r2c3 = st.columns(3)

with r2c1:
    age = fdf["Age Group"].value_counts().reset_index()
    age.columns = ["Age Group", "Count"]
    fig = px.bar(age, x="Count", y="Age Group", title="📊 Age Groups",
                 color="Age Group", color_discrete_sequence=COLORS, text_auto=True, orientation="h")
    fig.update_traces(marker_line_width=0, textposition="outside")
    fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.35)
    st.plotly_chart(fig, use_container_width=True)

with r2c2:
    sessions = {
        "General": fdf["Which sessions would you like to attend? (General Session)"].eq("Yes").sum(),
        "English": fdf["Which sessions would you like to attend? (English Session)"].eq("Yes").sum(),
        "Ladies": fdf["Which sessions would you like to attend? (Ladies Session)"].eq("Yes").sum(),
        "Children's": fdf["Which sessions would you like to attend? (Childrens Session)"].eq("Yes").sum(),
    }
    sess_df = pd.DataFrame(list(sessions.items()), columns=["Session", "Count"])
    fig = px.bar(sess_df, x="Session", y="Count", title="📋 Sessions",
                 color="Session", color_discrete_sequence=COLORS, text_auto=True)
    fig.update_traces(marker_line_width=0, textposition="outside")
    fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.4)
    st.plotly_chart(fig, use_container_width=True)

with r2c3:
    state_counts = fdf["Address (State)"].value_counts().reset_index()
    state_counts.columns = ["State", "Count"]
    fig = px.choropleth(state_counts, locations="State", locationmode="USA-states",
                        color="Count", scope="usa", title="🗺️ By State",
                        color_continuous_scale=["#e0e7ff", "#667eea", "#302b63"])
    fig.update_layout(**CHART_LAYOUT, geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor="rgba(0,0,0,0)"),
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# --- Row 3: Payment + Hotel + Airport ---
r3c1, r3c2, r3c3 = st.columns(3)

with r3c1:
    status_counts = fdf["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig = px.pie(status_counts, names="Status", values="Count", title="💳 Payment",
                 color_discrete_sequence=["#00b09b", "#f5576c", "#fee140"], hole=0.55)
    fig.update_traces(textinfo="percent+label", textfont_size=11,
                      marker=dict(line=dict(color="#1a1a2e", width=2)))
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

with r3c2:
    hotel = fdf["Do you need hotel room(s)?"].value_counts().reset_index()
    hotel.columns = ["Hotel Needed", "Count"]
    fig = px.pie(hotel, names="Hotel Needed", values="Count", title="🏨 Hotel",
                 color_discrete_sequence=COLORS, hole=0.55)
    fig.update_traces(textinfo="percent+label", textfont_size=11,
                      marker=dict(line=dict(color="#1a1a2e", width=2)))
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

with r3c3:
    pickup = fdf["Do you need airport pickup?"].value_counts().reset_index()
    pickup.columns = ["Pickup", "Count"]
    fig = px.bar(pickup, x="Pickup", y="Count", title="✈️ Airport Pickup",
                 color="Pickup", color_discrete_sequence=COLORS, text_auto=True)
    fig.update_traces(marker_line_width=0, textposition="outside")
    fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.4)
    st.plotly_chart(fig, use_container_width=True)

# --- Registrant Table ---
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("### 📋 Registrant Details")

display_cols = ["Full Name", "Email", "Gender", "Age Group", "Ticket Level", "Status",
                "Address (City)", "Address (State)", "Ticket Total ($ Amount)", "Sold Date"]
table_df = fdf[display_cols].sort_values("Sold Date", ascending=False).reset_index(drop=True)

search = st.text_input("🔍 Search registrants", "", placeholder="Type name, email, city...")
if search:
    mask = table_df.apply(lambda row: search.lower() in str(row.values).lower(), axis=1)
    table_df = table_df[mask]

st.markdown(f"Showing {len(table_df)} registrants")

html_table = table_df.to_html(index=False, escape=True, classes="reg-table")
st.markdown(f"""
<style>
    .reg-table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
    .reg-table th {{
        background: #667eea; color: #fff; padding: 10px 12px;
        text-align: left; font-weight: 600; position: sticky; top: 0;
    }}
    .reg-table td {{ padding: 8px 12px; color: #ffffff; border-bottom: 1px solid #1a1a3a; }}
    .reg-table tr:hover td {{ background: rgba(102,126,234,0.15); }}
    .reg-table tr:nth-child(even) td {{ background: rgba(255,255,255,0.03); }}
</style>
<div style="max-height:450px;overflow-y:auto;border-radius:12px;border:1px solid #1a1a3a;">
{html_table}
</div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div style="background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
            border-radius:16px;margin-top:20px;padding:20px;text-align:center;
            box-shadow:0 6px 20px rgba(0,0,0,0.12);">
    <p style="color:#c0c0e0;font-size:0.85rem;margin:0;">
        NACOG 2026 Conference Dashboard &nbsp;•&nbsp; 📍 Denver, Colorado
    </p>
</div>
""", unsafe_allow_html=True)
