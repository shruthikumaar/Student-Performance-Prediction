import streamlit as st
import numpy as np
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Performance AI",
    page_icon="🎓",
    layout="wide"
)

# ---------------- SAFE MODEL LOADING ----------------
try:
    model = joblib.load("model.pkl")
except:
    model = None
    st.error("⚠️ Model file not found. Please ensure 'model.pkl' is in the same folder.")

# ---------------- HEADER ----------------
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
        }
        .sub-text {
            text-align: center;
            font-size: 18px;
            color: gray;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 Student Performance AI System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Predict performance and understand student learning behavior using AI</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------- LAYOUT ----------------
left, middle, right = st.columns([1, 2, 1])

with middle:
    st.subheader("📌 Enter Student Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        study_hours = st.slider("📚 Study Hours", 0, 12, 5)

    with col2:
        attendance = st.slider("🏫 Attendance (%)", 0, 100, 75)

    with col3:
        sleep = st.slider("😴 Sleep Hours", 0, 12, 6)

    st.markdown("")

    predict_btn = st.button("🚀 Predict Performance")

    if predict_btn:
        if model is None:
            st.error("Model not loaded. Please check model.pkl")
        else:
            input_data = np.array([[study_hours, attendance, sleep]])

            with st.spinner("Analyzing performance..."):
                prediction = model.predict(input_data)

            score = float(prediction[0])

            st.markdown("---")

            # BIG RESULT BOX
            st.markdown(f"""
                <div style="
                    padding: 25px;
                    border-radius: 15px;
                    background-color: #1f1f2e;
                    text-align: center;
                ">
                    <h2 style="color:white;">🎯 Predicted Score</h2>
                    <h1 style="color:#00ffcc;">{score:.2f} / 100</h1>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("")

            # Performance category
            if score >= 80:
                st.success("🌟 Excellent Performance")
                st.balloons()
            elif score >= 60:
                st.info("👍 Good Performance - Can Improve")
            else:
                st.warning("⚠️ Needs Improvement")

# ---------------- FULL WIDTH INFO SECTION ----------------
st.markdown("---")

colA, colB = st.columns(2)

with colA:
    st.subheader("📊 How AI Works")
    st.write("""
    This system uses Machine Learning to analyze:
    - Study habits
    - Attendance patterns
    - Sleep cycle

    Then predicts expected exam performance.
    """)

with colB:
    st.subheader("📈 Improvement Strategy")
    st.write("""
    ✔ Study consistently (4–6 hrs/day)  
    ✔ Maintain attendance above 75%  
    ✔ Sleep 6–8 hours daily  
    ✔ Avoid last-minute preparation  
    """)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Built using Streamlit | Student Performance AI System")