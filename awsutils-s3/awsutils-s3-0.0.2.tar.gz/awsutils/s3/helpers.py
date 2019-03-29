def mb_to_bytes(mb):
    """Convert Megabytes value to bytes."""
    return mb * 1024 * 1024


class S3Helpers:
    def __init__(self, transfer_mode, chunk_size, multipart_threshold):
        """
        AWS CLI S3 uploader.

        :param transfer_mode: Upload/download mode
        :param chunk_size: Size of chunk in multipart upload in MB
        :param multipart_threshold: Minimum size in MB to upload using multipart.
        """
        self.transfer_mode = transfer_mode
        self.chunk_size = mb_to_bytes(chunk_size)
        self.multipart_threshold = mb_to_bytes(multipart_threshold)

    def _upload_single_part(self, local_path, remote_path):
        """
        Upload a file or folder to an S3 bucket in a single part.

        :param local_path: Path to file on local disk
        :param remote_path: S3 key, aka remote path relative to S3 bucket's root
        """
        pass

    def _upload_multi_part(self, local_path, remote_path):
        """
        Upload a file or folder to an S3 bucket in multiple parts.

        :param local_path: Path to file on local disk
        :param remote_path: S3 key, aka remote path relative to S3 bucket's root
        """
        pass

    def _upload_needed(self, local_path, remote_path):
        """
        Determine weather a file needs to be uploaded to S3.

        :param local_path: Path to file on local disk
        :param remote_path: S3 key, aka remote path relative to S3 bucket's root
        """
        pass

    def _download_needed(self, local_path, remote_path):
        """
        Determine weather a file needs to be download from S3.

        :param local_path: Path to file on local disk
        :param remote_path: S3 key, aka remote path relative to S3 bucket's root
        """
        pass

    def _multi_part_needed(self, local_path):
        """
        Determine weather a multi-part file upload is needed

        :param local_path: Path to file on local disk
        """
        pass
