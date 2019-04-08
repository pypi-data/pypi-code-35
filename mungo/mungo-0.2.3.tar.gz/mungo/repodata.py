import bz2
import copy
import json
import os
import pickle
import sys
from collections import defaultdict
from datetime import datetime, timezone
from os.path import getmtime, basename
from urllib.error import URLError
from urllib.request import Request, urlopen


def _store_parsed_data(self, mtime):
    cachedir = _cachedir()
    target_file = os.path.sep.join([cachedir, 'repodata.pickle'])
    os.makedirs(cachedir, exist_ok=True)
    import pickle
    pickle.dump(self.d, target_file)
    if mtime:
        os.utime(target_file, (mtime, mtime))
    else:
        print("Warning: TODO some notes about mtime", file=sys.stderr)


def download_repo(url, name, offline=False):
    return Repodata.from_url(url, name, offline)


def get_repository_data(channels: list, njobs=8, offline=False):
    # retrieve repodata asynchronously
    urls = []
    for channel in channels:
        for arch in ['linux-64', 'noarch']:
            if channel != "defaults":
                urls.append((f"https://conda.anaconda.org/{channel}/{arch}", f"{channel}/{arch}"))
            else:
                for c in ['main', 'free', 'pro', 'r']:
                    urls.append((f"https://repo.anaconda.com/pkgs/{c}/{arch}", f"{c}/{arch}"))

    from joblib import Parallel, delayed
    return list(Parallel(n_jobs=njobs)(delayed(download_repo)(url, name, offline) for url, name in urls))


def merge_repodata(repodatas):
    ret = Repodata.empty()
    ret.d = copy.deepcopy(repodatas[0].d)  # deepcopy since we do not want to modify the contents of `repodatas[0].d`!
    for r in repodatas[1:]:
        for name, versions in r.d.items():
            for version in versions:
                if version not in ret.d[name]:
                    ret.d[name][version] = r.d[name][version]
    return ret


def _mtime(f):
    return datetime.fromtimestamp(getmtime(f))


def _mtime_timestamp(f):
    return _mtime(f).replace(tzinfo=timezone.utc).timestamp()


def _cachedir():
    return os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))


def parse_repodata(reponame, json_data):
    ret = defaultdict(dict)

    if json_data is None:
        return ret

    packages = json_data["packages"]

    for filename, p in packages.items():
        new_version = "{version}.{build}".format(version=p["version"], build=p["build_number"])
        p["fn"] = filename
        p["channel"] = f"https://conda.anaconda.org/{reponame}"
        ret[p["name"]][new_version] = p

    for name, versions in ret.items():
        for v_name, v_value in versions.items():
            v_value["reponame"] = reponame
    return ret


class Repodata:

    def __init__(self, name, data):
        self.name = name
        self.d = data

    @classmethod
    def empty(cls):
        return cls(None, defaultdict(dict))

    @classmethod
    def _from_json(cls, name, json_data, cache=True, remote_mtime=None):
        repository_data = parse_repodata(name, json_data)
        if cache:
            local_dir = os.path.expanduser(os.path.join(_cachedir(), 'conda', 'repos', name))
            local_file = os.path.join(local_dir, 'repodata.pickle')
            if os.path.exists(local_file):
                local_mtime = _mtime_timestamp(local_file)
                if not remote_mtime or remote_mtime > local_mtime:
                    # print(f"Remote {name}/repodata is newer, updating {local_file}.")
                    with open(local_file, 'wb') as writer:
                        pickle.dump(repository_data, writer)
                    os.utime(local_file, (remote_mtime, remote_mtime))
                else:
                    # print(f"{local_file} is up to date")
                    pass
            else:
                # print(f"Saving {name}/repodata to {local_file}")
                os.makedirs(local_dir, exist_ok=True)
                with open(local_file, 'wb') as writer:
                    pickle.dump(repository_data, writer)
                if remote_mtime:
                    os.utime(local_file, (remote_mtime, remote_mtime))
        return cls(name, repository_data)

    @classmethod
    def _from_pickle(cls, name, pickle_file):
        with open(pickle_file, 'rb') as reader:
            repository_data = pickle.load(reader)
        return cls(name, repository_data)

    @classmethod
    def from_file(cls, filename):
        opener = bz2.open if filename.endswith('.bz2') else open
        with opener(filename, 'rb') as reader:
            json_data = json.load(reader)
        return cls._from_json(filename, json_data)

    @classmethod
    def from_environment(cls, environment):
        ret = defaultdict(dict)
        # This is a linux only, default path only version of conda's `list_all_known_prefixes`.
        environments_file = os.path.expanduser('~/.conda/environments.txt')
        if not os.path.exists(environments_file):
            raise ValueError("Could not read environment information from ~/.conda/environments.txt.")
        with open(environments_file, 'rt') as reader:
            # FIXME assumption that first line of environments.txt corresponds to base env path might be incorrect
            #default_env_path = reader.readline().strip()
            #default_env_name = os.getenv("CONDA_DEFAULT_ENV", "base")
            default_env_name = "base" #TODO this is not correct in old conda
            env_map = {basename(path): path for path in map(str.strip, reader)}
            #env_map[default_env_name] = default_env_path
        meta_dir = os.path.join(env_map.get(environment, default_env_name), "conda-meta")
        for file in os.listdir(meta_dir):
            if not file.endswith(".json"):
                continue

            with open(os.path.join(meta_dir, file), 'rb') as reader:
                p = json.load(reader)
                name = p["name"]
                p["installed"] = True
            new_version = "{version}.{build}".format(version=p["version"], build=p["build_number"])
            ret[name][new_version] = p
        return cls(environment, ret)

    @classmethod
    def from_url(cls, url, repository_name, offline=False):
        repodata_url = url + "/repodata.json.bz2"
        local_dir = os.path.expanduser(os.path.join(_cachedir(), 'conda', 'repos', repository_name))
        local_file = os.path.join(local_dir, 'repodata.pickle')
        headers = {}

        if offline: # TODO if offline check if pickle exist
            return cls._from_pickle(repository_name, local_file)

        if os.path.exists(local_file):
            local_timestamp = _mtime(local_file)
            d = local_timestamp.strftime('%a, %d %b %Y %H:%M:%S %Z')
            headers["If-Modified-Since"] = d
        request = Request(repodata_url, headers=headers)
        # The following code is slightly unwieldy, sorry for that
        with urlopen(Request(repodata_url, method='HEAD')) as conn:
            last_modified = conn.headers.get('last-modified', None)
            if last_modified:
                last_modified = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
                last_modified = last_modified.replace(tzinfo=timezone.utc).timestamp()
                if os.path.exists(local_file):
                    if last_modified <= _mtime_timestamp(local_file):
                        return cls._from_pickle(repository_name, local_file)
        try:
            with urlopen(request) as conn:
                json_data_compressed = conn.read()
                data = json.loads(bz2.decompress(json_data_compressed))
                return cls._from_json(repository_name, data, remote_mtime=last_modified)
        except URLError as e:
            if e.getcode() == 304:  # NOT MODIFIED
                return cls._from_pickle(repository_name, local_file)
            else:
                raise e
# end
