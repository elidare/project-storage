import pandas as pd
import warnings
import joblib

warnings.filterwarnings("ignore", message="X does not have valid feature names")

model = joblib.load("sample_time_predictor_LGBM.pkl")


def get_estimate_charging_time(ev_model, current_soc, soc_diff, max_power, temp):
    test_data = pd.DataFrame([{
        "EVModel": ev_model,
        "min_soc": current_soc,
        "soc_diff": soc_diff,
        "max_power": max_power,
        "mean_temp": temp
    }])
    predicted_sample_time = model.predict(test_data)
    return predicted_sample_time.item()

