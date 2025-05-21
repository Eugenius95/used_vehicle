import streamlit as st
import pandas as pd
import numpy as np
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
# Set page title and configuration
st.set_page_config(page_title="Interactive Data Table Example", layout="wide")

# Add a title and description
st.title("Interactive Data Table Demo")
st.write("This example shows how to create and filter data tables in Streamlit.")

# Create a sample dataframe# The `@st.cache_data` decorator in the provided Streamlit code snippet is
# used to cache the result of a function that generates data. This
# decorator is a part of Streamlit's caching mechanism, which helps improve
# the performance of the app by storing the result of the function and
# returning it from the cache when the function is called with the same
# input parameters.

@st.cache_data
def generate_data():
    # Create random sales data
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    
    products = ["Laptop", "Smartphone", "Tablet", "Monitor", "Headphones"]
    regions = ["North", "South", "East", "West", "Central"]
    
    data = {
        "Date": np.random.choice(dates, 500),
        "Product": np.random.choice(products, 500),
        "Region": np.random.choice(regions, 500),
        "Sales": np.random.randint(5, 100, 500) * 10,
        "Units": np.random.randint(1, 10, 500),
        "Customer_Rating": np.round(np.random.uniform(1, 5, 500), 1)
    }
    
    df = pd.DataFrame(data)
    return df

# Generate the data
df = generate_data()

# Display sidebar filters
st.sidebar.header("Filter Data")

# Date range filter
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Product filter
all_products = df["Product"].unique().tolist()
selected_products = st.sidebar.multiselect(
    "Select Products",
    options=all_products,
    default=all_products
)

# Region filter
all_regions = df["Region"].unique().tolist()
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=all_regions,
    default=all_regions
)

# Sales range filter
min_sales = int(df["Sales"].min())
max_sales = int(df["Sales"].max())
sales_range = st.sidebar.slider(
    "Sales Range",
    min_value=min_sales,
    max_value=max_sales,
    value=(min_sales, max_sales)
)

# Apply filters
filtered_df = df.copy()

# Date filter
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df["Date"].dt.date >= start_date) & 
                             (filtered_df["Date"].dt.date <= end_date)]

# Product filter
if selected_products:
    filtered_df = filtered_df[filtered_df["Product"].isin(selected_products)]

# Region filter
if selected_regions:
    filtered_df = filtered_df[filtered_df["Region"].isin(selected_regions)]

# Sales filter
filtered_df = filtered_df[(filtered_df["Sales"] >= sales_range[0]) & 
                         (filtered_df["Sales"] <= sales_range[1])]

# Create tabs for different view options
tab1, tab2, tab3 = st.tabs(["Data Table", "Sales Summary", "Settings"])

with tab1:
    # Display table stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(filtered_df))
    with col2:
        st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
    with col3:
        st.metric("Average Rating", f"{filtered_df['Customer_Rating'].mean():.1f}/5.0")
    
    # Add search functionality
    search_term = st.text_input("Search in data (any column)")
    
    if search_term:
        # Convert all to string for searching
        search_mask = np.column_stack([
            filtered_df[col].astype(str).str.contains(search_term, case=False, na=False)
            for col in filtered_df.columns
        ]).any(axis=1)
        filtered_df = filtered_df[search_mask]
    
    # Display the data table with pagination
    st.dataframe(
        filtered_df,
        use_container_width=True,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "Sales": st.column_config.NumberColumn("Sales ($)", format="$%d"),
            "Customer_Rating": st.column_config.NumberColumn("Rating", format="%.1f ⭐")
        },
        hide_index=True
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download filtered data as CSV",
        csv,
        "filtered_data.csv",
        "text/csv",
        key='download-csv'
    )

with tab2:
    # Create summary tables
    st.subheader("Sales Summary by Product")
    product_summary = filtered_df.groupby("Product").agg({
        "Sales": ["sum", "mean", "count"],
        "Units": "sum",
        "Customer_Rating": "mean"
    })
    product_summary.columns = ["Total Sales", "Avg Sale", "Transactions", "Units Sold", "Avg Rating"]
    st.dataframe(product_summary.sort_values("Total Sales", ascending=False), use_container_width=True)
    
    st.subheader("Sales Summary by Region")
    region_summary = filtered_df.groupby("Region").agg({
        "Sales": ["sum", "mean", "count"],
        "Units": "sum",
        "Customer_Rating": "mean"
    })
    region_summary.columns = ["Total Sales", "Avg Sale", "Transactions", "Units Sold", "Avg Rating"]
    st.dataframe(region_summary.sort_values("Total Sales", ascending=False), use_container_width=True)

with tab3:
    # Settings for table display
    st.subheader("Table Display Settings")
    col_options = st.multiselect(
        "Select columns to display",
        options=df.columns.tolist(),
        default=df.columns.tolist()
    )
    
    sort_col = st.selectbox("Sort by column", options=df.columns.tolist())
    sort_ascending = st.checkbox("Sort ascending", value=False)
    
    # Display settings applied
    if col_options:
        sorted_df = filtered_df[col_options].sort_values(by=sort_col, ascending=sort_ascending)
        st.dataframe(sorted_df, use_container_width=True)

# Add info about the data and app
st.sidebar.markdown("---")
st.sidebar.info("""
This is a demo showcasing Streamlit's data table capabilities with filtering, 
searching, and customization options. The data is randomly generated.
""")