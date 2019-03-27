try:
    import colorama
    COLORAMA = True
    colorama.init()
except BaseException:
    COLORAMA = False


# convenience functions for colorama ##############################3

def blue(s):
    if COLORAMA:
        return (colorama.Fore.BLUE) + str(s) + (colorama.Style.RESET_ALL)
    else:
        return s

def red(s):
    if COLORAMA:
        return (colorama.Fore.RED) + str(s) + (colorama.Style.RESET_ALL)
    else:
        return s


def orange(s):
    if COLORAMA:
        return (colorama.Fore.YELLOW) + str(s) + (colorama.Style.RESET_ALL)
    else:
        return s

    
def b_orange(s):
    if COLORAMA:
        return (colorama.Fore.YELLOW) + (colorama.Style.BRIGHT) + \
            str(s) + (colorama.Style.RESET_ALL)
    else:
        return s

    
def b_red(s):
    if COLORAMA:
        return (colorama.Fore.RED) + (colorama.Style.BRIGHT) + \
            str(s) + (colorama.Style.RESET_ALL)
    else:
        return s

def b_blue(s):
    if COLORAMA:
        return (colorama.Fore.BLUE) + (colorama.Style.BRIGHT) + \
            str(s) + (colorama.Style.RESET_ALL)
    else:
        return s

    

def green(s):
    if COLORAMA:
        return (colorama.Fore.GREEN) + str(s) + (colorama.Style.RESET_ALL)
    else:
        return s


def b_green(s):
    if COLORAMA:
        return (colorama.Fore.GREEN) + (colorama.Style.BRIGHT) + \
            str(s) + (colorama.Style.RESET_ALL)
    else:
        return s


def dim(s):
    if COLORAMA:
        return (colorama.Style.DIM) + str(s) + (colorama.Style.RESET_ALL)
    else:
        return s


def bright(s):
    if COLORAMA:
        return (colorama.Style.BRIGHT) + str(s) + (colorama.Style.RESET_ALL)
    else:
        return s


def cyan(s):
    if COLORAMA:
        return (colorama.Fore.CYAN) + str(s) + (colorama.Style.RESET_ALL)
    else:
        return s


def b_cyan(s):
    if COLORAMA:
        return (colorama.Fore.CYAN) + (colorama.Style.BRIGHT) + \
            str(s) + (colorama.Style.RESET_ALL)
    else:
        return s
