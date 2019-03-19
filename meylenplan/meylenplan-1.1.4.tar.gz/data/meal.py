class Meal(object):

    def __init__(self, name, additives, potentially_not_a_meal=False):
        self.name = name
        self.additives = additives
        self.price = None
        self.potentially_not_a_meal = potentially_not_a_meal
