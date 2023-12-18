import pandas as pd

# Load the CSV file
file_path = "blockReward_titled.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Assuming your values are in a column named 'Value'
# Replace 'Value' with the actual column name
data = data.sort_values(by="mev_rewards", ascending=False)

# Calculate the percentiles and print the values

print("percetiles going by 10%")
print("--------------------------------")
for percentile in range(0, 100, 10):
    lower_bound = data["mev_rewards"].quantile(percentile / 100.0)
    upper_bound = data["mev_rewards"].quantile((percentile + 10) / 100.0)

    # Adjust the bounds for the first and last values in this percentile range
    values_in_percentile = data[
        (data["mev_rewards"] <= upper_bound) & (data["mev_rewards"] >= lower_bound)
    ]

    first_value = values_in_percentile.iloc[0]["mev_rewards"]
    last_value = values_in_percentile.iloc[-1]["mev_rewards"]

    print(f"Percentile {percentile}-{percentile+10}:")
    print(f"  First value: {first_value}")
    print(f"  Last value: {last_value}\n")

print("percetiles going by 1% 91-100%")
print("--------------------------------")
for percentile in range(90, 100):
    lower_bound = data["mev_rewards"].quantile(percentile / 100.0)
    upper_bound = data["mev_rewards"].quantile((percentile + 1) / 100.0)

    # Adjust the bounds for the first and last values in this percentile range
    values_in_percentile = data[
        (data["mev_rewards"] <= upper_bound) & (data["mev_rewards"] >= lower_bound)
    ]

    first_value = values_in_percentile.iloc[0]["mev_rewards"]
    last_value = values_in_percentile.iloc[-1]["mev_rewards"]

    print(f"Percentile {percentile}-{percentile+10}:")
    print(f"  First value: {first_value}")
    print(f"  Last value: {last_value}\n")
