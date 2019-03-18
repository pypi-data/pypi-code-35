import os
import re
import tempfile
from typing import Tuple

from google.cloud import storage

from ...base import DataNode
from ...utils import deprecated


class GcsDataNode(DataNode):
    @deprecated
    def _to_tempfile(self, content: str) -> str:

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(content)
            abs_path = f.name

        return abs_path

    def _get_blob_meta(self, gs_uri: str) -> Tuple[str, str]:
        """Extract `bucketname` and `blob_path` from an gs-uri
        Return:
            tuple: (bucketname, blob_path)
        """
        try:
            matched = re.search(r"gs:\/\/(?P<host>[^:\/ ]+)\/(.+)", gs_uri)
            bucketname, blob_path = matched.group(1), matched.group(2)
        except Exception as err:
            print(
                (
                    "Invalid URI value, should match the pattern:"
                    fr' `gs:\/\/(?P<host>[^:\/ ]+)\/(.+)`, got: "{gs_uri}"'
                )
            )

            raise err

        return (bucketname, blob_path)

    def _get_blob(self, gs_uri: str) -> storage.Blob:
        """Retrieve blob object by `google.cloud.storage` api"""

        bucketname, blob_path = self._get_blob_meta(gs_uri)
        client = storage.Client()
        bucket = client.get_bucket(bucketname)

        blob = bucket.blob(blob_path)

        return blob

    def copy_to(self, dest_node: "GcsDataNode"):

        from google.cloud import storage

        client = storage.Client()

        src: str = self.data.source.fullpath
        dest: str = dest_node.data.source.fullpath

        src_bucket_name, src_blob_path = self._get_blob_meta(src)
        dest_bucket_name, dest_blob_path = self._get_blob_meta(dest)

        src_bucket = client.get_bucket(src_bucket_name)
        dest_bucket = client.get_bucket(dest_bucket_name)

        src_blob = src_bucket.blob(src_blob_path)

        src_bucket.copy_blob(src_blob, dest_bucket, new_name=dest_blob_path)

    def load(self, fullpath: str = "", mode: str = "wb") -> str:
        """Download data from gcs to local temp file by `google.cloud.storage` api

        Params:
            mode: mode for operating temp files, default: 'w'.
            fullpath: full file path on gcs, should starts with `gs://...`, optional.
        """

        fullpath: str = fullpath or self.data.source.fullpath

        blob = self._get_blob(fullpath)

        with tempfile.NamedTemporaryFile(mode=mode, delete=False) as f:
            blob.download_to_file(f)
            abs_path = f.name

        return abs_path

    def dump(
        self, path: str = None, content: str = "", fullpath: str = "", mode: str = "w"
    ) -> None:
        """Dump data to gcs through `google.cloud.storage` api.

        Params:
            bucket_name: to construct client api of google cloud storage service.
            path: dump data from a source(local) file path.
                  NOTE: Instead of dumping directory,
                        archive the directory into a single file, then dump.
            mode: mode for operating temp files, default: 'w'.
            content: if local `path` is not provided, dump content into tempfile, then dump to gcs.
            fullpath: full file path on gcs, should starts with `gs://...`, optional.
        Return:
            None
        """

        # If `path` is provided, ignore `content` parameter.
        if path:
            if not os.path.isfile(path):
                raise ValueError(f'Invalid file `path`, got: "{path}"')

        else:
            with tempfile.NamedTemporaryFile(mode=mode, delete=False) as f:
                f.write(content)
                path = f.name

        fullpath: str = fullpath or self.data.source.fullpath

        blob = self._get_blob(fullpath)

        blob.upload_from_filename(path)
