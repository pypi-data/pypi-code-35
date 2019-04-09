from os.path import join, basename

from dcdataset.datasets import AbstractDataset
from dcdataset.utils import download_url_if_not_exits, extract_compressed_file


class IMDBReview(AbstractDataset):
    url = "http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
    extracted_files = [
        join("aclimdb", "train"),
        join("aclimdb", "test"),
        join("aclimdb", "imdbEr.txt"),
        join("aclimdb", "imdb.vocab"),
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

        success = download_url_if_not_exits(self.url, destination_dir)
        if not success:
            return False

        extract_compressed_file(join(destination_dir, basename(self.url)), True)

        return True
