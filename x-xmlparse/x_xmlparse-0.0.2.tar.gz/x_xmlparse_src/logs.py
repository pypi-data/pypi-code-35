import  logging
from termcolor import colored

def L(*args, e=False):
    if e:
        print(colored("[x]", 'red', attrs=['bold']) + " ".join(["{}".format(i) for i in args]))
    else:
        print(colored("[-]", 'green', attrs=['bold']) + colored(" ".join(["{}".format(i) for i in args]), 'blue'))
