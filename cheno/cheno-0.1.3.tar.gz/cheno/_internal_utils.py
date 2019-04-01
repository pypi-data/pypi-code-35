import numpy as np

# TODO: Refactor function such that algorithm is moved to multiprocessing, 
# and names are formulated more generale
def _gen_ranks_subsets(size, w, runs):
    size_total = sum(size)
    lb = (size[0] * (size[0] + 1)) / 2
    ub = size[0] * (size_total + (size_total - size[0] + 1)) / 2

    if not lb < w < ub:
        raise ValueError(
            f'The sum you have inputed has to be between: {lb} and {ub}')

    # Find a good initial config
    ranks = [np.random.choice(
        np.arange(1, size_total + 1), size[0], replace=False)]
    min_diff = abs(sum(ranks[0]) - w)
    for _ in range(runs):
        cur = np.random.choice(
            np.arange(1, size_total + 1), size[0], replace=False)
        if abs(sum(cur) - w) < min_diff:
            ranks[0] = cur
    ranks.append(np.asarray([x for x in np.arange(1, size_total + 1) if x not in ranks[0]]))

    if sum(ranks[0]) == w:
        if size[0] < size[1]:
            return ranks
        return [ranks[1], ranks[0]]

    # Initialize values
    r = abs(w - sum(ranks[0]))
    best = ranks

    # # FIXME: Refactor with a randomized algo.
    for i in range(runs):
        if w < sum(ranks[0]):
            next_lesser, next_lesser_idx = _next_lesser(ranks[1], ranks[0][size[0] - (i % size[0]) - 1])
            if next_lesser != -1:
                ranks[1][next_lesser_idx] = ranks[0][size[0] - (i % size[0]) - 1]
                ranks[0][size[0] - (i % size[0]) - 1] = next_lesser
            else:
                ranks[0] = sorted(ranks[0])
        elif w > sum(ranks[0]):
            next_greater, next_greater_idx = _next_greater(
                ranks[1], ranks[0][size[0] - (i % size[0]) - 1])
            if next_greater != -1:
                ranks[1][next_greater_idx] = ranks[0][size[0] - (i % size[0]) - 1]
                ranks[0][size[0] - (i % size[0]) - 1] = next_greater
            else:
                ranks[0] = sorted(ranks[0])
        else:
            break

        if abs(w - sum(ranks[0])) < r:
            best = ranks

    if size[0] < size[1]:
        return best
    return [best[1], best[0]]


def _next_lesser(rest, v):
    if rest is None or len(rest) <= 0:
        raise ValueError('Comparing values in an empty list.')
    if not all(rest[i] <= rest[i + 1] for i in range(len(rest) - 1)):
        raise ValueError('List is not sorted.')

    for i, e in enumerate(reversed(rest)):
        if v > e:
            return e, len(rest) - i - 1
    return -1, -1


def _next_greater(rest, v):
    if rest is None or len(rest) <= 0:
        raise ValueError('Comparing values in an empty list.')
    if not all(rest[i] <= rest[i + 1] for i in range(len(rest) - 1)):
        raise ValueError('List is not sorted.')

    for i, e in enumerate(rest):
        if v < e:
            return e, i
    return -1, -1
