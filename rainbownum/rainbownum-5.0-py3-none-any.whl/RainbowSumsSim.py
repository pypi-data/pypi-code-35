from .RainbowSim import RainbowSim

"""
Rainbow Equation of the form:
a_1*x_1 + a_2*x_2 + ... + a_i*x_i = b
"""


class RbSumsEq(RainbowSim):
    def __init__(self, n, a, b=0, mod=False):
        super(RbSumsEq, self).__init__(n, a, b, mod)

        # upon initialization of equation the sets are generated
        self.__generate_sums()

    def get_equation(self):
        """
        Get a string-representation of the current equation.

        :return:
        string: Algebraic form of equation with a-coefficients and b-value
        """

        eq = ""
        for i in self.a:
            eq += str(i) + "x + "
        eq = eq[:-2] + "= " + str(self.b)
        return eq

    def __generate_sums(self):
        """
        Generate sums for the given equation.

        :return:
        None
        """

        if self.mod:
            values = list(range(self.k - 1))
        else:
            values = list(range(1, self.k))
        self.__recur_gen_sums(values, 0)

    def __recur_gen_sums(self, values, loop):
        """
        Recursively generate sums for the given equation.

        :param values: array of possible sums
        :param loop: index of x_i in sum that is currently being tested

        :return:
        None
        """

        k = self.k - 1
        if loop == k:
            return
        if self.mod:
            stop_case = self.n - k + loop
        else:
            stop_case = self.n - k + loop + 1
        while values[loop] <= stop_case:

            self.__recur_gen_sums(values, loop + 1)

            if loop == k - 1:
                sum = 0
                out = [0 for _ in range(self.k)]
                for i in range(len(values)):
                    sum = sum + self.a[i] * values[i]
                    out[i] = values[i]
                valid = True

                # account for different orders of taking the modulo
                sum1 = (sum - self.b) / -self.a[k]
                sum2 = 0
                if self.mod:
                    sum1 = sum1 % self.n
                    sum2 = (sum - self.b) % self.n
                    sum2 = sum2 / -self.a[k]

                # ensure that sums are not decimals
                if sum1 != int(sum1) and sum2 != int(sum2):
                    valid = False
                if sum1 == int(sum1):
                    out[k] = int(sum1)
                elif sum2 == int(sum2):
                    out[k] = int(sum2)
                else:
                    valid = False

                # ensure sum is within valid bounds
                valid = self._set_leq_n(out, valid)

                # ensure elements of sum are distinct
                valid = self._is_distinct(out, valid)

                # if mod=False then decrement values in sum since arrays start at 0
                out = self._decrement_if_not_mod(out, valid)

                self._add_set(out, valid)

            # iterate elements in values
            values[loop] = values[loop] + 1
            for lp in range(loop + 1, k):
                values[lp] = values[lp - 1] + 1
