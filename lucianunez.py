import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Airbnb Analysis", layout="wide")

st.title("🏡 Airbnb Analysis")
st.markdown("Analyzing *Airbnb* data in :blue[Madrid]")


df = pd.read_csv("airbnb.csv")
df["last_review"] = pd.to_datetime(df["last_review"], errors='coerce').astype(str)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Overview", "Top Hosts", "Price Analysis", "Maps", "Insights", "Price Simulator"])

if page == "Overview":
    st.subheader("Dataset Overview")
    st.dataframe(df[["name", "neighbourhood_group", "neighbourhood", "price", "reviews_per_month", "last_review"]].head())

elif page == "Top Hosts":
    st.subheader("Top Hosts in Madrid")
    hosts = df.groupby(["host_id", "host_name"]).size().reset_index()
    hosts["host"] = hosts["host_id"].astype(str) + " - " + hosts["host_name"]
    top = st.radio("Show top:", [3, 5, 10, 20, 50])
    top_hosts = hosts.sort_values(by=0, ascending=False).head(top)
    fig = px.bar(top_hosts, x=0, y="host", orientation='h', hover_name="host_name", labels={"0": "Listings"})
    st.plotly_chart(fig, use_container_width=True)

elif page == "Price Analysis":
    tab1, tab2 = st.tabs(["By Neighbourhood Group", "By Listing Type"])
    
    with tab1:
        st.subheader("Prices by Neighbourhood Group")
        fig1 = px.box(df[df["price"] < 600], x="neighbourhood_group", y="price", labels={"price": "Price (€)", "neighbourhood_group": "Group"})
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        st.subheader("Prices by Listing Type")
        fig2 = px.box(df[df["price"] < 600], x="room_type", y="price", labels={"price": "Price (€)", "room_type": "Type"})
        fig2.update_layout(yaxis=dict(range=[0, 600]))
        st.plotly_chart(fig2, use_container_width=True)


elif page == "Insights":
    st.subheader("Most Reviewed Apartments")
    top_reviews = df.sort_values(by="reviews_per_month", ascending=False).head(10)
    fig3 = px.bar(top_reviews, x="neighbourhood", y="reviews_per_month", color="room_type", title="Top 10 Reviewed", labels={"neighbourhood": "Area", "reviews_per_month": "Reviews/Month"})
    st.plotly_chart(fig3, use_container_width=True)
    
    st.subheader("Price vs Reviews")
    fig4 = px.scatter(df, x="price", y="reviews_per_month", color="room_type", title="Price vs Reviews", labels={"price": "Price (€)", "reviews_per_month": "Reviews/Month"})
    fig4.update_layout(xaxis=dict(range=[0, 1000]), yaxis=dict(range=[0, 30]))
    st.plotly_chart(fig4, use_container_width=True)

elif page == "Maps":
    st.subheader("Listings Map")
    group = st.selectbox("Select a group", df["neighbourhood_group"].unique())
    df_map = df[df["neighbourhood_group"] == group]
    st.map(df_map[["latitude", "longitude"]])

elif page == "Price Simulator":
    st.subheader("Price Simulator")
    area = st.selectbox("Select Area", df["neighbourhood"].unique())
    room = st.selectbox("Select Type", df["room_type"].unique())
    guests = st.slider("Guests", 1, 10, 2)
    
    filtered = df[(df["neighbourhood"] == area) & (df["room_type"] == room)]
    prices = filtered["price"].describe()[["25%", "50%", "75%"]]
    
    st.write(f"For a **{room}** in **{area}** for **{guests}** guests:")
    st.write(f"Recommended Price Range:")
    st.write(f"- Lower: €{prices['25%']:.2f}")
    st.write(f"- Median: €{prices['50%']:.2f}")
    st.write(f"- Higher: €{prices['75%']:.2f}")
    
