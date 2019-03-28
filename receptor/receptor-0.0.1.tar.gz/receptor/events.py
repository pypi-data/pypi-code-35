import argparse
import asyncio


async def mainloop():
    loop = asyncio.get_running_loop()


def main(sys_args=None):
    parser = argparse.ArgumentParser("receptor")
    args = parser.parse_args(sys_args)
    asyncio.run(mainloop())
