from .LinkedLists import SetLinkedList
from .LinkedLists import ColoringLinkedList
import time, sys, warnings, multiprocessing as mp, queue


def _generate_process(coloring, used, loop, type, n, a, b, mod, start, timeLimit, queue):
    from .RainbowCartesianSumsSim import RbCartesianSumsEq
    from .RainbowSumsSim import RbSumsEq

    if type == "<class 'rainbownum.RainbowCartesianSumsSim.RbCartesianSumsEq'>":
        eq = RbCartesianSumsEq(n[0], n[1], a, b)
    elif type == "<class 'rainbownum.RainbowSumsSim.RbSumsEq'>":
        eq = RbSumsEq(n[0], a, b, mod)
    eq.set_time_limit(timeLimit)
    eq.start = start
    eq._gen_colorings(coloring, used, loop, queue)
    return


class RainbowSim:
    def __init__(self, n, a, b, mod):
        if type(n) is not int or n < 1:
            raise TypeError("Scalar n must be an integer greater than or equal to 1")
        self.n = n

        for i in a:
            if type(i) is not int or i is 0:
                raise TypeError("Vector a[] can only contain nonzero integers")
        self.a = a
        self.k = len(a)

        # TODO INSERT WARNINGS FOR b TYPE
        self.b = b

        if type(mod) is not bool:
            raise TypeError("Boolean mod must be either", True, "for Zn or", False, "for [n].")
        self.mod = mod

        self.sets = [0 for _ in range(n + 1)]
        for i in range(n + 1):
            self.sets[i] = SetLinkedList()
        self._generate_sums()

        self.colorings = ColoringLinkedList()

        self.timeLimit = 43200  # 12 hours
        self.start = 0

        self.queue = mp.Queue()
        self.processes = []
        self.cores = mp.cpu_count()
        if self.cores == 1:
            self.splits = 1
        elif self.cores == 2:
            self.splits = 2  # two processes
        elif self.cores <= 8:
            self.splits = 3  # five processes
        elif self.cores <= 16:
            self.splits = 4  # 13? processes
        else:
            self.splits = 5
        if "win" in sys.platform and sys.version_info[0] != 3 or sys.version_info[1] != 7 or sys.version_info[2] != 0:
            warnings.warn("""WARNING: Windows users must use Python 3.7.0 to take advantage of multiprocessing.""")
            self.splits = 1

    def run(self):
        self.start = time.time()
        coloring = [-1 for _ in range(self.n)]
        coloring[0] = 0
        used = [0 for _ in range(self.n)]
        used[0] = 1

        self._gen_colorings(coloring, used, 1, self.queue)

        temp_colorings = []
        running = self.processes
        while running:
            try:
                while 1:
                    temp_colorings.append(self.queue.get(False))
            except queue.Empty:
                pass
            time.sleep(0.5)  # Give tasks a chance to put more data in
            if not self.queue.empty():
                continue
            running = [p for p in running if p.is_alive()]

        temp_colorings.sort()
        for data in temp_colorings:
            self.colorings.add_coloring(data[0], data[1])

        if time.time() - self.start > self.timeLimit:
            print("\naS(" + self.get_equation() + ", n = " + str(self.n) + ") computation exceed time limit.")
            return None
        print("\naS(" + self.get_equation() + ", n = " + str(self.n) + ") = ", str(self.colorings.maxColors + 1))
        print("Total colorings:", self.colorings.len)
        print("Time:", time.time() - self.start)
        return 1

    def _gen_colorings(self, coloring, used, loop, queue):
        if time.time() - self.start > self.timeLimit:
            return
        if loop == self.n:
            return
        for i in range(0, self.n):
            if i != 0 and used[i - 1] == 0:
                if loop == self.splits:
                    temp = self.colorings.head
                    i = 1
                    while temp is not None:
                        i += 1
                        # TODO look into if this is the problem put()
                        queue.put([temp.data, self.colorings.maxColors])
                        temp = temp.next
                return
            used[i] += 1
            coloring[loop] = i
            if self._contains_rainbow_sum(coloring, loop):
                used[i] -= 1
                continue
            if loop == self.splits - 1:
                if str(type(self)) == "<class 'rainbownum.RainbowCartesianSumsSim.RbCartesianSumsEq'>":
                    p = mp.Process(target=_generate_process, args=(
                    coloring.copy(), used.copy(), loop + 1, str(type(self)), [self.M, self.N], self.a, self.b, self.mod,
                    self.start, self.timeLimit, self.queue))
                else:
                    p = mp.Process(target=_generate_process, args=(
                    coloring.copy(), used.copy(), loop + 1, str(type(self)), [self.n], self.a, self.b, self.mod,
                    self.start, self.timeLimit, self.queue))
                self.processes.append(p)
                p.start()
            else:
                self._gen_colorings(coloring, used, loop + 1, queue)
            if loop == self.n - 1:
                colors = 0
                for j in used:
                    if j == 0:
                        break
                    colors += 1
                colors = max(coloring) + 1
                self.colorings.add_coloring(coloring, colors)
            used[i] -= 1

    def _contains_rainbow_sum(self, coloring, new):
        temp = self.sets[new].head.next
        while temp is not None:
            skip = False
            used = [0 for _ in range(self.n)]
            unique = True
            for i in temp.data:
                if i > new:
                    skip = True
                    break
                used[coloring[i]] += 1
                if used[coloring[i]] > 1:
                    unique = False
            if skip:
                temp = temp.next
                continue
            if unique:
                return True
            temp = temp.next
        return False

    def check_coloring(self, coloring):
        for i in range(1, self.n):
            if self._contains_rainbow_sum(coloring, i) is True:
                print("INVALID: Coloring", coloring, "for n =", self.n, "contains rainbow sums :(")
                return
        print("VALID: Coloring", coloring, "for n =", self.n, "works!")

    def print_extreme_colorings(self, quantity=-1):
        if self.start != -1:
            temp = self.colorings.head
            i = 0
            while temp is not None and (i < quantity or quantity < 0):
                if i == 0:
                    print(temp, end='')
                else:
                    print(',', temp, end='')
                temp = temp.next
                i += 1
        print()

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
                    print('\n', n, ':', [i + 1 for i in temp.data], end='')
                else:
                    print('\n', n, ':', temp, end='')
            if temp is not None:
                temp = temp.next
                while temp is not None:
                    if self.mod:
                        print(',', temp, end='')
                    else:
                        print(',', [i + 1 for i in temp.data], end='')
                    temp = temp.next
        print()

    def set_time_limit(self, t):
        self.timeLimit = t

    def time_limit_reached(self):
        return self.start < 0

    def _is_distinct(self, out, valid):
        if not valid:
            return False
        for i in out[:-1]:
            if i == out[self.k - 1]:
                return False
        return True

    def _set_leq_n(self, out, valid):
        if not valid:
            return False
        if not self.mod and 1 > out[self.k - 1] or out[self.k - 1] > self.n:
            return False
        return True

    def _decrement_if_not_mod(self, out, valid):
        if not valid or self.mod:
            return out
        for i in range(self.k):
            out[i] = out[i] - 1
        return out

    def _add_set(self, out, valid):
        if not valid:
            return
        for i in out:
            self.sets[i].add_set(out)
        self.sets[self.n].add_set(out)
