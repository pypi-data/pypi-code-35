def is_closed(input):
    open = []

    for character in input:
        if character == "(" or character == "[" or character == "{":
          open.append(character)
        elif character == ")":
            if len(open) == 0:
                print("False")
                return
            if open[-1] != "(":
                print("False")
                return
            else:
                del open[-1]
        elif character == "]":
            if len(open) == 0:
                print("False")
                return
            if open[-1] != "[":
                print("False")
                return
            else:
                del open[-1]
        elif character == "}":
            if len(open) == 0:
                print("False")
                return
            if open[-1] != "{":
                print("False")
                return
            else:
                del open[-1]
        
    print("True")
