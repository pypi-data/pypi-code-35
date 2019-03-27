#!/usr/bin/python3
from PyQt5 import QtDBus
import sys


def main():
    bus = QtDBus.QDBusConnection.sessionBus()
    interface = QtDBus.QDBusInterface("org.qoob.session", "/org/qoob/session", "org.qoob.session", bus)
    cmd = "%".join(str(arg) for arg in sys.argv[1:])

    if cmd.lower().count("--help"):
        print("General options")
        print("--delete: Trigger the delete event for the current media")
        print("--delete-no-confirm: Delete the current media without confirmation")
        print("--shuffle on/off: Enable/disable or toggle shuffle option")
        print("--repeat off/all/single:  Disable, change repeat mode or toggle repeat option")
        print("--quiet: When this flag is enabled, the command is only passed if the player is already open")
        print("--clear: Clear the library view")
        print("--folder: Load music files from one or multiples folders")
        print("--file: Load one or multiples music files")
        print("--quit: Close the player")
        print()
        print("Playback options")
        print("--play")
        print("--pause")
        print("--play-pause")
        print("--stop")
        print("--previous")
        print("--next")

    # Pass the arguments to the existing bus
    elif interface.isValid():
        interface.call("parse", cmd)
        sys.exit(0)

    # Create a new instance
    elif not cmd.lower().count("--quiet"):
        try:
            import qoob.main as qoob
        except ImportError:
            import main as qoob
        qoob.main(cmd)

if __name__ == '__main__':
    main()
