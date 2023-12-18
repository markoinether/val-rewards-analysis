import pandas as pd
import random

# from block_proposals import simulate_block_proposals
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "blockReward_titled.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Sort the data based on the 'mev_rewards' column
data = data.sort_values(by="mev_rewards", ascending=False)


def simulate_block_proposals(
    active_validator_set, num_of_my_validators, days_in_operation
):
    seconds_per_day = 86400
    slot_time = 12
    slots_per_day = seconds_per_day // slot_time
    total_slots = slots_per_day * days_in_operation
    block_proposals = 0

    for _ in range(total_slots):
        if random.randint(1, active_validator_set) <= num_of_my_validators:
            block_proposals += 1
    print("block proposals:", block_proposals)
    return block_proposals


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


# active_validator_set = 888822
# num_of_my_validators = 1000
# days_in_operation = 365
# reward_per_attestation = 10007000000000  # sampled at 23/12/15
# cons_reward_per_proposal = 43840000000000000  # sampled at 23/12/15


# block_proposed = simulate_block_proposals(
#     active_validator_set, num_of_my_validators, days_in_operation
# )

# mev_rewards_list, mev_rewards_sum = give_random_mev_rewards(block_proposed)
# attestation_rewards = get_attestation_rewards(
#     num_of_my_validators, days_in_operation, reward_per_attestation
# )
# consensus_proposer_rewards = get_consensus_proposer_rewards(
#     block_proposed, cons_reward_per_proposal
# )

# total_rewards = mev_rewards_sum + consensus_proposer_rewards + attestation_rewards
# average_per_validator_per_day = total_rewards / num_of_my_validators / days_in_operation

# # print(f"Random Rewards: {random_rewards}")
# print(f"Sum of mev_rewards_sum: {mev_rewards_sum:.2e}")
# print(f"Sum of attestation_rewards: {attestation_rewards:.2e}")
# print(f"Sum of consensus_proposer_rewards: {consensus_proposer_rewards:.2e}")
# print(f"Sum of total_rewards: {total_rewards:.2e}")
# print(f"average_per_validator_per_day: {average_per_validator_per_day:.2e}")


def run_simulation(days_in_operation, num_of_my_validators):
    active_validator_set = 888822
    reward_per_attestation = 10007000000000
    cons_reward_per_proposal = 43840000000000000

    block_proposed = simulate_block_proposals(
        active_validator_set, num_of_my_validators, days_in_operation
    )

    # Randomly generated rewards
    mev_rewards_list, mev_rewards_sum = give_random_mev_rewards(block_proposed)

    # Other rewards
    attestation_rewards = get_attestation_rewards(
        num_of_my_validators, days_in_operation, reward_per_attestation
    )
    consensus_proposer_rewards = get_consensus_proposer_rewards(
        block_proposed, cons_reward_per_proposal
    )

    total_rewards = mev_rewards_sum + consensus_proposer_rewards + attestation_rewards
    print(f"Sum of total_rewards: {total_rewards:.2e}")
    return total_rewards


# inputs
num_of_my_validators = 10000
days_in_operation = 365

# Running the simulation 100 times
simulations = 100
total_rewards_results = [
    run_simulation(days_in_operation, num_of_my_validators) for _ in range(simulations)
]

# Sorting the total rewards results in descending order
sorted_total_rewards_results = sorted(total_rewards_results, reverse=True)

first_value = sorted_total_rewards_results[0]  # Biggest value
last_value = sorted_total_rewards_results[-1]  # Smallest value


# Calculating mean and median of the sorted total rewards
mean_total_rewards = sum(sorted_total_rewards_results) / len(
    sorted_total_rewards_results
)
median_total_rewards = sorted_total_rewards_results[
    len(sorted_total_rewards_results) // 2
]

trimmed_sorted_total_rewards_results = sorted_total_rewards_results[2:-2]

# print(f"sorted_total_rewards_results: {sorted_total_rewards_results}")
# print(f"trimmed_sorted_total_rewards_results: {trimmed_sorted_total_rewards_results}")

mean_trimmed_sorted_total_rewards_results = sum(
    trimmed_sorted_total_rewards_results
) / len(trimmed_sorted_total_rewards_results)
median_trimmed_sorted_total_rewards_results = trimmed_sorted_total_rewards_results[
    len(trimmed_sorted_total_rewards_results) // 2
]


# # Plotting the results - Not ordered
# plt.figure(figsize=(12, 6))
# plt.bar(range(1, (simulations + 1)), total_rewards_results, color="blue")
# plt.axhline(y=mean_total_rewards, color="blue", linestyle="-", label="Mean")
# plt.axhline(y=median_total_rewards, color="green", linestyle="-", label="Median")
# plt.axhline(
#     y=mean_trimmed_sorted_total_rewards_results,
#     color="yellow",
#     linestyle="-",
#     label="Mean_trimmed",
# )
# plt.axhline(
#     y=median_trimmed_sorted_total_rewards_results,
#     color="orange",
#     linestyle="-",
#     label="Median_trimmed",
# )
# plt.xlabel("Simulation Number")
# plt.ylabel("Total Rewards")
# plt.title(
#     f"Total Rewards running {num_of_my_validators} validators {days_in_operation} days from {simulations} Simulations \n*trimmed means that 2 highest and 2 lowest values were removed"
# )
# plt.legend()
# plt.show()


# Plotting the sorted results in red
plt.figure(figsize=(12, 6))
plt.bar(range(1, (simulations + 1)), sorted_total_rewards_results, color="red")
plt.axhline(
    y=mean_total_rewards,
    color="blue",
    linestyle="-",
    label=f"Mean: {mean_total_rewards:.2e}",
)
plt.axhline(
    y=median_total_rewards,
    color="green",
    linestyle="-",
    label=f"Median: {median_total_rewards:.2e}",
)
plt.axhline(
    y=mean_trimmed_sorted_total_rewards_results,
    color="yellow",
    linestyle="-",
    label=f"Mean_trimmed: {mean_trimmed_sorted_total_rewards_results:.2e}",
)
plt.axhline(
    y=median_trimmed_sorted_total_rewards_results,
    color="orange",
    linestyle="-",
    label=f"Median_trimmed: {median_trimmed_sorted_total_rewards_results:.2e}",
)
plt.text(
    1,
    first_value,
    f"First: {first_value:.2e}",
    color="black",
    verticalalignment="bottom",
)
plt.text(
    len(sorted_total_rewards_results),
    last_value,
    f"Last: {last_value:.2e}",
    color="black",
    verticalalignment="top",
)
plt.xlabel("Simulation Number")
plt.ylabel("Total Rewards")
plt.title(
    f"Total Rewards running {num_of_my_validators} validators {days_in_operation} days from {simulations} Simulations (Descending Order) \n*trimmed means that 2 highest and 2 lowest values were removed"
)
plt.legend()
plt.show()


plt.text(
    1,
    first_value,
    f"First: {first_value:.2e}",
    color="black",
    verticalalignment="bottom",
)
plt.text(
    len(trimmed_sorted_total_rewards_results),
    last_value,
    f"Last: {last_value:.2e}",
    color="black",
    verticalalignment="top",
)


# plt.axhline(y=trimmed_mean_total_rewards, color='blue', linestyle='-', label=f'Mean: {trimmed_mean_total_rewards:.2e}')
# plt.axhline(y=trimmed_median_total_rewards, color='green', linestyle='-', label=f'Median: {trimmed_median_total_rewards:.2e}')

# plt.figure(figsize=(12, 6))
# plt.bar(range(1, 101), sorted_total_rewards_results, color='red')
# plt.axhline(y=mean_total_rewards, color='blue', linestyle='-', label='Mean')
# plt.axhline(y=median_total_rewards, color='green', linestyle='-', label='Median')
# plt.xlabel('Simulation Number')
# plt.ylabel('Total Rewards')
# plt.title('Total Rewards from 100 Simulations (Descending Order)')
# plt.legend()
# plt.show()
