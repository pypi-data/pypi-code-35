from photospicker.exception.uploader_exception import UploaderException
from photospicker.uploader.abstract_uploader import AbstractUploader
from dropbox.dropbox import Dropbox
from dropbox.exceptions import ApiError
from dropbox.files import DeleteError
import re


class DropboxUploader(AbstractUploader):
    """Upload picked photo to Dropbox"""

    def __init__(self, api_token, folder_name='photos-picker'):
        """
        Constructor

        :param str api_token: Dropbox api token
        :param str folder_name: Dropbox folder name
        """
        super(DropboxUploader, self).__init__('/' + folder_name)

        if not re.match('^/[A-Za-z0-9._-]+$', self._path):
            raise UploaderException(
                UploaderException.INVALID_DIR_NAME,
                "Invalid dir name {dirname}".format(dirname=self._path)
            )

        self._dbx = Dropbox(api_token)

    def initialize(self):
        """Check name and clear remote directory"""
        # Clear application directory
        try:
            self._dbx.files_delete_v2(self._path)
        except ApiError as e:
            if not isinstance(e.error, DeleteError) \
                    or not e.error.is_path_lookup():
                raise e

    def upload(self, binary, original_filename):
        """
        Upload or copy files to destination

        :param str binary           : binary data to upload
        :param str original_filename: original file name
        """
        # Upload file
        path = "{root_dir}/{photo_name}".format(
            root_dir=self._path,
            photo_name=self._build_filename(original_filename)
        )
        self._dbx.files_upload(binary, path)
