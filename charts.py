import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLORS = ["#667eea", "#f5576c", "#00b09b", "#fa709a", "#4facfe", "#fee140", "#96c93d", "#764ba2"]

CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(18,18,42,0.5)",
    font=dict(family="Inter", color="#e0e0f0"),
    margin=dict(l=10, r=10, t=40, b=10),
    title_font=dict(size=14, color="#ffffff"),
    height=280,
)

def render_kpis(fdf):
    total_reg = len(fdf)
    total_revenue = fdf["Ticket Total ($ Amount)"].sum()
    paid = (fdf["Status"] == "completed").sum()
    pending = (fdf["Status"] == "pending offline payment").sum()
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

def render_row1(fdf):
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        daily = fdf.dropna(subset=["Sold Date"]).groupby(fdf["Sold Date"].dt.date).size().reset_index(name="Count")
        daily.columns = ["Date", "Count"]
        daily["Cumulative"] = daily["Count"].cumsum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily["Date"], y=daily["Cumulative"], fill="tozeroy",
                                 line=dict(color="#667eea", width=3), fillcolor="rgba(102,126,234,0.15)"))
        fig.update_layout(**CHART_LAYOUT, title="📈 Registration Growth",
                         xaxis=dict(tickfont=dict(color="#ffffff"), title_font=dict(color="#ffffff")),
                         yaxis=dict(tickfont=dict(color="#ffffff"), title_font=dict(color="#ffffff")))
        st.plotly_chart(fig, use_container_width=True)
    with r1c2:
        lc = fdf["Ticket Level"].value_counts().reset_index()
        lc.columns = ["Ticket Level", "Count"]
        fig = px.pie(lc, names="Ticket Level", values="Count", title="🎫 Ticket Level",
                     color_discrete_sequence=COLORS, hole=0.55)
        fig.update_traces(textinfo="value+label", textfont_size=11, marker=dict(line=dict(color="#1a1a2e", width=2)))
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with r1c3:
        g = fdf["Gender"].value_counts().reset_index()
        g.columns = ["Gender", "Count"]
        fig = px.bar(g, x="Gender", y="Count", title="👥 Gender", color="Gender", color_discrete_sequence=COLORS, text_auto=True)
        fig.update_traces(marker_line_width=0, textposition="outside")
        fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.4)
        st.plotly_chart(fig, use_container_width=True)

def render_row2(fdf):
    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        a = fdf["Age Group"].value_counts().reset_index()
        a.columns = ["Age Group", "Count"]
        fig = px.bar(a, x="Count", y="Age Group", title="📊 Age Groups", color="Age Group",
                     color_discrete_sequence=COLORS, text_auto=True, orientation="h")
        fig.update_traces(marker_line_width=0, textposition="outside")
        fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.35)
        st.plotly_chart(fig, use_container_width=True)
    with r2c2:
        sessions = {
            "General": fdf["Which sessions would you like to attend? (General Session)"].eq("Yes").sum() +
                       fdf.get("Session Preference (General Session)", pd.Series(dtype=str)).eq("Yes").sum(),
            "English": fdf["Which sessions would you like to attend? (English Session)"].eq("Yes").sum() +
                       fdf.get("Session Preference (English Session)", pd.Series(dtype=str)).eq("Yes").sum(),
            "Ladies": fdf["Which sessions would you like to attend? (Ladies Session)"].eq("Yes").sum() +
                      fdf.get("Session Preference (Ladies Session)", pd.Series(dtype=str)).eq("Yes").sum(),
            "Children's": fdf["Which sessions would you like to attend? (Childrens Session)"].eq("Yes").sum() +
                          fdf.get("Session Preference (Childrens Session)", pd.Series(dtype=str)).eq("Yes").sum(),
        }
        sess_df = pd.DataFrame(list(sessions.items()), columns=["Session", "Count"])
        fig = px.bar(sess_df, x="Session", y="Count", title="📋 Sessions", color="Session",
                     color_discrete_sequence=COLORS, text_auto=True)
        fig.update_traces(marker_line_width=0, textposition="outside")
        fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.4)
        st.plotly_chart(fig, use_container_width=True)
    with r2c3:
        sc = fdf["Address (State)"].value_counts().reset_index()
        sc.columns = ["State", "Count"]
        fig = px.choropleth(sc, locations="State", locationmode="USA-states", color="Count", scope="usa",
                            title="🗺️ By State", color_continuous_scale=["#e0e7ff", "#667eea", "#302b63"])
        fig.update_layout(**CHART_LAYOUT, geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor="rgba(0,0,0,0)"), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

def render_row3(fdf):
    r3c1, r3c2, r3c3 = st.columns(3)
    with r3c1:
        sc = fdf["Status"].value_counts().reset_index()
        sc.columns = ["Status", "Count"]
        fig = px.pie(sc, names="Status", values="Count", title="💳 Payment",
                     color_discrete_sequence=["#00b09b", "#f5576c", "#fee140"], hole=0.55)
        fig.update_traces(textinfo="value+label", textfont_size=11, marker=dict(line=dict(color="#1a1a2e", width=2)))
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with r3c2:
        h = fdf["Do you need hotel room(s)?"].value_counts().reset_index()
        h.columns = ["Hotel Needed", "Count"]
        fig = px.pie(h, names="Hotel Needed", values="Count", title="🏨 Hotel",
                     color_discrete_sequence=COLORS, hole=0.55)
        fig.update_traces(textinfo="value+label", textfont_size=11, marker=dict(line=dict(color="#1a1a2e", width=2)))
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with r3c3:
        p = fdf["Do you need airport pickup?"].value_counts().reset_index()
        p.columns = ["Pickup", "Count"]
        fig = px.bar(p, x="Pickup", y="Count", title="✈️ Airport Pickup", color="Pickup",
                     color_discrete_sequence=COLORS, text_auto=True)
        fig.update_traces(marker_line_width=0, textposition="outside")
        fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.4)
        st.plotly_chart(fig, use_container_width=True)

def render_row4(fdf):
    r4c1, r4c2, r4c3 = st.columns(3)
    with r4c1:
        meal_cols = [c for c in fdf.columns if c.lower().startswith("food: do you wish to add meal plan") or c.lower().startswith("food: do you wish to add a meal plan")]
        meal = pd.concat([fdf[c].dropna() for c in meal_cols])
        m = meal.value_counts().reset_index()
        m.columns = ["Meal Plan", "Count"]
        fig = px.pie(m, names="Meal Plan", values="Count", title="🍽️ Meal Plan",
                     color_discrete_sequence=COLORS, hole=0.55)
        fig.update_traces(textinfo="value+label", textfont_size=11, marker=dict(line=dict(color="#1a1a2e", width=2)))
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with r4c2:
        diet = pd.Series(dtype=str)
        for c in [c for c in fdf.columns if "dietary restrictions" in c.lower()]:
            d = fdf[c].dropna().astype(str)
            d = d[d.str.strip() != ""]
            diet = pd.concat([diet, d])
        if len(diet) > 0:
            dc = diet.value_counts().head(8).reset_index()
            dc.columns = ["Restriction", "Count"]
            fig = px.bar(dc, x="Count", y="Restriction", title="🥗 Dietary Restrictions", color="Restriction",
                         color_discrete_sequence=COLORS, text_auto=True, orientation="h")
            fig.update_traces(marker_line_width=0, textposition="outside")
            fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.35)
        else:
            fig = go.Figure()
            fig.update_layout(**CHART_LAYOUT, title="🥗 Dietary Restrictions",
                              annotations=[dict(text="No data", showarrow=False, font=dict(size=16, color="#667eea"))])
        st.plotly_chart(fig, use_container_width=True)
    with r4c3:
        ch = fdf["Church Name"].dropna()
        ch = ch[ch.str.strip() != ""]
        if len(ch) > 0:
            cc = ch.value_counts().head(8).reset_index()
            cc.columns = ["Church", "Count"]
            fig = px.bar(cc, x="Count", y="Church", title="⛪ Top Churches", color="Church",
                         color_discrete_sequence=COLORS, text_auto=True, orientation="h")
            fig.update_traces(marker_line_width=0, textposition="outside")
            fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.35)
        else:
            fig = go.Figure()
            fig.update_layout(**CHART_LAYOUT, title="⛪ Top Churches",
                              annotations=[dict(text="No data", showarrow=False, font=dict(size=16, color="#667eea"))])
        st.plotly_chart(fig, use_container_width=True)

def render_row5(fdf):
    r5c1, r5c2, r5c3 = st.columns(3)
    with r5c1:
        night_cols = [c for c in fdf.columns if c.startswith("Nights Staying in the Hotel")]
        nights = {c.split("(")[-1].replace(")", "").strip(): (fdf[c] == "Yes").sum() for c in night_cols}
        ndf = pd.DataFrame(list(nights.items()), columns=["Night", "Bookings"])
        ndf = ndf[ndf["Bookings"] > 0]
        if len(ndf) > 0:
            fig = px.bar(ndf, x="Night", y="Bookings", title="🌙 Hotel Nights",
                         color="Bookings", color_continuous_scale=["#667eea", "#f5576c"], text_auto=True)
            fig.update_traces(textposition="outside")
            fig.update_layout(**CHART_LAYOUT, showlegend=False, coloraxis_showscale=False)
        else:
            fig = go.Figure()
            fig.update_layout(**CHART_LAYOUT, title="🌙 Hotel Nights",
                              annotations=[dict(text="No data", showarrow=False, font=dict(size=16, color="#667eea"))])
        st.plotly_chart(fig, use_container_width=True)
    with r5c2:
        rp = fdf["Room 1 Preference"].dropna()
        rp = rp[rp.str.strip() != ""]
        if len(rp) > 0:
            rc = rp.value_counts().reset_index()
            rc.columns = ["Room Type", "Count"]
            fig = px.pie(rc, names="Room Type", values="Count", title="🛏️ Room Preference",
                         color_discrete_sequence=COLORS, hole=0.55)
            fig.update_traces(textinfo="value+label", textfont_size=11, marker=dict(line=dict(color="#1a1a2e", width=2)))
            fig.update_layout(**CHART_LAYOUT)
        else:
            fig = go.Figure()
            fig.update_layout(**CHART_LAYOUT, title="🛏️ Room Preference",
                              annotations=[dict(text="No data", showarrow=False, font=dict(size=16, color="#667eea"))])
        st.plotly_chart(fig, use_container_width=True)
    with r5c3:
        children = fdf[fdf["Which sessions would you like to attend? (Childrens Session)"].eq("Yes")]
        ca = children["Age of the Child"].dropna()
        ca = ca[ca.str.strip() != ""]
        if len(ca) > 0:
            ac = ca.value_counts().reset_index()
            ac.columns = ["Age", "Count"]
            fig = px.bar(ac, x="Age", y="Count", title=f"👶 Children ({len(children)})", color="Age",
                         color_discrete_sequence=COLORS, text_auto=True)
            fig.update_traces(marker_line_width=0, textposition="outside")
            fig.update_layout(**CHART_LAYOUT, showlegend=False, bargap=0.4)
        else:
            fig = go.Figure()
            fig.update_layout(**CHART_LAYOUT, title=f"👶 Children ({len(children)})",
                              annotations=[dict(text=f"{len(children)} registered", showarrow=False, font=dict(size=16, color="#667eea"))])
        st.plotly_chart(fig, use_container_width=True)

def render_airport(fdf):
    st.markdown("### ✈️ Airport Logistics")
    pickup_df = fdf[fdf["Do you need airport pickup?"].eq("Yes")][
        ["Full Name", "Pickup Airport", "Arrival Date", "Arrival Time", "Arrival Airline", "Arrival Flight #"]
    ].fillna("")
    dropoff_df = fdf[fdf["Do you need airport drop off?"].eq("Yes")][
        ["Full Name", "Drop Off Airport", "Departure Date", "Departure Time", "Departure Airline", "Departure Flight #"]
    ].fillna("")
    ac1, ac2 = st.columns(2)
    with ac1:
        st.markdown(f"**🛬 Pickups ({len(pickup_df)})**")
        if len(pickup_df) > 0:
            st.markdown(f'<div style="max-height:250px;overflow-y:auto;border-radius:8px;border:1px solid #1a1a3a;">{pickup_df.to_html(index=False, escape=True, classes="reg-table")}</div>', unsafe_allow_html=True)
        else:
            st.markdown("No pickup requests")
    with ac2:
        st.markdown(f"**🛫 Drop-offs ({len(dropoff_df)})**")
        if len(dropoff_df) > 0:
            st.markdown(f'<div style="max-height:250px;overflow-y:auto;border-radius:8px;border:1px solid #1a1a3a;">{dropoff_df.to_html(index=False, escape=True, classes="reg-table")}</div>', unsafe_allow_html=True)
        else:
            st.markdown("No drop-off requests")

def render_table(fdf):
    st.markdown("### 📋 Registrant Details")
    display_cols = ["Full Name", "Email", "Gender", "Age Group", "Ticket Level", "Status",
                    "Address (City)", "Address (State)", "Ticket Total ($ Amount)", "Sold Date"]
    table_df = fdf[display_cols].sort_values("Sold Date", ascending=False).reset_index(drop=True)
    search = st.text_input("🔍 Search registrants", "", placeholder="Type name, email, city...")
    if search:
        table_df = table_df[table_df.apply(lambda row: search.lower() in str(row.values).lower(), axis=1)]
    st.markdown(f"Showing {len(table_df)} registrants")
    st.markdown(f'<div style="max-height:450px;overflow-y:auto;border-radius:12px;border:1px solid #1a1a3a;">{table_df.to_html(index=False, escape=True, classes="reg-table")}</div>', unsafe_allow_html=True)
