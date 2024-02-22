import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
file_path = "blockReward_titled.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Ensure 'mev_rewards' is sorted in ascending order for cumulative calculations
data = data.sort_values(by="mev_rewards", ascending=True)


def plot_relative_percentile_stats(start_percentile, end_percentile, step):
    percentiles = []
    relative_sums = []
    total_sum = data["mev_rewards"].sum()

    for percentile in np.arange(start_percentile, end_percentile, step):
        lower_bound = data["mev_rewards"].quantile(percentile / 100.0)
        upper_bound = data["mev_rewards"].quantile((percentile + step) / 100.0)

        # Filter the data for the current percentile range
        values_in_percentile = data[
            (data["mev_rewards"] > lower_bound) & (data["mev_rewards"] <= upper_bound)
        ]

        # Calculate the sum for the current percentile and its relative part of the total sum
        percentile_sum = values_in_percentile["mev_rewards"].sum()
        relative_sum = (percentile_sum / total_sum) * 100  # Convert to percentage

        percentiles.append(f"{percentile}-{percentile + step}")
        relative_sums.append(relative_sum)

    # Plotting
    plt.figure(figsize=(14, 8))
    bars = plt.bar(percentiles, relative_sums, color="yellow")

    # Label each bar with its relative sum value
    for bar, rel_sum in zip(bars, relative_sums):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{rel_sum:.2f}%",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.xlabel("Percentile")
    plt.ylabel("Relative Sum (%)")
    plt.title("Relative Sum by Percentile")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("mev_analysis_relative_100_chart", dpi=200)
    # plt.show()


# Plot stats for each 10-percentile range
plot_relative_percentile_stats(0, 100, 1)
