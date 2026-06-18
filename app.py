import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
import hashlib
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Student AI Dashboard", layout="wide")

# ---------------- MODEL ----------------
model = joblib.load("model.pkl")

# ---------------- ADMIN CREDENTIALS ----------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- USERS FILE ----------------
USER_FILE = "users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

with open(USER_FILE, "r") as f:
    users = json.load(f)

# ---------------- DATA FILE ----------------
DATA_FILE = "data.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["user", "date", "study_hours", "attendance", "sleep_hours", "marks"])
    df.to_csv(DATA_FILE, index=False)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False


# ---------------- AUTH PAGE ----------------
def auth_page():
    st.title("🎓 Student Performance AI System")

    menu = st.radio("Choose Option", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # ---------------- SIGN UP ----------------
    if menu == "Sign Up":
        if st.button("Create Account"):
            if username in users:
                st.error("User already exists ❌")
            else:
                users[username] = hash_password(password)
                with open(USER_FILE, "w") as f:
                    json.dump(users, f)
                st.success("Account created 🎉 Now login")

    # ---------------- LOGIN ----------------
    if menu == "Login":
        if st.button("Login"):

            # ADMIN LOGIN
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user = "admin"
                st.session_state.is_admin = True
                st.rerun()

            # USER LOGIN
            elif username in users and users[username] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.session_state.is_admin = False
                st.rerun()

            else:
                st.error("Invalid Credentials ❌")


# ---------------- LOGIN CHECK ----------------
if not st.session_state.logged_in:
    auth_page()
    st.stop()


# ---------------- ADMIN PANEL ----------------
if st.session_state.is_admin:
    st.title("🛡️ Admin Dashboard")

    st.subheader("👤 Registered Users")

    for user in users:
        st.write(user)

    st.subheader("🔧 Reset User Password")

    selected_user = st.selectbox("Select User", list(users.keys()))
    new_pass = st.text_input("New Password", type="password")

    if st.button("Reset Password"):
        users[selected_user] = hash_password(new_pass)

        with open(USER_FILE, "w") as f:
            json.dump(users, f)

        st.success("Password reset successfully ✅")

    if st.button("Logout Admin"):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        st.session_state.user = None
        st.rerun()

    st.stop()


# ---------------- USER DASHBOARD ----------------
st.sidebar.success(f"Logged in as {st.session_state.user}")

st.title("📊 Student Dashboard")
st.markdown("Track your performance, predict marks, and improve daily 🚀")

# ---------------- LOGOUT ----------------
if st.button("🔙 Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()


# ---------------- INPUT ----------------
study = st.slider("📚 Study Hours", 0, 12, 5)
attendance = st.slider("🏫 Attendance (%)", 0, 100, 75)
sleep = st.slider("😴 Sleep Hours", 0, 12, 6)
marks = st.slider("📝 Marks (Optional)", 0, 100, 50)


# ---------------- SAVE DATA ----------------
if st.button("💾 Save Data"):
    new_row = {
        "user": st.session_state.user,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "study_hours": study,
        "attendance": attendance,
        "sleep_hours": sleep,
        "marks": marks
    }

    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    st.success("Data Saved Successfully ✅")


# ---------------- AI PREDICTION ----------------
st.subheader("🤖 AI Prediction")

if st.button("Predict Score"):
    pred = model.predict([[study, attendance, sleep]])[0]

    st.markdown(f"### 🎯 Predicted Score: `{pred:.2f}`")

    if pred >= 80:
        st.balloons()
        st.success("🌟 Excellent Performance")
    elif pred >= 60:
        st.info("👍 Good Performance")
    else:
        st.warning("⚠️ Needs Improvement")


# ---------------- GRAPH ----------------
st.subheader("📊 Study Hours Trend")

df = pd.read_csv(DATA_FILE)
user_df = df[df["user"] == st.session_state.user]

if not user_df.empty:
    user_df = user_df.sort_values("date")
    st.line_chart(user_df.set_index("date")[["study_hours"]])
else:
    st.info("No data yet. Start saving entries 📊")


# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Student AI Dashboard | Built with Streamlit")