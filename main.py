import streamlit as st
import pandas as pd
import altair as alt

def load_data():
    df = pd.read_csv("chocosales.csv")
    # convert date column to datetime data type
    df.Date = pd.to_datetime(df.Date, format="%d-%b-%y")
    # convert the Amount column to float datatype
    df.Amount = df.Amount.str.replace("$", "").str.replace(",", "").str.strip().astype("float")
    df["Price/Box"] = round(df.Amount / df["Boxes Shipped"], 2)
    return df

df = load_data()

# App title
st.title("Chocolates Sales App")

# create filters
filters = {
    "Sales Person": df["Sales Person"].unique(),
    "Country": df["Country"].unique(),
    "Product": df["Product"].unique(),
}

# store user selection
selected_filters = {}

# generate multi-select widgets dynamically
for key, options in filters.items():
    selected_filters[key]=st.sidebar.multiselect(key,options)

# let's have the full data
filtered_df = df.copy()

# apply filter selection to the data
for key, selected_values in selected_filters.items():
    if selected_values:
        filtered_df = filtered_df[filtered_df[key].isin(selected_values) ]


# display the data
st.dataframe(filtered_df.head())

# calculations
no_of_transactions = len(filtered_df)
total_revenue = filtered_df["Amount"].sum()
total_boxes = filtered_df["Boxes Shipped"].sum()
no_of_products = filtered_df["Product"].nunique()

# streamlit column component
col1, col2, col3, col4, = st.columns(4)
with col1:
    st.metric("Transactions", no_of_transactions)

with col2:
    st.metric("Total Revenue", total_revenue)

with col3:
    st.metric("Total Boxes", total_boxes)

with col4:
    st.metric("Products", no_of_products)

# charts
st.subheader("Products with Largest Revenue")

top_products = filtered_df.groupby("Product")["Amount"].sum().nlargest(5).reset_index()

st.write(top_products)

# altair plotting library

st.subheader("Top 5 Products by Revenue")
# configure the bar chart
chart = alt.Chart(top_products).mark_bar().encode(
    x=alt.X('Amount:Q', title="Revenue ($)"),
    y=alt.Y("Product:N"),
    color = alt.Color("Product", legend = None)
).properties(height = 300)

# display the chart
st.altair_chart(chart, use_container_width= True)
