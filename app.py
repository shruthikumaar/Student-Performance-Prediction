import streamlit as st
import numpy as np
import joblib

# ---------------- LOAD MODEL ----------------
model = joblib.load("model.pkl")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Student AI", layout="wide")

st.title("🎓 Student Performance Predictor")

st.markdown("Enter details to predict student marks using AI")

# ---------------- INPUT UI ----------------
col1, col2, col3 = st.columns(3)

with col1:
    study_hours = st.slider("Study Hours", 0, 12, 5)

with col2:
    attendance = st.slider("Attendance (%)", 0, 100, 75)

with col3:
    sleep_hours = st.slider("Sleep Hours", 0, 12, 6)

# ---------------- PREDICTION ----------------
if st.button("Predict"):
    input_data = np.array([[study_hours, attendance, sleep_hours]])
    prediction = model.predict(input_data)[0]

    st.success(f"Predicted Marks: {prediction:.2f}")

    if prediction >= 80:
        st.balloons()
        st.info("Excellent Performance 🌟")
    elif prediction >= 60:
        st.info("Good Performance 👍")
    else:
        st.warning("Needs Improvement ⚠️")