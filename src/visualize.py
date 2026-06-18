import pandas as pd
import matplotlib.pyplot as plt
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "..", "data", "student_data.csv")

df = pd.read_csv(data_path)

# Create graph
plt.scatter(df["StudyHours"], df["Marks"])

plt.title("Study Hours vs Marks")
plt.xlabel("Study Hours")
plt.ylabel("Marks")

plt.savefig("../study_hours_vs_marks.png")

print("Graph saved successfully!")