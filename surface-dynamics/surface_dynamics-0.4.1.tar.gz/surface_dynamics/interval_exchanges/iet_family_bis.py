def NonNegativeOrthant(dim, base_ring=QQ):
    V = FreeModule(base_ring, dim)
    return Polyhedron(rays=V.basis(), base_ring=base_ring) 

class MultiPermutation(object):
    r"""
    Not-necessarily connected permutations.

    Given a non-connected permutation, do we have a condition
    to ensure that a.e. parameters give rise to a union of
    minimal iet (generalization to Minsky-Weiss).

    Trivial: just check projections!
    """
    def num_components(self):
        r"""
        Return the number of components.
        """
        pass

    def vanishing_SAF0_components(self):
        r"""
        Return the indices of the components whose Sah-Arnoux-Fathi invariant
        is identically zero.
        """

class IETFamily(object):
    r"""
    Linear family of interval exchange transformations.
    """
    def __init__(self, p, cone):
        self._p = [p]
        self._cone = cone
        self._dim = len(p)   # ambient dimension

    def _check(self):
        if self._cone.ambient_dim() != len(p):
            raise ValueError('length of the permutation and ambient dimension of the cone mismatch')
        z = self._cone.base_ring().zero()
        V = self._cone.vertices()
        if len(V) != 1 or not V[0].vector().is_zero() or self._cone.lines():
            raise ValueError("not a cone")
        for r in self._cone.rays_list():
            if any(z <= 0 for z in r):
                raise ValueError("the cone is not contained in the non-negative orthant")

        if p.alphabet() != list(range(self._cone.ambient_dim()):

    def set_connection_and_induce(self):
        r"""
        Restrict the cone to force the last connection
        """
        dim = self._cone
        i = p[0][-1]
        j = p[1][-1]
        l = [0] * (dim + 1)
        l[i+1] = 1
        l[j+1] = -1
        L = Polyhedron(eqns = [l], base_ring = self._cone.base_ring())
        C = self._cone.intersection(L)
        if x(C.dimension() != self._cone.dimension() - 1:
            return None

        # drop the last interval and split the permutations into possibly
        # several permutations

