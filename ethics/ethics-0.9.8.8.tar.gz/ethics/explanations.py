from pysat.solvers import Solver
from ethics.language import *
from ethics.tools import *
from itertools import combinations


def noDuplicate(r, s):
    for e in r:
        if set(e) == set(s):
            return False
    return True


def minimalSets(setofsets):
    r = []
    for s1 in setofsets:
        no = False
        for s2 in setofsets:
            if set(s1) > set(s2):
                no = True
                break
        if not no and noDuplicate(r, s1):
            r += [s1]
    return r


def generateReasons(model, principle):
    suff = generateSufficientReasons(model, principle)
    necc = generateNecessaryReasons(model, principle)

    result = []
    perm = model.evaluate(principle)

    for c in suff:
        result.append({"model": model, "perm": perm, "reason": c, "type": "sufficient"})
    for c in necc:
        result.append({"model": model, "perm": perm, "reason": c, "type": "necessary"})

    return result


def identifyINUSReasons(reasons):
    suff = [r["reason"] for r in reasons if r["type"] == "sufficient"]
    nec = [r["reason"] for r in reasons if r["type"] == "necessary"]
    inus = []

    for rn in nec:
        rn_check = None
        if isinstance(rn, str):
            rn_check = [rn]
        else:
            rn_check = rn.getClause()
        for rs in suff:
            rs_check = None
            if isinstance(rs, str):
                rs_check = [rs]
            else:
                rs_check = rs.getConj()
            if set(rn_check) <= set(rs_check):
                inus.append(Formula.makeDisjunction(rn_check))
                break
    return inus


def isAlreadyCovered(cand, results):
    for r in results:
        if set(r) <= set(cand):
            return True
    return False


def suffReasons(fo):

    d, m = fo.dimacs()
    s = Solver()
    s.append_formula(d)
    
    # Rename
    suff = [mapBackToFormulae(e, m) for e in s.enum_models()]
    s.delete()
    
    #print("SUFFLEN", len(suff))
    
    # Are there sufficient subsets of the models?
    realsuffs = []
    for cand in suff:
        for k in range(1, len(cand)+1):
            for c in combinations(cand, k):
                if not isAlreadyCovered(c, realsuffs):
                    f = And(Formula.makeConjunction(c), Not(fo)).cnf()
                    f = f.dimacs()[0]
                    s = Solver()
                    s.append_formula(f)
                    if not s.solve():
                        realsuffs.append(list(c))
                    s.delete()
    
    return realsuffs


def generateSufficientReasons(model, principle):
    perm = principle.permissible()
    if perm:
        f = principle.mapSymbolToFormula(principle.buildConjunction()).cnf()
    else:
        f = principle.mapSymbolToFormula(Not(principle.buildConjunction())).cnf()
    suff = suffReasons(f)
    # Filter: Only the satisfied ones    
    suff = [Formula.makeConjunction(e) for e in suff if model.models(Formula.makeConjunction(e))]
    return suff


def generateNecessaryReasons(model, principle):
    perm = principle.permissible()
    if perm:
        f = principle.mapSymbolToFormula(Not(principle.buildConjunction())).cnf()
    else:
        f = principle.mapSymbolToFormula(principle.buildConjunction()).cnf()
    suff = suffReasons(f)
    
    result = []
    for rs in suff:
        cl = []
        for s in rs:
            if not model.models(s):
                cl.append(s)
        if len(cl) > 0:
            cl_neg = []
            for c in cl:
                cl_neg.append(Not(c).nnf())
            result.append(Formula.makeDisjunction(cl_neg))
    return result


