import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# ---------------- LOAD DATA ----------------
DATA_PATH = "data\student_data.csv"

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(" student_data.csv not found. Please place it in project root folder.")

df = pd.read_csv(DATA_PATH)

# ---------------- CLEAN COLUMN NAMES ----------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("Columns in dataset:", df.columns)

# ---------------- REQUIRED COLUMNS ----------------
required_cols = ["study_hours", "attendance", "sleep_hours", "marks"]

missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    raise KeyError(f"❌ Missing columns in dataset: {missing_cols}")

# ---------------- FEATURES & TARGET ----------------
X = df[["study_hours", "attendance", "sleep_hours"]]
y = df["marks"]

# ---------------- TRAIN TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- MODEL ----------------
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ---------------- SAVE MODEL ----------------
joblib.dump(model, "model.pkl")

print("✅ model.pkl trained and saved successfully!")