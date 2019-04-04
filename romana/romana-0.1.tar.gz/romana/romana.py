ROMAN_LITERALS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def _convert(roman_lit):
    try:
        literals = [ROMAN_LITERALS[l] for l in roman_lit]
    except KeyError:
        return False

    result = literals[0]

    for literal in literals[1:]:
        if literal > result:
            result = literal - result
        elif literal <= result:
            result += literal

    return result


print(_convert("ASD"))
