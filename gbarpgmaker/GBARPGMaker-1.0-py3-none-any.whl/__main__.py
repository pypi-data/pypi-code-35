import argparse
import sys

from GBARPGMaker.GBARPGMaker import GBARPGMaker


def main():
    parser = argparse.ArgumentParser(description='GBARPGMaker description')

    parser.add_argument("command", choices=["new", "make", "inter"])

    args = parser.parse_args()

    sys.path.append("./")

    import config

    if args.command == "new":
        config.targets = []
        config.excluded_targets = []
        grm = GBARPGMaker(config)
        grm.make_game()
    elif args.command == "make":
        grm = GBARPGMaker(config)
        grm.make_game()
    elif args.command == "inter":
        grm = GBARPGMaker(config)
        m = grm.maps[list(grm.maps.keys())[0]]
        s = grm.sprite_graphics[list(grm.sprite_graphics.keys())[0]]
        __import__('IPython').embed()


if __name__ == "__main__":
    main()

