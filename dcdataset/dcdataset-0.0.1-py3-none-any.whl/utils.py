import gzip
import hashlib
import os
import tarfile
import zipfile
from os.path import exists, dirname, splitext


def download_url_if_not_exits(url, dataset_local_dir, md5=None) -> bool:
    """Download a file from a url and place it in dataset_local_dir
    if the file is not existed in dataset_local_dir

    Args:
        url (str): URL to download file from
        dataset_local_dir (str): Directory to place downloaded file in,
            typically, top_level_data_dir/dataset_name
        md5 (str): MD5 checksum of the download. If None, do not check

    Returns:
        indicate if download is successful
    """
    from six.moves import urllib

    filename = os.path.basename(url)
    fpath = os.path.join(dataset_local_dir, filename)

    if not exists(dataset_local_dir):
        os.makedirs(dataset_local_dir)

    # downloads file
    if os.path.isfile(fpath) and (check_integrity(fpath, md5) if md5 is not None else True):
        print('File is already downloaded and verified: ' + fpath)
    else:
        try:
            print('Downloading ' + url + ' to ' + fpath)
            urllib.request.urlretrieve(
                url, fpath
            )
        except OSError:
            if url[:5] == 'https':
                url = url.replace('https:', 'http:')
                print('Failed download. Trying https -> http instead.'
                      ' Downloading ' + url + ' to ' + fpath)
                try:
                    urllib.request.urlretrieve(
                        url, fpath
                    )
                except:
                    return False
            else:
                return False

    return True


def check_integrity(fpath:str, md5=None):
    if md5 is None:
        return True
    if not os.path.isfile(fpath):
        return False
    md5o = hashlib.md5()
    with open(fpath, 'rb') as f:
        # read in 1MB chunks
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            md5o.update(chunk)
    md5c = md5o.hexdigest()
    if md5c != md5:
        return False
    return True


def extract_gzip(file_path: str, remove_finished: bool = True) -> None:
    """
    extract gzip file from file_path to file_path
    Args:
        file_path: place of .gz file
        remove_finished: remove original compressed file

    Returns:

    """
    print('Extracting {}'.format(file_path))
    with open(file_path.replace('.gz', ''), 'wb') as out_f, \
            gzip.GzipFile(file_path) as zip_f:
        out_f.write(zip_f.read())
    if remove_finished:
        os.remove(file_path)


def extract_tar_gz(file_path: str, remove_finished: bool = True) -> None:
    """
    extract tar.gz file from file_path to directory of file_path
    Args:
        file_path: place of .tar.gz file
        remove_finished: remove original compressed file

    Returns:

    """
    tar = tarfile.open(file_path, "r:gz")
    tar.extractall(path=dirname(file_path))
    tar.close()
    if remove_finished:
        os.remove(file_path)


def extract_zip(file_path: str, remove_finished: bool = True):
    """
        extract .zip file from file_path to directory of file_path
        Args:
            file_path: place of .zip file
            remove_finished: remove original compressed file

        Returns:

        """
    zip_ref = zipfile.ZipFile(file_path, 'r')
    zip_ref.extractall(dirname(file_path))
    zip_ref.close()
    if remove_finished:
        os.remove(file_path)


def extract_compressed_file(file_path: str, remove_finished: bool = True) -> None:
    """
    extract all supported compressed file to its current directory (dirname(file_path))
    Args:
        file_path: place of compressed
        remove_finished: remove original compressed file

    Returns:

    """
    print(f"Extracting {file_path}")
    file_name, extension = splitext(file_path)
    unknown_extension = None

    if extension == '.zip':
        extract_zip(file_path, remove_finished)
    elif extension == '.gz':
        _, second_extension = splitext(file_name)
        if second_extension == '.tar':
            extract_tar_gz(file_path, remove_finished)
        elif second_extension == '':
            extract_gzip(file_path, remove_finished)
        else:
            unknown_extension = extension + second_extension
    else:
        unknown_extension = extension

    if unknown_extension is not None:
        print(f"cannot extract compressed file with extenstion {unknown_extension}")
