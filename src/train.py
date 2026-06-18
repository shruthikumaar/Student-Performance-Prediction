import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib

# Load dataset
df = pd.read_csv("../data/student_data.csv")

X = df[["StudyHours"]]
y = df["Marks"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Test model
y_pred = model.predict(X_test)

# Calculate accuracy
score = r2_score(y_test, y_pred)

print("R² Score:", round(score, 4))

# Save model
joblib.dump(model, "../models/student_model.pkl")

print("Model saved successfully!")