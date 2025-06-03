import random

def should_run_with_probability(probability: float):
    random_number = random.random()
    return random_number < probability
