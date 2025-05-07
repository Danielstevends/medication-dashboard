import streamlit as st
import pandas as pd

# Load your dataset from the data folder
df = pd.read_csv("data/historical_medication_transactions_2025.csv")

st.title("💊 Medication Transactions Dashboard")
st.markdown("**Data from January to April 2025**")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

# Ensure Medication_Name is treated as string and drop missing
med_names = df["Medication_Name"].dropna().astype(str).unique()
med_filter = st.sidebar.multiselect(
    "Select Medication(s):", 
    sorted(med_names)
)

date_range = st.sidebar.date_input("Select Date Range:", [])

# Filter logic
filtered_df = df.copy()

if med_filter:
    filtered_df = filtered_df[filtered_df["Medication_Name"].isin(med_filter)]

if len(date_range) == 2:
    start = date_range[0].strftime("%Y/%m/%d")
    end = date_range[1].strftime("%Y/%m/%d")
    filtered_df = filtered_df[
        (filtered_df["Date"] >= start) & (filtered_df["Date"] <= end)
    ]

#  Display metrics
st.metric("Total Transactions", len(filtered_df))
st.write(f"Showing **{len(filtered_df)}** records")
st.dataframe(filtered_df)

## Graph 1: Daily tansaction trend
st.subheader("📈 Transactions per Day")
chart_df = filtered_df.groupby("Date").size().reset_index(name="Transactions")
    
# Sort by date to make chart correct
chart_df["Date"] = pd.to_datetime(chart_df["Date"], errors="coerce")
chart_df = chart_df.sort_values("Date")
st.bar_chart(chart_df.set_index("Date"))


## Graph 2: Daily transactions per medication
st.subheader("📈 Daily Transactions per Medication")

# Make sure Date is datetime
filtered_df["Date"] = pd.to_datetime(filtered_df["Date"], errors="coerce")

# Group by Date and Medication
line_df = (
    filtered_df.groupby(["Date", "Medication_Name"])
    .size()
    .reset_index(name="Transactions")
)

# Pivot: rows = dates, columns = medication names
pivot_df = line_df.pivot(index="Date", columns="Medication_Name", values="Transactions").fillna(0)

# Sort by date
pivot_df = pivot_df.sort_index()

# Plot line chart
st.line_chart(pivot_df)
