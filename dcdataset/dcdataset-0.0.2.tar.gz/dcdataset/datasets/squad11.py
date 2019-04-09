from os.path import basename, splitext, join

from dcdataset.datasets import AbstractDataset
from dcdataset.utils import download_url_if_not_exits, extract_compressed_file


class Squad11(AbstractDataset):
    urls = [
        "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json",
        "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json",
        "http://nlp.stanford.edu/data/glove.840B.300d.zip",
    ]
    files = [
        "train-v1.1.json",
        "dev-v1.1.json",
        "glove.840B.300d.zip",
    ]

    extracted_files = [
        "train-v1.1.json",
        "dev-v1.1.json",
        "glove.840B.300d.txt",
    ]

    def download_to_dir(self, destination_dir: str) -> bool:
        """
        download all the files to the destination_dir
            this will put all the train/test/meta files under destination_dir
        Args:
            destination_dir: local destination directory, toplevel_datadir/dataset_name

        Returns:
            indicates if download is successful
        """
        self.destination_dir = destination_dir

        for url in self.urls:
            success = download_url_if_not_exits(url, destination_dir)
            if not success:
                return False

            _, extension = splitext(url)
            if extension == '.zip':
                extract_compressed_file(join(destination_dir, basename(url)), True)

        return True
