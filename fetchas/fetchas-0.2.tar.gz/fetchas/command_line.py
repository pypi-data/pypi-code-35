import fetchas
import sys

def main():
    fetchas.main()

def fetch_as_mobile():
    args = ['-a', 'mobile'].extend(sys.argv[1:])
    fetchas.main(args)
