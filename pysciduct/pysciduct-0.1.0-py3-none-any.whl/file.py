from sciduct.sciduct_service import SciDuctServiceClientBase
import requests
import json
from urllib.parse import urljoin
from jsonschema import validate

class FileService(SciDuctServiceClientBase):
    """File Service"""

    schema = {
        'type': 'object',
        'properties': {
            'name': { 'type': 'string' }
        },
        'required': ['name']
    }

    __service_name__ = "file"

    def initialize(self):
        """Initialize the user's home on the File Service.
        """
        url = urljoin(self.url, 'initialize')
        self._get(url, accept='*/*')

    @SciDuctServiceClientBase.rpc('ls')
    def list(self, path):
        """List the contents of directory at path.

        :param path: Path to the directory.
        :type path: str
        :returns: A list of all files and directories in path.
        """
        if type(path) is not str:
            raise TypeError("path must be a path string")

        return [path]

    @SciDuctServiceClientBase.rpc('create')
    def create(self, to_create, path):
        """
        Create file metadata

        :param to_create: Metadata for the file to be created.  This can be
            either a dict or a json str.
        :type to_create: dict or str
        :param path: Path to directory where file will be created.
        :type path: str
        :returns: A dictionary representing the file just created.
        """
        # Check to_create type
        if type(to_create) is dict:
            pass
        elif type(to_create) is str:
            to_create = json.loads(to_create)
        else:
            # If not None, but also not an expected type, raise a TypeError.
            raise TypeError("to_create must be a json dictionary or a json string")

        validate(to_create, self.schema)

        return [to_create, path]

    @SciDuctServiceClientBase.rpc('delete')
    def delete(self, id_or_path, recursive=False):
        """
        Delete file on file service.

        :param id_or_path: File id or path to file on the file service to be
            deleted.
        :type id_or_path: str
        :param recursive: Delete recursively if True. (default False)
        :type recursive: bool
        :returns: True if file is deleted; False otherwise.
        """
        if type(id_or_path) is not str:
            raise TypeError("id_or_path must be a string containing the id or path"
                            "of the file")

        # TODO: In the future we should wrap this with a try/except and determine
        # what went wrong, i.e. raise ValueError when id_or_path is invalid.
        return [id_or_path, recursive]

    def put(self, path, data):
        """
        Upload file data to a file on the file service.

        :param path: Path to the file on the file service to be populated.
        :type path: str
        :param data: Data to be uploaded.
        :type data: file
        """
        url = urljoin(self.url, 'file' + path)

        headers = {
            'authorization': str(self.session.token)
        }

        requests.put(url, headers=headers, data=data)

    @SciDuctServiceClientBase.rpc('patch')
    def patch(self, id_or_path, *patch_set):
        """
        Patch file metadata.

        :param id_or_path: File id or path to file on the file service to be
            patched.
        :type id_or_path: str
        :param \*patch_set: List of patches to be applied to the file.  These
            patches can be either json str or dict.  See file service
            documentation for patch format.
        :type \*patch_set: list of json str or dict
        :returns: Metadata for file after patch is applied.
        """
        if type(id_or_path) is not str:
            raise TypeError("id_or_path must be a string containing the id or path"
                            "of the file")

        # This is to support intermixed strings and dictionaries of json.  This
        # could raise ValueErrors or TypeErrors
        mapper = lambda patch: patch if type(patch) is dict else json.loads(patch)
        patch_set = list(map(mapper, patch_set))

        return [id_or_path, patch_set]

    @SciDuctServiceClientBase.rpc('move')
    def move(self, source, destination):
        """
        Move file at source to destination.

        :param source: File or container to be moved.
        :type source: str
        :param destination: Container where source will be moved to.
        :type destination: str
        :returns: Metadata for file after move.
        """
        if type(source) is not str:
            raise TypeError("source must be a path string")

        if type(destination) is not str:
            raise TypeError("destination must be a path string")

        return [source, destination]

    @SciDuctServiceClientBase.rpc('rename')
    def rename(self, source, new_name):
        """
        Rename file.  Note this can be achieved using a patch command.

        :param source: File or container to be renamed.
        :type source: str
        :param new_name: New name for file.
        :type new_name: str
        :returns: Metadata for the renamed file.
        """
        if type(source) is not str:
            raise TypeError("source must be a path string")

        if type(new_name) is not str:
            raise TypeError("New file name must be a string")

        return [source, new_name]

    @SciDuctServiceClientBase.rpc('copy')
    def copy(self, source, destination, recursive = False):
        """
        Copy file at source to destination.

        :param source: File or container to be copied.
        :type source: str
        :param destination: Container where source will be copied to.
        :type destination: str
        :param recursive: Copy recursively if True. (default False)
        :type recursive: bool
        :returns: Metadata for newly copied file.
        """
        if type(source) is not str:
            raise TypeError("source must be a path string")

        if type(destination) is not str:
            raise TypeError("destination must be a path string")

        return [source, destination, recursive]

    def get_meta(self, path):
        """
        Get metadata for file on file service.
        """
        path = 'file' + path
        return self._get(path, accept='application/vsmetadata+json').json()
        

    def get_lines(self, id_or_path):
        """
        Get lines from file on file service.
        
        :param id_or_path: File id or file path on file service.
        :type id_or_path: str
        :returns: An iterator for the lines of the file.
        """
        path = 'file' + id_or_path
        resp = self._get(path, accept='binary/octet-stream', stream=True)

        if resp.status_code is not 200:
            raise ValueError("error reading {0}: {1}".format(id_or_path,
                resp.text))

        return resp.iter_lines()

    def get(self, path):
        return self._get(path).json()

    def get_chunks(self, id_or_path, chunk_size=1):
        """
        Get chunks of bytes from file on file service.
        
        :param id_or_path: File id or file path on file service.
        :type id_or_path: str
        :param chunk_size: Number of bytes per chunk to be read into memory. (default 1)
        :type chunk_size: int
        :returns: An iterator for the chunks of the file.
        """
        path = 'file' + id_or_path
        resp = self._get(path, accept='binary/octet-stream', stream=True)

        if resp.status_code is not 200:
            raise ValueError("error reading {0}: {1}".format(id_or_path,
                resp.text))

        return resp.iter_content(chunk_size=chunk_size)

    @SciDuctServiceClientBase.rpc('find')
    def find(self, root, query, recursive = False):
        """
        Search for files matching query.
        
        :param root: Path to directory where search will be conducted.
        :type root: str
        :param query: Query describing desired files.  See file service
            documentation for details.
        :type query: str
        :param recursive: Search subdirectories if True. (default False)
        :type recursive: bool
        :returns: A list of files matching query.
        """
        return [root, query, recursive]

    @SciDuctServiceClientBase.rpc('chown')
    def chown(self, source, new_owner):
        """
        Change ownership of a file.

        :param source: Path to file.
        :type source: str
        :param new_owner: New owner for the file.
        :type new_owner: str
        :returns: Metadata for file after chown is performed.
        """
        if type(new_owner) is not str:
            raise TypeError("new_owner must be string")

        if type(source) is not str:
            raise TypeError("source must be string")

        return [source, new_owner]
            
    @SciDuctServiceClientBase.rpc('grant')
    def grant(self, source, privilege, users, recursive = False):
        """
        Grant permssisions for a file to a user.

        :param source: Path to file.
        :type source: str
        :param privilege: Privilege to be granted.
        :type privilege: str
        :param users: Users who will receive permission.
        :type users: str
        :param recursive: Grant permissions recursively if True.  (default False)
        :type recursive: bool
        :returns: Metadata for file after granting permission to user.
        """
        if type(users) is not str:
            raise TypeError("users must be string")

        if type(privilege) is not str:
            raise TypeError("privilege must be string")

        if type(source) is not str:
            raise TypeError("source must be string")

        return [privilege, source, users, recursive]

    @SciDuctServiceClientBase.rpc('revoke')
    def revoke(self, source, privilege, users, recursive=False):
        """
        Revoke permssisions for a file from a user.

        :param source: Path to file.
        :type source: str
        :param privilege: Privilege to be revoked.
        :type privilege: str
        :param users: Users who will have their permission revoked.
        :type users: str
        :param recursive: Revoke permissions recursively if True.  (default False)
        :type recursive: bool
        :returns: Metadata for file after permission has been revoked.
        """
        if type(users) is not str:
            raise TypeError("users must be string")

        if type(privilege) is not str:
            raise TypeError("privilege must be string")

        if type(source) is not str:
            raise TypeError("source must be string")

        return [privilege, source, users, recursive]
