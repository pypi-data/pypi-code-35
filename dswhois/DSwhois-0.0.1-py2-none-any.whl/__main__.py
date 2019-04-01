import sys
from .query import DomainInfo
import json

def main():
    args = sys.argv[1:]
    if len(args) == 1:
        domain_info = DomainInfo()
        domain_name = args[0]
        print (json.dumps(domain_info.query(domain_name), indent=4, sort_keys=True))
    else:
        print("Invalid domain!")

if __name__ == '__main__':
    main()
