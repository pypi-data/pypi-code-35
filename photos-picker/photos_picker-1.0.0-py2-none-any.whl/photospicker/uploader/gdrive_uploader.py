from io import BytesIO
from photospicker.exception.uploader_exception import UploaderException
from photospicker.uploader.abstract_uploader import AbstractUploader
from pydrive.drive import GoogleDrive
import re


class GDriveUploader(AbstractUploader):
    """Upload picked photo to Google Drive"""

    def __init__(self, gauth, folder_name='photos-picker'):
        """
        Constructor

        :param pydrive.auth.GoogleAuth gauth: GoogleAth authentified instance
        :param str folder_name: Google Drive folder name
        """
        super(GDriveUploader, self).__init__(folder_name)

        if not re.match('^[A-Za-z0-9._-]+$', self._path):
            raise UploaderException(
                UploaderException.INVALID_DIR_NAME,
                "Invalid dir name {dirname}".format(dirname=self._path)
            )

        self._gdrive = GoogleDrive(gauth)
        self._folder = None

    def initialize(self):
        """Clear remote directory"""
        query = "mimeType = 'application/vnd.google-apps.folder'"\
                + " and title = '{dir}' and trashed=false"
        query = query.format(dir=self._path)
        folders = self._gdrive.ListFile({"q": query}).GetList()

        count = len(folders)

        # Remove old folder if exists
        if count == 0:
            # Create folder
            folder_metadata = {
                'title': self._path,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            self._folder = self._gdrive.CreateFile(folder_metadata)
            self._folder.Upload()
        elif count == 1:
            self._folder = folders[0]
            # Remove previously uploaded files
            query = "'{folder_id}' in parents and trashed=false"
            files = self._gdrive.ListFile(
                {"q": query.format(folder_id=self._folder['id'])}
            ).GetList()
            for file_to_delete in files:
                file_to_delete.Delete()
        else:
            raise UploaderException(
                UploaderException.MANY_DIRS,
                "Many dirs named {dir}; can't continue".format(dir=self._path)
            )

    def upload(self, binary, original_filename):
        """
        Upload or copy files to destination

        :param str binary           : binary data to upload
        :param str original_filename: original file name
        """
        filename = self._build_filename(original_filename)
        gfile = self._gdrive.CreateFile({
            'title': filename,
            "parents": [{"kind": "drive#fileLink", "id": self._folder['id']}]
        })
        gfile.content = BytesIO(binary)
        gfile.Upload()
