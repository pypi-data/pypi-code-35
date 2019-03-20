from sys import argv
from os.path import isfile, split, isdir

__doc__ = """
Commands:
send    - Send a file.
receive - Receive a file.
"""


if not len(argv) >= 2:
    print("Wrong number of arguments.")
    print(__doc__)
elif argv[1] == "send":
    from udp_filetransfer import send
    try:
        filepath = argv[2]
    except IndexError:
        filepath = input("Enter file path (can be relative to cwd): ")
    if isfile(filepath):
        send(filepath)
    else:
        print("File does not exist. Exitting...")
elif argv[1] == "receive":
    from udp_filetransfer import receive
    print(receive())
else:
    print("Wrong argument.")
    print(__doc__)

