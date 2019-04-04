import os
import stat
from pathlib import Path
import yaml
import hashlib
import sys
from distutils.dir_util import copy_tree
from collections import defaultdict
import zlib
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from itertools import repeat
from collections import defaultdict


class Config():
    "Creates a default config file 'config.yml' in $HOME (default `~/.jovian/`)"
    DEFAULT_CONFIG_LOCATION = os.path.expanduser('~/.jovian')
    DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_LOCATION + '/config.yml'
    DEFAULT_CONFIG = {
        'data_path': DEFAULT_CONFIG_LOCATION + '/data',
        'objects_path': DEFAULT_CONFIG_LOCATION + '/objects',
        'data_archive_path': DEFAULT_CONFIG_LOCATION + '/archive',
        'model_path': DEFAULT_CONFIG_LOCATION + '/models'
    }

    @classmethod
    def get_key(cls, key):
        "Get the path to `key` in the config file."
        return cls.get().get(key, cls.DEFAULT_CONFIG.get(key, None))

    @classmethod
    def get_path(cls, path, ensure_exists=True):
        "Get the `path` in the config file."
        path = _expand_path(cls.get_key(path))
        if ensure_exists:
            _ensure_exists(path)
        return path

    @classmethod
    def data_path(cls):
        "Get the path to data in the config file."
        return cls.get_path('data_path')

    @classmethod
    def data_archive_path(cls):
        "Get the path to data archives in the config file."
        return cls.get_path('data_archive_path')

    @classmethod
    def objects_path(cls):
        "Get the path to objects in the config file."
        return cls.get_path('objects_path')

    @classmethod
    def model_path(cls):
        "Get the path to fastai pretrained models in the config file."
        return cls.get_path('model_path')

    @classmethod
    def get(cls, fpath=None, create_missing=True):
        "Retrieve the `Config` in `fpath`."
        fpath = _expand_path(fpath or cls.DEFAULT_CONFIG_PATH)
        if not fpath.exists() and create_missing:
            cls.create(fpath)
        assert fpath.exists(
        ), 'Could not find config at: {fpath}. Please create'
        with open(str(fpath), 'r') as yaml_file:
            return yaml.safe_load(yaml_file)

    @classmethod
    def create(cls, fpath):
        "Creates a `Config` from `fpath`."
        fpath = _expand_path(fpath)
        assert(fpath.suffix == '.yml')
        print("fpath", fpath)
        if fpath.exists():
            return
        fpath.parent.mkdir(parents=True, exist_ok=True)
        with open(str(fpath), 'w') as yaml_file:
            yaml.dump(cls.DEFAULT_CONFIG, yaml_file, default_flow_style=False)


def _expand_path(fpath):
    return Path(fpath).expanduser()


def _ensure_exists(dpath):
    if not dpath.exists():
        os.makedirs(str(dpath), exist_ok=True)
    assert(dpath.is_dir())


def _mk_read_only(dpath):
    os.chmod(str(dpath), stat.S_IREAD)


def _mk_exec(dpath):
    os.chmod(str(dpath), stat.S_IEXEC | stat.S_IREAD)


def _set_permissions(directory, verbose=0, dry_run=True):
    directory = str(directory)
    for root, dirs, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            if verbose == 1:
                print("Setting RO", filepath)
            if not dry_run:
                _mk_read_only(filepath)
        if verbose == 1:
            print("Setting EX", root)
        if not dry_run:
            _mk_exec(root)


def _to_str(string):
    try:
        return string.decode("utf-8")
    except ValueError:
        return string


def _get_datasets():
    data_path = Config().data_path()
    datasets = [sub_dir for sub_dir in sorted(
        data_path.iterdir()) if sub_dir.is_dir()]
    return datasets


def _get_versions(dataset):
    versions = []
    for version in dataset.iterdir():
        if version.is_file():
            version_content = get_decompressed_content(_get_content(version))
            is_data = _to_str(version_content)[0:4] == "data"
            if is_data:
                versions.append(str(version.name))
            else:
                print("skipping", version.name)
    return versions


def _get_datasets_with_version():
    datasets = _get_datasets()
    versions = dict()
    for dataset in datasets:
        versions[str(dataset.name)] = _get_versions(dataset)
    return versions


def _get_filtered_versions(expected_version, versions):
    if expected_version is None:
        return versions

    return [version for version in versions if version.startswith(expected_version)]


def _parse_name_version(name_with_version):
    args_list = name_with_version.split("/")
    args_len = len(args_list)
    if args_len == 1:
        return args_list[0], None
    elif args_len >= 2:
        return args_list[0], args_list[1]
    else:
        return "", None


def _get_object_path_by_hash(hash):
    prefix = hash[0:2]
    name_new = hash[2:]
    return Config.objects_path() / prefix / name_new


def _get_object_by_hash(hash):
    path = _get_object_path_by_hash(hash)
    return _get_content(path)


def _print(content_list=[], header=None, footer=False):
    if header is not None:
        print()
        print(header)
        print("-" * 100)

    print("\n".join(content_list))

    if footer:
        print("-" * 100, "\n")


def list_datasets():
    content_list = []
    datasets = _get_datasets_with_version()
    for key in sorted(datasets.keys()):
        content_list.append("{} : {}".format(
            key, sorted(datasets[key])))

    _print(content_list, "Datasets:", True)


def list_cache(verbose=1):
    content_list = []
    archive_path = Config.data_archive_path()
    datasets = _get_datasets_with_version()
    filtered_datasets = {}
    for dataset in sorted(datasets.keys()):
        versions = datasets[dataset]
        filtered_versions = filter(
            lambda version: (archive_path / dataset / version).exists(), 
            versions)
        filtered_datasets[dataset] = list(filtered_versions)


    for key in sorted(filtered_datasets.keys()):
        content_list.append("{} : {}".format(
            key, sorted(filtered_datasets[key])))

    if verbose == 1:
        _print(content_list, "Caches:", True)
    
    return filtered_datasets


def generate_dataset(name_with_version):
    name, version = _parse_name_version(name_with_version)
    src_path_rel = Config().data_path() / name
    src_path = src_path_rel.absolute()

    if not src_path.is_dir():
        header = "Dataset not found: {}".format(name)
        datasets = _get_datasets_with_version()
        _print(["Available datasets are:", list(datasets.keys())], header=header, footer=True)
        return

    versions = _get_versions(src_path)
    filtered_versions = _get_filtered_versions(version, versions)
    num_versions = len(filtered_versions)

    if num_versions == 1:
        version = filtered_versions[0]
    else:
        header = "Dataset version not found:", "{}/{}".format(name, version)
        _print(["Available versions are:"] + versions, header, True)
        return

    src_version_path = src_path / version

    _print(header = "Generating dataset: {}/{}".format(name, version))

    data_repo_content = _to_str(
        get_decompressed_content(_get_content(src_version_path)))

    cmd, data_hash, dataset_name = data_repo_content.split(" ")

    _parse_node(cmd, data_hash, Config.data_archive_path() / name, version)


def _parse_cmd_line(line, root, name):
    line_split = line.split(" ")
    if line_split[0] == "tree":
        cmd_tree, hash_tree, name_tree = line_split
        _parse_node(cmd_tree, hash_tree, root / name, name_tree)
    elif line_split[1] == "blob":
        _, cmd_blob, hash_blob, name_blob = line_split
        _parse_node(cmd_blob, hash_blob, root / name, name_blob)
    else:
        return


def _parse_node(cmd, hash, root, name, dry_run=False):

    do_parallel_process = True
    do_symlink = False

    if cmd == "data":
        _ensure_exists(root / name)
    elif cmd == "tree":
        _ensure_exists(root / name)
    elif cmd == "blob":
        if not dry_run:
            if do_symlink:
                src_obj_path = _get_object_path_by_hash(hash)
                dst_path = root/name
                if not (dst_path.exists() and dst_path.resolve() == src_obj_path):
                    os.symlink(str(src_obj_path), str(dst_path))
            else:
                node = get_decompressed_content(_get_object_by_hash(hash))
                write_content(root / name, node)
        return
    else:
        return

    node_string = _to_str(get_decompressed_content(_get_object_by_hash(hash)))

    if len(node_string) == 0:
        return

    node_string_list = node_string.split("\n")
    blob_list = []
    tree_list = []

    for line in node_string_list:
        line_split = line.split(" ")
        if line_split[0] == "tree":
            tree_list.append(line)
        elif line_split[1] == "blob":
            blob_list.append(line)

    if do_parallel_process:
        with ProcessPoolExecutor() as executor:
            for line, res in tqdm(zip(blob_list, executor.map(_parse_cmd_line, blob_list, repeat(root), repeat(name)))):
                a = 1
    else:
        for line in tqdm(blob_list):
            _parse_cmd_line(line, root, name)

    for line in tree_list:
        _parse_cmd_line(line, root, name)

    return


def mount_dataset(name_with_version, mount_as=None):
    name, version = _parse_name_version(name_with_version)
    src_path = (Config().data_path() / name).absolute()

    if not src_path.is_dir():
        header = "Dataset not found: " + name
        content_list = ["Available datasets are:"] + list(_get_datasets_with_version().keys())
        _print(content_list, header, True)
        return

    versions = _get_versions(src_path)
    filtered_versions = _get_filtered_versions(version, versions)
    num_versions = len(filtered_versions)

    if num_versions == 1:
        version = filtered_versions[0]
    else:
        header = "Dataset version not found: " + "{}/{}".format(name, version)
        content_list = ["Available versions are:"] + versions
        _print(content_list, header, True)
        return

    dataset_cache = list_cache(verbose = 0)

    if name not in dataset_cache or version not in dataset_cache[name]:
        generate_dataset("{}/{}".format(name, version))
    

    mount_name = mount_as or name

    dst_path = _expand_path(mount_name).absolute()
    src_cache_version_path = Config().data_archive_path() / name / version

    if not dst_path.exists():
        os.symlink(str(src_cache_version_path), str(dst_path))
        _print(header = "Successfully mounted: {}/{} as {}".format(name, version, mount_name))
    else:
        _print(header = "Destination folder exists: {}".format(mount_name))


def _check_file(fname):
    size = os.path.getsize(fname)
    with open(fname, "rb") as f:
        hash_nb = hashlib.md5(f.read(2**20)).hexdigest()
    return size, hash_nb


def _check_str(string):
    size = len(string.encode("utf-8"))
    hash_nb = hashlib.md5(string.encode("utf-8")).hexdigest()
    return size, hash_nb


def _get_content(fname):
    with open(str(fname), "rb") as f:
        data = f.read()
        return data


def write_content(fname, content):
    with open(str(fname), "wb") as f:
        f.write(content)


def create_object(name, content):
    prefix = name[0:2]
    name_new = name[2:]
    folder = Config.objects_path() / prefix
    _ensure_exists(folder)
    fname = str(folder / name_new)
    write_content(fname, content)


def get_compressed_content(content, compress=True):
    if compress:
        return zlib.compress(content)
    else:
        return content


def get_decompressed_content(content, compress=True):
    if compress:
        try:
            return zlib.decompress(content)
        except zlib.error:
            return content
    else:
        return content


def _create_dataset(name, version, content):
    folder = Config.data_path() / name
    _ensure_exists(folder)
    fname = str(folder / version)
    write_content(fname, content)


def load_objects_set():
    folder = Config.objects_path()
    objects_set = set()
    for sub in folder.iterdir():
        if sub.is_dir():
            for x in sub.iterdir():
                if x.is_file():
                    name = sub.name + x.name
                    objects_set.add(name)
    return objects_set


def process_file(name, root, objects):
    filepath = os.path.join(root, name)
    size, hash_nb = _check_file(filepath)
    file_str = "{} blob {} {}".format(size, hash_nb, name)
    if hash_nb not in objects:
        content = get_compressed_content(_get_content(filepath))
        create_object(hash_nb, content)
        objects.add(hash_nb)

    return file_str


def process_dir(folder, root, dir_dict):
    folder_key = os.path.join(root, folder)
    folder_str = "tree {} {}".format(dir_dict[folder_key], folder)
    return folder_str


def create_dataset(directory, verbose=0):
    directory = os.path.abspath(str(directory))
    print("directory", directory)
    dir_dict = defaultdict(str)

    objects = load_objects_set()
    initial_objects = len(objects)
    print("objects", initial_objects)

    dataset_name = None

    do_parallel_process = True

    try:
        for i, (root, dirs, files) in enumerate(os.walk(directory, topdown=False)):
            if verbose == 1:
                print(root, dirs, files)

            contents = []
            sorted_files = sorted(files)

            if do_parallel_process:
                with ThreadPoolExecutor() as executor:
                    print("executing...", len(sorted_files))
                    for name, file_str in tqdm(zip(sorted_files, executor.map(process_file, sorted_files, repeat(root), repeat(objects)))):
                        contents.append(file_str)
            else:
                for name in tqdm(sorted_files):
                    file_str = process_file(name, root, objects)
                    contents.append(file_str)

            sorted_dirs = sorted(dirs)
            for folder in sorted_dirs:
                folder_str = process_dir(folder, root, dir_dict)
                contents.append(folder_str)

            file_content = "\n".join(contents)
            size, hash_nb = _check_str(file_content)
            if hash_nb not in objects:
                content = get_compressed_content(file_content.encode("utf-8"))
                create_object(hash_nb, content)
                objects.add(hash_nb)

            dir_dict[root] = hash_nb
            dataset_abs_name = root

    except:
        import traceback
        # Print the stack traceback
        traceback.print_exc()
        return -2

    dataset_name = os.path.basename(dataset_abs_name)
    data_content = "data {} {}".format(
        dir_dict[dataset_abs_name], dataset_name)
    size, dataset_version = _check_str(data_content)

    _create_dataset(dataset_name, dataset_version,
                    get_compressed_content(data_content.encode("utf-8")))

    print("Creating dataset", dataset_name, dataset_version)
    print("Creating", len(objects) - initial_objects, "objects")
    print("================================")
