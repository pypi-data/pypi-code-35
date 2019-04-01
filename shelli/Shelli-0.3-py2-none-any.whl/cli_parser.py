"""
Defines helpers for managing argument parsing
"""

import argparse

def get():
    """Returns args as compiled by argparse"""

    parser = argparse.ArgumentParser(description='Execute commands in across server groups')

    parser.add_argument(
        '-c', '--config',
        default='~/.shelli.yml',
        help='Path to YAML configuration file',
    )

    parser.add_argument(
        'target',
        help='Target to run as defined in the YAML',
    )

    return parser.parse_args()
