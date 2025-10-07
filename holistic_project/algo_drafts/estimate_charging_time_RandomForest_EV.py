import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
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

# Features and target
X = df[["EVModel", "min_soc", "soc_diff", "max_power", "mean_temp"]]
y = df["sample_time"]

# Step 2: Encode Categorical Variable
# Preprocess categorical and numeric features
categorical = ["EVModel"]
numeric = ["min_soc", "soc_diff", "max_power", "mean_temp"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", "passthrough", numeric)
    ]
)

# Step 3: Choose and Train a Model
# Create pipeline: preprocessing + model
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
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
    "EVModel": "Volkswagen ID.4",
    "min_soc": 20,
    "soc_diff": 60,
    "max_power": 11000,
    "mean_temp": 5
}])

predicted_time = model.predict(example)[0]
print(f"⏱️ Predicted sample_time: {predicted_time:.2f}")


# # Step 6: Feature Importance
# # Extract the trained RandomForest model
# rf = model.named_steps["regressor"]
# encoder = model.named_steps["preprocessor"].named_transformers_["cat"]
#
# # Get one-hot feature names
# encoded_feature_names = encoder.get_feature_names_out(categorical)
# feature_names = np.concatenate([encoded_feature_names, numeric])
#
# # Get feature importances
# importances = rf.feature_importances_
#
# # Sort features by importance
# indices = np.argsort(importances)[::-1]
#
# # Plot top 15 features
# plt.figure(figsize=(10, 6))
# plt.barh(np.array(feature_names)[indices][:30][::-1],
#          importances[indices][:30][::-1], color="skyblue", edgecolor="black")
# plt.xlabel("Feature Importance")
# plt.title("Top 30 Important Features for Predicting Sample Time")
# plt.tight_layout()
# plt.savefig("../images/feature_importance.png", dpi=300)
# plt.close()
#
# print("📊 Feature importance graph saved as images/feature_importance.png")
#
# # Step 7: Save model
# joblib.dump(model, "sample_time_predictor.pkl")
# print("💾 Model saved as sample_time_predictor.pkl")

playsound('../extras/notification-metallic-chime-fast-gamemaster-audio-higher-tone-2-00-01.mp3')
