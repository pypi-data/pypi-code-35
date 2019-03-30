import methoddispatch
import math
import itertools
import operator
import networkx as nx
import copy
from functools import reduce

from crestdsl.caching import Cache

from .tctl import *  # I know, I know...  but otherwise the formulas become unreadable !!
from .tctl import AtomicProposition, NamedAtomicProposition  # * in tctl only offers some of the classes, we need all !
from .normalform import normalform
from .pointwise import PointwiseModelChecker, CREST_PROPS

from crestdsl.simulation.epsilon import Epsilon

import logging
logger = logging.getLogger(__name__)

PA = NamedAtomicProposition("pa")  # we need this as a constant


# https://stackoverflow.com/a/45325587/3793083
def float_gcd(a, b, rtol=1e-05, atol=1e-08):
    t = min(abs(a), abs(b))
    while abs(b) > rtol * t + atol:
        a, b = b, a % b
    return a


def get_gcd(operands):
    return reduce(float_gcd, operands)


class ContinuousModelChecker(PointwiseModelChecker):
    """
    This is the CONTINUOUS model checker, which operates on sets of nodes.
    Before doing pointwise model checking, it adapts the formula and CREST Kripke structure
    according to Lepri et al.  Read the paper for more information.

    WARNING: I guess this can be slow for very large state spaces!
    """

    def calculate_gcd_and_gamma(self, formula, crestKripke):
        # calculate GCD & gamma (it's half)
        edge_weights = {w for (u, v, w) in crestKripke.edges.data('weight') if w is not None}
        logger.debug(f"edge_weights: {edge_weights}")
        bounds = set()
        if formula is not None:
            formula_intervals = [(interval.start, interval.end) for interval in formula.get_intervals()]
            bounds = {bound for tuple in formula_intervals for bound in tuple}
        logger.debug(f"interval bounds: {bounds}")
        gcd_operands = set.union(edge_weights, bounds) - {None, 0, math.inf}  # filter None, zero and infinite
        logger.debug(f"GCD operands: {gcd_operands}")
        self.gcd = get_gcd(gcd_operands)
        self.gamma = self.gcd/2
        return self.gamma

    def gamma_split(self, crestKripke, gamma):
        edges_to_change = [e for e in crestKripke.edges.data('weight') if e[2] > gamma]
        logger.debug(f"Need to split {len(edges_to_change)} transitions during gamma split")
        for src, tgt, weight in edges_to_change:
            src_props = crestKripke.nodes[src].get(CREST_PROPS, dict())
            edge_transitions = crestKripke.get_edge_data(src, tgt).get("transitions", [])
            parts = int(round(weight / gamma))  # how many parts this transition is split into

            crestKripke.remove_edge(src, tgt)
            # add new edges
            prev = src  # stores the source of new edge, target is created
            for idx in range(1, parts):
                newnode = hash(src) + hash(tgt) + idx
                crestKripke.add_node(newnode, crest_props=copy.copy(src_props), gammanode=True)
                crestKripke.add_edge(prev, newnode, weight=gamma, transitions=[])
                if idx % 2 == 0:  # even
                    crestKripke.nodes[newnode][CREST_PROPS][PA] = False
                else:  # odd
                    crestKripke.nodes[newnode][CREST_PROPS][PA] = True
                prev = newnode
            crestKripke.add_edge(prev, tgt, weight=gamma, transitions=edge_transitions)
        logger.info(f"Finished gcd/2-transformation, gcd/2 = {gamma}")
        return crestKripke

    def gamma_split_optimised(self, crestKripke, gamma):
        """ all outgoing transitions from a node have the same length.
        (otherwise we wouldn't have must semantics)
        We can therefore group the edges per node until the last new node."""

        original_nodes = list(crestKripke.nodes())
        for node in original_nodes:
            outgoing = list(crestKripke.out_edges(node, data="weight"))
            if len(outgoing) > 0 and outgoing[0][2] > gamma:
                src_props = crestKripke.nodes[node].get(CREST_PROPS, dict())

                parts = int(round(outgoing[0][2] / gamma))  # how many parts this transition is split into

                # create list of new nodes
                prev = node  # stores the source of new edge, target is created
                for idx in range(1, parts):
                    newnode = hash(node) + idx
                    crestKripke.add_node(newnode, crest_props=copy.copy(src_props), gammanode=True)
                    crestKripke.add_edge(prev, newnode, weight=gamma, transitions=[])
                    if idx % 2 == 0:  # even
                        crestKripke.nodes[newnode][CREST_PROPS][PA] = False
                    else:  # odd
                        crestKripke.nodes[newnode][CREST_PROPS][PA] = True
                    prev = newnode

                # connect last new node to targets and
                # remove original edge between src and tgt
                for src, tgt, weight in outgoing:
                    edge_transitions = crestKripke.get_edge_data(src, tgt).get("transitions", [])
                    crestKripke.add_edge(prev, tgt, weight=gamma, transitions=edge_transitions)
                    crestKripke.remove_edge(src, tgt)

        logger.info(f"Finished gcd/2-transformation, gcd/2 = {gamma}")
        return crestKripke

    def make_CREST_Kripke(self, formula, crestKripke=None):
        logger.info(f"Adapting Kripke for continuous model checking (gcd/2-transformation)")
        crestKripke = super().make_CREST_Kripke(formula, crestKripke)

        # replace epsilons so we have all absolute values
        epsilon_replaced = crestKripke.copy()
        for src, tgt, weight in epsilon_replaced.edges.data('weight'):
            if isinstance(weight, Epsilon):
                epsilon_replaced.edges[src, tgt]['weight'] = weight.to_number(eps_value=0)

        if self.has_zero_cycles(epsilon_replaced):
            logger.warning("Epsilon was set to zero. Thus we have now cycles of total length 0. This can lead to problems in certain algorithms.")

        self.calculate_gcd_and_gamma(formula, epsilon_replaced)

        # split each edge according to self.gamma
        # (don't worry about the repsective system states,
        #  we only care about properties for now)
        GAMMA_Kripke = epsilon_replaced.copy()

        self.gamma_split_optimised(GAMMA_Kripke, self.gamma)  # in place edit of the CK

        logger.debug(f"size before: {len(crestKripke.nodes())} nodes, {len(crestKripke.edges())} transitions")
        logger.debug(f"size after: {len(GAMMA_Kripke.nodes())} nodes, {len(GAMMA_Kripke.edges())} transitions")
        return GAMMA_Kripke


    def check_tctl(self, formula, systemstate=None):
        crestKripke = self.make_CREST_Kripke(formula)

        logger.info(f"Checking formula {formula}")

        formula = normalform(formula)  # translate to normalform
        logger.info(f"normalform {formula}")
        logger.info(f"alpha(normalform) {self.alpha(formula)}")
        formula = normalform(self.alpha(formula))

        logger.info(f"NF(alpha(NF(formula)) {formula}")
        formula = self.beta(formula)  # adapt formula according to paper

        logger.info(f"beta(NF(alpha(NF(formula))) {formula}")

        logger.debug(f"alpha-beta Transformed formula: {formula}")

        sat_set = self.is_satisfiable(formula, crestKripke)

        if systemstate is None:
            systemstate = crestKripke.graph["root"]

        logger.info(f"Found {len(sat_set)} nodes that satisfy formula {str(formula)}.\n The state we're interested in is among them -> {(systemstate in sat_set)}")
        return systemstate in sat_set

    """ START BETA """

    @methoddispatch.singledispatch
    def beta(self, formula):
        msg = f"Don't know how to do beta-transform on formula {formula} of type {type(formula)}"
        logger.error(msg)
        raise ValueError(msg)

    @beta.register(bool)
    def beta_bool(self, formula):
        return formula

    @beta.register(AtomicProposition)
    def beta_AP(self, formula):
        return formula

    @beta.register(Not)
    def beta_Not(self, formula):
        return Not(self.beta(formula.phi))

    @beta.register(And)
    def beta_And(self, formula):
        return And(self.beta(formula.phi), self.beta(formula.psi))

    @beta.register(EU)
    def beta_EU(self, formula):
        new_psi = EU(self.beta(formula.phi), (And(self.beta(formula.psi), Or(Not(PA), self.beta(formula.phi)))), formula.interval)
        if formula.interval.ininterval(0):
            return Or(self.beta(formula.psi), new_psi)
        return new_psi

    @beta.register(AU)
    def beta_AU(self, formula):
        new_psi = AU(self.beta(formula.phi), (And(self.beta(formula.psi), Or(Not(PA), self.beta(formula.phi)))), formula.interval)
        if formula.interval.ininterval(0):
            return Or(self.beta(formula.psi), new_psi)
        return new_psi

    """ END BETA """

    """ Start ALPHA """
    @methoddispatch.singledispatch
    def alpha(self, formula):
        return formula

    @alpha.register(bool)
    def alpha_bool(self, formula):
        return formula

    @alpha.register(AtomicProposition)
    def alpha_AP(self, formula):
        return formula

    @alpha.register(Not)
    def alpha_Not(self, formula):
        return Not(self.alpha(formula.phi))

    @alpha.register(And)
    def alpha_And(self, formula):
        return And(self.alpha(formula.phi), self.alpha(formula.psi))

    @alpha.register(EU)
    def alpha_EU(self, formula):
        intvl = formula.interval
        a_phi = self.alpha(formula.phi)
        a_psi = self.alpha(formula.psi)

        I_1 = Interval()
        I_1.start = intvl.start if (intvl.start_operator == operator.ge) else (intvl.start + self.gamma)
        I_1.end = intvl.end if (intvl.end_operator == operator.le) else (intvl.end - self.gamma)

        I_2 = (Interval() >= intvl.start) <= intvl.end

        p1 = And(Not(PA), EU(a_phi, a_psi, interval=I_1))
        p2 = And(PA,      EU(a_phi, a_psi, interval=I_2))
        return Or(p1, p2)

    @alpha.register(AU)
    def alpha_AU(self, formula):
        intvl = formula.interval
        a_phi = self.alpha(formula.phi)
        a_psi = self.alpha(formula.psi)

        I_1 = Interval()
        I_1.start = intvl.start if (intvl.start_operator == operator.ge) else (intvl.start + self.gamma)
        I_1.end = intvl.end if (intvl.end_operator == operator.le) else (intvl.end - self.gamma)

        I_2 = (Interval() >= intvl.start) <= intvl.end

        p1 = And(Not(PA), AU(a_phi, a_psi, interval=I_1))
        p2 = And(PA,      AU(a_phi, a_psi, interval=I_2))
        return Or(p1, p2)
    """ END ALPHA """
