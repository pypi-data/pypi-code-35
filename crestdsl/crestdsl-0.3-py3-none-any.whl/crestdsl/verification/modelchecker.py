import itertools
import networkx as nx
from functools import reduce

from .continuous import ContinuousModelChecker
from .pointwise import CREST_PROPS

#
# from .tctl import *  # I know, I know...  but otherwise the formulas become unreadable !!
# from .tctl import NamedAtomicProposition, TCTLFormula  # * in tctl only offers some of the classes, we need all !
from .statespace import EXPLORED
# from .reachabilitycalculator import ReachabilityCalculator

import logging
logger = logging.getLogger(__name__)


class ModelChecker(ContinuousModelChecker):

    def make_CREST_Kripke(self, formula, crestKripke=None):
        logger.info(f"Adapting Kripke for model checking (remove epsilon, gcd/2-transformation)")
        crestKripke = super().make_CREST_Kripke(formula, crestKripke)

        # INFO: What to do with explored leaf nodes (where time advance infinitely, but properties don't change)
        # We should add a self-loop to indicate that time advances
        # Thoughts:
        # --> self-loops work, because in the end an advance kinda returns to the state where all properties remain the same
        # --> since we operate on Propositions and not the actual states, this should work nicely
        # --> we do not change the state space after all, only the crestKripke for the analysis
        # --> we create a Strongly Connected Component with one state where all properties remain the same
        # --> but what is the transition time?
        # --> It should not be 0, because the formal semantics exclude zeno behaviour.
        # --> Also the EUab algorithm is weird. Epsilon would be a possibility, but this would be replaced by gamma too.

        # --> maybe we should do GCD/2 (i.e. gamma), to show that time advances?
        # --> the algorithm really doesn't care much,
        # --> but it should be a multiple of gamma so that we don't need another gcd calculation !!
        # --> if it's a multiple, we need additional states. Therefore it's gamma.
        # --> Let's test it!

        # iterate over explored leaves
        for node, explored in crestKripke.nodes(data=EXPLORED, default=False):
            if crestKripke.out_degree(node) == 0 and explored:
                crestKripke.add_edge(node, node, weight=self.gcd)   # don't introduce new state

        # split again
        self.gamma_split_optimised(crestKripke, self.gamma)

        return crestKripke

    """ a few optimisations """

    def issatisfiable_tctlAnd(self, formula, crestKripke):
        if formula.phi is False or formula.psi is False:
            # logger.debug(f"And Shortcut {formula}")
            return set()
        if formula.phi is True:
            # logger.debug(f"And Shortcut {formula}")
            return self.is_satisfiable(formula.psi, crestKripke)
        if formula.psi is True:
            # logger.debug(f"And Shortcut {formula}")
            return self.is_satisfiable(formula.phi, crestKripke)
        # Default
        return super().issatisfiable_tctlAnd(formula, crestKripke)

    def issatisfiable_tctlOr(self, formula, crestKripke):
        if formula.phi is True or formula.psi is True:
            # logger.debug(f"Or Shortcut {formula}")
            return crestKripke.nodes
        if formula.phi is False:
            # logger.debug(f"Or Shortcut {formula}")
            return self.is_satisfiable(formula.psi, crestKripke)
        if formula.psi is False:
            # logger.debug(f"Or Shortcut {formula}")
            return self.is_satisfiable(formula.phi, crestKripke)
        # Default
        return super().issatisfiable_tctlOr(formula, crestKripke)

    def Sat_EU(self, formula, crestKripke, phi_set=None, psi_set=None):
        """ Original implementation of Lepri et al """
        Q1 = phi_set if (phi_set is not None) else self.is_satisfiable(formula.phi, crestKripke)
        Q2 = psi_set if (psi_set is not None) else self.is_satisfiable(formula.psi, crestKripke)

        Q1_view = crestKripke.subgraph(Q1)
        Q = set()
        Q_todo = Q2  # not yet visited

        while len(Q_todo) > 0:
            q = Q_todo.pop()
            Q.add(q)  # say that we visited it

            Q_todo |= set(Q1_view.pred[q]) - Q  # add the predecessors of q we haven't seen yet
        return Q
