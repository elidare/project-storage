import pandas as pd
import numpy as np
import warnings
import joblib
import time
import matplotlib.pyplot as plt


from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from lightgbm import LGBMRegressor
from playsound import playsound  # To play sound when analysis is finished
from math import sqrt

# To exclude UserWarning: X does not have valid feature names, but LGBMRegressor was fitted with feature names
warnings.filterwarnings("ignore", message="X does not have valid feature names")

# === Step 1: Load Data ===
df = pd.read_csv("evmodel_summary.csv")

# Features and target
categorical = ["EVModel"]
numeric = ["min_soc", "soc_diff", "max_power", "mean_temp"]
target = "sample_time"

X = df[categorical + numeric]
y = df[target]

# === Step 2: Split Data ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Step 3: Preprocessor ===
preprocessor = ColumnTransformer(transformers=[
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ("num", StandardScaler(), numeric)
])

# === Step 4: Pipeline ===
model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LGBMRegressor(
        n_estimators=400,
        learning_rate=0.1,
        num_leaves=50,
        subsample=1.0,
        colsample_bytree=1.0,
        random_state=42
    ))
])

# === Step 5: Train Model (with timing) ===
start_time = time.time()
model.fit(X_train, y_train)
end_time = time.time()

training_time = end_time - start_time
print(f"✅ Model trained in {training_time:.2f} seconds")

# === Step 6: Evaluate ===
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = sqrt(mean_squared_error(y_test, y_pred))

print(f"R² Score: {r2:.3f}")
print(f"RMSE: {rmse:.3f}")

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

# Save pipeline
joblib.dump(model, "sample_time_predictor_LGBM_compressed.pkl", compress=3)
print("✅ Trained pipeline saved as sample_time_predictor_LGBM.pkl")

# # === Step 7: Feature Importance ===
# lgb_model = model.named_steps["model"]
# encoder = model.named_steps["preprocessor"].named_transformers_["cat"]
# encoded_feature_names = encoder.get_feature_names_out(categorical)
# feature_names = np.concatenate([encoded_feature_names, numeric])
# importances = lgb_model.feature_importances_
#
# # Sort by importance
# indices = np.argsort(importances)[::-1]
#
# # === Step 8: Plot ===
# plt.figure(figsize=(10, 6))
# plt.barh(np.array(feature_names)[indices][:30][::-1],
#          importances[indices][:30][::-1],
#          color="skyblue", edgecolor="black")
# plt.xlabel("Feature Importance")
# plt.title("Top 30 Important Features for Predicting Sample Time (LGBM + EVModel)")
# plt.tight_layout()
# plt.savefig("../images/feature_importance_LGBM_with_EV.png", dpi=300)
# plt.close()
#
# print("📊 Feature importance plot saved to ../images/feature_importance_LGBM_with_EV.png")

# # Param fitting
# param_grid = {
#     "model__n_estimators": [200, 300, 400, 500],
#     "model__learning_rate": [0.01, 0.05, 0.1],
#     "model__num_leaves": [31, 50, 70],
#     "model__subsample": [0.7, 0.8, 1.0],
# }
#
# search = RandomizedSearchCV(model, param_distributions=param_grid,
#                             n_iter=10, cv=3, scoring="r2", n_jobs=-1, random_state=42)
#
# search.fit(X_train, y_train)
# print("Best parameters:", search.best_params_)
# print("Best R²:", search.best_score_)
# # Best parameters: {'model__subsample': 1.0, 'model__num_leaves': 50, 'model__n_estimators': 400, 'model__learning_rate': 0.1}
# # Best R²: 0.8893514811264674

# Finish sound
playsound('../extras/notification-metallic-chime-fast-gamemaster-audio-higher-tone-2-00-01.mp3')
