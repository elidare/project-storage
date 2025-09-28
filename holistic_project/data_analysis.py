# pip install playsound==1.2.2
from playsound import playsound  # To play sound when analysis is finished
import matplotlib.pyplot as plt
import pandas as pd
import csv


filename = "public_passenger_dataset.csv"  # Downloaded CSV


# How many rows in csv in total
def get_lines_count():
    with open(filename, "r", encoding="utf-8") as f:
        row_count = sum(1 for row in f) - 1  # subtract header
    return row_count


# How many countries
def get_countries():
    country_counts = {}

    for chunk in pd.read_csv(filename, usecols=["country"], chunksize=1000000):
        # Count countries in this chunk
        chunk_counts = chunk["country"].value_counts()

        # Merge with global counts
        for country, count in chunk_counts.items():
            country_counts[country] = country_counts.get(country, 0) + count

    # Convert to a Series (sorted like value_counts)
    country_counts_series = pd.Series(country_counts).sort_values(ascending=False)

    return country_counts_series


# Shows min and max sampleTime10sIncrement for chosen country
def get_sample_min_max(country):
    country_filter = country

    chunks = pd.read_csv(filename, chunksize=1000000)
    filtered_list = []

    for chunk in chunks:
        subset = chunk[(chunk["country"] == country_filter)]
        filtered_list.append(subset)

    filtered_df = pd.concat(filtered_list).sort_values(by="soc")

    # Sort by soc ascending
    filtered_df = (filtered_df[["country", "EVModel", "year", "month", "soc", "tempC", "sampleTime10sIncrement", "weekday", "avgPowerW"]]
                   .sort_values(by="sampleTime10sIncrement", ascending=True))

    #filtered_df.to_csv(f"{country_filter}_filtered_data.csv", index=False)

    # 10 rows with smallest sampleTime10sIncrement
    min_soc = filtered_df.nsmallest(10, "sampleTime10sIncrement")
    # 10 rows with largest sampleTime10sIncrement
    max_soc = filtered_df.nlargest(10, "sampleTime10sIncrement")
    pd.set_option("display.max_columns", None)
    print("10 lowest sampleTime10sIncrement:")
    print(min_soc[["country", "EVModel", "month", "soc", "tempC", "sampleTime10sIncrement", "weekday", "avgPowerW"]])

    print("\n10 highest sampleTime10sIncrement:")
    print(max_soc[["country", "EVModel", "month", "soc", "tempC", "sampleTime10sIncrement", "weekday", "avgPowerW"]])

    return filtered_df


# Charges on weekdays graph for all the countries
def get_graph_weekdays():
    # Dictionary: {country: {weekday: count}}
    weekday_counts = {}

    # Process in chunks
    for chunk in pd.read_csv(filename, usecols=["country", "weekday"], chunksize=500000):
        grouped = chunk.groupby(["country", "weekday"]).size()

        for (country, weekday), count in grouped.items():
            if country not in weekday_counts:
                weekday_counts[country] = {}
            weekday_counts[country][weekday] = weekday_counts[country].get(weekday, 0) + count

    # Convert nested dict → DataFrame
    weekday_df = pd.DataFrame(weekday_counts).fillna(0).astype(int)

    # Reorder weekdays if needed
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_df = weekday_df.reindex(weekday_order)

    # Plot grouped bar chart
    weekday_df.plot(kind="bar", figsize=(12, 6))
    plt.ylabel("Number of Days (rows)")
    plt.xlabel("Weekday")
    plt.title("Counts of Weekdays per Country")
    plt.legend(title="Country")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("weekday_counts_by_country.png", dpi=300)
    plt.close()


# Get max sampleTime for each transaction, calculate mean power, min/max soc, add tempC
def get_max_sample(filename):
    stats = {}

    i = 0
    chunksize = 500_000  # adjust to your machine

    for chunk in pd.read_csv(filename, usecols=[
                             "country", "transactionId", "EVModel", "year", "month", "weekday",
                             "soc", "avgPowerW", "sampleTime10sIncrement", "tempC"
                             ],
                             chunksize=chunksize):
        # Show progress
        print(i * chunksize)
        i += 1

        # Drop NaN if necessary
        chunk = chunk.dropna(subset=["transactionId", "soc", "avgPowerW", "sampleTime10sIncrement", "tempC", "EVModel",
                                     "year", "month", "weekday"])

        grouped = chunk.groupby("transactionId").agg({
            "EVModel": "first",
            "year": "first",
            "month": "first",
            "weekday": "first",
            "sampleTime10sIncrement": ["min", "max"],
            "soc": ["min", "max"],
            "avgPowerW": ["mean", "max"],
            "tempC": ["mean"]
        })

        # Merge into dictionary
        for tid, row in grouped.iterrows():
            evmodel = row[("EVModel", "first")]
            year = row[("year", "first")]
            month = row[("month", "first")]
            weekday = row[("weekday", "first")]
            if tid not in stats:
                stats[tid] = {
                    "EVModel": evmodel,
                    "year": year,
                    "month": month,
                    "weekday": weekday,
                    "min_sample": row[("sampleTime10sIncrement", "min")],
                    "max_sample": row[("sampleTime10sIncrement", "max")],
                    "min_soc": row[("soc", "min")],
                    "max_soc": row[("soc", "max")],
                    "mean_power_sum": row[("avgPowerW", "mean")],
                    "mean_power_count": 1,
                    "max_power": row[("avgPowerW", "max")],
                    "mean_temp_sum": row[("tempC", "mean")],
                    "mean_temp_count": 1
                }
            else:
                stats[tid]["min_sample"] = min(stats[tid]["min_sample"], row[("sampleTime10sIncrement", "min")])
                stats[tid]["max_sample"] = max(stats[tid]["max_sample"], row[("sampleTime10sIncrement", "max")])
                stats[tid]["min_soc"] = min(stats[tid]["min_soc"], row[("soc", "min")])
                stats[tid]["max_soc"] = max(stats[tid]["max_soc"], row[("soc", "max")])
                # accumulate mean properly
                stats[tid]["mean_power_sum"] += row[("avgPowerW", "mean")]
                stats[tid]["mean_power_count"] += 1
                stats[tid]["max_power"] = max(stats[tid]["max_power"], row[("avgPowerW", "max")])
                stats[tid]["mean_temp_sum"] += row[("tempC", "mean")]
                stats[tid]["mean_temp_count"] += 1

    # Convert to DataFrame
    final_stats = pd.DataFrame([
        {
            "transactionId": tid,
            "EVModel": v["EVModel"],
            "year": v["year"],
            "month": v["month"],
            "weekday": v["weekday"],
            "min_sample": v["min_sample"],
            "max_sample": v["max_sample"],
            "min_soc": v["min_soc"],
            "max_soc": v["max_soc"],
            "mean_power": v["mean_power_sum"] / v["mean_power_count"],
            "max_power": v["max_power"],
            "mean_temp": v["mean_temp_sum"] / v["mean_temp_count"]
        }
        for tid, v in stats.items()
    ])

    pd.set_option("display.max_columns", None)
    print(final_stats.head())
    final_stats.to_csv(f"transactions_alldata_{filename}", index=False)


# Save only chosen country data to csv to make smaller csv
def save_filtered_as_csv(country):
    output_file = f"{country}_only.csv"

    chunksize = 500_000  # adjust as needed
    first_chunk = True

    for chunk in pd.read_csv(filename, chunksize=chunksize):
        country_chunk = chunk[chunk["country"] == country]
        if not country_chunk.empty:
            country_chunk.to_csv(
                output_file,
                mode="w" if first_chunk else "a",  # write first time, append after
                index=False,
                header=first_chunk  # write header only once
            )
            first_chunk = False

    print("Data saved to", output_file)


def sort_by_transaction_sample(filename):
    sorted_file = f"sorted_{filename}"
    # Load the filtered file
    df = pd.read_csv(filename)

    # Sort by transactionId, then by sampleTime10sIncrement
    df = df.sort_values(by=["transactionId", "sampleTime10sIncrement"], ascending=[True, True])

    # Save back to CSV
    df.to_csv(sorted_file, index=False)

    print("Sorted data saved to", sorted_file)


def get_unique_trans_number(filename):
    print(filename)
    df = pd.read_csv(filename, usecols=["transactionId"])
    unique_count = df["transactionId"].nunique()

    print("Unique transactions:", unique_count)


# Shows if there is any soc decrease during charging
# NB: Uses sorted files!!
def find_desc_soc(filename):
    output_file = "soc_desc_Finland.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write the header row
        writer.writerow(["transaction", "soc", "previous_soc", "sample_time", "previous_sample_time", "temp"])

        with open(filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)  # list of column names
            current_transaction = ""
            previous_soc = None
            previous_sample_time = None

            for row in reader:
                transaction, soc, sample_time, temp = row[0], int(row[6].replace(".0", "")), int(row[8]), row[7]
                if not current_transaction:
                    current_transaction = transaction
                if not previous_soc:
                    previous_soc = soc
                if not previous_sample_time:
                    previous_sample_time = sample_time

                if transaction == current_transaction:
                    if soc < previous_soc and sample_time > previous_sample_time:
                        print(transaction, soc, previous_soc, sample_time, previous_sample_time)
                        writer.writerow([transaction, soc, previous_soc, sample_time, previous_sample_time, temp])
                else:
                    current_transaction = transaction

                previous_soc = soc
                previous_sample_time = sample_time

        print("Data written to", output_file)


# NB: Uses sorted files!!
def find_transactions_over_80(filename):
    output_file = "transactions_over_80_Finland.csv"
    transactions = set()

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # list of column names

        for row in reader:
            transaction, soc = row[0], int(row[6].replace(".0", ""))

            if soc > 80:
                transactions.add(transaction)

    with open(output_file, "w", newline="", encoding="utf-8") as f2:
        writer = csv.writer(f2)

        # Write the header row
        writer.writerow(["transaction"])

        for transaction in list(transactions):
            writer.writerow([transaction])


# Uses aggregated file
def find_transactions_soc(filename):
    df = pd.read_csv(filename)
    output_file = f"filtered_{filename}"

    filtered = df[(df["min_soc"] < 20) & (df["max_soc"] > 95)]

    filtered.to_csv(output_file, index=False)

    print(filtered.head())
    print("Matching transactions:", len(filtered))


def get_graph_soc_sample(filename, transaction_id):
    chunksize = 500_000
    parts = []

    for chunk in pd.read_csv(filename, chunksize=chunksize):
        match = chunk[chunk["transactionId"] == transaction_id]
        if not match.empty:
            parts.append(match)

    # Combine and sort by sample time
    one_tx = pd.concat(parts).sort_values(by="sampleTime10sIncrement")

    # Plot SOC vs sample time
    plt.figure(figsize=(10, 6))
    plt.plot(one_tx["sampleTime10sIncrement"], one_tx["soc"], marker="o", linestyle="-")
    plt.title(f"SOC vs Sample Time (Transaction {transaction_id})")
    plt.xlabel("Sample Time (10s increment)")
    plt.ylabel("SOC")
    plt.grid(True)
    plt.tight_layout()

    # Save the figure as a PNG file
    plt.savefig(f"images/soc_vs_sampleTime_{transaction_id}.png", dpi=300)
    plt.close()

    print("Graph saved.png")


def get_graphs_soc_sample(filename):
    with open("filtered_transactions_sorted_Finland_only.csv", "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # list of column names

        counter = 0

        for row in reader:
            transaction_id = row[0]
            get_graph_soc_sample(filename, transaction_id)
            print(counter, "Done")

            counter += 1

            if counter > 20:  # get the first 20 graphs
                break


def get_graph_max_power(country):
    filename = f"transactions_sorted_{country}_only.csv"

    df = pd.read_csv(filename)

    plt.figure(figsize=(10,6))
    plt.hist(df["max_power"], bins=50, color="steelblue", edgecolor="black")
    plt.title("Distribution of Max Power")
    plt.xlabel("Max Power (W)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"images/max_power_distribution_{country}.png", dpi=300)
    plt.close()

    print("Histogram saved to max_power_distribution.png")

    # df["max_power"].plot(kind="density", figsize=(10,6), color="purple")
    # plt.title("Density Plot of Max Power")
    # plt.xlabel("Max Power (W)")
    # plt.tight_layout()
    # plt.savefig(f"images/max_power_density_{country}.png", dpi=300)
    # plt.close()


def get_graph_max_power_percentage(country):
    filename = f"transactions_sorted_{country}_only.csv"

    df = pd.read_csv(filename)

    # Define power bins (in kW or W depending on your data)
    #
    bins = [0, 11_000, 22_000, 50_000, 100_000, 150_000, 200_000, 250_000, 300_000, 350_000, 500_000]
    labels = ["0-11kW", "11-22kW", "22-50kW", "50-100kW",
              "100-150kW", "150-200kW", "200-250kW", "250-300kW", "300-350kW", "350+kW"]

    # Assign each max_power to a bin
    df["power_range"] = pd.cut(df["max_power"], bins=bins, labels=labels, right=False)

    # Count and calculate percentage
    counts = df["power_range"].value_counts().sort_index()
    percentages = (counts / len(df) * 100).round(2)

    # Print as a table
    print("📊 Percentage of records in each max_power range:")
    for rng, pct in percentages.items():
        print(f"{rng}: {pct}%")

    # Plot a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(percentages.index.astype(str), percentages.values, color="skyblue", edgecolor="black")
    plt.title("Percentage of Max Power by Range")
    plt.xlabel("Max Power Range")
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"images/max_power_percentage_{country}.png", dpi=300)
    plt.close()

    print("Chart saved to max_power_percentage.png")


def get_graph_max_sample_time_by_model(country):
    input_file = f"transactions_alldata_{country}_only.csv"
    output_csv = f"average_max_sample_by_EVModel_{country}.csv"
    df = pd.read_csv(input_file)

    # Group by EVModel and calculate the mean of max_sample
    avg_max_sample = df.groupby("EVModel")["max_sample"].mean().sort_values()
    avg_max_sample.to_csv(output_csv, header=["average_max_sample"])

    # Plot as a bar chart
    plt.figure(figsize=(120, 60))
    avg_max_sample.plot(kind="bar", color="skyblue", edgecolor="black")

    plt.title("Average Max Sample by EV Model")
    plt.xlabel("EV Model")
    plt.ylabel("Average Max Sample")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Save to a PNG file
    plt.savefig(f"images/average_max_sample_by_EVModel_{country}.png", dpi=300)
    plt.close()

    print("Graph saved to average_max_sample_by_EVModel.png")


def get_number_transactions_by_model(country):
    df = pd.read_csv(f"transactions_alldata_{country}_only.csv")

    # Count transactions per EVModel
    transactions_per_model = df["EVModel"].value_counts()

    print(transactions_per_model)
    transactions_per_model.to_csv(f"transactions_per_model_{country}.csv")


def sort_models(country):
    df = pd.read_csv(f"transactions_per_model_{country}.csv")

    # Sort by model name (assuming first column is EVModel)
    df_sorted = df.sort_values(by="EVModel", ascending=True)

    # Save to a new CSV
    df_sorted.to_csv(f"transactions_per_model_sorted_{country}.csv", index=False)

    print("Sorted file saved as transactions_per_model_sorted.csv")


# print(get_lines_count())
# print(get_countries())
# get_sample_min_max("Norway")
# get_graph_weekdays()
# get_graph_weekday_soc_range()

# save_filtered_as_csv("Sweden")

# sort_by_transaction_sample("Finland_only.csv")
# sort_by_transaction_sample("Sweden_only.csv")

# get_unique_trans_number("sorted_Finland_only.csv")
# get_unique_trans_number("sorted_Sweden_only.csv")

# Some State of Charge info
# find_desc_soc("sorted_Finland_only.csv")
# find_transactions_over_80("sorted_Finland_only.csv")
# find_transactions_soc("transactions_sorted_Finland_only.csv")

# --- Get graph of 1 or many transactions: soc by sampleTime
# get_graph_soc_sample("sorted_Finland_only.csv", "000b81cceff65c80a3fd7a190c82396c0670c800ac23a9f3b5ec7be92c30a057")
# get_graphs_soc_sample("sorted_Finland_only.csv")

# get_graph_max_power("Finland")
# get_graph_max_power("Norway")
# get_graph_max_power_percentage("Finland")
# get_graph_max_power_percentage("Norway")

# --- Get aggregated data: each transaction, and its
# transactionId,EVModel,year,month,weekday,min_sample,max_sample,min_soc,max_soc,mean_power,max_power,mean_temp
# get_max_sample("Finland_only.csv")
# get_max_sample("Norway_only.csv")
# get_max_sample("United Kingdom_only.csv")

# --- Get max sampleTime by each model (+ csv) - first call get_max_sample()
# get_graph_max_sample_time_by_model("Finland")
# get_graph_max_sample_time_by_model("Norway")
# get_graph_max_sample_time_by_model("United Kingdom")

# --- Get EVModel,count csv and sort them by EVModel - first call get_max_sample()
# get_number_transactions_by_model("Finland")
# sort_models("Finland")
# get_number_transactions_by_model("Norway")
# sort_models("Norway")
# get_number_transactions_by_model("United Kingdom")
# sort_models("United Kingdom")

# Play downloaded sound when everything is done (not pushed to git)
playsound('notification-metallic-chime-fast-gamemaster-audio-higher-tone-2-00-01.mp3')

# todo:
# of all countries or Finland:
# how long were the sessions? biggest sample out of same transaction id
# the same with weekday
# see a couple of long sessions and how the soc is increasing
# + dependance of temp?

# usual time to charge - mean?
# how often end charge is not 100?
# what day is usually longer charges?
# are there any descending soc within a transaction?
