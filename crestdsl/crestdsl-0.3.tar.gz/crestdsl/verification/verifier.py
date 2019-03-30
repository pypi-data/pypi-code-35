import math

from . import tctl
from .modelchecker import ModelChecker
from .statespace import StateSpace

import logging
logger = logging.getLogger(__name__)

def reachable(check):
    form = tctl.EF(check)
    return Verifier(formula=form)

def always(check):
    form = tctl.AG(check)
    return Verifier(formula=form)

def always_reachable(check):
    form = tctl.AG(tctl.AF(check))
    return Verifier(formula=form)

def always_reachable_within(check, timer):
    form = tctl.AG(tctl.AF(check, interval=Interval() <= timer))
    return Verifier(formula=form)

class Verifier(object):

    def __init__(self, formula, system=None):
        self.formula = formula
        self.system = system
        self.explored = False

    def set_system(self, system):
        self.system = system
        self.statespace = StateSpace(system)

    def in_system(self, system):
        self.set_system(system)
        return self

    def explore(self):
        explore_time = self.formula.interval.end
        if explore_time == math.inf:
            logger.warning(f"Caution: No end time set for formula. This means statespace will be explored until exhausted (or forever !!)")
        self.statespace.explore_until_time(explore_time)

    def check(self, draw_result=False):
        logger.info(f"Evaluating satisfiability of formula {self.formula}")
        self.explore()
        assert self.statespace is not None, "The verifier does not have access to a statespace. Have you set the system?"
        mc = ModelChecker(self.statespace)
        result = mc.check(self.formula)
        if draw_result:
            mc.draw(self.formula)
        logger.info(f"Formula {self.formula} is satisfiable: {result}")
        return result


    def before(self, time):
        self.formula.interval.end = time
        return self


    def after(self, time):
        self.formula.interval.start = time
        return self
