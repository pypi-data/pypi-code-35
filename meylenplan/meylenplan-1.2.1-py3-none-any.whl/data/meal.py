class Meal(object):

    def __init__(self, name, allergens, potentially_not_a_meal=False):
        self.name = name
        self.allergens = allergens
        self.price = None
        self.potentially_not_a_meal = potentially_not_a_meal
