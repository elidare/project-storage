import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from playsound import playsound  # To play sound when analysis is finished
import matplotlib.pyplot as plt
import numpy as np
import joblib

# Step 1: Load and Prepare Your Data
# Load data
# df = pd.read_csv("evmodel_summary.csv")
df = pd.read_csv("evmodel_summary.csv").sample(frac=0.8, random_state=42)  # For testing take smaller sample

# Drop missing values (recommended)
df = df.dropna(subset=["min_soc", "soc_diff", "max_power", "mean_temp", "sample_time"])

# Features and target
X = df[["min_soc", "soc_diff", "max_power", "mean_temp"]]
y = df["sample_time"]

# Step 3: Choose and Train a Model
model = Pipeline([
    ("model", RandomForestRegressor(
        n_estimators=50,
        random_state=42,
        n_jobs=-1
    ))
])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
start_time = time.time()
model.fit(X_train, y_train)
training_time = time.time() - start_time

print(f"✅ Training completed in {training_time:.2f} seconds")

# Step 4: Evaluate Performance
# Predictions
y_pred = model.predict(X_test)

# Metrics
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae:.2f}")
print(f"R² Score: {r2:.3f}")

# Step 5: Make Predictions
example = pd.DataFrame([{
    #"EVModel": "Volkswagen ID.4",
    "min_soc": 20,
    "soc_diff": 60,
    "max_power": 11000,
    "mean_temp": 5
}])

predicted_time = model.predict(example)[0]
print(f"⏱️ Predicted sample_time: {predicted_time:.2f}")


# Step 6: Feature Importance
# Extract the trained RandomForest model
rf = model.named_steps["model"]

feature_names = ["min_soc", "soc_diff", "max_power", "mean_temp"]

# Get feature importances
importances = rf.feature_importances_

# Sort features by importance
indices = np.argsort(importances)[::-1]

# Plot top 15 features
plt.figure(figsize=(10, 6))
plt.barh(np.array(feature_names)[indices][::-1],
         importances[indices][::-1], color="skyblue", edgecolor="black")
plt.xlabel("Feature Importance")
plt.title("Important Features for Predicting Sample Time")
plt.tight_layout()
plt.savefig("../images/feature_importance_no_EV.png", dpi=300)
plt.close()

print("📊 Feature importance graph saved as images/feature_importance_no_EV.png")

# Step 7: Save model
joblib.dump(model, "sample_time_predictor_08_50_no_EV.pkl")
print("💾 Model saved as sample_time_predictor_08_50_no_EV.pkl")

playsound('../extras/notification-metallic-chime-fast-gamemaster-audio-higher-tone-2-00-01.mp3')
