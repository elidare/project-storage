import csv


models = set()
with open("../data_analysis/transactions_per_model_Finland.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        mds = [m.lower() for m in row["EVModel"].split(', ')]
        models.update(mds)
    sorted_models = sorted(models)


with open("unique_ev_models.txt", "w", encoding="utf-8") as f:
    for model in sorted_models:
        f.write(f"{model}\n")
