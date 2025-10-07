import pandas as pd
import warnings
import joblib


# To exclude UserWarning: X does not have valid feature names, but LGBMRegressor was fitted with feature names
warnings.filterwarnings("ignore", message="X does not have valid feature names")

model = joblib.load("sample_time_predictor_LGBM.pkl")

# # EVModel,sample_time,min_soc,soc_diff,mean_power,max_power,mean_temp
# # BYD Atto 3,990,10.0,45.0,58921.346534653465,69784.0,9.0
# example = pd.DataFrame([{
#     "EVModel": "BYD Atto 3",
#     "min_soc": 10,
#     "soc_diff": 45,
#     "max_power": 70000,
#     "mean_temp": 9
# }])
# # Predicted sample_time: 1276.39, real 990, 5 min more

# # "Inmotion, Opel Mokka-e, Peugeot e-208, Peugeot e-Expert",1080,26.0,30.0,36660.34112149533,40401.0,3.0
# example = pd.DataFrame([{
#     "EVModel": "Peugeot e-Expert",
#     "min_soc": 26,
#     "soc_diff": 30,
#     "max_power": 40000,
#     "mean_temp": 3
# }])
# # Predicted sample_time: 1490.11, real 1080, 6 min more

# "Audi Q4 e-tron, Skoda Enyaq iV, Volkswagen ID.4, Volkswagen ID.5, Volkswagen ID.Buzz",1760,57.0,32.0,53920.22014260249,63714.0,16.0
# Mercedes-Benz eVito,2720,64.0,32.0,33398.09541511772,45202.0,2.0
# "Audi Q8 e-tron, Audi e-tron",1070,84.0,15.0,50716.692660550456,81566.0,29.0
# "Audi Q4 e-tron, Volkswagen ID.5, Skoda Enyaq 85, Porsche Macan",2270,63.0,35.0,46407.59336419753,71141.0,22.0
# Maxus eDeliver 9,2720,43.0,51.0,61321.9222614841,73344.0,19.0
sample_times = [1760, 2720, 1070, 2270, 2720]
test_data = pd.DataFrame([
    {"EVModel": "Skoda Enyaq iV", "min_soc": 57, "soc_diff": 32, "max_power": 65000, "mean_temp": 16},
    {"EVModel": "Mercedes-Benz eVito", "min_soc": 64, "soc_diff": 32, "max_power": 50000, "mean_temp": 2},
    {"EVModel": "Audi e-tron", "min_soc": 84, "soc_diff": 15, "max_power": 80000, "mean_temp": 29},
    {"EVModel": "Skoda Enyaq", "min_soc": 63, "soc_diff": 35, "max_power": 70000, "mean_temp": 22},
    {"EVModel": "Maxus eDeliver 9", "min_soc": 43, "soc_diff": 51, "max_power": 73000, "mean_temp": 19},
])

# Predict using the loaded pipeline
predicted_sample_time = model.predict(test_data)

# Show results
for i, time_sec in enumerate(predicted_sample_time):
    print(
        f"Example {i + 1}: Predicted sample_time = {time_sec:.2f} seconds; "
        f"real sample {sample_times[i]}, difference {time_sec - sample_times[i]}")

"""
Example 1: Predicted sample_time = 1820.99 seconds;real sample 1760, difference 60.99351072669015
Example 2: Predicted sample_time = 2541.38 seconds;real sample 2720, difference -178.61553769758848
Example 3: Predicted sample_time = 942.16 seconds;real sample 1070, difference -127.83999683583829
Example 4: Predicted sample_time = 2240.12 seconds;real sample 2270, difference -29.882598255846005
Example 5: Predicted sample_time = 2464.89 seconds;real sample 2720, difference -255.1123285688027
"""
