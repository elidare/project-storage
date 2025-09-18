import matplotlib.pyplot as plt
import pandas as pd
import csv


filename = "public_passenger_dataset.csv"  # Downloaded CSV


# Lines in csv
def get_lines_count():
    with open(filename, "r", encoding="utf-8") as f:
        row_count = sum(1 for row in f) - 1  # subtract header
    return row_count


# Countries
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


# ------ Country + year + quarter, soc sorted
def get_soc(country):
    country_filter = country
    # year_filter = 2024
    # quarter_filter = 1

    chunks = pd.read_csv(filename, chunksize=1000000)
    filtered_list = []

    for chunk in chunks:
        subset = chunk[
            (chunk["country"] == country_filter)
            # &
            # (chunk["year"] == year_filter) &
            # (chunk["quarter"] == quarter_filter)
            ]
        filtered_list.append(subset)

    filtered_df = pd.concat(filtered_list).sort_values(by="soc")

    # Sort by soc ascending
    filtered_df = (filtered_df[["country", "EVModel", "year", "month", "soc", "tempC", "sampleTime10sIncrement", "weekday", "avgPowerW"]]
                   .sort_values(by="soc", ascending=True))

    #filtered_df.to_csv(f"{country_filter}_{year_filter}_{quarter_filter}_filtered_data.csv", index=False)

    # 10 rows with smallest soc
    min_soc = filtered_df.nsmallest(10, "soc")
    # 10 rows with largest soc
    max_soc = filtered_df.nlargest(10, "soc")
    pd.set_option("display.max_columns", None)
    print("10 lowest soc:")
    print(min_soc[["country", "EVModel", "month", "soc", "tempC", "sampleTime10sIncrement", "weekday", "avgPowerW"]])

    print("\n10 highest soc:")
    print(max_soc[["country", "EVModel", "month", "soc", "tempC", "sampleTime10sIncrement", "weekday", "avgPowerW"]])

    return filtered_df


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


def get_graph_soc_sample(country):
    filtered_df = get_soc(country)
    # Only for the filtered country
    plt.figure(figsize=(10, 6))
    plt.scatter(
        filtered_df["sampleTime10sIncrement"],
        filtered_df["soc"],
        alpha=0.5
    )
    plt.xlabel("Sample Time Increment (10s)")
    plt.ylabel("State of Charge (SOC)")
    plt.title("SOC vs. Sample Time Increment")
    plt.grid(True)
    # Save to file
    plt.savefig(f"soc_vs_time_{country}.png", dpi=300)
    plt.close()  # closes figure to free memory


def get_graph_model_soc():
    # All countries
    soc_sums = {}
    soc_counts = {}

    # Process CSV in chunks
    for chunk in pd.read_csv(filename, usecols=["EVModel", "soc"], chunksize=1000000):
        # Drop rows with missing soc
        chunk = chunk.dropna(subset=["soc"])

        # Group by model
        grouped = chunk.groupby("EVModel")["soc"].agg(["sum", "count"])

        for model, row in grouped.iterrows():
            soc_sums[model] = soc_sums.get(model, 0) + row["sum"]
            soc_counts[model] = soc_counts.get(model, 0) + row["count"]

    # Compute average SOC per model
    avg_soc = {model: soc_sums[model] / soc_counts[model] for model in soc_sums}

    # Convert to DataFrame
    avg_soc_df = pd.DataFrame(list(avg_soc.items()), columns=["EVModel", "Average_SOC"])
    avg_soc_df = avg_soc_df.sort_values("Average_SOC", ascending=False)

    # Plot
    plt.figure(figsize=(50, 60))  # tall figure
    plt.barh(avg_soc_df["EVModel"], avg_soc_df["Average_SOC"])
    plt.xlabel("Average SOC")
    plt.ylabel("EV Model")
    plt.title("Average SOC per EV Model")
    plt.tight_layout()
    plt.savefig("avg_soc_per_model.png", dpi=300)
    plt.close()


def get_graph_power_sample():
    # Dictionaries to track min and max per sample time
    power_min = {}
    power_max = {}

    # Process CSV in chunks
    for chunk in pd.read_csv(filename, usecols=["sampleTime10sIncrement", "avgPowerW"], chunksize=500000):
        # Drop rows with missing values
        chunk = chunk.dropna(subset=["sampleTime10sIncrement", "avgPowerW"])

        # Group by sample time
        grouped = chunk.groupby("sampleTime10sIncrement")["avgPowerW"].agg(["min", "max"])

        for t, row in grouped.iterrows():
            if t in power_min:
                power_min[t] = min(power_min[t], row["min"])
                power_max[t] = max(power_max[t], row["max"])
            else:
                power_min[t] = row["min"]
                power_max[t] = row["max"]

    # Convert to DataFrame
    power_range_df = pd.DataFrame({
        "sampleTime10sIncrement": list(power_min.keys()),
        "minPower": list(power_min.values()),
        "maxPower": list(power_max.values())
    })

    # Sort by sample time
    power_range_df = power_range_df.sort_values("sampleTime10sIncrement")

    # Plot range as filled band
    plt.figure(figsize=(12, 6))
    plt.fill_between(
        power_range_df["sampleTime10sIncrement"],
        power_range_df["minPower"],
        power_range_df["maxPower"],
        alpha=0.3,
        color="skyblue",
        label="Power range (min–max)"
    )
    plt.plot(
        power_range_df["sampleTime10sIncrement"],
        power_range_df["minPower"],
        color="blue", linestyle="--", label="Min Power"
    )
    plt.plot(
        power_range_df["sampleTime10sIncrement"],
        power_range_df["maxPower"],
        color="red", linestyle="--", label="Max Power"
    )

    plt.xlabel("Sample Time Increment (10s)")
    plt.ylabel("Power (W)")
    plt.title("Range of Power (min–max) vs. Sample Time Increment")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("power_range_vs_time.png", dpi=300)
    plt.close()


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


def get_graph_weekday_soc_range():
    # Dictionaries for min and max SOC per weekday
    soc_min = {}
    soc_max = {}

    # Process in chunks
    for chunk in pd.read_csv(filename, usecols=["weekday", "soc"], chunksize=500000):
        chunk = chunk.dropna(subset=["weekday", "soc"])
        grouped = chunk.groupby("weekday")["soc"].agg(["min", "max"])

        for weekday, row in grouped.iterrows():
            if weekday in soc_min:
                soc_min[weekday] = min(soc_min[weekday], row["min"])
                soc_max[weekday] = max(soc_max[weekday], row["max"])
            else:
                soc_min[weekday] = row["min"]
                soc_max[weekday] = row["max"]

    # Convert to DataFrame
    soc_range_df = pd.DataFrame({
        "weekday": list(soc_min.keys()),
        "minSOC": list(soc_min.values()),
        "maxSOC": list(soc_max.values())
    })

    # Order weekdays
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    soc_range_df["weekday"] = pd.Categorical(soc_range_df["weekday"], categories=weekday_order, ordered=True)
    soc_range_df = soc_range_df.sort_values("weekday")

    # Plot as error bars (min–max)
    plt.figure(figsize=(10, 6))
    plt.errorbar(
        soc_range_df["weekday"],
        (soc_range_df["minSOC"] + soc_range_df["maxSOC"]) / 2,  # mid point
        yerr=(soc_range_df["maxSOC"] - soc_range_df["minSOC"]) / 2,  # half range
        fmt="o",
        ecolor="red",
        capsize=5,
        label="SOC range"
    )

    plt.xlabel("Weekday")
    plt.ylabel("SOC")
    plt.title("SOC Range (min–max) per Weekday")
    plt.grid(True, axis="y")
    plt.legend()
    plt.tight_layout()
    plt.savefig("soc_range_per_weekday.png", dpi=300)
    plt.close()


# print(get_lines_count())
# print(get_countries())
# get_soc()
# get_graph_soc_sample("Norway")
# get_sample_min_max("Norway")
# get_graph_model_soc()  # Average soc per models
# get_graph_power_sample()
# get_graph_weekdays()
get_graph_weekday_soc_range()


# of all countries:
# Draw graph of weekday - avgPower?
# Weekday - soc?
# model - avg power
# temp - avg power
#
