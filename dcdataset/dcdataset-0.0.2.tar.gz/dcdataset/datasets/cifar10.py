from os.path import join

from dcdataset.datasets import AbstractDataset
from dcdataset.utils import download_url_if_not_exits, check_integrity, \
    extract_compressed_file


class CIFAR10(AbstractDataset):
    dataset_info = {}
    base_folder = 'cifar-10-batches-py'
    url = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
    filename = "cifar-10-python.tar.gz"
    tgz_md5 = 'c58f30108f718f92721af3b95e74349a'
    train_list = [
        ['data_batch_1', 'c99cafc152244af753f735de768cd75f'],
        ['data_batch_2', 'd4bba439e000b95fd0a9bffe97cbabec'],
        ['data_batch_3', '54ebc095f3ab1f0389bbae665268c751'],
        ['data_batch_4', '634d18415352ddfa80567beed471001a'],
        ['data_batch_5', '482c414d41f54cd18b22e5b47cb7c3cb'],
    ]

    test_list = [
        ['test_batch', '40351d587109b95175f43aff81a1287e'],
    ]
    meta = {
        'filename': 'batches.meta',
        'key': 'label_names',
        'md5': '5ff9c542aee3614f3951f8cda6e48888',
    }

    extracted_files = [
        join(base_folder, 'data_batch_1'),
        join(base_folder, 'data_batch_2'),
        join(base_folder, 'data_batch_3'),
        join(base_folder, 'data_batch_4'),
        join(base_folder, 'data_batch_5'),
        join(base_folder, 'test_batch'),
        join(base_folder, 'batches.meta'),
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

        success = download_url_if_not_exits(self.url, destination_dir, self.tgz_md5)
        if not success:
            return False

        extract_compressed_file(join(destination_dir, self.filename), True)

        return self._check_integrity()

    def _check_integrity(self) -> bool:
        for fentry in (self.train_list + self.test_list):
            filename, md5 = fentry[0], fentry[1]
            fpath = join(self.destination_dir, self.base_folder, filename)
            if not check_integrity(fpath, md5):
                return False
        return True
