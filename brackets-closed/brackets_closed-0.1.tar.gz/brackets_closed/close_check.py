def is_closed(input):
    open = 0

    for character in input:
        if character == "(" or character == "[" or character == "{":
            open += 1
        if character == ")" or character == "]" or character == "}":
            open -= 1

    if open != 0:
        return False
    else:
        return True
