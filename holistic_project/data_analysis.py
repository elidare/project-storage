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
                             "country", "transactionId", "soc", "avgPowerW", "sampleTime10sIncrement", "tempC"
                             ],
                             chunksize=chunksize):
        # Show progress
        print(i * chunksize)
        i += 1

        # Drop NaN if necessary
        chunk = chunk.dropna(subset=["transactionId", "soc", "avgPowerW", "sampleTime10sIncrement", "tempC"])

        grouped = chunk.groupby("transactionId").agg({
            "sampleTime10sIncrement": ["min", "max"],
            "soc": ["min", "max"],
            "avgPowerW": ["mean", "max"],
            "tempC": ["mean"]
        })

        # Merge into dictionary
        for tid, row in grouped.iterrows():
            if tid not in stats:
                stats[tid] = {
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
                stats[tid]["min_sample"] = max(stats[tid]["min_sample"], row[("sampleTime10sIncrement", "min")])
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
    final_stats.to_csv(f"transactions_{filename}", index=False)


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


# print(get_lines_count())
# print(get_countries())
# get_sample_min_max("Norway")
# get_graph_weekdays()
# get_graph_weekday_soc_range()

# save_filtered_as_csv("Finland")
# save_filtered_as_csv("Norway")

# sort_by_transaction_sample("Finland_only.csv")
# sort_by_transaction_sample("Norway_only.csv")

# get_max_sample("Finland_only.csv")  # todo fix min sample and check max sample
# get_max_sample("Norway_only.csv")

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
