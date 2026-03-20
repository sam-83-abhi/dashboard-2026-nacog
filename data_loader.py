import pandas as pd
import streamlit as st
import pathlib

def clean_money(series):
    return pd.to_numeric(series.astype(str).str.replace("$","",regex=False).str.replace(",","",regex=False), errors="coerce").fillna(0)

@st.cache_data(ttl=3600)
def load_data(file):
    df = pd.read_csv(file, encoding="utf-8-sig")
    df["Sold Date"] = pd.to_datetime(df["Sold Date"], errors="coerce")
    for col in ["Ticket Price ($ Amount)", "Ticket Total ($ Amount)"]:
        df[col] = clean_money(df[col])
    df["Hotel Cost"] = clean_money(df["How many hotel rooms do you need? ($ Amount)"])
    df["Meal Cost"] = clean_money(df.get("Food: Do you wish to add a meal plan? ($ Amount)", pd.Series(dtype=str)))
    df["Full Name"] = df["Name (First Name)"].astype(str).str.strip() + " " + df["Name (Last Name)"].astype(str).str.strip()
    return df

def get_data():
    uploaded = st.sidebar.file_uploader("📂 Upload GeneralRegistration.csv", type="csv")
    local_csv = pathlib.Path("GeneralRegistration.csv")
    if uploaded:
        return load_data(uploaded)
    elif local_csv.exists():
        return load_data(str(local_csv))
    else:
        st.info("📂 Please upload your GeneralRegistration.csv file using the sidebar.")
        st.stop()
