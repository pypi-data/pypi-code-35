from ethics.language import *


def isResult(setofsets, cand):
    for s in setofsets:
        if len(set(s).intersection(set(cand))) == 0:
            return False
    return True


def makeUnion(setofsets):
    r = set()
    for s in setofsets:
        r = r.union(s)
    return r


def searchSet(setofsets, s):
    frontier = [[]]
    goals = []
    for f in frontier:
        if len(goals) > 0:
            return goals
        for e in s:
            if e not in f:
                exp = f + [e]
                if isResult(setofsets, exp):
                    goals += [exp]
                else:
                    frontier += [exp]


def searchAllSets(setofsets, s):
    frontier = [[]]
    goals = []
    for f in frontier:
        for e in s:
            if e not in f:
                exp = f + [e]
                if isResult(setofsets, exp):
                    goals += [exp]
                else:
                    frontier += [exp]
    return goals


def smallestHittingSet(setofsets):
    s = makeUnion(setofsets)
    return searchSet(setofsets, s)
    

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


def alltHittingSets(setofsets):
    s = makeUnion(setofsets)
    allsets = searchAllSets(setofsets, s)
    return minimalSets(allsets)

# <Mwa, perm, reason, type> 
def generateReasons(formel, perm, model, principle): 
    if perm:
        formel_grounded = principle.mapSymbolToFormula(formel)
    else:
        formel_grounded = principle.mapSymbolToFormula(Not(formel))
    result = []
    #print("START DNF " + str(time.time()))
    formel_dnf = formel_grounded.dnf(model, principle)
    #print("END DNF " + str(time.time()))
    #print("START CONJ LIST " + str(time.time()))
    formel_dnf_list = formel_dnf.asConjList()
    #print("END CONJ LIST " + str(time.time())+ " len: "+str(len(formel_dnf_list)))
    #print("START TRUE CONJUNCTIONS")
    trueConjunctions = []
    for c in formel_dnf_list:
        if model.models(Formula.makeConjunction(c)):
            trueConjunctions.append(c)
    #print("END TRUE CONJUNCTIONS " + str(time.time())+ " len: "+str(len(trueConjunctions)))
    #print("START MINIMAL SETS " + str(time.time()))
    trueConjunctions = minimalSets(trueConjunctions)
    #print("END MINIMAL SETS " + str(time.time())  + " len: "+str(len(trueConjunctions)))
    #print("START SUFFICIENT REASONS " + str(time.time()))
    for c in trueConjunctions:
        result.append({"model": model, "perm": perm, "reason": Formula.makeConjunction(c), "type": "sufficient"})
    #print("END SUFFICIENT REASONS " + str(time.time()))   
    #print("START NECESSARY REASONS " + str(time.time()))
    for c in alltHittingSets(trueConjunctions):
        result.append({"model": model, "perm": perm, "reason": Formula.makeDisjunction(c), "type": "necessary"})
    #print("END NECESSARY REASONS " + str(time.time()))
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
