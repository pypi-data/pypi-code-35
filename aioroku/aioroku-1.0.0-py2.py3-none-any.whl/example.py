from aioroku import AioRoku
from argparse import ArgumentParser
import asyncio

import aiohttp

TO = aiohttp.ClientTimeout(total=5)


def get_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--roku_ip', '-r', metavar="ROKU_IP_ADDRESS")
    arg_parser.add_argument('--verbose', '-v', action="count",
                            help='increase verbosity of output')
    args = arg_parser.parse_args()
    roku_ip = args.roku_ip
    return roku_ip


async def main(host):
    async with aiohttp.ClientSession(timeout=TO) as session:
        fauxku = AioRoku(host, session)
        print(await fauxku.sw_info)
        print(await fauxku.power_state)


if __name__ == '__main__':
    r_ip = get_args()
    loop = asyncio.get_event_loop()

    loop.run_until_complete(main(r_ip))
    loop.close()
