import argparse

def get():
    parser = argparse.ArgumentParser(description='Execute commands in across server groups')

    parser.add_argument(
      'target',
      help='Target to run as defined in the YAML',
    )

    return parser.parse_args()
