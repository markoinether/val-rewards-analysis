import pandas as pd
from block_proposals import simulate_block_proposals

# Load the CSV file
file_path = "blockReward_titled.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Sort the data based on the 'mev_rewards' column
data = data.sort_values(by="mev_rewards", ascending=False)


def give_random_mev_rewards(num_of_rewards):
    """
    Return a list of randomly sampled MEV rewards and their total sum.

    :param num_of_rewards: Number of rewards to sample
    :return: List of sampled rewards and their total sum
    """
    sampled_rewards = (
        data["mev_rewards"].sample(n=num_of_rewards, replace=True).tolist()
    )
    sum_of_sampled_rewards = sum(sampled_rewards)
    return sampled_rewards, sum_of_sampled_rewards


random_rewards, sum_of_rewards = give_random_mev_rewards(10)
print(f"Random Rewards: {random_rewards}")
print(f"Sum of Sampled Rewards: {sum_of_rewards}")


active_validator_set = 888822
num_of_my_validators = 10
days_in_operation = 365
simulations = 10  # Number of simulations to average over

simulate_block_proposals = simulate_block_proposals(
    active_validator_set, num_of_my_validators, days_in_operation
)


print(f"Average number of block proposals: {average_proposals}")
