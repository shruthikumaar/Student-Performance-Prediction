import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Load dataset
df = pd.read_csv("../data/student_data.csv")

# Features and target
X = df[["StudyHours"]]
y = df["Marks"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "../models/student_model.pkl")

# Prediction
prediction = model.predict(pd.DataFrame({"StudyHours": [7]}))

print("Predicted Marks for 7 study hours:", prediction[0])
print("Model saved successfully!")