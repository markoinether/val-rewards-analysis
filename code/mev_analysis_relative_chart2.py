import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
file_path = "blockReward_titled.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Ensure 'mev_rewards' is sorted in ascending order for cumulative calculations
data = data.sort_values(by="mev_rewards", ascending=True)


def plot_relative_percentile_stats_with_median(start_percentile, end_percentile, step):
    percentiles = []
    relative_sums = []
    medians_up_to_percent = []
    total_sum = data["mev_rewards"].sum()

    for percentile in np.arange(start_percentile, end_percentile, step):
        lower_bound = data["mev_rewards"].quantile(percentile / 100.0)
        upper_bound = data["mev_rewards"].quantile((percentile + step) / 100.0)

        # Filter the data for the current percentile range
        values_in_percentile = data[
            (data["mev_rewards"] > lower_bound) & (data["mev_rewards"] <= upper_bound)
        ]

        percentile_sum = values_in_percentile["mev_rewards"].sum()
        relative_sum = (percentile_sum / total_sum) * 100  # Convert to percentage

        # Calculate the median value and sum up to the median
        median_value = values_in_percentile["mev_rewards"].median()
        sum_up_to_median = values_in_percentile[
            values_in_percentile["mev_rewards"] <= median_value
        ]["mev_rewards"].sum()
        percent_up_to_median = (
            sum_up_to_median / total_sum
        ) * 100  # Convert to percentage

        percentiles.append(f"{percentile}-{percentile + step}")
        relative_sums.append(relative_sum)
        medians_up_to_percent.append(percent_up_to_median)

    # Plotting
    plt.figure(figsize=(14, 8))
    bars = plt.bar(percentiles, relative_sums, color="yellow")

    # Label each bar with its relative sum value and median information
    for bar, rel_sum, med_percent in zip(bars, relative_sums, medians_up_to_percent):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"Sum: {rel_sum:.2f}%",
            ha="center",
            va="bottom",
            fontsize=8,
        )
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() / 2,
            f"Median: {med_percent:.2f}%",
            ha="center",
            va="center",
            fontsize=8,
            color="red",
        )

    plt.xlabel("Percentile")
    plt.ylabel("Relative Sum (%)")
    plt.title("Relative Sum and Median Value by Percentile")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("mev_analysis_relative_chart2", dpi=200)
    # plt.show()


# Plot stats for each 10-percentile range
plot_relative_percentile_stats_with_median(90, 100, 1)
