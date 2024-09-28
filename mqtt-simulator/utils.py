import random

def shouldRunWithProbability(probability: float):
    random_number = random.random()
    return random_number < probability
