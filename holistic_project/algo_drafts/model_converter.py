import joblib

# Load your existing model
model = joblib.load("sample_time_predictor_LGBM.pkl")

# Extract the regressor
lgb_model = model.named_steps["model"]
lgb_model.booster_.save_model("lgbm_model.txt")

# Save preprocessing metadata
import json
preprocessor = model.named_steps["preprocessor"]
json.dump(preprocessor.get_feature_names_out().tolist(), open("features.json", "w"))
