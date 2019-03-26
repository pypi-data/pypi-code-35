r"""
Counting functions for fatgraphs
"""

from __future__ import print_function, absolute_import

from collections import defaultdict

from sage.misc.cachefunc import cached_function
from sage.misc.misc_c import prod
from sage.rings.integer_ring import ZZ
from sage.rings.rational_field import QQ
from sage.arith.all import factorial, binomial

#
# Counting function
#

@cached_function
def _unicellular_dv_rec(pv):
    assert all(x[0] >= 3 and x[1] >= 1 for x in pv)

def _unicellular_no2_pv(pv):
    if pv.get(1, 0):
        # string
        pv[1] -= 1
        res = QQ.zero()
        for i,j in list(pv.items()):
            if i == 1:
                continue
            jj = m.get(i-1, 0)
            ppv[i] -= 1
            if i-1 in ppv:
                ppv[i-1] += 1
            else:
                ppv[i-1] = 1

            k = tuple((i,j) for i,j in sorted(ppv.items()) if j)
            res += (i-1) * ppv[i-1] / m1 * _unicellular_no2_pv(ppv)
            ppv[i-1] -= 1
            ppv[i] += 1

        return res

    else:
        # cut and join
        raise NotImplementedError

def unicellular_dv(dv):
    r"""
    Return the number of (unrooted, unlabelled) unicellular fat graphs
    with prescribed vertex degrees ``dv``.
    """
    n = sum(dv)
    pv = to_exp(dv)

    # number of edges
    if n % 2:
        raise ValueError
    ne = n // 2

    # genus
    g = 1 + ne - len(dv)
    if g % 2:
        raise ValueError
    g //= 2

    coeff = 1

    # dilaton
    m2 = sum(x == 2 for x in dv)
    if m2:
        coeff *= binomial(ne - 1, m2)
        dv = [x for x in dv if x != 2]

    return coeff * _unicellular_no2_exp(to_exp(dv))

##############################################################################
# Counting based on exhaustive generation                                    #
# (mainly for debugging since we have string/dilaton/cut-and-join available) #
##############################################################################

@cached_function
def _epsilon_lazy(g, nmax):
    r"""
    Count of unicellular maps with fixed degree sequence.

    INPUT:

    - ``g`` - the genus

    - ``nmax`` -- maximum number of vertices

    OUTPUT: a pair of dictionaries

    EXAMPLES::

        sage: from surface_dynamics.topology.fat_graph_count import _epsilon_lazy

        sage: laut, lnum = _epsilon_lazy(0, 4)
        sage: for k in sorted(laut):
        ....:     print(k, laut[k])
        (1, 1) 1/2
        (2, 1, 1) 1/2
        (2, 2, 1, 1) 1/2
        (3, 1, 1, 1) 1/3
        sage: for k in sorted(lnum):
        ....:     print(k, lnum[k])
        (1, 1) 1
        (2, 1, 1) 1
        (2, 2, 1, 1) 1
        (3, 1, 1, 1) 1
    """
    from .fat_graph import FatGraphs_g_nf_nv
    from collections import defaultdict
    from sage.rings.all import ZZ, QQ
    res_aut = defaultdict(QQ)  # degrees -> number of unrooted maps (weight 1/Aut)
    res_num = defaultdict(ZZ)  # degrees -> number of unrooted maps (weight 1)
    for cm,a in FatGraphs_g_nf_nv(g, nmax, 1, intermediate=True):
        d = tuple(sorted(cm.face_degrees(), reverse=True))
        a = 1 if a is None else a.group_cardinality()
        res_aut[d] += QQ((1,a))
        res_num[d] += 1
    return res_aut, res_num

@cached_function
def _epsilon(g):
    from collections import defaultdict
    from sage.rings.all import ZZ, QQ
    from .fat_graph import FatGraphs_g_nf_nv
    res_aut = defaultdict(QQ)  # degrees -> number of unrooted maps (weight 1/Aut)
    res_num = defaultdict(ZZ)  # degrees -> number of unrooted maps (weight 1)
    for cm,a in FatGraphs_g_nf_nv(g, 1, 4*g-2, vertex_min_degree=3, intermediate=True):
        d = tuple(sorted(cm.vertex_degrees(), reverse=True))
        a = 1 if a is None else a.group_cardinality()
        res_aut[d] += QQ((1,a))
        res_num[d] += 1
    return res_aut, res_num

def to_exp(mu):
    d = defaultdict(int)
    for m in mu:
        d[m] += 1
    return d

def to_flat(d):
    r = []
    for i in sorted(d, reverse=True):
        j = d[i]
        if j:
            r.extend([i]*j)
    return tuple(r)

def fact_mult(k):
    return prod(factorial(x) for x in to_exp(k).values())

def part_string(mu):
    return '\\left[' + ','.join('%d' % i if j==1 else '%d^%d' % (i,j) for i,j in sorted(to_exp(mu).items(), reverse=True)) + '\\right]'




def check_unicellular_string(g, n):
    r"""
    Check the string equation (adding poles).
    """
    L = dict(_epsilon_lazy(g, n)[0])
    for k in L:
        if 1 in k and k != (1,1):
            m = to_exp(k)
            t = m[1]
            m[1] -= 1
            s = 0   # labeled version
            ss = 0  # unlabeled version
            for i,j in m.items():
                if i == 1:
                    continue
                jj = m.get(i-1, 0)
                m[i] -= 1
                if i-1 in m:
                    m[i-1] += 1
                else:
                    m[i-1] = 1
                kk = to_flat(m)
                s  += (i-1) * j * fact_mult(kk) * L[kk]  # labeled
                ss += (i-1) * (jj + 1) * L[kk] / t       # unlabeled
                m[i-1] -= 1
                m[i] += 1
            assert fact_mult(k) * L[k] == s, k
            assert L[k] == ss, (k, L[k], ss)

def check_unicellular_dilaton(g, n):
    r"""
    Check the dilaton equation (adding regular point).
    """
    L = dict(_epsilon_lazy(g, n)[0])
    for k in L:
        if 2 in k:
            # version where we removed a single "2"
            m = to_exp(k)
            t = m[2]
            m[2] -= 1
            kk = to_flat(m)
            n = (sum(kk)) / 2
            assert t * L[k] == n * L[kk]
            assert fact_mult(k) * L[k] == fact_mult(kk) * n * L[kk]

            # version where we removed all "2" at once
            m = to_exp(k)
            t = m[2]
            m[2] = 0
            kk = to_flat(m)
            n = (sum(kk)) / 2
            assert L[k] == binomial(n+t-1,t) * L[kk]
            n = (sum(k)) / 2
            assert L[k] == binomial(n-1,t) * L[kk]

def check_unicellular_cut_and_join(g, n):
    r"""
    Check cut-and-join equation that relates the counting for (g,n) in terms
    of (g-1,n+1) and (g,n-1).
    """
    L = dict(_epsilon_lazy(g,n)[0])
    LL = dict(_epsilon_lazy(g-1,n+1)[0])
    for k in sorted(L, key=lambda k: (-len(k), k), reverse=True):
        D = list(k)

        s1 = 0
        for j in range(1,len(D)):
            for i in range(j):
                if D[i] == D[j] == 1:
                    continue
                dj = D.pop(j)
                di = D.pop(i)
                D.append(di+dj-2)
                s1 += (di + dj - 2) * fact_mult(D) * L[tuple(sorted(D, reverse=True))]
                assert D.pop() == di+dj-2
                D.insert(i, di)
                D.insert(j, dj)
                assert D == list(k)

        s2 = 0
        for i in range(len(D)):
            di = D[i]
            if di < 4:
                continue
            D.pop(i)
            for a in range(1, di - 2):
                b = di - 2 - a
                D.append(a)
                D.append(b)
                s2 += a * b * fact_mult(D) * LL[tuple(sorted(D, reverse=True))]
                assert D.pop() == b
                assert D.pop() == a
            D.insert(i, di)
            assert D == list(k)

        assert sum(k) / 2 * fact_mult(k) * L[k] == s1 + s2 / 2

