from test_containers.app import HELP_TEXT, run
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=HELP_TEXT)
    parser.add_argument("--config", help="configuration file to get the tests from", required=True)
    args = parser.parse_args()
    run(args.config)
