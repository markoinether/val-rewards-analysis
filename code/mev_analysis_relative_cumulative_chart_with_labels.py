import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
file_path = "blockReward_titled.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Ensure 'mev_rewards' is sorted in ascending order for cumulative calculations
data = data.sort_values(by="mev_rewards", ascending=True)


def plot_relative_percentile_stats_with_median_and_cumulative(
    start_percentile, end_percentile, step
):
    percentiles = []
    relative_sums = []
    cumulative_sums = []  # To store cumulative sums
    medians_up_to_percent = []
    total_sum = data["mev_rewards"].sum()
    cumulative_sum = 0  # Initialize cumulative sum

    for percentile in np.arange(start_percentile, end_percentile, step):
        lower_bound = data["mev_rewards"].quantile(percentile / 100.0)
        upper_bound = data["mev_rewards"].quantile((percentile + step) / 100.0)

        values_in_percentile = data[
            (data["mev_rewards"] > lower_bound) & (data["mev_rewards"] <= upper_bound)
        ]
        percentile_sum = values_in_percentile["mev_rewards"].sum()
        relative_sum = (percentile_sum / total_sum) * 100  # Convert to percentage
        cumulative_sum += percentile_sum  # Update cumulative sum
        cumulative_sum_percent = (
            cumulative_sum / total_sum
        ) * 100  # Convert cumulative sum to percentage

        percentiles.append(f"{percentile}-{percentile + step}")
        relative_sums.append(relative_sum)
        cumulative_sums.append(cumulative_sum_percent)  # Store cumulative sum percent
        medians_up_to_percent.append(
            0
        )  # Placeholder for medians_up_to_percent calculation

    # Plotting
    fig, ax = plt.subplots(figsize=(14, 8))
    bar_width = 0.35  # Width of the bars
    index = np.arange(len(percentiles))

    # Plotting the relative sum bars
    bars_relative = ax.bar(
        index - bar_width / 2,
        relative_sums,
        bar_width,
        label="Relative Sum",
        color="yellow",
    )
    # Plotting the cumulative sum bars next to the relative sum bars
    bars_cumulative = ax.bar(
        index + bar_width / 2,
        cumulative_sums,
        bar_width,
        label="Cumulative Sum",
        color="gold",
    )

    # Label each relative sum bar and cumulative sum bar
    for bar_rel, bar_cum, rel_sum, cum_sum in zip(
        bars_relative, bars_cumulative, relative_sums, cumulative_sums
    ):
        ax.text(
            bar_rel.get_x() + bar_rel.get_width() / 2,
            bar_rel.get_height(),
            f"Sum: {rel_sum:.2f}%",
            ha="center",
            va="bottom",
            fontsize=8,
        )
        ax.text(
            bar_cum.get_x() + bar_cum.get_width() / 2,
            bar_cum.get_height(),
            f"Cumulative Sum: {cum_sum:.2f}%",
            ha="center",
            va="bottom",
            fontsize=8,
            color="blue",
        )

    ax.set_xlabel("Percentile")
    ax.set_ylabel("Relative Sum (%)")
    ax.set_title("Relative Sum and Cumulative Sum by Percentile")
    ax.set_xticks(index)
    ax.set_xticklabels(percentiles, rotation=45)
    ax.legend()
    plt.tight_layout()
    plt.savefig("mev_analysis_relative_cumulative_chart_with_labels.png", dpi=200)
    # plt.show()


# Plot stats for each 10-percentile range with cumulative sum and labels
plot_relative_percentile_stats_with_median_and_cumulative(0, 100, 10)
