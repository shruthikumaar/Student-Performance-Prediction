import streamlit as st
import joblib
import numpy as np

# Load model (FIXED)
model = joblib.load("models/student_model.pkl")

# UI
st.title("📊 Student Performance Predictor")
st.write("Predict marks based on study hours")

# Input
hours = st.number_input(
    "Enter Study Hours",
    min_value=0.0,
    max_value=24.0,
    step=0.5
)

# Predict
if st.button("Predict"):
    input_data = np.array([[hours]])
    prediction = model.predict(input_data)

    st.success(f"Predicted Marks: {prediction[0]:.2f}")