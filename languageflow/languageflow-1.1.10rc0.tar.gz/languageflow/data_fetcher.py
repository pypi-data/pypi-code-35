import os
import shutil
from tabulate import tabulate
from languageflow.datasets import REPO
from languageflow.file_utils import cached_path, CACHE_ROOT
from pathlib import Path
import zipfile


class DataFetcher:
    @staticmethod
    def download_data(data):
        if data not in REPO:
            print(f"No matching distribution found for '{data}'")
            return

        filepath = REPO[data]["filepath"]
        cache_dir = REPO[data]["cache_dir"]
        filepath = Path(CACHE_ROOT) / cache_dir / filepath
        if Path(filepath).exists():
            print(f"Data is already existed: '{data}' in {filepath}")
            return

        if data == "VNESES":
            url = "https://www.dropbox.com/s/m4agkrbjuvnq4el/VNESEcorpus.txt?dl=1"
            cached_path(url, cache_dir=cache_dir)
            shutil.move(Path(CACHE_ROOT) / cache_dir / "VNESEcorpus.txt?dl=1",
                        Path(CACHE_ROOT) / cache_dir / filepath)

        if data == "VNTQ_SMALL":
            url = "https://www.dropbox.com/s/b0z17fa8hm6u1rr/VNTQcorpus-small.txt?dl=1"
            cached_path(url, cache_dir=cache_dir)
            shutil.move(Path(CACHE_ROOT) / cache_dir / "VNTQcorpus-small.txt?dl=1",
                        Path(CACHE_ROOT) / cache_dir / filepath)

        if data == "VNTQ_BIG":
            url = "https://www.dropbox.com/s/t4z90vs3qhpq9wg/VNTQcorpus-big.txt?dl=1"
            cached_path(url, cache_dir=cache_dir)
            shutil.move(Path(CACHE_ROOT) / cache_dir / "VNTQcorpus-big.txt?dl=1",
                        Path(CACHE_ROOT) / cache_dir / filepath)

        if data == "VNTC":
            url = "https://www.dropbox.com/s/4iw3xtnkd74h3pj/VNTC.zip?dl=1"
            cached_path(url, cache_dir=cache_dir)
            filepath = Path(CACHE_ROOT) / cache_dir / "VNTC.zip?dl=1"
            cache_folder = Path(CACHE_ROOT) / cache_dir
            zip = zipfile.ZipFile(filepath)
            zip.extractall(cache_folder)
            os.remove(filepath)

    @staticmethod
    def list():
        datasets = []
        for key in REPO:
            name = key
            type = REPO[key]["type"]
            license = REPO[key]["license"]
            year = REPO[key]["year"]
            directory = REPO[key]["cache_dir"]
            datasets.append([name, type, license, year, directory])

        print(tabulate(datasets,
                       headers=["Name", "Type", "License", "Year", "Directory"],
                       tablefmt='orgtbl'))
