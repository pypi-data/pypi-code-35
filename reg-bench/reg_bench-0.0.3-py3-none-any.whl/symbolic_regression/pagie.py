from .util import generate_evenly_spaced_data_set


def pagie_func1(x, y):
    return 1.0 / x ** (-4) + 1.0 / y ** (-4)


def generate_pagie1():
    train = generate_evenly_spaced_data_set(pagie_func1, 0.4, (-5, 5))
    test = generate_evenly_spaced_data_set(pagie_func1, 0.4, (-5, 5))
    return train, test


all_problems = {"pagie1": generate_pagie1}
