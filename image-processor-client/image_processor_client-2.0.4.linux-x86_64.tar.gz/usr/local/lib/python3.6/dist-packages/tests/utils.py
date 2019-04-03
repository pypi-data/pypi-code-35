import asyncio
import os


def run_async(function):
    return asyncio.get_event_loop().run_until_complete(function)


def get_files(path):
    return os.listdir(path)
