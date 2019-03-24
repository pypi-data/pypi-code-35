from Fortuna import *
import random


if __name__ == "__main__":

    print("\nFortuna Test Suite: RNG Storm Engine")

    print("\nTruffleShuffle")
    some_list = [i * 2 for i in range(11)]
    truffle_shuffle = TruffleShuffle(some_list)
    distribution_timer(truffle_shuffle)

    print(f"\nQuantumMonty({some_list})")
    quantum_monty = QuantumMonty(some_list)
    distribution_timer(quantum_monty.uniform)
    distribution_timer(quantum_monty.front)
    distribution_timer(quantum_monty.back)
    distribution_timer(quantum_monty.middle)
    distribution_timer(quantum_monty.quantum)
    distribution_timer(quantum_monty.front_gauss)
    distribution_timer(quantum_monty.back_gauss)
    distribution_timer(quantum_monty.middle_gauss)
    distribution_timer(quantum_monty.quantum_gauss)
    distribution_timer(quantum_monty.front_poisson)
    distribution_timer(quantum_monty.back_poisson)
    distribution_timer(quantum_monty.middle_poisson)
    distribution_timer(quantum_monty.quantum_poisson)
    distribution_timer(quantum_monty.quantum_monty)

    print("\nWeighted Choice")
    population = [36, 30, 24, 18]
    cum_weights = [1, 10, 100, 1000]
    rel_weights = [1, 9, 90, 900]
    cum_weighted_choice = CumulativeWeightedChoice(zip(cum_weights, population))
    distribution_timer(cum_weighted_choice)
    cum_weighted_choice = RelativeWeightedChoice(zip(rel_weights, population))
    distribution_timer(cum_weighted_choice)

    print("\nFlexCat")
    some_dict = {1: [1, 2, 3], 2: [10, 20, 30], 3: [100, 200, 300]}
    flex_cat = FlexCat(some_dict)
    distribution_timer(flex_cat)

    print("\nRandom Numbers")
    distribution_timer(random_below, 10)
    distribution_timer(random_int, -5, 5)
    distribution_timer(random_range, 1, 20, 2)
    distribution_timer(d, 10)
    distribution_timer(dice, 2, 6)
    distribution_timer(percent_true, 33.33)
    distribution_timer(plus_or_minus, 5)

    print("\nBase Cases")
    distribution_timer(random.randrange, 10)
    distribution_timer(random.randint, -5, 5)
    distribution_timer(random.randrange, 1, 21, 2)
    distribution_timer(random.choice, some_list)
    distribution_timer(random.choices, population, weights=rel_weights)
    distribution_timer(random.choices, population, cum_weights=cum_weights)

    print("\nExperimental: RNG Vortex Engine")
    distribution_timer(vortex_random_below, 10)
