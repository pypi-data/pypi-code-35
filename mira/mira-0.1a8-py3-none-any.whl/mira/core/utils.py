from typing import List


def compute_contained(si: List[int], so: List[int]):
    """Compute the percentage of one box that is contained
    within another box.

    Args:
        si: A list of four values, xi, yi, wi, yi
            for the inner box
        so: A list of four values, xo, yo, wo, yo
            for the outer box

    Returns:
        The total overlap
    """
    xi, yi, wi, hi = si
    xo, yo, wo, ho = so

    # Find the width and height of the box within the inner
    # box that is missing from the outer box
    wnc = max(min(xo-xi, wi), 0) + max(min((xi + wi) - (xo+wo), wi), 0)
    hnc = max(min(yo-yi, hi), 0) + max(min((yi + hi) - (yo+ho), hi), 0)

    # Compute the size of the contained box
    wc = wi - wnc
    hc = hi - hnc

    inner = (hi*wi)
    if inner == 0:
        return 0
    return (wc*hc) / inner
