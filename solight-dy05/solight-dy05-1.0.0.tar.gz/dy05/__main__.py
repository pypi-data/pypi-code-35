#!/usr/bin/python3

import sys
import pigpio
from dy05 import DY05

def main():
    if len(sys.argv) < 4:
        print("Error: insufficient number of arguments", file=sys.stderr)
        print("Usage: dy05 ADDRESS SOCKET on|off", file=sys.stderr)
        sys.exit(1)

    address = int(sys.argv[1])

    if address < 0 or address > 1048575:
        print("Invalid address. Valid addresses are 0-1048575 (inclusive)", file=sys.stderr)
        sys.exit(1)

    socket = int(sys.argv[2])
    if socket < 0 or socket > 4:
        print("Invalid socket. Valid sockets are 0-4 (inclusive). 0 Means all in group.", file=sys.stderr)
        sys.exit(1)

    if sys.argv[3] == "on":
        action = 1
    elif sys.argv[3] == "off":
        action = 0
    else:
        print("Invalid action. Valid actions are \"on\" and \"off\".", file=sys.stderr)
        sys.exit(1)

    dy05 = DY05(pigpio.pi(), 17)

    dy05.send(address, socket, action)

if __name__ == "__main__":
    main()
