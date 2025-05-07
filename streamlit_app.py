import streamlit as st
import pandas as pd

st.set_page_config(page_title="Alkelink Dashboard", layout="wide")

# Hardcoded users
VALID_USERS = {
    "daniel-sitompul": "Danieliscool123!",
    "rashmi-varma": "Danieliscool123!"
}

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login form
if not st.session_state.authenticated:
    st.title("🔐 Login to Alkelink Dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        if username in VALID_USERS and VALID_USERS[username] == password:
            st.session_state.authenticated = True
            st.session_state.user = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("❌ Invalid username or password")

    st.stop()  # Stop here if not authenticated

# If authenticated, show the dashboard
st.sidebar.markdown(f"👤 Logged in as: **{st.session_state.user}**")
st.sidebar.button("🚪 Log out", on_click=lambda: st.session_state.update({"authenticated": False}))

# ======== DASHBOARD =========
df = pd.read_csv("data/historical_medication_transactions_2025.csv")

st.title("💊 Medication Transactions Dashboard")
st.markdown("**Data from January to April 2025**")

st.sidebar.header("🔍 Filter Data")
med_names = df["Medication_Name"].dropna().astype(str).unique()
med_filter = st.sidebar.multiselect("Select Medication(s):", sorted(med_names))
date_range = st.sidebar.date_input("Select Date Range:", [])

filtered_df = df.copy()
if med_filter:
    filtered_df = filtered_df[filtered_df["Medication_Name"].isin(med_filter)]
if len(date_range) == 2:
    start = date_range[0].strftime("%Y/%m/%d")
    end = date_range[1].strftime("%Y/%m/%d")
    filtered_df = filtered_df[(filtered_df["Date"] >= start) & (filtered_df["Date"] <= end)]

st.metric("Total Transactions", len(filtered_df))
st.write(f"Showing **{len(filtered_df)}** records")
st.dataframe(filtered_df)

# Graph 1: Daily transactions
st.subheader("📈 Transactions per Day")
chart_df = filtered_df.groupby("Date").size().reset_index(name="Transactions")
chart_df["Date"] = pd.to_datetime(chart_df["Date"], errors="coerce")
chart_df = chart_df.sort_values("Date")
st.bar_chart(chart_df.set_index("Date"))

# Graph 2: Daily transactions per medication
st.subheader("📈 Daily Transactions per Medication")
filtered_df["Date"] = pd.to_datetime(filtered_df["Date"], errors="coerce")
line_df = filtered_df.groupby(["Date", "Medication_Name"]).size().reset_index(name="Transactions")
pivot_df = line_df.pivot(index="Date", columns="Medication_Name", values="Transactions").fillna(0).sort_index()
st.line_chart(pivot_df)
