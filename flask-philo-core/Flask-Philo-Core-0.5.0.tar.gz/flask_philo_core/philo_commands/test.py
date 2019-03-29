import argparse
import os
import pytest


def run():
    BASE_DIR = os.getcwd()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--q', help='test file path', required=False,
        default=os.path.join(BASE_DIR, 'tests'))
    parser.add_argument(
        '--x', help='regex for tests to be run', required=False,
        default='test_')
    args, extra_params = parser.parse_known_args()
    exit(pytest.main(['-s', args.q, '-k', args.x]))
