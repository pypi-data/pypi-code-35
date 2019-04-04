import readline
readline.parse_and_bind("tab: menu-complete")
import getch



def rlinput(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
       return input(prompt)
    finally:
       readline.set_startup_hook()

class Completer:

    def __init__(self, words):

        self.words = words
        self.prefix = None

    def complete(self, prefix, index):
        if prefix != self.prefix:
            # we have a new prefix!
            # find all words that start with this prefix
            self.matching_words = [
                w for w in self.words if w.startswith(prefix)
                ]
            self.prefix = prefix
        try:
            return self.matching_words[index]
        except IndexError:
            return None


def query_choice(choices,
                 prompt="Choice: ",
                 default=None, single_char=False,
                 allow_other=False,
                 case_insensitive=False):


    while True:
        if single_char:
            print(prompt, end=' ')
            choice = getch.getche()
            print()
        else:
            completer = Completer(choices)
            readline.set_completer(completer.complete)
            choice = rlinput(prompt=prompt, prefill=default or None)
            readline.set_completer(None)

        if not allow_other:
            if (
                    (case_insensitive and choice not in choices)
                    or (not case_insensitive
                        and choice.lower()
                        not in [ c.lower() for c in choices ]
                    )
            ):
                print("%s not one of: %s" %(choice, ','.join(choices)))
                continue
        return choice

def query_yes_no(prompt=">>> ", default="y", single_char=False):

    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        choices = " [y/n] "
    elif default in ["yes", "y"]:
        choices = " [Y/n] "
    elif default in ["no", "n"]:
        choices = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    choice = query_choice("yn", prompt=prompt + choices,
                          default=default,
                          single_char=single_char, case_insensitive=True)
    if default is not None and choice == '':
        return valid[default]
    elif choice in valid:
        return valid[choice]

readline.parse_and_bind("tab: menu-complete")

# print query_yes_no(single_char=True)
# print query_choice(["foo", "bar", "baz"])
# print query_choice(["foo", "bar", "baz"], default="foo", allow_other=True)
