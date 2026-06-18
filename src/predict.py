import joblib
import pandas as pd

# Load saved model
model = joblib.load("../models/student_model.pkl")

# New data for prediction
new_data = pd.DataFrame({"StudyHours": [8]})

# Predict
prediction = model.predict(new_data)

print("Predicted Marks:", prediction[0])