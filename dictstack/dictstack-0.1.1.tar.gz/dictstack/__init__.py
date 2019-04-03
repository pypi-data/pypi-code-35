class DictStack:
    def __init__(self, *args, **kwargs):
        self._stack = [dict(*args, **kwargs)]

    def __setitem__(self, k, v):
        self._stack[-1][k] = v

    def __getitem__(self, k):
        for i in reversed(range(0, len(self._stack))):
            if k in self._stack[i]:
                return self._stack[i][k]

        raise KeyError(k)

    def keys(self):
        all_keys = set()

        for i in range(0, len(self._stack)):
            all_keys |= set(self._stack[i].keys())

        return all_keys

    def __len__(self):
        return len(self.keys())

    def push(self):
        self._stack.append({})

    def pop(self):
        self._stack.pop()
