r"""
Fat graph and iteration over fat graphs.

This is done following the McKay algorithm.
"""

from __future__ import absolute_import, print_function
from six.moves import range, map, zip

from sage.misc.cachefunc import cached_function

from array import array
from collections import deque
from surface_dynamics.misc.permutation import *

###########################
# Miscellaneous functions #
###########################

def _perm_recompute_angle(p, a, i):
    r"""
    Reset the angles of the orbit of i by p in the array a
    """
    a[i] = 0
    j = p[i]
    k = 1
    while j != i:
        a[j] = k
        k += 1
        j = p[j]

def num_and_weighted_num(it):
    from sage.rings.integer_ring import ZZ
    from sage.rings.rational_field import QQ
    s = QQ.zero()
    n = ZZ.zero()
    for _,aut in it:
        n += ZZ.one()
        if aut is None:
            s += QQ.one()
        else:
            s += QQ((1,aut.group_cardinality()))
    return n,s

#####################
# Fat graph #
#####################


# fa is only used for unicellular maps
class FatGraph(object):
    r"""
    EXAMPLES:

    The once punctured torus::

        sage: from surface_dynamics import FatGraph

        sage: vp = '(0,2,1,3)'
        sage: ep = '(0,1)(2,3)'
        sage: fp = '(0,2,1,3)'
        sage: FatGraph(vp, ep, fp)
        Fat graph with passport ([4], [4])
         vp = (0,2,1,3)
         ep = (0,1)(2,3)
         fp = (0,2,1,3)

    Actually it is enough to specify 2 of the 3 permutations::

        sage: vp = '(0,3,1)(4)(2,5,6,7)'
        sage: ep = '(0,1)(2,3)(4,5)(6,7)'
        sage: fp = '(0,3,7,5,4,2)(1)(6)'
        sage: F0 = FatGraph(vp=vp, ep=ep, fp=fp)
        sage: F1 = FatGraph(ep=ep, fp=fp)
        sage: F2 = FatGraph(vp=vp, fp=fp)
        sage: F3 = FatGraph(vp=vp, ep=ep)
        sage: F0 == F1 and F0 == F2 and F0 == F3
        True
    """
    __slots__ = ['_n',  # number of darts (non-negative integer)
                 '_vp', # vertex permutation (array of length _n)
                 '_ep', # edge permutation (array of length _n)
                 '_fp', # face permutation (array of length _n)
                 # cycle decompositions
                 # labels
                 '_vl', # vertex labels (array of length _n)
                 '_fl', # face labels (array of length _n)
                 # angles
                 '_fa', # face angles (array of length _n)
                 # numbers
                 '_nv', # number of vertices (non-negative integer)
                 '_nf', # number of faces (non-negative integer)
                 # degrees
                 '_vd', # vertex degrees (array of length _nv)
                 '_fd'] # face degrees (array of length _nf)

    def __init__(self, vp=None, ep=None, fp=None, max_num_dart=None, check=True):
        vp, ep, fp = constellation_init(vp, ep, fp)
        self._vp = vp
        self._ep = ep
        self._fp = fp
        if len(vp) != len(ep) or len(vp) != len(fp):
            raise ValueError("invalid permutations")
        self._n = len(vp)   # number of darts
        self._nf = 0        # number of faces

#        self._vl, self._va, self._vd = perm_dense_cycles_and_angles(vp)
        self._vl, _, self._vd = perm_dense_cycles_and_angles(vp)
        self._nv = len(self._vd) # number of vertices
        self._fl, self._fa, self._fd = perm_dense_cycles_and_angles(fp)
        self._nf = len(self._fd) # number of faces

        if max_num_dart is not None:
            if max_num_dart < self._n:
                raise ValueError
            self._realloc(max_num_dart)

        if check:
            self._check()

    def _realloc(self, max_num_dart):
            if max_num_dart < self._n:
                return
            self._vp.extend([-1] * (max_num_dart - self._n))
            self._ep.extend([-1] * (max_num_dart - self._n))
            self._fp.extend([-1] * (max_num_dart - self._n))
            self._vl.extend([-1] * (max_num_dart - self._n))
            self._fl.extend([-1] * (max_num_dart - self._n))
#            self._va.extend([-1] * (max_num_dart - self._n))
            self._fa.extend([-1] * (max_num_dart - self._n))
            self._vd.extend([-1] * (max_num_dart - self._nv))
            self._fd.extend([-1] * (max_num_dart - self._nf))

    @staticmethod
    def from_unicellular_word(X):
        r"""
        Build a fat graph from a word on the letters {0, ..., n-1} where
        each letter appears exactly twice.

        EXAMPLES::

            sage: from surface_dynamics import FatGraph
            sage: FatGraph.from_unicellular_word([0,1,0,2,3,4,1,4,3,2])
            Fat graph with passport ([10], [4, 2, 2, 2])
             vp = (0,3)(1,2,6,7)(4,9)(5,8)
             ep = (0,2)(1,6)(3,9)(4,8)(5,7)
             fp = (0,1,2,3,4,5,6,7,8,9)
            sage: FatGraph.from_unicellular_word([0,1,2,0,3,2,4,1,3,4])
            Fat graph with passport ([10], [6, 4])
             vp = (0,6,2,7,9,4)(1,3,5,8)
             ep = (0,3)(1,7)(2,5)(4,8)(6,9)
             fp = (0,1,2,3,4,5,6,7,8,9)
        """
        n = len(X)
        m = n // 2
        ep = [None] * n
        vp = [None] * n
        fp = list(range(1,n)) + [0]
        symb_to_pos = [None] * m
        for i,k in enumerate(X):
            j = symb_to_pos[k]
            if j is not None:
                ep[i] = j
                ep[j] = i
                vp[(j + 1) % n] = i
                vp[(i + 1) % n] = j
            else:
                symb_to_pos[k] = i
        return FatGraph(vp, ep, fp)

    def _check(self, error=RuntimeError):
        vp = self._vp
        vl = self._vl
        vd = self._vd

        ep = self._ep

        fp = self._fp
        fl = self._fl
        fd = self._fd
        fa = self._fa

        n = self._n
        nf = self._nf
        nv = self._nv

        m = sum(vp[i] != -1 for i in range(n))

        if not perm_check(vp, n):
            raise ValueError("invalid vertex permutation: %s" % vp)
        if not perm_check(ep, n):
            raise ValueError("invalid edge permutation: %s" % ep)
        if not perm_check(fp, n):
            raise ValueError("invalid face permutation: %s" % fp)

        if perm_num_cycles(vp, n) != self._nv:
            raise error("wrong number of vertices")
        if perm_num_cycles(fp, n) != self._nf:
            raise error("wrong number of faces")

        if len(vl) < n or len(fl) < n or len(vd) < nv or len(fd) < nf:
               raise error("inconsistent lengths")

        if any(x < 0 or x > n for x in vd[:nv]) or sum(vd[:nv]) != m:
            raise error("invalid vertex degrees")
        if any(x < 0 or x > n for x in fd[:nf]) or sum(fd[:nf]) != m:
            raise error("invalid face degrees")

        ffd = [0] * nf
        vvd = [0] * nv

        for i in range(n):
            if vp[i] == -1:
                if ep[i] != -1 or fp[i] != -1:
                    raise ValueError("inconsistent dart activity for i={}".format(i))
                continue
            elif ep[i] == -1 or fp[i] == -1:
                raise ValueError("inconsistent dart activity for i={}".format(i))

            if fp[ep[vp[i]]] != i:
                raise error("fp[ep[vp[%d]]] = %d" % (i, fp[ep[vp[i]]]))
            if fl[i] < 0 or fl[i] >= nf:
                raise error("face label out of range: fl[%d] = %d" % (i, fl[i]))
            if vl[i] < 0 or vl[i] >= nv:
                raise error("vertex label out of range: vl[%d] = %d" % (i, vl[i]))

            if fl[fp[i]] != fl[i]:
                raise error("fl[fp[%d]] = %d while fl[%d] = %d" %(i, fl[fp[i]], i, fl[i]))
            
            if vl[vp[i]] != vl[i]:
                raise error("vl[vp[%d]] = vl[%d] = %d while vl[%d] = %d" %(i, vp[i], vl[vp[i]], i, vl[i]))

#            if va[vp[i]] != va[i] + 1:
#                if va[i] != vd[vl[i]] - 1 or va[vp[i]] != 0:
#                    raise error("inconsistent vertex angles (degree %d): va[%d] = %d but va[vp[%d]] = va[%d] = %d" % (vd[vl[i]], i, va[i], i, vp[i], va[vp[i]]))

            if fa[fp[i]] != fa[i] + 1:
                if fa[i] != fd[fl[i]] - 1 or fa[fp[i]] != 0:
                    raise error("inconsistent face angles (degree %d): fa[%d] = %d but fa[fp[%d]] = fa[%d] = %d" % (fd[fl[i]], i, fa[i], i, fp[i], fa[fp[i]]))

            ffd[fl[i]] += 1
            vvd[vl[i]] += 1

        if vvd != vd[:nv]:
            raise error("inconsistent face labels/degrees, got %s instead of vd = %s" % (vvd, vd[:nv]))
        if ffd != fd[:nf]:
            raise error("inconsistent vertex labels/degrees, got %s instead of fd = %s" %(ffd, fd[:nf]))

    def __copy__(self):
        r"""
        EXAMPLES::

            sage: from surface_dynamics.topology.fat_graph import FatGraph

            sage: vp = '(0,2,1,3)'
            sage: ep = '(0,1)(2,3)'
            sage: fp = '(0,2,1,3)'
            sage: cm = FatGraph(vp, ep, fp)
            sage: cm2 = cm.__copy__()
            sage: cm2._check()
        """
        cm = FatGraph.__new__(FatGraph)
        cm._vp = self._vp[:]
        cm._ep = self._ep[:]
        cm._fp = self._fp[:]
        cm._n = self._n
        cm._nf = self._nf
        cm._nv = self._nv
        cm._vl = self._vl[:]
        cm._fl = self._fl[:]
        cm._vd = self._vd[:]
        cm._fd = self._fd[:]
#        cm._va = self._va[:]
        cm._fa = self._fa[:]
        return cm

    def __repr__(self):
        n = self._n
        fd = self._fd[:self._nf]
        vd = self._vd[:self._nv]
        fd.sort(reverse=True)
        vd.sort(reverse=True)
        return 'Fat graph with passport (%s, %s)\n vp = %s\n ep = %s\n fp = %s' %(fd, vd, perm_cycle_string(self._vp, n=n), perm_cycle_string(self._ep, n=n), perm_cycle_string(self._fp, n=n))

    def __eq__(self, other):
        r"""
        TESTS::

            sage: from surface_dynamics.topology.fat_graph import FatGraph

            sage: vp = '(0,2,1,3)'
            sage: ep = '(0,1)(2,3)'
            sage: fp = '(0,2,1,3)'
            sage: cm1 = FatGraph(vp, ep, fp)
            sage: cm2 = FatGraph(vp, ep, fp, 100)
            sage: cm1 == cm2
            True
        """
        if type(self) != type(other):
            raise TypeError

        if self._n != other._n or self._nf != other._nf or self._nv != other._nv:
            return False

        for i in range(self._n):
            if self._vp[i] != other._vp[i] or \
               self._ep[i] != other._ep[i] or \
               self._fp[i] != other._fp[i]:
                   return False

        # here we ignore the vertex and face labels...
        return True

    def __ne__(self, other):
        return not self == other

    def vertex_permutation(self, copy=True):
        if copy:
            return self._vp[:self._n]
        else:
            return self._vp

    def edge_permutation(self, copy=True):
        if copy:
            return self._ep[:self._n]
        else:
            return self._ep

    def face_permutation(self, copy=True):
        if copy:
            return self._fp[:self._n]
        else:
            return self._fp

    def vertex_profile(self):
        return perm_cycle_type(self._vp, self._n)

    def num_darts(self):
        return self._n

    def num_folded_edges(self):
        return sum(self._ep[i] == 1 for i in range(self._n))

    def num_faces(self):
        return self._nf

    def num_vertices(self):
        return self._nv

    def vertices(self):
        return perm_cycles(self._vp, True, n)

    def vertex_degrees(self):
        return self._vd[:self._nv]

    def edges(self):
        return perm_cycles(self._ep, True, n)

    def num_edges(self):
        return self._n // 2

    def faces(self):
        return self._nf

    def face_degrees(self):
        return self._fd[:self._nf]

    def euler_characteristic(self):
        return self._nf - self._n//2 + self._nv

    def dual(self):
        r"""
        Return the dual fat graph.

        EXAMPLES::

            sage: from surface_dynamics.topology.fat_graph import FatGraph
            sage: FatGraph(vp=None,ep='(0,1)',fp='(0)(1)').dual()
            Fat graph with passport ([1, 1], [2])
             vp = (0,1)
             ep = (0,1)
             fp = ()
        """
        return FatGraph(vp = perm_invert(self._vp, self._n),
                        ep = perm_invert(self._ep, self._n),
                        fp = perm_invert(self._fp, self._n))

    def kontsevich_volume_rational_function(self, R=None):
        r"""
        This is not under an appropriate form...
        """
        raise NotImplementedError
        print('This is not quite the form under which we would like it... it should remains factorized')
        from sage.rings.rational_field import QQ
        from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing

        nf = self._nf
        fl = self._fl
        n = self._n
        ep = self._ep
        if R is None:
            R = PolynomialRing(QQ, 'b', nf)
        gens = R.gens()
        res = R.one()
        for i in range(self._n):
            j = ep[i]
            if j < i:
                continue
            res *= 1 / self.automorphism_group().group_cardinality() / (gens[fl[i]] + gens[fl[j]])
        return res

    ##############################
    # Augmentation and reduction #
    ##############################

    def _check_alloc(self, n, nv, nf):
        if len(self._vp) < n or \
           len(self._ep) < n or \
           len(self._fp) < n or \
           len(self._vl) < n or \
           len(self._fl) < n or \
           len(self._fa) < n or \
           len(self._fd) < nf or \
           len(self._vd) < nv:
               raise TypeError("reallocation needed")

    def split_face(self, i, j):
        r"""
        Insert an edge to split the face that contains the darts i and j.

        One of the face will contains i, fp[i], ..., j (the x-face) and the rest
        will consist of the complement (the y-face).

        The converse operation is implemented in :meth:`remove_edge`.

        EXAMPLES:

        The once punctured torus::

            sage: from surface_dynamics.topology.fat_graph import FatGraph

            sage: vp = '(0,2,1,3)'
            sage: ep = '(0,1)(2,3)'
            sage: fp = '(0,2,1,3)'
            sage: eps = '(0,1)(2,3)(4,5)'

            sage: vp20 = '(0,4,2,5,1,3)'
            sage: fp20 = '(0,5)(1,3,4,2)'
            sage: cm = FatGraph(vp, ep, fp, 6)
            sage: cm.split_face(2,0)
            sage: cm == FatGraph(vp20, eps, fp20)
            True

            sage: vp10 = '(0,4,2,1,5,3)'
            sage: fp10 = '(0,2,5)(1,3,4)'
            sage: cm = FatGraph(vp, ep, fp, 6)
            sage: cm.split_face(1,0)
            sage: cm == FatGraph(vp10, eps, fp10)
            True

            sage: vp30 = '(0,4,2,1,3,5)'
            sage: fp30 = '(0,2,1,5)(3,4)'
            sage: cm = FatGraph(vp, ep, fp, 6)
            sage: cm.split_face(3,0)
            sage: cm == FatGraph(vp30, eps, fp30)
            True

            sage: vp00 = '(0,5,4,2,1,3)'
            sage: fp00 = '(0,2,1,3,4)(5)'
            sage: cm = FatGraph(vp, ep, fp, 6)
            sage: cm.split_face(0,0)
            sage: cm == FatGraph(vp00, eps, fp00)
            True

            sage: vp22 = '(0,2,5,4,1,3)'
            sage: fp22 = '(0,4,2,1,3)(5)'
            sage: cm = FatGraph(vp, ep, fp, 6)
            sage: cm.split_face(2,2)
            sage: cm == FatGraph(vp22, eps, fp22)
            True

        A genus 2 surface::

            sage: vp = '(0,3,6,8)(1,10,9,12,5)(2,7,4,11)(13)'
            sage: ep = '(0,1)(2,3)(4,5)(6,7)(8,9)(10,11)(12,13)'
            sage: fp = '(0,5,7,3,11,1,8,10,4,12,13,9,6,2)'
            sage: cm = FatGraph(vp, ep, fp, 21)
            sage: cm.split_face(0,1); cm._check()
            sage: cm.split_face(4,13); cm._check()
            sage: cm.split_face(5,14); cm._check()
            sage: cm.remove_edge(18); cm._check()
            sage: cm.remove_edge(16); cm._check()
            sage: cm.remove_edge(14); cm._check()
            sage: cm == FatGraph(vp, ep, fp, 21)
            True
        """
        vp = self._vp
        vl = self._vl
        vd = self._vd
#        va = self._va

        ep = self._ep

        fp = self._fp
        fl = self._fl
        fd = self._fd
        fa = self._fa

        n = self._n
        nf = self._nf
        nv = self._nv

        i = int(i)
        j = int(j)
        if i < 0 or i >= self._n or j < 0 or j >= n or fl[i] != fl[j]:
            raise ValueError("invalid darts i=%d and j=%d for face splitting" %(i, j))

        self._check_alloc(n + 2, nv, nf + 1)

        x = self._n
        y = self._n + 1
        ii = ep[vp[i]] # = fp^-1(i)
        jj = ep[vp[j]] # = fp^-1(j)

        ep[x] = y
        ep[y] = x

        self._n += 2
        self._nf += 1

        if i == j:
            # add a monogon
            # fp (i A) -> (i A x)(y)
            # vp (... i ...) -> (... i y x ...)
            fp[ii] = x
            fp[x] = i
            fp[y] = y
            vp[x] = vp[i]
            vp[y] = x
            vp[i] = y


            vl[x] = vl[y] = vl[i]
            fl[x] = fl[i]
            fl[y] = nf

            fd[fl[i]] += 1
            fd[nf] = 1

            vd[vl[i]] += 2

            fa[y] = 0

            # TODO: we can do better
#            _perm_recompute_angle(vp, va, x)
            _perm_recompute_angle(fp, fa, x)

        else:
            # general case
            # update permutations:
            # fp  (i A j B)               -> (i A x) (j B y)
            # ep                          -> (x y)
            # vp  (... i ...) (... j ...) -> (... i y ...) (... j x ...)
            fp[jj] = x
            fp[x] = i
            fp[ii] = y
            fp[y] = j

            vp[y] = vp[i]
            vp[i] = y
            vp[x] = vp[j]
            vp[j] = x

            # update labels, degrees and angles
            vl[x] = vl[j]
            vl[y] = vl[i]

            fl[x] = fl[i]
            fl[y] = fl[j]

            dfy = 0  # degree of the y-face
            while fl[y] != nf:
                fl[y] = nf
                y = fp[y]
                dfy += 1
            dfx = fd[fl[x]] + 2 - dfy

            fd[fl[x]] = dfx
            fd[fl[y]] = dfy
            vd[vl[x]] += 1
            vd[vl[y]] += 1

            # TODO: we can do better
#            _perm_recompute_angle(vp, va, x)
#            _perm_recompute_angle(vp, va, y)
            _perm_recompute_angle(fp, fa, x)
            if fl[x] != fl[y]:
                _perm_recompute_angle(fp, fa, y)

    def remove_edge(self, i):
        r"""
        Remove an edge.

        If the edge has the same face on both sides, then the genus drops by 1.
        Inverse operation of :meth:`split_face` or :meth:`trisect_face`.

        EXAMPLES::

            sage: from surface_dynamics.topology.fat_graph import FatGraph

            sage: vp = '(0,2,1,3)'
            sage: ep = '(0,1)(2,3)'
            sage: fp = '(0,2,1,3)'
            sage: cm = FatGraph(vp, ep, fp)

            sage: eps = '(0,1)(2,3)(4,5)'
            sage: vp20 = '(0,5,4,2,1,3)'
            sage: fp20 = '(0,2,1,3,4)(5)'
            sage: cm2 = FatGraph(vp20, eps, fp20, 6)
            sage: cm2.remove_edge(4)
            sage: cm2 == cm
            True
            sage: cm2 = FatGraph(vp20, eps, fp20, 6)
            sage: cm2.remove_edge(5)
            sage: cm2 == cm
            True

            sage: vp10 = '(0,4,2,5,1,3)'
            sage: fp10 = '(0,5)(1,3,4,2)'
            sage: cm2 = FatGraph(vp10, eps, fp10)
            sage: cm2.remove_edge(4)
            sage: cm2 == cm
            True
            sage: cm2 = FatGraph(vp10, eps, fp10)
            sage: cm2.remove_edge(5)
            sage: cm2 == cm
            True

            sage: vp30 = '(0,4,2,1,5,3)'
            sage: fp30 = '(0,2,5)(1,3,4)'
            sage: cm2 = FatGraph(vp30, eps, fp30)
            sage: cm2.remove_edge(4)
            sage: cm2 == cm
            True
            sage: cm2 = FatGraph(vp30, eps, fp30)
            sage: cm2.remove_edge(5)
            sage: cm2 == cm
            True

            sage: vp00 = '(0,5,4,2,1,3)'
            sage: fp00 = '(0,2,1,3,4)(5)'
            sage: cm2 = FatGraph(vp00, eps, fp00)
            sage: cm2.remove_edge(4)
            sage: cm2 == cm
            True

            sage: vp22 = '(0,2,5,4,1,3)'
            sage: fp22 = '(0,4,2,1,3)(5)'
            sage: cm2 = FatGraph(vp00, eps, fp00)
            sage: cm2.remove_edge(4)
            sage: cm2 == cm
            True
        """
        vp = self._vp
        ep = self._ep
        fp = self._fp

        vl = self._vl
        fl = self._fl

#        va = self._va
        fa = self._fa

        vd = self._vd
        fd = self._fd

        n = self._n
        nf = self._nf
        nv = self._nv

        i = int(i)
        if i < 0 or i >= self._n:
            raise ValueError("dart index out of range")
        j = ep[i]

        fi = fl[i]
        fj = fl[j]
        if fi == fj:
            raise ValueError("i=%d and j=%d on the same face" %(i,j))
        fmin = min(fi, fj)
        if i < n - 2 or j < n - 2 or max(fi, fj) != nf-1:
            raise NotImplementedError

        ii = ep[vp[i]]
        jj = ep[vp[j]]
        if fd[fl[i]] == 1:
            # monogon
            assert vp[i] == j
            fp[jj] = fp[j]
            vp[fp[j]] = vp[j]
#            _perm_recompute_angle(vp, va, vp[j])
            _perm_recompute_angle(fp, fa, fp[j])
        elif fd[fl[j]] == 1:
            # monogon
            assert vp[j] == i
            fp[ii] = fp[i]
            vp[fp[i]] = vp[i]
#            _perm_recompute_angle(vp, va, vp[i])
            _perm_recompute_angle(fp, fa, fp[i])
        else:
            # none of them are monogons
            fp[ii] = fp[j]
            fp[jj] = fp[i]

            vp[fp[j]] = vp[i]
            vp[fp[i]] = vp[j]

            # TODO: we can do better
#            _perm_recompute_angle(vp, va, vp[i])
#            _perm_recompute_angle(vp, va, vp[j])
            _perm_recompute_angle(fp, fa, fp[i])

        # update vertex and face degrees
        vd[vl[i]] -= 1
        vd[vl[j]] -= 1

        d = fd[fl[i]] + fd[fl[j]] - 2
        fd[fmin] = d

        # update face labels
        k = fp[i]
        while fl[k] != fmin:
            fl[k] = fmin
            k = fp[k]
        k = fp[j]
        while fl[k] != fmin:
            fl[k] = fmin
            k = fp[k]

        self._n -= 2
        self._nf -= 1

    def split_vertex(self, i, j):
        r"""
        Insert a new edge to split the vertex located at the darts i and j.
        
        This operation keeps the genus constant. The inverse operation is implemented
        in :meth:`contract_edge`.

        EXAMPLES::

            sage: from surface_dynamics.topology.fat_graph import FatGraph

            sage: vp = '(0,2,1,3)'
            sage: ep = '(0,1)(2,3)'
            sage: fp = '(0,2,1,3)'
            sage: eps = '(0,1)(2,3)(4,5)'

            sage: vp02 = '(0,4,1,3)(2,5)'
            sage: fp02 = '(0,4,2,1,3,5)'
            sage: cm = FatGraph(vp, ep, fp, 6)
            sage: cm.split_vertex(0,2)
            sage: cm == FatGraph(vp02, eps, fp02)
            True

            sage: vp01 = '(0,4,3)(1,5,2)'
            sage: fp01 = '(0,2,4,1,3,5)'
            sage: cm = FatGraph(vp, ep, fp, 6)
            sage: cm.split_vertex(0,1)
            sage: cm == FatGraph(vp01, eps, fp01)
            True

            sage: vp03 = '(0,4)(1,3,5,2)'
            sage: fp03 = '(0,2,1,4,3,5)'
            sage: cm = FatGraph(vp, ep, fp, 6)
            sage: cm.split_vertex(0,3)
            sage: cm == FatGraph(vp03, eps, fp03)
            True
        """
        vp = self._vp
        ep = self._ep
        fp = self._fp
        vl = self._vl
        fl = self._fl
#        va = self._va
        fa = self._fa
        n = self._n
        nf = self._nf
        nv = self._nv
        vd = self._vd
        fd = self._fd

        i = int(i)
        j = int(j)
        if i < 0 or i >= self._n or j < 0 or j >= self._n or vl[i] != vl[j]:
            raise ValueError("invalid darts i=%d and j=%d for vertex splitting" %(i, j))

        self._check_alloc(n + 2, nv + 1, nf)

        x = self._n
        y = self._n + 1
        ii = vp[i]
        jj = vp[j]
        ep[x] = y
        ep[y] = x
        self._n += 2
        self._nv += 1

        if i == j:
            # introduce a vertex of degree 1
            vp[x] = ii
            vp[i] = x
            vp[y] = y

            fp[y] = i
            fp[x] = y
            fp[ep[ii]] = x

            fl[x] = fl[y] = fl[i]
            vl[x] = vl[i]
            vl[y] = nv

            vd[vl[x]] += 1
            vd[vl[y]] = 1

            fd[fl[x]] += 2

#            va[y] = 0
#            _perm_recompute_angle(vp, va, x)
            _perm_recompute_angle(fp, fa, x)

        else:
            # general case
            # update permutations
            # fp (... i ...) (... j ...) -> (... y i ...) (... x j ...)
            # ep                         -> (x y)
            # vp (A i B j)               -> (A i x) (B j y)
            vp[x] = jj
            vp[i] = x
            vp[y] = ii
            vp[j] = y

            fp[ep[jj]] = x
            fp[x] = j
            fp[ep[ii]] = y
            fp[y] = i 

            # update labels and degrees

            fl[x] = fl[j]
            fl[y] = fl[i]

            vl[x] = vl[i]
            vl[y] = vl[j]

            dvy = 0
            while vl[y] != nv:
                vl[y] = nv
                y = vp[y]
                dvy += 1
            dvx = vd[vl[x]] + 2 - dvy

            vd[vl[x]] = dvx
            vd[vl[y]] = dvy
            fd[fl[x]] += 1
            fd[fl[y]] += 1

            #  TODO: we can do better...
#            _perm_recompute_angle(vp, va, x)
#            _perm_recompute_angle(vp, va, y)
            _perm_recompute_angle(fp, fa, x)
            if fl[x] != fl[y]:
                _perm_recompute_angle(fp, fa, y)

    def contract_edge(self, i):
        r"""
        Contract an edge between two distinct zeros.

        Inverse operation of :meth:`split_vertex` except that here we allow
        vertices of degree one.

        EXAMPLES::

            sage: from surface_dynamics.topology.fat_graph import FatGraph

            sage: vp = '(0,2,1,3)'
            sage: ep = '(0,1)(2,3)'
            sage: fp = '(0,2,1,3)'
            sage: eps = '(0,1)(2,3)(4,5)'

            sage: vp02 = '(0,4,1,3)(2,5)'
            sage: fp02 = '(0,4,2,1,3,5)'
            sage: cm = FatGraph(vp02, eps, fp02)
            sage: cm.contract_edge(4)
            sage: cm == FatGraph(vp, ep, fp)
            True
            sage: cm = FatGraph(vp02, eps, fp02)
            sage: cm.contract_edge(5)
            sage: cm == FatGraph(vp, ep, fp)
            True

            sage: vp01 = '(0,4,3)(1,5,2)'
            sage: fp01 = '(0,2,4,1,3,5)'
            sage: cm = FatGraph(vp01, eps, fp01)
            sage: cm.contract_edge(4)
            sage: cm == FatGraph(vp, ep, fp)
            True
            sage: cm = FatGraph(vp01, eps, fp01)
            sage: cm.contract_edge(5)
            sage: cm == FatGraph(vp, ep, fp)
            True

            sage: vp03 = '(0,4)(1,3,5,2)'
            sage: fp03 = '(0,2,1,4,3,5)'
            sage: cm = FatGraph(vp03, eps, fp03)
            sage: cm.contract_edge(4)
            sage: cm == FatGraph(vp, ep, fp)
            True
            sage: cm = FatGraph(vp03, eps, fp03)
            sage: cm.contract_edge(5)
            sage: cm == FatGraph(vp, ep, fp)
            True

        Degree 1 vertices::

            sage: cm = FatGraph('(0,2)(1)(3)', '(0,1)(2,3)', '(0,1,2,3)')
            sage: cm.contract_edge(2)
            sage: cm
            Fat graph with passport ([2], [1, 1])
             vp = ()
             ep = (0,1)
             fp = (0,1)
            sage: cm2 = FatGraph('(0,2)(1)(3)', '(0,1)(2,3)', '(0,1,2,3)')
            sage: cm2.contract_edge(3)
            sage: cm == cm2
            True
        """
        vp = self._vp
        ep = self._ep
        fp = self._fp

        vl = self._vl
        fl = self._fl

#        va = self._va
        fa = self._fa

        vd = self._vd
        fd = self._fd

        n = self._n
        nf = self._nf
        nv = self._nv

        i = int(i)
        if i < 0 or i >= self._n:
            raise ValueError("dart index out of range")
        j = ep[i]
        if vl[i] == vl[j]:
            raise ValueError("i=%d and j=%d on the same vertex" %(i,j))

        vi = vl[i]
        vj = vl[j]
        vmin = min(vi, vj)
        if i < n - 2 or j < n - 2 or max(vi, vj) != nv-1:
            raise NotImplementedError

        ii = ep[vp[i]]
        jj = ep[vp[j]]
        if vd[vl[i]] == 1:
            # vertex of degree one
            assert fp[j] == i
            vp[fp[i]] = vp[j]
            fp[jj] = fp[i]

#            _perm_recompute_angle(vp, va, vp[j])
            _perm_recompute_angle(fp, fa, fp[i])

        elif vd[vl[j]] == 1:
            # vertex of degree one
            assert fp[i] == j
            vp[fp[j]] = vp[i]
            fp[ii] = fp[j]

#            _perm_recompute_angle(vp, va, vp[i])
            _perm_recompute_angle(fp, fa, fp[j])
        else:
            vp[fp[i]] = vp[i]
            vp[fp[j]] = vp[j]
            fp[ii] = fp[i]
            fp[jj] = fp[j]

#            _perm_recompute_angle(vp, va, vp[i])
            _perm_recompute_angle(fp, fa, fp[i])
            _perm_recompute_angle(fp, fa, fp[j])


        # update vertex and face degree
        fd[fl[i]] -= 1
        fd[fl[j]] -= 1

        d = vd[vl[i]] + vd[vl[j]] - 2
        vd[vmin] = d

        # update vertex labels
        k = vp[i]
        while vl[k] != vmin:
            vl[k] = vmin
            k = vp[k]
        k = vp[j]
        while vl[k] != vmin:
            vl[k] = vmin
            k = vp[k]

        self._n -= 2
        self._nv -= 1

    def trisect_face(self, i, j, k):
        r"""
        Insert a bridge

        INPUT:

        - ``i``, ``j``, ``k`` - dart in the same face in counter-clockwise
          order


        EXAMPLES::

            sage: from surface_dynamics.topology.fat_graph import FatGraph

            sage: vp = '(0,2,1,3)'
            sage: ep = '(0,1)(2,3)'
            sage: fp = '(0,2,1,3)'
            sage: cm = FatGraph(vp, ep, fp, 8)

            sage: vp021 = '(0,7,2,6,5,1,4,3)'
            sage: ep021 = '(0,1)(2,3)(4,5)(6,7)'
            sage: fp021 = '(0,5,1,3,7,2,4,6)'
            sage: cm021 = FatGraph(vp021, ep021, fp021)
            sage: cm.trisect_face(0, 2, 1)
            sage: cm == cm021
            True

            sage: cm = FatGraph(vp, ep, fp, 10)
            sage: cm.trisect_face(0, 0, 3)

            sage: cm = FatGraph(vp, ep, fp, 10)
            sage: cm.trisect_face(0, 3, 3)

            sage: cm = FatGraph(vp, ep, fp, 10)
            sage: cm.trisect_face(0, 3, 0)

            sage: cm = FatGraph(vp, ep, fp, 10)
            sage: cm.trisect_face(0, 0, 0)
        """
        vp = self._vp
        ep = self._ep
        fp = self._fp

        vl = self._vl
        fl = self._fl

#        va = self._va
        fa = self._fa

        vd = self._vd
        fd = self._fd

        n = self._n
        nf = self._nf
        nv = self._nv

        i = int(i)
        j = int(j)
        k = int(k)

        if i < 0 or i >= n or j < 0 or j >= n or k < 0 or k >= n:
            raise ValueError("dart index out of range")
        if fl[i] != fl[j] or fl[i] != fl[k]:
            raise ValueError("darts in distinct faces")
        cc = (fa[i] <= fa[j] <= fa[k]) or \
             (fa[j] <= fa[k] <= fa[i]) or \
             (fa[k] <= fa[i] <= fa[j])
        if not cc:
            raise ValueError("i,j,k not in counterclockwise order")

        self._check_alloc(n + 4, nv, nf)
        self._n += 4

        ii = ep[vp[i]] # = fp^-1(i) at the end of B
        jj = ep[vp[j]] # = fp^-1(j) at the end of A
        kk = ep[vp[k]] # = fp^-1(k) at the end of C

        x = n
        y = n + 1
        xx = n + 2
        yy = n + 3

        ep[x] = y
        ep[y] = x
        ep[xx] = yy
        ep[yy] = xx

        fl[x] = fl[y] = fl[xx] = fl[yy] = fl[i]
        vl[x] = vl[k]
        vl[xx] = vl[y] = vl[j]
        vl[yy] = vl[i]

        fd[fl[i]] += 4
        vd[vl[i]] += 1
        vd[vl[j]] += 2
        vd[vl[k]] += 1

        if i == j == k:
            # face: -> (x xx y yy j C) 
            # (j C kk)
            vp[x] = vp[j]
            vp[yy] = x
            vp[y] = yy
            vp[xx] = y
            vp[j] = xx

            fp[kk] = x
            fp[x] = xx
            fp[xx] = y
            fp[y] = yy
            fp[yy] = j
        elif i == j:
            # face: -> (x xx y k B yy j C)
            # (j C kk) (k B ii)
            vp[yy] = vp[j]
            vp[y] = yy
            vp[xx] = y
            vp[j] = xx
            vp[x] = vp[k]
            vp[k] = x

            fp[ii] = yy
            fp[yy] = j
            fp[kk] = x
            fp[x] = xx
            fp[xx] = y
            fp[y] = k
        elif j == k:
            # face: -> (x xx i A y k B yy)
            # (i A jj) (k B ii)
            vp[yy] = vp[i]
            vp[i] = yy
            vp[y] = vp[k]
            vp[xx] = y
            vp[x] = xx
            vp[k] = x

            fp[ii] = yy
            fp[yy] = x
            fp[x] = xx
            fp[xx] = i
            fp[jj] = y
            fp[y] = k
        elif k == i:
            # face: -> (x xx i A y yy j C)
            # (i A jj) (j C kk)
            vp[y] = vp[j]
            vp[xx] = y
            vp[j] = xx
            vp[x] = vp[i]
            vp[yy] = x
            vp[i] = yy

            fp[kk] = x
            fp[x] = xx
            fp[xx] = i
            fp[jj] = y
            fp[y] = yy
            fp[yy] = j
        else:
            # general case
            # vertex: (...i...)(...j...)(...k...) -> (...i yy...)(...j xx y...)(...k x...)
            # edge  : add (x y) (xx yy)
            # face  : (i A j C k B) -> (x xx i A y k B yy j C)
            #
            # (i A jj) (j C kk) (k B ii)
            vp[yy] = vp[i]
            vp[i] = yy
            vp[y] = vp[j]
            vp[xx] = y
            vp[j] = xx
            vp[x] = vp[k]
            vp[k] = x

            fp[kk] = x
            fp[x] = xx
            fp[xx] = i
            fp[jj] = y
            fp[y] = k
            fp[ii] = yy
            fp[yy] = j

#        _perm_recompute_angle(vp, va, i)
#        if vl[i] != vl[j]:
#            _perm_recompute_angle(vp, va, j)
#        if vl[k] != vl[i] and vl[k] != vl[j]:
#            _perm_recompute_angle(vp, va, k)

        _perm_recompute_angle(fp, fa, i)

    def remove_face_trisection(self, x):
        ep = self._ep
        fp = self._fp
        fl = self._fl
        fa = self._fa
        fd = self._fd
        vp = self._vp
#        va = self._va
        vl = self._vl
        vd = self._vd

        x = int(x)
        xx = fp[x]
        y = ep[x]
        yy = ep[xx]

        if fl[x] != fl[y] or fl[x] != fl[xx] or fl[x] != fl[yy] or \
           not (fa[x] < fa[xx] < fa[y] < fa[yy] or
                fa[xx] < fa[y] < fa[yy] < fa[x] or
                fa[y] < fa[yy] < fa[x] < fa[xx] or
                fa[yy] < fa[x] < fa[xx] < fa[y]):
            raise ValueError("not a trisection")

        # face: (x xx i A y k B yy j C) -> (i A j C k B)
        #    -> (i A jj) (j C kk) (k B ii)
        i = fp[xx]
        k = fp[y]
        j = fp[yy]
        ii = ep[vp[yy]] # = fp^-1(yy)
        jj = ep[vp[y]]  # = fp^-1(y)
        kk = ep[vp[x]]  # = fp^-1(x)

        if fp[xx] == y and fp[y] == yy:
            # vertex (... j xx y yy x ...) -> (... j ...)
            # face (x xx y yy j C) -> (j C)
            # (j C kk)
            assert vp[j] == xx
            assert vp[xx] == y
            assert vp[yy] == x
            vp[j] = vp[x]
            fp[kk] = j
        elif fp[xx] == y:
            # face: (x xx y k B yy j C) -> (j C k B)
            # (j C kk) (k B ii)
            assert fp[y] != yy and fp[yy] != x
            assert vp[j] == xx
            assert vp[xx] == y
            assert vp[y] == yy
            vp[j] = vp[yy]
            assert vp[k] == x
            vp[k] = vp[x]
            fp[kk] = k
            fp[ii] = j
        elif fp[yy] == x:
            # face: (x xx i A y k B yy) -> (i A k B)
            # (i A jj) (k B ii)
            assert fp[xx] != y and fp[y] != yy
            assert vp[i] == yy
            vp[i] = vp[yy]
            assert vp[k] == x
            assert vp[x] == xx
            assert vp[xx] == y
            vp[k] = vp[y]
            fp[ii] = i
            fp[jj] = k
        elif fp[y] == yy:
            # face: (x xx i A y yy j C) -> (i A j C)
            # (i A jj) (j C kk)
            assert fp[xx] != y and fp[yy] != x
            assert vp[i] == yy
            assert vp[yy] == x
            vp[i] = vp[x]
            assert vp[j] == xx
            assert vp[xx] == y
            vp[j] = vp[y]
            fp[kk] = i
            fp[jj] = j
        else:
            # face: (x xx i A y k B yy j C) -> (i A j C k B)
            # (i A jj) (j C kk) (k B ii)
            assert fp[xx] != y and fp[y] != yy and fp[yy] != x
            assert vp[i] == yy
            vp[i] = vp[yy]
            assert vp[j] == xx
            assert vp[xx] == y
            vp[j] = vp[y]
            assert vp[k] == x
            vp[k] = vp[x]
            fp[jj] = j
            fp[kk] = k
            fp[ii] = i

        self._n -= 4
        fd[fl[i]] -= 4
        vd[vl[i]] -= 1
        vd[vl[j]] -= 2
        vd[vl[k]] -= 1

        assert perm_check(vp, self._n), vp
        assert perm_check(fp, self._n), fp

        if i < self._n:
            _perm_recompute_angle(fp, fa, i)
#            _perm_recompute_angle(vp, va, i)
        if j != i and j < self._n:
#            _perm_recompute_angle(vp, va, j)
            _perm_recompute_angle(fp, fa, j)
        if k != i and k != j and k < self._n:
#            _perm_recompute_angle(vp, va, k)
            _perm_recompute_angle(fp, fa, k)

    ######################################
    # canonical labels and automorphisms #
    ######################################

    def _good_starts(self, i0=-1):
        r"""
        EXAMPLES::

            sage: from surface_dynamics.topology.fat_graph import FatGraph

            sage: CM = []
            sage: w = [0,1,2,3,4,5,0,6,7,1,2,5,3,4,6,7]
            sage: CM.append(FatGraph.from_unicellular_word(w))
            sage: vp = '(0,15,3,6,8)(1,14,18,10,9,12,5,19)(2,7,4,17,11)(13,16)'
            sage: ep = '(0,1)(2,3)(4,5)(6,7)(8,9)(10,11)(12,13)(14,15)(16,17)(18,19)'
            sage: fp = '(0,19,14)(1,8,10,17,13,9,6,2,15)(3,11,18,5,7)(4,12,16)'
            sage: CM.append(FatGraph(vp, ep, fp))
            sage: for cm in CM:
            ....:     gs = set(cm._good_starts())
            ....:     assert gs
            ....:     for i in range(cm.num_darts()):
            ....:         ggs = cm._good_starts(i)
            ....:         if i in gs:
            ....:             ggs = cm._good_starts(i)
            ....:             assert ggs and ggs[0] == i and sorted(ggs) == sorted(gs), (gs, ggs, i)
            ....:         else:
            ....:             assert not ggs, (gs, ggs, i)
        """
        n = self._n
        ep = self._ep
        vd = self._vd
        fd = self._fd
        vl = self._vl
        fl = self._fl
        fa = self._fa
        if i0 == -1:
            ans = []
        else:
            ans = [i0]

        if self._nv > 1:
            # start at edges with distinct start and end
            # and maximize the degrees of vertices, then
            # the degree of adjacent faces
            if i0 != -1:
                j0 = ep[i0]
                if vl[i0] == vl[j0]:
                    return None
                best = (vd[vl[i0]], vd[vl[j0]], fl[i0] != fl[j0], fd[fl[i0]], fd[fl[j0]])
            else:
                best = None
            for i in range(self._n):
                if i == i0:
                    continue
                j = ep[i]
                if vl[i] == vl[j]:
                    continue
                cur = (vd[vl[i]], vd[vl[j]], fl[i] != fl[j], fd[fl[i]], fd[fl[j]])
                if best is None:
                    best = cur
                if cur > best:
                    if i0 != -1:
                        return None
                    else:
                        del ans[:]
                        best = cur
                if cur == best:
                    ans.append(i)

        elif self._nf > 1:
            # start at edges with distinct faces and
            # maximize the degrees
            if i0 != -1:
                j0 = ep[i0]
                if fl[i0] == fl[j0]:
                    return None
                best = (fd[fl[i0]], fd[fl[j0]])
            else:
                best = None
            for i in range(self._n):
                if i == i0:
                    continue
                j = ep[i]
                if fl[i] == fl[j]:
                    continue
                cur = (fd[fl[i]], fd[fl[j]])
                if best is None:
                    best = cur
                if cur > best:
                    if i0 != -1:
                        return None
                    else:
                        del ans[:]
                        best = cur
                if cur == best:
                    ans.append(i)
        else:
            # one face, one vertex
            # minimize the face angle between i and ep[i]
            if i0 != -1:
                j0 = ep[i0]
                best = fa[j0] - fa[i0]
                if best < 0: best += n
            else:
                best = None
            for i in range(self._n):
                if i == i0:
                    continue
                j = ep[i]
                cur = fa[j] - fa[i]
                if cur < 0: cur += n
                if best is None:
                    best = cur
                if cur < best:
                    if i0 != -1:
                        return None
                    else:
                        del ans[:]
                        best = cur
                if cur == best:
                    ans.append(i)

        return ans

    def _canonical_labelling_from(self, i0):
        r"""
        Edges gets relabelled (2i, 2i+1).

        OUTPUT: a triple ``(fc, fd, rel)`` where
        
        - ``fc`` is the list of edges seen along the walk (with respect to the new
          numbering)
        
        - ``fd``: face degrees seen along the walk

        - ``rel``: relabelling map {current labels} -> {canonical labels}

        EXAMPLES::
   
            sage: from surface_dynamics.topology.fat_graph import FatGraph

            sage: vp = '(0,15,3,6,8)(1,14,18,10,9,12,5,19)(2,7,4,17,11)(13,16)'
            sage: ep = '(0,1)(2,3)(4,5)(6,7)(8,9)(10,11)(12,13)(14,15)(16,17)(18,19)'
            sage: fp = '(0,19,14)(1,8,10,17,13,9,6,2,15)(3,11,18,5,7)(4,12,16)'
            sage: cm = FatGraph(vp, ep, fp)
            sage: for i in range(20):
            ....:     fc, fd, rel = cm._canonical_labelling_from(i)
            ....:     assert len(fc) == 20
            ....:     assert sorted(fd, reverse=True) == [9, 5, 3, 3]
            ....:     assert sorted(rel) == list(range(20))
        """
        n = self._n

        fc = []  # faces seen along the walk
        fd = []  # face degrees seen along the walk
        rel = [-1] * n # dart relabeling

        m = n // 2
        ep = self._ep
        fp = self._fp

        rel[i0] = 0
        fc.append(0)
        c = 2         # current dart number
        i = fp[i0]
        wait = deque([ep[i0]])
        cyc = [0]
        d = 1
        while i != i0:
            if rel[i] == -1:
                j = ep[i]
                if rel[j] != -1:
                    assert rel[j] % 2 == 0
                    rel[i] = rel[j] + 1
                else:
                    rel[i] = c
                    c += 2
                    wait.append(j)
            fc.append(rel[i])
            d += 1
            i = fp[i]
        fd.append(d)

        while wait:
            i0 = wait.popleft()
            if rel[i0] != -1:
                continue
            assert rel[ep[i0]] != -1 and rel[ep[i0]] % 2 == 0
            rel[i0] = rel[ep[i0]] + 1
            fc.append(rel[i0])
            i = fp[i0]
            d = 1
            while i != i0:
                if rel[i] == -1:
                    j = ep[i]
                    if rel[j] != -1:
                        assert rel[j] % 2 == 0
                        rel[i] = rel[j] + 1
                    else:
                        rel[i] = c
                        c += 2
                        wait.append(j)
                fc.append(rel[i])
                i = fp[i]
                d += 1
            fd.append(d)

        # we might want to complete the relabelling somewhere else
        assert len(fc) == self._n, (fc, fd, rel)
        assert len(fd) == self._nf, (fc, fd, rel)

        return fc, fd, rel

    def _canonical_labelling_from_if_smaller(self, best, i0):
        r"""
        """
        cur = self._canonical_labelling_from(i0)
        if cur[0] < best[0]:
            # smaller
            return 1, cur
        elif cur[0] == best[0]:
            if cur[1] < best[1]:
                # smaller
                return 1, cur
            elif cur[1] == best[1]:
                # equal
                return 0, cur
            else:
                # larger
                return -1, cur
        else:
            # larger
            return -1, None

    def _clean_good_starts(self, test_roots, good_roots, i, aut_grp, aut):
        r"""
        Move the elements in test_roots to good_roots when they
        happen to be in the orbit of the automorphism group
        """
        return

    def _is_canonical(self, i0):
        r"""
        Return a pair ``(answer, automorphisms)`` where answer is a boolean
        that says whether this map is in canonical form and ``automorphisms`` form
        a generating set of the group of automorphisms.

        EXAMPLES::

            sage: from surface_dynamics.topology.fat_graph import FatGraph

            sage: vp = '(0,15,3,6,8)(1,14,18,10,9,12,5,19)(2,7,4,17,11)(13,16)'
            sage: ep = '(0,1)(2,3)(4,5)(6,7)(8,9)(10,11)(12,13)(14,15)(16,17)(18,19)'
            sage: fp = '(0,19,14)(1,8,10,17,13,9,6,2,15)(3,11,18,5,7)(4,12,16)'
            sage: cm = FatGraph(vp, ep, fp)
            sage: any(cm._is_canonical(i)[0] for i in range(20))
            True

        A genus 1 example with 4 symmetries::

            sage: vp = '(0,8,6,4,3,7)(1,9,11,5,2,10)'
            sage: ep = '(0,1)(2,3)(4,5)(6,7)(8,9)(10,11)'
            sage: fp = '(0,10,9)(2,4,11)(1,7,8)(3,5,6)'
            sage: cm = FatGraph(vp, ep, fp)
            sage: for i in range(12):
            ....:     test, aut_grp = cm._is_canonical(i)
            ....:     if test: print(aut_grp.group_cardinality())
            4
            4
            4
            4
        """
        roots = self._good_starts(i0)
        if roots is None:
            return False, None

        if len(roots) == 1:
            return True, None

        # perform complete relabelling
        P = PermutationGroupOrbit(self._n, [], roots)
        i = next(P)
        assert i == i0
        best = self._canonical_labelling_from(i)
        rel0 = perm_invert(best[2])

        for i in P:
            test, cur = self._canonical_labelling_from_if_smaller(best, i)

            if test == 1:
                return False, None

            elif test == 0:
                fc, fd, rel = cur
                aut = perm_compose(rel, rel0)
                P.add_generator(aut)

        return True, P

    def automorphism_group(self):
        r"""
        EXAMPLES::

            sage: from surface_dynamics.topology.fat_graph import FatGraph
            sage: from surface_dynamics.misc.permutation import perm_conjugate

        The four unicellular map with 4 edges in genus 2::

            sage: cm0 = FatGraph.from_unicellular_word([0,1,0,1,2,3,2,3])
            sage: cm1 = FatGraph.from_unicellular_word([0,1,0,2,1,3,2,3])
            sage: cm2 = FatGraph.from_unicellular_word([0,1,0,2,3,1,2,3])
            sage: cm3 = FatGraph.from_unicellular_word([0,1,2,3,0,1,2,3])
            sage: for cm in [cm0, cm1, cm2, cm3]:
            ....:     P = cm.automorphism_group()
            ....:     print(P.group_cardinality())
            ....:     vp = cm.vertex_permutation()
            ....:     ep = cm.edge_permutation()
            ....:     fp = cm.face_permutation()
            ....:     for a in P.gens():
            ....:         pp = perm_conjugate(vp, a)
            ....:         assert pp == vp, (vp, pp)
            2
            1
            1
            8

            sage: cm = FatGraph.from_unicellular_word([0,1,2,3,0,4,1,2,3,4])
            sage: cm.automorphism_group().group_cardinality()
            2

        An example with two faces::

            sage: vp = '(0,9,5,6,7,4,8,1,2,3)'
            sage: ep = '(0,2)(1,3)(4,6)(5,7)(8,9)'
            sage: fp = '(0,1,2,3,8)(4,5,6,7,9)'
            sage: cm = FatGraph(vp,ep,fp)
            sage: cm.automorphism_group()
            PermutationGroupOrbit(10, [(0,4)(1,5)(2,6)(3,7)(8,9)])
        """
        roots = self._good_starts()
        P = PermutationGroupOrbit(self._n, [], roots)
        if len(roots) == 1:
            return P
        i0 = next(P)
        best = self._canonical_labelling_from(i0)
        rel0 = perm_invert(best[2])

        for i in P:
            test, cur = self._canonical_labelling_from_if_smaller(best, i)

            if test == 1:
                rel0 = perm_invert(cur[2])
                best = cur
            elif test == 0:
                fc, fd, rel = cur
                aut = perm_compose(rel, rel0)
                P.add_generator(aut)

        return P

    def relabel(self, r):
        r"""
        Relabel according to the permutation ``p``

        EXAMPLES::

            sage: from surface_dynamics.topology.fat_graph import FatGraph

            sage: cm = FatGraph.from_unicellular_word([0,1,0,1,2,3,2,3])
            sage: cm.relabel([4,7,0,2,3,5,1,6])
            sage: cm._check()
        """
        n = self._n
        self._vp = perm_conjugate(self._vp, r, n)
        self._ep = perm_conjugate(self._ep, r, n)
        self._fp = perm_conjugate(self._fp, r, n)
        
        vl = [None] * n
        fl = [None] * n
#        va = [None] * n
        fa = [None] * n

        for i in range(n):
            j = r[i]
            vl[j] = self._vl[i]
            fl[j] = self._fl[i]
#            va[j] = self._va[i]
            fa[j] = self._fa[i]

        self._vl = vl
        self._fl = fl
#        self._va = va
        self._fa = fa


####################################################
# Canonical augmentation and exhaustive generation #
####################################################

def augment1(cm, aut_grp, depth, intermediate):
    r"""
    Given a unicellular map ``cm`` with a single vertex and automorphism group
    ``aut_grp``, iterate through all its canonical extensions that are
    uniface-univertex maps of greater genus.

    Add two edes.
    """
    if intermediate or depth == 0:
        yield cm, aut_grp
    if depth == 0:
        return

    n = cm._n
    fd = cm._fd
    fl = cm._fl
    fp = cm._fp
    i = 0
    if aut_grp is None:
        R = range(n)
    else:
        aut_grp.reset_iterator()
        R = aut_grp
    for i in R:
        j = i
        for sj in range(fd[fl[i]]):
            k = j
            for sk in range(fd[fl[i]] - sj + (i != j)):
                #print("(%d, %d, %d)" % (i, j, k))
                cm.trisect_face(i, j, k)
                test, aaut_grp = cm._is_canonical(n)
                if test:
                    for X in augment1(cm, aaut_grp, depth - 1, intermediate):
                        yield X
                cm.remove_face_trisection(n)
                k = fp[k]
            j = fp[j]
        i = fp[i]

def augment2(cm, aut_grp, depth, intermediate):
    r"""
    Given a map ``cm`` with a single vertex and automorphism group ``aut_grp``
    iterate through all its canonical extensions that are obtained by splitting
    one face into two faces.

    Add one edge.

    Here we need only to consider the faces with maximal degree.

    EXAMPLES::

        sage: from surface_dynamics.topology.fat_graph import FatGraph, \
        ....:          augment2, num_and_weighted_num

        sage: cm0 = FatGraph.from_unicellular_word([0,1,0,1,2,3,2,3])
        sage: cm1 = FatGraph.from_unicellular_word([0,1,0,2,1,3,2,3])
        sage: cm2 = FatGraph.from_unicellular_word([0,1,0,2,3,1,2,3])
        sage: cm3 = FatGraph.from_unicellular_word([0,1,2,3,0,1,2,3])
        sage: cm0._realloc(10)
        sage: cm1._realloc(10)
        sage: cm2._realloc(10)
        sage: cm3._realloc(10)
        sage: P0 = cm0.automorphism_group()
        sage: P1 = cm1.automorphism_group()
        sage: P2 = cm2.automorphism_group()
        sage: P3 = cm3.automorphism_group()
        sage: from itertools import chain
        sage: I = chain(augment2(cm0,P0,1,False),
        ....:           augment2(cm1,P1,1,False),
        ....:           augment2(cm2,P2,1,False),
        ....:           augment2(cm3,P3,1,False))
        sage: num_and_weighted_num(I)
        (53, 483/10)
    """
    if intermediate or depth == 0:
        yield cm, aut_grp
    if depth == 0:
        return

    n = cm._n
    fp = cm._fp
    fd = cm._fd
    fl = cm._fl
    fdmax = max(fd)
    if aut_grp is None:
        R = range(n)
    else:
        aut_grp.reset_iterator()
        R = aut_grp
    for i in R:
        if fd[fl[i]] != fdmax:
            continue

        j = i
        for _ in range(fd[fl[i]]):
            cm.split_face(i, j)
            test, aaut_grp = cm._is_canonical(n)
            if test:
                for X in augment2(cm, aaut_grp, depth-1, intermediate):
                    yield X
            cm.remove_edge(n)
            j = fp[j]

def augment3(cm, aut_grp, depth, min_degree, intermediate):
    r"""
    Given a map ``cm``, its automorphism group ``aut_grp`` and a degree
    sequence ``ds`` iterate through all its canonical extensions that
    are obtained by splitting one vertex into two vertices and so that
    it is still possible to reach the degree sequence ``ds``.

    Add ``depth`` edges.

    Here we only need to consider the vertices with maximal degree.
    """
    if intermediate or depth == 0:
        yield cm, aut_grp
    if depth == 0:
        return

    n = cm._n
    fp = cm._fp
    vp = cm._vp
    vd = cm._vd
    vl = cm._vl
    vdmax = max(cm._vd)
    if aut_grp is None:
        R = range(n)
    else:
        aut_grp.reset_iterator()
        R = aut_grp
    for i in R:
#        if vd[vl[i]] <= min_degree:
#            continue
        j = i
        for _ in range(min_degree - 1):
            j = vp[j]
        for _ in range(vd[vl[i]] - min_degree + 1):
            cm.split_vertex(i, j)
            test, aaut_grp = cm._is_canonical(n)
            if test:
                for X in augment3(cm, aaut_grp, depth-1, min_degree, intermediate):
                    yield X
            cm.contract_edge(n)
            j = vp[j]

def FatGraphs_g_nf_nv(g, nf, nv, vertex_min_degree=1, intermediate=False):
    r"""
    Iterator through the fatgraphs of given genus, number of faces
    and number of vertices.

    INPUT:

    - ``g`` - the genus

    - ``nf`` - number of faces

    - ``nv`` - number of vertices

    - ``vertex_min_degree`` - minimal number of vertices

    - ``intermediate`` - if set to ``True`` then return all graphs with genus = g,
      number of faces <= nf and number of vertices <= nv

    EXAMPLES::

        sage: from surface_dynamics.topology.fat_graph import FatGraphs_g_nf_nv, \
        ....:     num_and_weighted_num

        sage: num_and_weighted_num(FatGraphs_g_nf_nv(0, 4, 1))
        (2, 5/6)
        sage: num_and_weighted_num(FatGraphs_g_nf_nv(0, 1, 4))
        (2, 5/6)

        sage: num_and_weighted_num(FatGraphs_g_nf_nv(1, 2, 1))
        (3, 5/3)
        sage: num_and_weighted_num(FatGraphs_g_nf_nv(1, 1, 2))
        (3, 5/3)

        sage: num_and_weighted_num(FatGraphs_g_nf_nv(0, 5, 1))
        (3, 7/4)
        sage: num_and_weighted_num(FatGraphs_g_nf_nv(0, 1, 5))
        (3, 7/4)

        sage: num_and_weighted_num(FatGraphs_g_nf_nv(2, 2, 1))
        (53, 483/10)
        sage: num_and_weighted_num(FatGraphs_g_nf_nv(2, 1, 2))
        (53, 483/10)

        sage: num_and_weighted_num(FatGraphs_g_nf_nv(3, 1, 1))
        (131, 495/4)

        sage: num_and_weighted_num(FatGraphs_g_nf_nv(2, 3, 1))
        (553, 539)
        sage: num_and_weighted_num(FatGraphs_g_nf_nv(2, 1, 3))
        (553, 539)

        sage: num_and_weighted_num(FatGraphs_g_nf_nv(1, 5, 1))
        (204, 385/2)
        sage: num_and_weighted_num(FatGraphs_g_nf_nv(1, 1, 5))
        (204, 385/2)

        sage: num_and_weighted_num(FatGraphs_g_nf_nv(0, 7, 1))
        (14, 11)
        sage: num_and_weighted_num(FatGraphs_g_nf_nv(0, 1, 7))
        (14, 11)

        sage: num_and_weighted_num((cm,a) for (cm,a) in FatGraphs_g_nf_nv(1, 2, 2, 1) if all(x >= 2 for x in cm.vertex_profile()))
        (14, 87/8)
        sage: num_and_weighted_num((cm,a) for (cm,a) in FatGraphs_g_nf_nv(1, 2, 2, 2))
        (14, 87/8)

        sage: num_and_weighted_num((cm,a) for (cm,a) in FatGraphs_g_nf_nv(1, 2, 2, 1) if all(x >= 3 for x in cm.vertex_profile()))
        (8, 47/8)
        sage: num_and_weighted_num((cm,a) for (cm,a) in FatGraphs_g_nf_nv(1, 2, 2, 3))
        (8, 47/8)

    Check that intermediate works correctly::

        sage: from collections import defaultdict
        sage: d = defaultdict(int)
        sage: for cm,a in FatGraphs_g_nf_nv(1, 3, 3, intermediate=True):
        ....:     d[cm.num_faces(), cm.num_vertices()] += 1
        sage: for k in sorted(d, reverse=True):
        ....:     num = sum(1 for _ in FatGraphs_g_nf_nv(1, k[0], k[1]))
        ....:     print(k, d[k], num)
        ....:     assert d[k] == num
        (3, 3) 2048 2048
        (3, 2) 180 180
        (3, 1) 11 11
        (2, 3) 180 180
        (2, 2) 24 24
        (2, 1) 3 3
        (1, 3) 11 11
        (1, 2) 3 3
        (1, 1) 1 1
    """
    if g == 0:
        if nf == 1 and nv == 1:
            # trivial map (g = 0, nv = 1, nf = 1)
            if vertex_min_degree == 0:
                yield FatGraph('', '', '')
            return
        elif nv > 1:
            # vertex splitting of the trivial map (g = 0, nv = 2, nf = 1)
            cm0 = FatGraph('(0)(1)', '(0,1)', '(0,1)')
            gg = g
            nnv = nv - 2
            nnf = nf - 1
        elif nf > 1:
            # face splitting of the trivial map (g = 0, nv = 1, nf = 2)
            cm0 = FatGraph('(0,1)', '(0,1)', '(0)(1)')
            gg = g
            nnv = nv - 1
            nnf = nf - 2
    else:
        # trisection of the trivial map (g = 1, nv = 1, nf = 1)
        cm0 = FatGraph.from_unicellular_word([0,1,0,1])
        gg = g - 1
        nnv = nv - 1
        nnf = nf - 1
    cm0._realloc(4 * g + 2 * (nf + nv - 2))

    a0 = cm0.automorphism_group()
    for cm1, a1 in augment1(cm0, a0, gg, False):
        for cm2, a2 in augment2(cm1, a1, nnf, intermediate):
            for cm3, a3 in augment3(cm2, a2, nnv, vertex_min_degree, intermediate):
                yield cm3, a3


#############################
# Various testing functions #
#############################

def split_face_random(cm):
    n = cm.num_darts()
    i = randrange(n)
    j = randrange(n)
    fl = cm._fl
    while fl[i] != fl[j]:
        i = randrange(n)
        j = randrange(n)
    cm.split_face(i, j)
    return i,j

def split_vertex_random(cm):
    n = cm.num_darts()
    vl = cm._vl
    i = randrange(n)
    j = randrange(n)
    while vl[i] != vl[j]:
        i = randrange(n)
        j = randrange(n)
    cm.split_vertex(i, j)
    return i,j

def trisect_random(cm):
    fa = cm._fa
    fl = cm._fl
    n = cm._n
    i = randrange(n)
    j = randrange(n)
    k = randrange(n)
    while fl[i] != fl[j] or fl[i] != fl[k]:
        i = randrange(n)
        j = randrange(n)
        k = randrange(n)

    if not (fa[i] <= fa[j] <= fa[k] or
            fa[j] <= fa[k] <= fa[i] or
            fa[k] <= fa[i] <= fa[j]):
        i,k = k,i
    cm.trisect_face(i, j, k)
    return i,j,k

def SomeFatGraphs():
    r"""
    Iterator through some fat graphs.
    """
    for l in [[0,1,0,1,2,3,2,3],
              [0,1,0,2,1,3,2,3],
              [0,1,0,2,3,1,2,3],
              [0,1,2,3,0,1,2,3],
              [0,0,1,2,3,2,3,1],
              [0,0,1,2,3,3,1,2],
              [0,1,0,2,3,1,3,2],
              [0,1,2,0,3,2,1,3],
              [0,1,0,2,3,4,1,4,3,2],
              [0,1,2,3,0,4,1,2,3,4],
              [0,1,2,3,4,0,1,2,3,4]]:
        # make curve from one face description
        cm = FatGraph.from_unicellular_word(l)
        yield cm
        vp = perm_invert(cm.face_permutation())
        ep = cm.edge_permutation()
        fp = perm_invert(cm.vertex_permutation())

        # dual (one vertex)
        cm = FatGraph(vp, ep, fp)
        cm._check()
        yield cm

    # other examples

    vp = '(0,9,5,6,7,4,8,1,2,3)'
    ep = '(0,2)(1,3)(4,6)(5,7)(8,9)'
    fp = '(0,1,2,3,8)(4,5,6,7,9)'
    cm = FatGraph(vp, ep, fp)
    yield cm

    vp = '(0,15,3,6,8)(1,14,18,10,9,12,5,19)(2,7,4,17,11)(13,16)'
    ep = '(0,1)(2,3)(4,5)(6,7)(8,9)(10,11)(12,13)(14,15)(16,17)(18,19)'
    fp = '(0,19,14)(1,8,10,17,13,9,6,2,15)(3,11,18,5,7)(4,12,16)'
    cm = FatGraph(vp, ep, fp)
    yield cm



def tests(depth=10, verbose=False):
    for cm in SomeFatGraphs():
        if verbose:
            print("TEST")
            print(cm)
        n = cm.num_darts()

        # add / remove edges
        cm2 = cm.__copy__()
        stack = []
        cm2._realloc(n + depth * (2 + 2 + 4))
        fp = cm2.face_permutation()
        fd = cm2._fd
        fa = cm2._fa
        fl = cm2._fl
        vl = cm2._vl
        for _ in range(depth):
            i, j =split_face_random(cm2)
            if verbose:
                print("split_face(%d, %d)" % (i,j))
            cm2._check()
            stack.append(cm2.__copy__())

            i, j = split_vertex_random(cm2)
            if verbose:
                print("split_vertex(%d, %d)" % (i,j))
            cm2._check()
            stack.append(cm2.__copy__())

            i, j, k = trisect_random(cm2)
            if verbose:
                print("trisect_face(%d, %d, %d)" % (i, j, k))
            cm2._check()
            stack.append(cm2.__copy__())

        assert cm2.num_faces() == cm.num_faces() + depth
        assert cm2.num_vertices() == cm.num_vertices() + depth
        assert cm2.euler_characteristic() == cm.euler_characteristic() - 2 * depth

        for _ in range(depth):
            assert cm2 == stack.pop()
            if verbose:
                print("remove_face_trisection(%d)" % (cm2.num_darts() - 4))
            cm2.remove_face_trisection(cm2.num_darts() - 4)
            cm2._check()
            assert cm2 == stack.pop()
            if verbose:
                print("contract_edge(%d)" % (cm2.num_darts() - 2))
            cm2.contract_edge(cm2.num_darts() - 2)
            cm2._check()
            assert cm2 == stack.pop()
            if verbose:
                print("remove_edge(%d)" % (cm2.num_darts() - 2))
            cm2.remove_edge(cm2.num_darts() - 2)
            cm2._check()
        assert cm2 == cm

        # automorphism group
        A = cm.automorphism_group()
        for g in A.gens():
            cm2 = cm.__copy__()
            cm2.relabel(g)
            cm2._check()
            assert cm == cm2

    def collapse(self, spanning_tree=None):
        r"""
        Return a ribbon graph callapsed along a spanning tree.

        The resulting graph is on the same surface as the preceding but has only
        one vertex. It could be used twice to provide a polygonal representation
        with one vertex and one face.

        EXAMPLES::

            sage: from surface_dynamics import *

            sage: R = RibbonGraph(vertices='(0,1,2,5)(3,7)(4,10,9)(6,11,12)(8,13)')
            sage: R.genus()
            1
            sage: R.num_vertices()
            5
            sage: R.num_edges()
            7
            sage: R.num_faces()
            2
            sage: R2 = R.collapse()
            sage: R2
            Ribbon graph with 1 vertex, 3 edges and 2 faces
            sage: R
            Ribbon graph with 5 vertices, 7 edges and 2 faces
            sage: R3 = R2.dual().collapse().dual()
            sage: R3
            Ribbon graph with 1 vertex, 2 edges and 1 face

        """
        from copy import deepcopy

        if spanning_tree is None:
            spanning_tree,_ = self.spanning_tree()

        darts_to_kill = set([])
        for v0,v1,e in spanning_tree.edges():
            darts_to_kill.add(e[0])
            darts_to_kill.add(e[1])

        new_edges = []
        for e in self.edges():
            if e[0] not in darts_to_kill:
                new_edges.append(e)

        new_faces = []
        for f in self.faces():
            ff = tuple(i for i in f if i not in darts_to_kill)
            if ff:
                new_faces.append(ff)

        return RibbonGraph(edges=tuple(new_edges), faces=tuple(new_faces))

    def boundaries(self):
        r"""
        Return the list of cycles which are boundaries.

        A cycle is a *boundary* if it bounds a face.

        EXAMPLES::

            sage: from surface_dynamics import *

            sage: r = RibbonGraph('(1,2,3)(4,5,6)','(1,2)(3,4)(5,6)')
            sage: r.boundaries()
            [[(1, 2)],  [(2, 1), (3, 4), (6, 5), (4, 3)], [(5, 6)]]

            sage: r = RibbonGraph('(1,2,3)(4,5)(6,7,8)',edges='(1,2)(3,4)(5,6)(7,8)')
            sage: r.boundaries()
            [[(1, 2)],  [(2, 1), (3, 4), (5, 6), (8, 7), (6, 5), (4, 3)], [(7, 8)]]
        """
        e = self.edge_perm()
        return sorted([[(i,e[i]) for i in f] for f in self.faces()])

    def cycle_basis(self, intersection=False, verbose=False):
        r"""
        Returns a base of oriented cycles of the Ribbon graph modulo boundaries.

        If ``intersection`` is set to True then the method also returns the
        intersection matrix of the cycles.

        EXAMPLES::

            sage: from surface_dynamics import *

            sage: r = RibbonGraph('(1,2,3)(4,5,6)','(1,2)(3,4)(5,6)')
            sage: r.cycle_basis()
            []

            sage: r = RibbonGraph('(1,2,3)(4,5)(6,7,8)',edges='(1,2)(3,4)(5,6)(7,8)')
            sage: r.cycle_basis()
            []

            sage: r = RibbonGraph('(1,4,5)(2,3)(6,7,8)',edges='(1,2)(3,4)(5,6)(7,8)')
            sage: r.cycle_basis()
            []

            sage: e = '(1,3)(2,4)(5,7)(6,8)'
            sage: f = '(1,2,3,4,5,6,7,8)'
            sage: r = RibbonGraph(edges=e,faces=f)
            sage: r.cycle_basis()
            [[[1, 3]], [[2, 4]], [[5, 7]], [[6, 8]]]

            sage: f = '(0,10,13)(6,17,11)(2,14,7)(15,12,3)(16,20,19)(18,1,9)(4,22,21)(23,8,5)'
            sage: e = tuple((i,i+1) for i in xrange(0,24,2))
            sage: r = RibbonGraph(edges=e,faces=f); r
            Ribbon graph with 2 vertices, 12 edges and 8 faces
            sage: c,m = r.cycle_basis(intersection=True)
            sage: c
            [[(0, 1), [4, 5]], [[8, 9]], [[12, 13]], [[14, 15], (1, 0)]]
            sage: m
            [ 0  1  0  0]
            [-1  0  0  0]
            [ 0  0  0  1]
            [ 0  0 -1  0]
        """
        T,o = self.spanning_tree()

        # build a Ribbon graph with one vertex and one face
        r = self.collapse(T).dual().collapse().dual()
        if T is None:
            return r.edges()

        if intersection:
            c = r.vertices()[0]
            M = len(c)
            I = []

        cycles = [] # the cycles
        for e in r.edges():
            if verbose:
                print("build cycle from edge %s between vertex v0=%d and v1=%d" %(str(e),self.dart_to_vertex(e[0]),self.dart_to_vertex(e[1])))

            # build the branch to the root from v0
            v0 = self.dart_to_vertex(e[0])
            if verbose:
                print(" build branch from v0=%d" % v0)
            p0 = []
            while v0 != 0:
                v0,_,e0 = T.incoming_edges(v0)[0] # (v_in,v_out,label)
                p0.append(e0)
                if verbose:
                    print(" add %d" % v0)
            if verbose:
                print(" branch is %s" % str(p0))
            # build the branch to the root from v1

            v1 = self.dart_to_vertex(e[1])
            if verbose:
                print(" build branch from v1=%d" % v1)
            p1 = []
            while v1 != 0:
                v1,_,e1 = T.incoming_edges(v1)[0]
                p1.append(e1)
                if verbose:
                    print(" add %d" % v1)
            if verbose:
                print(" branch is %s" % str(p1))
            # clean the branches by removing common part
            while p0 and p1 and p0[-1] == p1[-1]:
                if verbose:
                    print("find common element", p0[-1])
                p0.pop(-1)
                p1.pop(-1)

            # add the cycle to the list
            cycles.append((p0,e,p1))

            # compute algebraic intersection with preceding cycles
            if intersection:
                i = []
                for _,ee,_ in cycles:
                    if verbose:
                        print("compute intersection")
                    p_in = c.index(e[1])
                    p_out = (c.index(e[0]) - p_in) % M
                    q_in  = (c.index(ee[1]) - p_in) % M
                    q_out = (c.index(ee[0]) - p_in) % M
                    if verbose:
                        print("  after reduction: p_out = %d, q_in = %d, q_out = %d" % (p_out, q_in, q_out))

                    # compute intersection
                    # p_in = 0 and the others 3 are positive
                    if q_in < p_out and p_out < q_out:
                        i.append(1)
                    elif q_out < p_out and p_out < q_in:
                        i.append(-1)
                    else:
                        i.append(0)

                I.append(i)

        # make cycle as list
        cycles = [p0[::-1]+[e]+[c[::-1] for c in p1] for p0,e,p1 in cycles]

        if intersection:
            m = matrix(len(cycles))
            for j in xrange(len(I)):
                for jj in xrange(len(I[j])):
                    m[j,jj] = I[j][jj]
                    m[jj,j] = -I[j][jj]

            return cycles, m
        return cycles

    def is_cycle(self,c):
        r"""
        Test whether ``c`` is a cycle.

        A *path* is a sequence of oriented edges such that each edge starts
        where the preceding one ends. A *cycle* is a path which starts where it
        ends.
        """
        for i in xrange(len(c)-1):
            if self.dart_to_vertex(c[i][1]) != self.dart_to_vertex(c[i+1][0]):
                return False
        if self.dart_to_vertex(c[-1][1]) != self.dart_to_vertex(c[0][0]):
            return False
        return True

