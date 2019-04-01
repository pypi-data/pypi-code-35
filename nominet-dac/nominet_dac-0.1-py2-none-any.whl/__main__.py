from gevent import monkey; monkey.patch_all()
import argparse
import time
from .dac import DAC
from .token_bucket import TokenBucket
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', 
        help="file of domains, single column", 
        required=False,
        type=argparse.FileType('r'))
    parser.add_argument('--domain', 
        help="single domain", 
        required=False,
        type=str)
    args = parser.parse_args()

    dac = DAC()
    dac.connect()
    tb = TokenBucket(time_interval_in_seconds=60, items_per_interval=1000)
    tb.start()
    if args.file:
        for line in args.file:
            print(dac.query_domain(line.strip()))
            tb.wait()
    if args.domain:
        print(dac.query_domain(args.domain))
