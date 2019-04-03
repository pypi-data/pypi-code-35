import re
import yaml
import shutil
import uuid
import magic
import requests
from tqdm import tqdm
import json
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from pathlib import Path
import logging
from tinydb import Query, TinyDB

from moderage.experiment import Experiment


class ModeRage():

    def __init__(self, config_file=None):

        self._server_config_defaults = {
            'host': 'localhost',
            'port': '8118',
        }

        self._local_config_defaults = {

        }

        self._logger = logging.getLogger("Mode Rage client")

        self._logger.info('Attempting to load Mode Rage config from  ./.mrconfig')

        mode, config = self._load_config(config_file)

        if mode == 'server':
            self._host = config['host']
            self._port = config['port']
            self._root_url = '%s:%s/v0/experiment' % (self._host, self._port)
            self._save = self._save_server
            self._load = self._load_server

        # Will save and load from local cache and use tinydb for file lookup
        if mode == 'local':
            self._save = self._save_local
            self._load = self._load_local

        self._cache_location = config['cache_location']
        if not self._cache_location.exists():
            self._cache_location.mkdir()

        self._logger.debug('Cache location: [%s]' % str(self._cache_location))

    def _load_config(self, config_location=None):
        """
        Looks for .mrconfig in local directory and loads settings if present
        """

        local_defaults = {
            'cache_location': Path.home().joinpath('.moderage')
        }

        # Use default config location if none is available
        if not config_location:
            config_location = './.mrconfig'

        try:
            with open(config_location, 'r') as config_file:
                config = yaml.safe_load(config_file)

                mode = config['mode']

                cache_location = Path(config['cache_location'] if 'cache_location' in config \
                    else local_defaults['cache_location'])

                # expand any tilde '~' characters to full directory
                cache_location = cache_location.expanduser()

                if mode == 'server':
                    server_config = config['server'] if 'server' in config else self._server_config_defaults
                    return 'server', {**server_config, 'cache_location': cache_location}
                elif mode == 'local':
                    local_config = config['local'] if 'local' in config else self._local_config_defaults
                    return 'local', {**local_config, 'cache_location': cache_location}

        except IOError as e:
            self._logger.info('Cannot load .mrconfig file. Using defaults.', e)

        return 'local', local_defaults

    def _save_local(self, meta_category, meta, files=None, parents=None):
        """
        Save using local tinydb and local cache only
        """

        meta_category_location = self._cache_location.joinpath(meta_category)

        if not meta_category_location.exists():
            meta_category_location.mkdir()

        db_location = meta_category_location.joinpath('db.json')
        db = TinyDB(str(db_location))

        id = str(uuid.uuid4())

        cache_location = meta_category_location.joinpath(id)
        if not cache_location.exists():
            cache_location.mkdir()

        # Move all the files into the cache
        file_info_list = []
        if files is not None:
            for file in files:
                file_info = {}
                file_info['id'] = str(uuid.uuid4())
                file_info['caption'] = file['caption']
                file_info['success'] = True
                file_info['contentType'] = file['contentType']

                # Save the filename and strip the directory information
                file_info['filename'] = Path(file['filename']).name

                # Save the location of the file in the filesystem
                location = str(cache_location.joinpath(file_info['id']))
                shutil.copy(file['filename'], location)
                file_info['location'] = location
                file_info_list.append(file_info)

        entry = {
            'id': id,
            'parents': parents,
            'meta': meta,
            'files': file_info_list
        }

        db.insert(entry)

        return Experiment(entry, self, cache_location=cache_location)


    def _save_server(self, meta_category, meta, parents=None, files=None):
        """
        Save using moderage server
        """

        parents = [{'id': str(p['id']), 'metaCategory': p['metaCategory']} for p in parents] if parents is not None else []


        create_payload = {
            'metaCategory': meta_category,
            'meta': meta,
            'parents': parents
        }


        create_response = requests.post('%s/create' % self._root_url, json=create_payload)

        assert create_response.status_code == 201, create_response.json()

        experiment = create_response.json()
        id = experiment['id']

        if files:

            files = files if files is not None else []
            file_info_list = []
            for file in files:
                file_info = dict.copy(file)
                file_info['filename'] = Path(file['filename']).name
                file_info_list.append(file_info)

            file_info_payload = {
                'files': file_info_list
            }

            multipart_payload = [('files', (Path(f['filename']).name, open(f['filename'], 'rb'))) for f in files]
            multipart_payload.append(('file_metadata', (None, json.dumps(file_info_payload))))
            multipart_encoder = MultipartEncoder(multipart_payload)

            self._logger.info('Experiment saved with id [%s]' % id)
            self._logger.info('Uploading %d files to experiment [%s]' % (len(files), id))

            # Set up a progress bar for upload progress
            with(tqdm(total=multipart_encoder.len, ncols=100, unit="bytes", bar_format="{l_bar}{bar}|")) as progress_bar:
                last_bytes_read = 0

                # Callback for progress to be output by tqdm progress bar
                def _upload_progress(monitor):
                    nonlocal last_bytes_read
                    progress_diff = monitor.bytes_read - last_bytes_read
                    progress_bar.update(progress_diff)
                    last_bytes_read = monitor.bytes_read

                multipart_monitor = MultipartEncoderMonitor(multipart_encoder, _upload_progress)

                upload_response = requests.post(
                    '%s/%s/%s/uploadFiles' % (self._root_url, meta_category, id),
                    data=multipart_monitor,
                    headers={'Content-Type': multipart_encoder.content_type}
                )

            assert upload_response.status_code == 200, upload_response.json()

            experiment = upload_response.json()

        return Experiment(experiment, self)


    def save(self, meta_category, meta, parents=None, files=None):
        """
        :param parents: list of objects containing the id and category of experiments that this experiment relies on

        for example:

        {
            "id": "05c0581c-7ece-4cad-a26f-0e415ea1b01d",
            "metaCategory": "grid_world"
        }

        :param meta_category: A category name for this experiment, or this dataset
        :param meta: meta information for this experiment or dataset
        :param files: A list of files and metadata associated with this experiment or dataset

        Files must be in the following format:

        [
            "filename": "./path/to/my/file.xyz",
            "caption": "This is a description of my file"
        ]

        :return:
        """

        self._logger.info('Saving data to category %s' % meta_category)

        if files is not None:
            files = [self._process_file_info(file) for file in files]

        return self._save(meta_category, meta, parents=parents, files=files)

    def load(self, id, meta_category, ignore_files=False):
        """
        Load an experiment
        :param id: the id of the experiment
        :param meta_category: the category of the experiment
        :param ignore_files: If this is set to true, the files will not be downloaded and cached
        """

        self._logger.info('Loading data with id [%s] in category [%s]' % (id, meta_category))

        return self._load(id, meta_category, ignore_files)

    def _load_local(self, id, meta_category, ignore_files=False):
        """
        Load using local tinydb and local cache only
        """

        meta_category_location = self._cache_location.joinpath(meta_category)

        db_location = meta_category_location.joinpath('db.json')
        db = TinyDB(str(db_location))

        ExperimentQuery = Query()
        search_result = db.search(ExperimentQuery.id == id)
        assert len(search_result) == 1

        experiment = search_result[0]

        experiment_file_location = meta_category_location.joinpath(id)

        return Experiment(experiment, self, cache_location=experiment_file_location)



    def _load_server(self, id, meta_category, ignore_files=False):
        """
        Load from moderage server
        """

        get_response = requests.get('%s/%s/%s' % (self._root_url, meta_category, id))
        assert get_response.status_code == 200, get_response.json()
        experiment = get_response.json()

        experiment_file_location = self._cache_location.joinpath(meta_category, id)

        if not experiment_file_location.exists():
            experiment_file_location.mkdir(parents=True)

        if not ignore_files and 'files' in experiment:

            self._logger.info('%d files found' % len(experiment['files']))

            # download the files from their uris
            for file_info in experiment['files']:

                cached_filename = experiment_file_location.joinpath(file_info['id'])

                # If we have not cached the file already, download it and move it to the cache directory
                if not cached_filename.exists():
                    self._logger.info('Downloading file: %s' % file_info['filename'])
                    self._download_file(file_info, str(cached_filename))
                else:
                    self._logger.info('File found in cache: %s' % file_info['filename'])

        return Experiment(experiment, self, cache_location=experiment_file_location)


    def _download_file(self, file_info, cached_filename):

        location = file_info['location']
        startswith = location.startswith('https://s3.amazonaws.com')
        if startswith:
            import boto3
            import botocore
            # Download the file
            s3 = boto3.client('s3')

            m = re.search('https://s3.amazonaws.com/(?P<bucket>\w+)/(?P<key>.+)', location)

            bucket = m.group('bucket')
            key = m.group('key')

            file_size = s3.head_object(Bucket=bucket, Key=key)['ContentLength']

            with(tqdm(total=file_size, ncols=100, unit="bytes", bar_format="{l_bar}{bar}|")) as progress_bar:

                # Callback for progress to be output by tqdm progress bar
                def _download_progress(chunk):
                    progress_bar.update(chunk)

                s3.download_file(bucket, key, cached_filename, Callback=_download_progress)

        elif location.startswith('http'):

            # Download the file
            with requests.get(location) as r:
                with open(cached_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)

    def _process_file_info(self, file):
        """
        Get the mime type of the file
        :param file:
        :return:
        """
        file['contentType'] = magic.from_file(file['filename'], True)

        return file
