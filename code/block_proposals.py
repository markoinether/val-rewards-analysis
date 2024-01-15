import random


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


def average_block_proposals(
    active_validator_set, num_of_my_validators, days_in_operation, simulations
):
    total_proposals = 0
    for _ in range(simulations):
        total_proposals += simulate_block_proposals(
            active_validator_set, num_of_my_validators, days_in_operation
        )

    return total_proposals / simulations


active_validator_set = 888822
num_of_my_validators = 10
days_in_operation = 365
simulations = 10  # Number of simulations to average over

# average_proposals = average_block_proposals(
#     active_validator_set, num_of_my_validators, days_in_operation, simulations
# )
# print(f"Average number of block proposals: {average_proposals}")


# _active_validator_set = 888822
# _num_of_my_validators = 1
# _days_in_operation = 365.25
# simulate_block_proposals(
#     _active_validator_set, _num_of_my_validators, _days_in_operation
# )
# print(simulate_block_proposals)
