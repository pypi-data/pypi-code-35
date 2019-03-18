from .RainbowSim import RainbowSim
import numpy as np


class RbCartesianSumsEq(RainbowSim):
    def __init__(self, m, n, a, b=[0, 0]):
        super(RbCartesianSumsEq, self).__init__(m * n, a, Point(b[0], b[1]), False)
        self.M = m  # rows
        self.N = n  # columns
        self.sums = self.sets
        self.__generate_sums()

    def get_equation(self):
        eq = ""
        for i in self.a:
            eq += str(i) + "x + "
        eq = eq[:-2] + "= " + str(self.b) + ", M = " + str(self.M) + ", N = " + str(self.N)
        return eq

    def __generate_sums(self):
        values = list(range(1, self.k))
        self.__recur_gen_sums(values, 0)

    def __recur_gen_sums(self, values, loop):
        k = self.k - 1
        if loop == k:
            return
        stop_case = self.n - k + loop
        while values[loop] <= stop_case:
            self.__recur_gen_sums(values, loop + 1)
            if loop == k - 1:
                sum = Point(0, 0)
                out = [0 for _ in range(self.k)]
                for i in range(len(values)):
                    sum = sum + self.a[i] * self.__translate(values[i])
                    out[i] = values[i]
                valid = True
                sum = (sum - self.b) / -self.a[k]
                if sum.x == int(sum.x) and sum.y == int(sum.y) and sum.x <= self.M and sum.y <= self.N:
                    out[k] = self.__point_to_i(sum)
                    valid = self._set_leq_n(out, valid)
                    valid = self._is_distinct(out, valid)
                    out = self._decrement_if_not_mod(out, valid)
                    self._add_set(out, valid)
            values[loop] = values[loop] + 1
            for lp in range(loop + 1, k):
                values[lp] = values[lp - 1] + 1

    def __translate(self, n):
        x = (n + self.N - 1) // self.N
        y = 1 + ((n - 1) % self.N)
        return Point(x, y)

    def __point_to_i(self, p):
        return self.N * (p.x - 1) + p.y

    def print_extreme_matrices(self, quantity=-1):
        if self.start != -1:
            temp = self.colorings.head
            i = 0
            while temp is not None and (i < quantity or quantity < 0):
                matrix = [temp.data[i * self.N:(i + 1) * self.N] for i in
                          range((len(temp.data) + self.N - 1) // self.N)]
                print(np.matrix(matrix), "\n")
                temp = temp.next
                i += 1
        print()

    def print_set_matrices(self, quantity=-1):
        sum = self.sums[self.n].head.next
        i = 0
        while sum.next is not None and (i < quantity or quantity < 0):
            matrix = [["*" for _ in range(self.N)] for _ in range(self.M)]
            for i in sum.data:
                p = self.__translate(i + 1)
                matrix[p.x - 1][p.y - 1] = "0"
            print(np.matrix(matrix), "\n")
            sum = sum.next
            i += 1
        return

    def print_sets(self, nums=-1):
        print('Sets Generated:', end='')
        if nums is -1 and self.mod:
            nums = list(range(self.n))
        elif nums is -1 and not self.mod:
            nums = list(range(1, self.n + 1))
        for n in nums:
            if self.mod:
                temp = self.sets[n].head.next
            else:
                temp = self.sets[n - 1].head.next
            if self.mod:
                print('\n', n, ':', temp, end='')
            else:
                if temp is not None:
                    print('\n', n, ':',
                          '[%s]' % ', '.join(map(str, [self.__translate(i + 1) for i in temp.data])), end='')
                else:
                    print('\n', n, ':', temp, end='')
            if temp is not None:
                temp = temp.next
                while temp is not None:
                    if self.mod:
                        print(',', temp, end='')
                    else:
                        print(',', '[%s]' % ', '.join(map(str, [self.__translate(i + 1) for i in temp.data])),
                              end='')
                    temp = temp.next
        print("\n")


class Point:
    def __init__(self, x, y):
        if int(x) != x:
            raise TypeError("Points cannot have parameter of type double: x")
        if int(y) != y:
            raise TypeError("Points cannot have parameter of type double: y")
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __rmul__(self, other):
        return Point(other * self.x, other * self.y)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"
