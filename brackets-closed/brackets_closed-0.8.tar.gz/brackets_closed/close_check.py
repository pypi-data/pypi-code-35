def is_closed(input):
    if len(input) == 0:
        print("Input must contain at least one bracket")
        return 0
    
    any_brackets = False
    open = []

    for character in input:
        if character == "(" or character == "[" or character == "{":
          open.append(character)
          any_brackets = True
        elif character == ")":
            if len(open) == 0:
                print("False")
                return 0
            if open[-1] != "(":
                print("False")
                return 0
            else:
                del open[-1]
        elif character == "]":
            if len(open) == 0:
                print("False")
                return 0
            if open[-1] != "[":
                print("False")
                return 0
            else:
                del open[-1]
        elif character == "}":
            if len(open) == 0:
                print("False")
                return 0
            if open[-1] != "{":
                print("False")
                return 0
            else:
                del open[-1]

    if any_brackets:
        print("True")
        return 1
    else:
        print("No brackets supplied")
        return 0
