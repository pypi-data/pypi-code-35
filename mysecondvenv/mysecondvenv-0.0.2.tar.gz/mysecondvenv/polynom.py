def solve_polynom(a, b, c):
    if a == 0:
        # One degree.
        return (-c / b, )
    det = b * b - (4 * a * c)
    if det < 0:
        # No real solution.
        return None

    det = det ** 0.5
    x1 = (b - det) / (2 * a)
    x2 = (b + det) / (2 * a)
    return x1, x2


print(solve_polynom(1, 1, -1))