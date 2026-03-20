import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="NACOG 2026 Dashboard", layout="wide")

# --- Password Protection ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True
    st.title("🔒 NACOG 2026 Dashboard")
    st.caption("Enter the password to access the dashboard")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if pwd == st.secrets.get("password", "nacog2026"):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    return False

if not check_password():
    st.stop()

# --- Custom CSS ---
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px; border-radius: 12px; color: white; text-align: center;
    }
    .metric-card h2 { font-size: 2.2rem; margin: 0; }
    .metric-card p { font-size: 0.95rem; margin: 0; opacity: 0.85; }
    .metric-green { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
    .metric-orange { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); }
    .metric-pink { background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%); }
    .metric-blue { background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%); }
</style>
""", unsafe_allow_html=True)

COLORS = px.colors.qualitative.Vivid

@st.cache_data
def load_data():
    df = pd.read_csv("GeneralRegistration.csv", encoding="utf-8-sig")
    df["Sold Date"] = pd.to_datetime(df["Sold Date"], errors="coerce")
    df["Ticket Price ($ Amount)"] = pd.to_numeric(df["Ticket Price ($ Amount)"], errors="coerce").fillna(0)
    df["Ticket Total ($ Amount)"] = pd.to_numeric(df["Ticket Total ($ Amount)"], errors="coerce").fillna(0)
    df["Hotel Cost"] = pd.to_numeric(df["How many hotel rooms do you need? ($ Amount)"], errors="coerce").fillna(0)
    df["Meal Cost"] = pd.to_numeric(df.get("Food: Do you wish to add a meal plan? ($ Amount)", pd.Series(dtype=float)), errors="coerce").fillna(0)
    df["Full Name"] = df["Name (First Name)"].astype(str).str.strip() + " " + df["Name (Last Name)"].astype(str).str.strip()
    return df

df = load_data()

st.title("🎉 NACOG 2026 Conference Dashboard")
st.caption(f"Data refreshed from GeneralRegistration.csv • {len(df)} registrations")

# --- Filters ---
with st.sidebar:
    st.header("🔍 Filters")
    statuses = st.multiselect("Status", df["Status"].dropna().unique(), default=df["Status"].dropna().unique())
    ticket_levels = st.multiselect("Ticket Level", df["Ticket Level"].dropna().unique(), default=df["Ticket Level"].dropna().unique())
    genders = st.multiselect("Gender", df["Gender"].dropna().unique(), default=df["Gender"].dropna().unique())

mask = df["Status"].isin(statuses) & df["Ticket Level"].isin(ticket_levels) & df["Gender"].isin(genders)
fdf = df[mask]

# --- KPI Cards ---
total_reg = len(fdf)
total_revenue = fdf["Ticket Total ($ Amount)"].sum()
paid = (fdf["Status"] == "completed").sum()
pending = total_reg - paid
hotel_rooms = fdf["Hotel Cost"].gt(0).sum()

c1, c2, c3, c4, c5 = st.columns(5)
for col, cls, label, val in [
    (c1, "", "Total Registrations", total_reg),
    (c2, "metric-green", "Revenue", f"${total_revenue:,.0f}"),
    (c3, "metric-blue", "Paid / Completed", paid),
    (c4, "metric-orange", "Pending Payment", pending),
    (c5, "metric-pink", "Hotel Bookings", hotel_rooms),
]:
    col.markdown(f'<div class="metric-card {cls}"><h2>{val}</h2><p>{label}</p></div>', unsafe_allow_html=True)

st.markdown("---")

# --- Row 1: Registrations Over Time + Ticket Level Breakdown ---
r1c1, r1c2 = st.columns(2)

with r1c1:
    daily = fdf.dropna(subset=["Sold Date"]).groupby(fdf["Sold Date"].dt.date).size().reset_index(name="Count")
    daily.columns = ["Date", "Count"]
    daily["Cumulative"] = daily["Count"].cumsum()
    fig = px.area(daily, x="Date", y="Cumulative", title="📈 Registration Growth",
                  color_discrete_sequence=["#667eea"], labels={"Cumulative": "Total Registrations"})
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

with r1c2:
    level_counts = fdf["Ticket Level"].value_counts().reset_index()
    level_counts.columns = ["Ticket Level", "Count"]
    fig = px.pie(level_counts, names="Ticket Level", values="Count", title="🎫 Ticket Level Breakdown",
                 color_discrete_sequence=COLORS, hole=0.45)
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

# --- Row 2: Gender + Age Group ---
r2c1, r2c2 = st.columns(2)

with r2c1:
    gender = fdf["Gender"].value_counts().reset_index()
    gender.columns = ["Gender", "Count"]
    fig = px.bar(gender, x="Gender", y="Count", title="👥 Gender Distribution",
                 color="Gender", color_discrete_sequence=COLORS, text_auto=True)
    fig.update_layout(template="plotly_white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with r2c2:
    age = fdf["Age Group"].value_counts().reset_index()
    age.columns = ["Age Group", "Count"]
    fig = px.bar(age, x="Age Group", y="Count", title="📊 Age Group Distribution",
                 color="Age Group", color_discrete_sequence=COLORS, text_auto=True)
    fig.update_layout(template="plotly_white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# --- Row 3: State Map + Session Preferences ---
r3c1, r3c2 = st.columns(2)

with r3c1:
    state_counts = fdf["Address (State)"].value_counts().reset_index()
    state_counts.columns = ["State", "Count"]
    fig = px.choropleth(state_counts, locations="State", locationmode="USA-states",
                        color="Count", scope="usa", title="🗺️ Registrations by State",
                        color_continuous_scale="Viridis")
    fig.update_layout(geo=dict(bgcolor="rgba(0,0,0,0)"))
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
    fig.update_layout(template="plotly_white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# --- Row 4: Payment Status + Hotel Needs ---
r4c1, r4c2 = st.columns(2)

with r4c1:
    status_counts = fdf["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig = px.pie(status_counts, names="Status", values="Count", title="💳 Payment Status",
                 color_discrete_sequence=["#38ef7d", "#ffd200", "#ee0979"], hole=0.45)
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

with r4c2:
    hotel = fdf["Do you need hotel room(s)?"].value_counts().reset_index()
    hotel.columns = ["Hotel Needed", "Count"]
    fig = px.pie(hotel, names="Hotel Needed", values="Count", title="🏨 Hotel Room Requests",
                 color_discrete_sequence=COLORS, hole=0.45)
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

# --- Row 5: Airport Pickup/Dropoff ---
r5c1, r5c2 = st.columns(2)

with r5c1:
    pickup = fdf["Do you need airport pickup?"].value_counts().reset_index()
    pickup.columns = ["Pickup", "Count"]
    fig = px.bar(pickup, x="Pickup", y="Count", title="✈️ Airport Pickup Requests",
                 color="Pickup", color_discrete_sequence=COLORS, text_auto=True)
    fig.update_layout(template="plotly_white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with r5c2:
    dropoff = fdf["Do you need airport drop off?"].value_counts().reset_index()
    dropoff.columns = ["Drop Off", "Count"]
    fig = px.bar(dropoff, x="Drop Off", y="Count", title="🛫 Airport Drop Off Requests",
                 color="Drop Off", color_discrete_sequence=COLORS, text_auto=True)
    fig.update_layout(template="plotly_white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# --- Registrant Table ---
st.markdown("---")
st.subheader("📋 Registrant Details")
display_cols = ["Full Name", "Email", "Gender", "Age Group", "Ticket Level", "Status",
                "Address (City)", "Address (State)", "Ticket Total ($ Amount)", "Sold Date"]
st.dataframe(fdf[display_cols].sort_values("Sold Date", ascending=False), use_container_width=True, height=400)
