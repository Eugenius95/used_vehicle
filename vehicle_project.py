import streamlit as st
#import numpy as np
import pandas as pd

df = pd.read_csv('/Users/eugenemonama/used_vehicle/cleanedvehicle.csv') # Reads CSV file
# print(df.head(10))
# 
st.set_page_config(page_title="Interactive dashboard", layout="wide")

# Heading on top
st.markdown("<h1 style='text-align: center;'>🚘MOTOR VEHICLE STOCK</h1>", unsafe_allow_html=True)

# Sidebar or top control for filters
st.subheader("🔎 Filter by Fuel Type and Price")

# Column layout for better UI
col1, col2 = st.columns(2)

with col1:
    # Fuel type selector
    fuel_types = df["fuel-type"].unique()
    selected_fuel = st.selectbox("Fuel Type", fuel_types)

with col2:
    # Price range slider
    min_price = int(df["price"].min()) #minimum price in $ 
    max_price = int(df["price"].max()) # maximum price in $
    price_range = st.slider("Price Range (USD)", min_price, max_price, (min_price, max_price), step=500)

# Apply filters
filtered_df = df[
    (df["fuel-type"] == selected_fuel) &
    (df["price"] >= price_range[0]) &
    (df["price"] <= price_range[1])
]

# Display results
st.markdown(f"### 📊 Results: {selected_fuel.capitalize()} Vehicles Priced ${price_range[0]} - ${price_range[1]}")
st.dataframe(filtered_df)
