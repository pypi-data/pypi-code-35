def match(strh, strp, n1, m1, n2, m2):
    """
    Main algorithm of the project. Compare the strings passed in input.

    Parameters
    ----------
    strh
        This is the human string
    strp
        This is the plant string
    n1
        This is the human string's first position
    m1
        This is the human string's last position
    n2
        This is the plant string's first position
    m2
        This is the plant string's last position

    Returns
    -------
    bool
        True if the strings in the chosen positions are same, False otherwise.

    Note
    --------
    pre: n1, m1, n2, m2 must be natural numbers
    pre: n1, m1, n2, m2 must not be decimal numbers
    pre: The last position of both strings must be greater than the first position of both strings
    pre: The human seed must be equal to the plant seed
    pre: The last position of both strings must be less than the lenght of both strings
    pre: The lenght of both strings must be greater or equal to one
    pre: Every letter of human string must be equals to "A" or "C" or "G" or "U"
    pre: Every letter of plant string must be equals to "A" or "C" or "G" or "U"

    """
    assert n1 >= 0 and n2 >= 0 and m1 >= 0 and m2 >= 0, "One of the positions of one of the seeds is not a natural number!"
    assert type(n1) is int and type(m1) is int and type(n2) is int and type(m2) is int, \
        "All positions must not be decimal numbers!"
    assert m1 >= n1 and m2 >= n2, "One of the final positions of one of the seeds is equal or smaller than the initial one!"
    assert m1 - n1 == m2 - n2, "The length of the 2 seeds is not the same!"
    assert m1 < len(strh) and m2 < len(strp), "One of the final positions is greater than the length of the corresponding seed!"
    assert len(strh) >= 1 and len(strp) >= 1, "One of the seeds has a length less than or equal to zero"
    i = n1
    while i < m1:
        if strh[i] not in {'A', 'C', 'G', 'U'}:
            assert False, "The letter in " + {i+1} + " position of the human string is not valid!"
        i += 1
    i = n2
    while i < m2:
        if strp[i] not in {'A', 'C', 'G', 'U'}:
            assert False, "The letter in " + {i+1} + " position of the plant string is not valid!"
        i += 1

    # Start match
    i = n1
    matched = True
    k = n2 - n1
    while i <= m1 and matched:
        matched = strh[i] == strp[i+k]
        i += 1

    return matched

