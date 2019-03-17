from .LinkedLists import SetLinkedList
from .LinkedLists import ColoringLinkedList
import time
import multiprocessing as mp


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

        self.colorings = ColoringLinkedList()

        self.timeLimit = 43200
        self.start = 0

        self.queue = mp.Queue()
        if mp.cpu_count() == 1:
            self.splits = 1
        elif mp.cpu_count() == 2:
            self.splits = 2
        elif mp.cpu_count() <= 8:
            self.splits = 3
        elif mp.cpu_count() <= 16:
            self.splits = 4
        else:
            self.splits = 5

    def run(self):
        self.start = time.time()
        coloring = [-1 for _ in range(self.n)]
        coloring[0] = 0
        used = [0 for _ in range(self.n)]
        used[0] = 1

        self._gen_colorings(coloring, used, 1, self.colorings, self.queue, self.splits)
        for p in mp.active_children():
            p.join()
        temp_colorings = []
        while not self.queue.empty():
            temp_colorings.append(self.queue.get())
        temp_colorings.sort()
        for data in temp_colorings:
            self.colorings.add_coloring(data[0], data[1])
        self.queue.close()

        if self.start == -1:
            print("\naS(" + self.get_equation() + ", n = " + str(self.n) + ") computation exceed time limit.")
            return None
        print("\naS(" + self.get_equation() + ", n = " + str(self.n) + ") = ", str(self.colorings.maxColors + 1))
        print("Total colorings:", self.colorings.len)
        print("Time:", time.time() - self.start)
        return 1

    def _gen_colorings(self, coloring, used, loop, colorings, queue, splits):
        if time.time() - self.start > self.timeLimit:
            self.start = -1
            return
        if loop == self.n:
            return
        for i in range(0, self.n):
            if i != 0 and used[i - 1] == 0:
                if loop == splits:
                    temp = colorings.head
                    i = 1
                    while temp is not None:
                        i += 1
                        queue.put([temp.data, colorings.maxColors])
                        temp = temp.next
                return
            used[i] += 1
            coloring[loop] = i
            if self._contains_rainbow_sum(coloring, loop):
                used[i] -= 1
                continue
            if loop == splits - 1:
                p = mp.Process(target=self._gen_colorings,
                               args=(coloring.copy(), used.copy(), loop + 1, ColoringLinkedList(), queue, splits))
                p.start()
            else:
                self._gen_colorings(coloring, used, loop + 1, colorings, queue, splits)
            if loop == self.n - 1:
                colors = 0;
                for j in used:
                    if j == 0:
                        break
                    colors += 1
                colors = max(coloring) + 1
                colorings.add_coloring(coloring, colors)
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
