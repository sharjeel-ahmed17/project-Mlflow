import streamlit as st
import requests

st.title("Ship Fuel Consumption Prediction")
st.write("Enter ship details to predict fuel consumption")

# Input fields
ship_type = st.selectbox("Ship Type", [
    "Oil Service Boat", "Tanker Ship", "Surfer Boat", "Fishing Trawler"
])

month = st.selectbox("Month", [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
])

distance = st.number_input("Distance (km)")

fuel_type = st.selectbox("Fuel Type", [
    "Diesel", "HFO"
])

weather_conditions = st.selectbox("Weather Conditions", [
    "Calm", "Stormy", "Moderate"
])

engine_efficiency = st.number_input("Engine Efficiency (%)")

# Predict button
if st.button("Predict"):
    response = requests.post(
        "http://localhost:8000/predict",
        params={
            "ship_type": ship_type,
            "month": month,
            "distance": distance,
            "fuel_type": fuel_type,
            "weather_conditions": weather_conditions,
            "engine_efficiency": engine_efficiency
        }
    )
    result = response.json()
    st.success(f"Predicted Fuel Consumption: **{result['predicted_fuel_consumption']} Litres**")