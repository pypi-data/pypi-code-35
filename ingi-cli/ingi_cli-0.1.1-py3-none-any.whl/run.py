import requests
import tempfile
import pprint
import subprocess
import argparse
import os, sys, stat

import dateutil.parser

# lets make sure urlparse works for both python 2 and 3
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from ingi.cache import Cache

cache = None

BINARY_MAP = {
    'Python': 'python',
    'Shell': 'bash'
}

class CLIException(Exception):
    pass


def get_input(message):
    """
    Checks whether python 2 or 3 input. Also useful for test mocking.
    :param message: The test message to show for input
    :returns: The user input
    """
    try:
        return raw_input(message)
    except NameError:
        return input(message)


def write_gists(gist_data, path, basepath=None):
    """
    Write all gist files contents' to the local filesystem.
    :param gist_data: The gist result as returned by github API.
    :param path: The path where to write all files from gist.
    :param basepath: Prefix for the file path
    """

    if basepath:
        path = os.path.join(basepath, path)

    # save the files locally
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
            
    for gist_file in gist_data['files'].values():
        filepath = os.path.join(path, gist_file['filename'])
        
        with open(filepath, 'a+') as f:
            f.write(gist_file['content'])


def get_gist_id_from_url(gist_url):
    """
    Strip the gist id from a gist html page url.
    :param gist_url: Gist html page url
    :returns: Stripped gist ID as a string.
    """
    parsed = urlparse(gist_url)
    gist_id = (parsed.path.split('/'))[-1]
    return gist_id


def get_gist_api_data(gist_id):
    """
    Get gist object from GitHub API.
    :param gist_id: GitHub gist ID
    :response: The gist dictionary
    """
    gist_path = 'https://api.github.com/gists/{}'.format(gist_id)
    result = requests.get(gist_path)

    if result.status_code != 200:
        raise CLIException("Could not find the gist for id '{}' ".format(gist_id))

    return result.json()


def invoke_gist(gist):
    """
    Run gist locally by entrypoint if it has a binary mapping.
    :param gist: Gist object as stored in local cache.
    """
    filepath = os.path.join(cache.cache_path, gist['local_filepath'], gist['entrypoint'])

    try:
        subprocess.call([BINARY_MAP[gist['language']], filepath])
    except KeyError:
        raise CLIException("No binary mapping for file type '{}' found.".format(gist['language']))


def determine_entrypoint(gist_data):
    """
    Determine the entrypoint for the gist if not known yet. Prompts the user if multiple
    files in gist.
    :param gist_data: gist dictionary returned from GitHub API.
    :returns: String filename to use as execution entrypoint.
    """

    if len(gist_data['files'].values()) > 1:
        # specify the entrypoint
        print("Multiple gist files found")
        for i, item in enumerate(gist_data['files'].values()):
            print("[{}] {}".format(i, item['filename']))

        try:
            choice = int(get_input("\nChoose an entry point: "))
        except ValueError:
            raise CLIException("Invalid choice, please specify a number as indicated with [].")

        return list(gist_data['files'].keys())[int(choice)]
    else:
        return list(gist_data['files'].keys())[0]


def load_gist(gist_id):
    """
    Fetch the gist by id, either from local cache or pulled from github.
    :param gist_id: The id of the github gist
    :returns: A gist object
    """
    gist_data = get_gist_api_data(gist_id)
    cached_obj = cache.is_gist_cached(gist_id, is_newer=dateutil.parser.parse(gist_data['updated_at']))

    if not cached_obj:
        entrypoint = determine_entrypoint(gist_data)

        cached_obj = cache.cache_gist(gist_data, entrypoint)
        write_gists(gist_data, cached_obj['local_filepath'], basepath=cache.cache_path)
        # make sure the local cache is updated
        cache.dump()
    else:
        print("Found cached gist {}\n".format(gist_id))

    return cached_obj

    # 784715a342e05b55072146c115fa537a
    # https://gist.github.com/ankushguptadelhi/784715a342e05b55072146c115fa537a


def interperet_call(args):
    """
    Check the args passed to cli and perform appropriate tasks.
    :param args: The arguments as parsed by python argparse
    """
    global cache

    # if getattr(args, 'wipe_cache', None) is not None:
    #     proceed = input("Are you sure you want to clear the cache? This cannot be undone (y/N): ")
    #     if proceed.lower() in ['y', 'yes']:
    #         Cache.clear()
    #     else:
    #         while proceed.lower() not in ['y', 'yes', 'n', 'no']:
    #             proceed = input("Incorrect option type 'y' or 'n': ")

    #         if proceed.lower() in ['y', 'yes']:
    #             Cache.clear()
    #     exit()

    cache = Cache()

    if not args.use_id:
        gist_id = get_gist_id_from_url(args.gist)
    else:
        gist_id = args.gist

    gist = load_gist(gist_id)

    if not args.save_only:
        invoke_gist(gist)


def main():
    parser = argparse.ArgumentParser(description='Execute gists locally from any language.')

    subs = parser.add_subparsers()
    get_parser = subs.add_parser('get')
    get_parser.add_argument('gist', help='The gist URL or ID.')
    get_parser.add_argument('--use_id', dest="use_id", action="store_true",
                        help='Whether a gist ID instead of html URL is specified.')
    get_parser.add_argument('--save_only', dest="save_only", action="store_true",
                        help="Just download and cache the gist, don't run it.")

    get_parser.set_defaults(save_only=False, use_id=False)

    cache_parser = subs.add_parser('cache')
    cache_parser.add_argument('--clear_cache', dest="wipe_cache", action="store_true", help='Wipe the cached data')
    cache_parser.set_defaults(wipe_cache=None)

    args = parser.parse_args()

    # easy way to unittest our CLI tool
    try:
        interperet_call(args)
    except CLIException as e:
        print("\n{}".format(e))