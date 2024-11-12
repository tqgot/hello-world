import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
# Assuming you have uploaded 'coffee_shop_sales.csv' in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload Coffee Shop Sales Dataset", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload a dataset to proceed.")
    st.stop()

# Preprocess data for analysis
data['transaction_date'] = pd.to_datetime(data['transaction_date'])
data['month_year'] = data['transaction_date'].dt.to_period('M')
data['weekday'] = data['transaction_date'].dt.weekday
data['hour'] = data['transaction_date'].dt.hour
data['sales'] = data['transaction_qty'] * data['unit_price']

# Sidebar filters
st.sidebar.header("Filter Panel")
selected_month = st.sidebar.selectbox("Select Month", data['month_year'].unique())
filtered_data = data[data['month_year'] == selected_month]

# Key Performance Indicators
total_sales = filtered_data['sales'].sum()
total_orders = filtered_data['transaction_id'].nunique()
total_quantity = filtered_data['transaction_qty'].sum()

# Month-over-Month metrics
previous_month_data = data[data['month_year'] == selected_month - 1]
prev_total_sales = previous_month_data['sales'].sum()
prev_total_orders = previous_month_data['transaction_id'].nunique()
prev_total_quantity = previous_month_data['transaction_qty'].sum()

sales_change = ((total_sales - prev_total_sales) / prev_total_sales) * 100 if prev_total_sales else 0
orders_change = ((total_orders - prev_total_orders) / prev_total_orders) * 100 if prev_total_orders else 0
quantity_change = ((total_quantity - prev_total_quantity) / prev_total_quantity) * 100 if prev_total_quantity else 0

# Display KPIs
st.title("☕ Coffee Shop Sales Dashboard")
st.markdown(f"### Sales Report for {selected_month}")
st.metric("Total Sales", f"${total_sales:,.0f}", f"{sales_change:.1f}% vs LM")
st.metric("Total Orders", f"{total_orders:,}", f"{orders_change:.1f}% vs LM")
st.metric("Total Quantity Sold", f"{total_quantity:,}", f"{quantity_change:.1f}% vs LM")

# Sales Trend Over the Period
st.subheader("Sales Trend Over the Period")
sales_trend = data.groupby(data['transaction_date'].dt.date)['sales'].sum()
st.line_chart(sales_trend)

# Sales by Weekday/Weekend
# st.subheader("Sales by Weekday / Weekend")
# filtered_data['is_weekend'] = filtered_data['weekday'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
# weekday_sales = filtered_data.groupby('is_weekend')['sales'].sum()
# st.pie_chart(weekday_sales)
# Sample data for demonstration (replace this with your actual data)
data = {
    'Weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    'Sales': [1000, 1200, 1100, 1400, 900, 700, 800]
}
weekday_sales = pd.DataFrame(data)

# Plotting the pie chart using Plotly
fig = px.pie(weekday_sales, values='Sales', names='Weekday', title="Sales by Weekday")

# Displaying the plot in Streamlit
st.plotly_chart(fig)

# Sales by Store Location
st.subheader("Sales by Store Location")
store_sales = filtered_data.groupby('store_location')['sales'].sum().sort_values()
st.bar_chart(store_sales)

# Sales by Product Category
st.subheader("Sales by Product Category")
product_category_sales = filtered_data.groupby('product_category')['sales'].sum().sort_values()
st.bar_chart(product_category_sales)

# Sales by Product Type
st.subheader("Sales by Product Type")
product_type_sales = filtered_data.groupby('product_type')['sales'].sum().sort_values()
st.bar_chart(product_type_sales)

# Sales Heatmap by Days and Hours
st.subheader("Sales by Days and Hours")
heatmap_data = filtered_data.pivot_table(values='sales', index='weekday', columns='hour', aggfunc='sum', fill_value=0)
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(heatmap_data, cmap="YlOrRd", ax=ax, annot=True, fmt=".1f")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Day of Week")
ax.set_title("Sales Heatmap")
st.pyplot(fig)

# Tooltip & Annotations (e.g., Peak Sales Times)
st.caption("Hover over visuals to see detailed insights.")

# Optionally, add additional insights or tips for users based on observed patterns
if sales_change > 20:
    st.success("Sales have significantly increased compared to the last month!")
elif sales_change < -20:
    st.warning("Sales have significantly decreased compared to the last month.")

st.sidebar.markdown("#### Instructions")
st.sidebar.info("Use the filters to navigate through months and see how the sales and orders vary by time and location.")

st.sidebar.markdown("#### About")
st.sidebar.write("This dashboard provides an interactive way for shop owners to track their coffee shop's sales, identify patterns, and make data-driven decisions.")
