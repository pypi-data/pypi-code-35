# -*- coding: utf-8 -*-
""" pyhasse.lpom module

is calculating averaged height and averaged height according
to the LPOMext model.

"""

import logging


class LPOM(object):
    """Calculation average height"""

    def __init__(self, precision=2):
        self.logger = logging.getLogger(__name__)
        self.hav = []
        self.precision = precision

    def calc_hav(self, downset, incompset, rred):
        """ calculates the averaged height

        according to the LPOM0 model.

        :param downset: list of elements in the principal downset
                        of repres. elements
        :param incompset: list of elements incomparable
                          with a certain element
        :param rred:  number of representative elements

        """

        self.hav = []
        for i in range(0, rred):
            d = len(downset[i])
            self.hav.append(round(1.0 * d * (rred + 1) /
                                  (1.0 * rred + 1.0 - 1.0 * len(incompset[i])),
                                  self.precision))
        return self.hav

    def calc_hav_ext(self, downset, upset, incompset, rred):
        """ calculates the averaged height according to the LPOMext model.

        :param downset: list of elements in the downsets
                        of repres. elements
        :param upset:   list of elements in the upsets
                        of repres. elements
        :param incompset: list of elements incomparable
                          with each repres. element
        :param rred: number of representative elements

        :var upset:  list of elements in the principal upset
                     of repres. elements
        :var pdown:  counts the elements in downset
        :var pup:    counts the elements in upset

        """
        self.hav = []
        for i in range(0, rred):
            self.hav.append(len(downset[i]))
        for i1 in range(0, rred):
            inc = 0
            for i2 in incompset[i1]:
                pdown = 0
                pup = 0
                for i3 in incompset[i2]:
                    if i3 in downset[i1]:
                        pdown += 1
                for i3 in incompset[i2]:
                    if i3 in upset[i1]:
                        pup += 1
                if (pdown + pup) != 0:
                    inc += 1.0 * pdown / (1.0 * pdown + 1.0 * pup)
                else:
                    inc += 0
            self.hav[i1] += inc
        for i1 in range(0, rred):
            self.hav[i1] = round(self.hav[i1], self.precision)
        return self.hav
