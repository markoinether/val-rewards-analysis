import pandas as pd

# Load the CSV file
file_path = "blockReward_titled.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Sort the data based on the 'mev_rewards' column
data = data.sort_values(by="mev_rewards", ascending=False)

# Calculate total sum, mean, and median for the entire dataset
total_sum = data["mev_rewards"].sum()
total_mean = data["mev_rewards"].mean()
total_median = data["mev_rewards"].median()


def print_percentile_stats(start_percentile, end_percentile, step):
    for percentile in range(start_percentile, end_percentile, step):
        lower_bound = data["mev_rewards"].quantile(percentile / 100.0)
        upper_bound = data["mev_rewards"].quantile((percentile + step) / 100.0)

        values_in_percentile = data[
            (data["mev_rewards"] <= upper_bound) & (data["mev_rewards"] >= lower_bound)
        ]

        percentile_sum = values_in_percentile["mev_rewards"].sum()
        percentile_mean = values_in_percentile["mev_rewards"].mean()
        percentile_median = values_in_percentile["mev_rewards"].median()
        percentile_std_err = values_in_percentile["mev_rewards"].sem()

        sum_ratio = percentile_sum / total_sum
        mean_ratio = percentile_mean / total_mean
        median_ratio = percentile_median / total_median

        print(f"Percentile {percentile}-{percentile + step}:")
        print(f"  First value: {values_in_percentile.iloc[0]['mev_rewards']}")
        print(f"  Last value: {values_in_percentile.iloc[-1]['mev_rewards']}")
        print(f"  Sum Ratio: {sum_ratio:.2f}")
        print(f"  Mean: {percentile_mean:.2e}")
        print(f"  Median: {percentile_median:.2e}")
        print(f"  Standard Error: {percentile_std_err:.2e}")
        print(f"  Mean Ratio: {mean_ratio:.2f}")
        print(f"  Median Ratio: {median_ratio:.2f}\n")


# Print stats for each 10-percentile range
print_percentile_stats(0, 100, 10)

# Print stats for each individual percentile from 91 to 100
print_percentile_stats(91, 100, 1)
