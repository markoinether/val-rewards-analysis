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


def get_attestation_rewards(
    num_of_my_validators, days_in_operation, reward_per_attestation
):
    seconds_per_day = 86400
    slot_time = 12
    slots_per_day = seconds_per_day // slot_time
    total_slots = slots_per_day * days_in_operation
    total_epochs = int(total_slots / 32)
    total_reward_per_validator = total_epochs * reward_per_attestation

    return total_reward_per_validator * num_of_my_validators


def get_consensus_proposer_rewards(num_of_rewards, reward_size):
    return num_of_rewards * reward_size


# simulations = 10  # Number of simulations to average over


active_validator_set = 888822
num_of_my_validators = 1000
days_in_operation = 365
reward_per_attestation = 10007000000000  # sampled at 23/12/15
cons_reward_per_proposal = 43840000000000000  # sampled at 23/12/15


block_proposed = simulate_block_proposals(
    active_validator_set, num_of_my_validators, days_in_operation
)

mev_rewards_list, mev_rewards_sum = give_random_mev_rewards(block_proposed)
attestation_rewards = get_attestation_rewards(
    num_of_my_validators, days_in_operation, reward_per_attestation
)
consensus_proposer_rewards = get_consensus_proposer_rewards(
    block_proposed, cons_reward_per_proposal
)

total_rewards = mev_rewards_sum + consensus_proposer_rewards + attestation_rewards
average_per_validator_per_day = total_rewards / num_of_my_validators / days_in_operation

# print(f"Random Rewards: {random_rewards}")
print(f"Sum of mev_rewards_sum: {mev_rewards_sum:.2e}")
print(f"Sum of attestation_rewards: {attestation_rewards:.2e}")
print(f"Sum of consensus_proposer_rewards: {consensus_proposer_rewards:.2e}")
print(f"Sum of total_rewards: {total_rewards:.2e}")
print(f"average_per_validator_per_day: {average_per_validator_per_day:.2e}")
