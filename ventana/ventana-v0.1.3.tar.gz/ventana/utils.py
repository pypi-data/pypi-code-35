def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def get_indices(i, n):
    if i < 5:
        return list(range(0, min(i + 5, n)))
    elif i >= n - 5:
        return list(range(i - 5, n - 1))
    else:
        return list(range(i - 5, i + 5))