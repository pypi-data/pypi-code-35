import os
import sys
import shutil
import argparse

import beepdrive.utils as utils
import beepdrive.bdrive as bdrive
import beepdrive.pyside as pyside

def main():
    # Argument parser
    parser = argparse.ArgumentParser(description=("BeepDrive, automated PoliMi BeeP folders download."))
    parser.add_argument("--path",
                        action="store",
                        help="Specify path to use BeepDrive in console mode."
                       )

    args = parser.parse_args()

    # Set system based temp path
    temp_path = utils.get_temp_path()

    # Reset temporary folder
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    os.makedirs(temp_path)

    if args.path:
        # Create folderpath
        if not os.path.exists(args.path):
            os.makedirs(args.path)

        app = bdrive.BeepDrive(temp_path, args.path)
    else:
        app = pyside.GUI(bdrive.BeepDrive(temp_path))

    app.run()

    # Remove temporary folder
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

if __name__ == "__main__":
    main()
