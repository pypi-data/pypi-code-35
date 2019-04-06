import functools
import random

import numpy as np


class ODE:
    def ode(self, **params):
        raise NotImplementedError

    @property
    def params(self):
        raise NotImplementedError

    def __call__(self):
        return self.ode(**self.params)


class yeast_glycolysis(ODE):
    def __init__(self):
        """As of doi:10.1371/journal.pone.0119821.t002 Table 2
        """
        s1 = 0.15, 1.6
        s2 = 0.19, 2.16
        s3 = 0.04, 0.20
        s4 = 0.1, 0.35
        s5 = 0.08, 0.3
        s6 = 0.14, 2.67
        s7 = 0.05, 0.1

        # sig1 = 1.8442
        # sig2 = 3.0449
        # sig3 = 0.1438
        # sig4 = 0.2746
        # sig5 = 0.1143
        # sig6 = 3.4437
        # sig7 = 0.0489

        sig1 = 0.4862  # Table 2 MD Schmidt et al. # doi: 10.1088/1478-3975/8/5/055011
        sig2 = 0.6263
        sig3 = 0.0503
        sig4 = 0.0814
        sig5 = 0.0379
        sig6 = 0.7478
        sig7 = 0.0159

        self.range = [s1, s2, s3, s4, s5, s6, s6]
        self.sigma = [sig1, sig2, sig3, sig4, sig5, sig6, sig7]

    def initial_conditions(self, noise=True, rng=random):
        noise = int(noise)
        return [
            max(0, rng.uniform(up, low) + rng.gauss(0, sigma))
            for (up, low), sigma in zip(self.range, self.sigma)
        ]

    @property
    def params(self):
        """As of doi:10.1371/journal.pone.0119821.t00 Table 1.
        """
        p = dict(
            j0=2.5,  #  mM min^-1
            k1=100.0,  #  mM^-1 min^-1
            k2=6.0,  #  mM^-1 min^-1
            k3=16.0,  #  mM^-1 min^-1
            k4=100.0,  #  mM^-1 min^-1
            k5=1.28,  #  min^-1
            k6=12.0,  #  mM^-1 min^-1
            k=1.8,  #  min^-1
            kappa=13.0,  #  min^-1
            q=4.0,  #
            K1=0.52,  #  mM
            psi=0.1,  #
            n=1.0,  #  mM
            a=4.0,  #  mM
        )
        return p

    def ode(self, j0, k1, k2, k3, k4, k5, k6, k, kappa, q, K1, psi, n, a):
        """
        Ruoff P, Christensen M, Wolf J, Heinrich R. Temperature dependency and temperature compensation in a model of yeast glycolytic oscillations.
        Biophys Chem 2003; 106: 179. doi: 10.1016/S0301-4622(03) 00191-1 PMID: 14556906
        """
        # @functools.wraps(self.ode)
        def dy(y, t):
            s1, s2, s3, s4, s5, s6, s7 = y

            h1 = 2.0 * k1 * s1 * s6 / (1.0 + (s6 / K1) ** q)
            h2 = k6 * s2 * s5
            h3 = k2 * s2 * (n - s5)
            h4 = k3 * s3 * (a - s6)
            h5 = k4 * s4 * s5

            ds1 = j0 - h1 / 2.0
            ds2 = h1 - h3 - h2
            ds3 = h3 - h4
            ds4 = h4 - h5 - kappa * (s4 - s7)
            ds5 = h3 - h5 - h2
            ds6 = -h1 + 2 * h4 - k5 * s6
            ds7 = psi * kappa * (s4 - s7) - k * s7
            return [ds1, ds2, ds3, ds4, ds5, ds6, ds7]

        return dy


class double_pendulum(ODE):
    def initial_conditions(self):
        return [0, 0, 1, 0]

    @property
    def params(self):
        p = dict(m=1, l=1, g=9.81)
        return p

    def ode(self, m, l, g):
        def dy(y, t):
            phi1, phi2, p1, p2 = y
            Dphi = phi1 - phi2

            temp = m * l ** 2
            denom = 16.0 - 9 * np.cos(Dphi) ** 2

            dphi1 = 6.0 / temp * (2.0 * p1 - 3.0 * np.cos(Dphi) * p2) / denom
            dphi2 = 6.0 / temp * (2.0 * p2 - 3.0 * np.cos(Dphi) * p1) / denom

            temp2 = dphi1 * dphi2 * np.sin(Dphi)
            dp1 = -0.5 * temp * (temp2 + 3 * g / l * np.sin(phi1))
            dp2 = -0.5 * temp * (-temp2 + g / l * np.sin(phi2))

            return [dphi1, dphi2, dp1, dp2]

        return dy

    @staticmethod
    def get_cartesian_coords(phi1, phi2, l):
        x1 = l / 2.0 * np.sin(phi1)
        y1 = -l / 2.0 * np.cos(phi1)
        x2 = x1 + l * np.sin(phi2)
        y2 = x2 + l * np.cos(phi2)
        return x1, y1, x2, y2
