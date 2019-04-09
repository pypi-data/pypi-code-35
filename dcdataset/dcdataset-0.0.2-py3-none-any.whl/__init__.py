from os.path import pardir, join
from typing import List

from dcdataset.datasets.cifar10 import CIFAR10
from dcdataset.datasets.imdb_review import IMDBReview
from dcdataset.datasets.squad11 import Squad11

dataset_name_dataset_class_map = {
    "cifar10": CIFAR10(),
    "squad11": Squad11(),
    "imdb_review": IMDBReview(),
}


def download_dataset_by_name(dataset_name: str, destination_dir:str) -> bool:
    """
    download known dataset by dataset name if not exists
    Args:
        dataset_name: known dataset name
        destination_dir: local destination directory, toplevel_datadir/dataset_name

    Returns:
        indicates if download is successful
    """
    dataset = dataset_name_dataset_class_map[dataset_name]
    return dataset.download_to_dir(destination_dir)


def get_all_known_dataset_names() -> List[str]:
    """
    get all known dataset names that is supported by this version of dcdataset
    Returns:
        a list of known dataset names
    """
    return [dataset for dataset in dataset_name_dataset_class_map.keys()]


def get_dcdataset_version() -> str:
    """
    get current dcdataset version
    Returns:
        current version
    """
    version = None
    with open(join(pardir, "README.md"), "r") as fh:
        for line in fh.readlines():
            if "Version" in line:
                version = line.split(":")[1].strip().rstrip('\n')

    return version
