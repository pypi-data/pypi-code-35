from collections import namedtuple
import datetime
import math
import random

import pytz

morning = datetime.datetime(2019, 5, 1, 8, 0, 0)
timezone = pytz.timezone("America/Los_Angeles")
timezone.localize(morning)
Point = namedtuple("Point", ["x", "y"])

def cartesian_distance(loc1, loc2):
    return math.sqrt(
        (loc1.x - loc1.x) ** 2 +
        (loc1.y - loc2.y) ** 2
    )

def geometric_median(locs):
    return (
        sum([l["longitude"] for l in locs]) / len(locs),
        sum([l["latitude"] for l in locs]) / len(locs)
    )

class Solution:
    def __init__(self, location, locations, radius=0.0001):
        self.loc = location
        self.locations = locations
        self.radius = radius

    def cost(self):
        return sum([cartesian_distance(self.loc, loc) for loc in self.locations])

    def neighbours(self):
        locs = [
            Point(self.loc.x + self.radius, self.loc.y),
            Point(self.loc.x - self.radius, self.loc.y),
            Point(self.loc.x, self.loc.y + self.radius),
            Point(self.loc.x, self.loc.y - self.radius)
        ]
        return [Solution(loc, self.locations, self.radius) for loc in locs]

    def __str__(self):
        return f"{self.loc}"

class TravelSolution:
    def __init__(self, location, locations, gmaps, radius=0.0001):
        self.loc = location
        self.locations = locations
        self.radius = radius
        self.gmaps = gmaps
        self._cost = None

    def cost(self):
        if self._cost:
            return self._cost

        r_driving = self.gmaps.distance_matrix(
            origins=self._src(),
            destinations=self._dst(),
            mode="driving",
            departure_time=morning)
        self._cost = sum(self._travel_times(r_driving))
        return self._cost

    def neighbours(self):
        locs = [
            Point(self.loc.x + self.radius, self.loc.y),
            Point(self.loc.x - self.radius, self.loc.y),
            Point(self.loc.x, self.loc.y + self.radius),
            Point(self.loc.x, self.loc.y - self.radius)
        ]
        return [TravelSolution(loc, self.locations, self.gmaps, self.radius) for loc in locs]

    def _src(self):
        return [(loc.y, loc.x) for loc in self.locations]

    def _dst(self):
        return [(self.loc.y, self.loc.x)]

    def _travel_times(self, response):
        """Return the travel times from the distance matrix api"""
        rows = response["rows"]
        times = []
        for row in rows:
            element = row["elements"][0]
            if element["status"] != "OK":
                print("Skipping", row)
                continue
            times.append(element["duration"]["value"])
        return times

    def __str__(self):
        return f"{self.loc}"

def hill_climb(sol, max_iterations=10000):
    for i in range(max_iterations):
        if i % 10:
            print(f"Iteration {i}")
        neighbours = sol.neighbours()
        best = sorted(neighbours, key=lambda n: n.cost())[0]
        if best.cost() >= sol.cost():
            break
        sol = best
    print(f"Solution found in {i} iterations")
    return sol

def simulated_annealing(sol, temp=1000, iters=100, coefficient=0.6):
    while temp > 1:
        print(f"Temperature is {temp}")
        for j in range(iters):
            if j % 10 == 0:
                print(f"Iteration {j}")
            n = random.choice(sol.neighbours())
            change = n.cost() - sol.cost()
            if change < 0 or random.random() < math.exp(-change/temp):
                sol = n
        temp = temp * 0.6
    return sol