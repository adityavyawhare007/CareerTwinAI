import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
data = pd.read_csv("dataset/career_dataset.csv")

# Create Label Encoders
encoders = {}

columns = [
    "Education",
    "Favorite_Subject",
    "Programming_Skill",
    "Communication",
    "Problem_Solving",
    "Interest",
    "Work_Style",
    "Career"
]

for column in columns:
    encoder = LabelEncoder()
    data[column] = encoder.fit_transform(data[column])
    encoders[column] = encoder

# Features (X)
X = data.drop("Career", axis=1)

# Target (Y)
y = data["Career"]

# Train Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Save Model
joblib.dump(model, "ml_model/career_model.pkl")

# Save Encoders
joblib.dump(encoders, "ml_model/label_encoders.pkl")

print("✅ AI Model Trained Successfully!")
print("✅ career_model.pkl created.")
print("✅ label_encoders.pkl created.")