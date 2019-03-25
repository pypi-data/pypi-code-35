# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""**AzureMLflowArtifactRepository** provides a class to up/download artifacts to storage backends in Azure."""

import os

from mlflow.entities import FileInfo
from mlflow.store.artifact_repo import ArtifactRepository
from mlflow.tracking.fluent import _get_or_start_run

from azureml._restclient.constants import RUN_ORIGIN


class AzureMLflowArtifactRepository(ArtifactRepository):
    """Define how to upload (log) and download potentially large artifacts from different storage backends."""

    def __init__(self, artifact_uri, store):
        """
        Construct an AzureMLflowArtifactRepository object.

        This object is used with any of the functions called from mlflow or from
        the client which have to do with artifacts.

        :param artifact_uri: Azure URI. This URI is never used within the object,
        but is included here, as it is included in ArtifactRepository as well.
        :type artifact_uri: str
        :param store: Store in which the run associated with this ArtifactRepository
        is located. The store is used to retreive the workspace object.
        :type store: AzureMLflowStore
        """
        self._artifact_uri = artifact_uri
        self._store = store

        run_uuid = _get_or_start_run().info.run_uuid
        self._amlflow_run = self._store._get_amlflow_run(run_uuid)
        self._container = self._amlflow_run.container

    def log_artifact(self, local_file, artifact_path=None):
        """
        Log a local file as an artifact.

        Optionally takes an ``artifact_path``, which renames the file when it is
        uploaded to the ArtifactRepository.

        :param local_file: Absolute or relative path to the artifact locally.
        :type local_file: str
        :param artifact_path: Path to a file in the AzureML run's outputs, to where
        the artifact is uploaded.
        :type artifact_path: str
        """
        dest_path = self._normalize_slashes(
            self._build_dest_path(
                local_file,
                artifact_path
            )
        )

        self._amlflow_run.aml_run._client.artifacts.upload_artifact(
            local_file,
            RUN_ORIGIN,
            self._container,
            dest_path
        )

    def log_artifacts(self, local_dir, artifact_path=None):
        """
        Log the files in the specified local directory as artifacts.

        Optionally takes an ``artifact_path``, which specifies the directory of
        the AzureML run under which to place the artifacts in the local directory.

        :param local_dir: Directory of local artifacts to log.
        :type local_dir: str
        :param artifact_path: Directory within the run's artifact directory in
        which to log the artifacts.
        :type artifact_path: str
        """
        dest_path = self._normalize_slashes(
            self._build_dest_path(
                local_dir,
                artifact_path
            )
        )
        local_dir = self._normalize_slash_end(local_dir)
        dest_path = self._normalize_slash_end(dest_path)

        self._amlflow_run.aml_run._client.artifacts.upload_dir(
            local_dir,
            RUN_ORIGIN,
            self._container,
            lambda fpath: dest_path + fpath[len(local_dir):]
        )

    def list_artifacts(self, path):
        """
        Return all the artifacts for this run_uuid directly under path.

        If path is a file, returns an empty list. Will error if path is neither a
        file nor directory. Note that list_artifacts will not return valid
        artifact sizes from Azure.

        :param path: Relative source path that contain desired artifacts
        :type path: str

        :return: List of artifacts as FileInfo listed directly under path.
        """
        # get and filter by paths

        artifacts = []
        for file_path in self._amlflow_run.aml_run._client.artifacts.get_file_paths(
            RUN_ORIGIN,
            self._container
        ):
            if path is None or file_path[:len(path)] == path:
                artifacts.append(file_path)

        # create fileinfos
        fileInfos = []
        for artifact in artifacts:
            fileInfos.append(FileInfo(
                path=artifact,
                is_dir=False,
                file_size=-1  # TODO: artifact size retrieval is not supported in Azure
            ))

        return fileInfos

    def download_artifacts(self, artifact_path):
        """
        Download an artifact file or directory to a local directory if applicable.

        Returns a local path for it. The caller is responsible for managing the
        lifecycle of the downloaded artifacts. Downloaded artifacts are stored
        relative to the returned path with the same relative path they are
        requested from the artifact repository.

        :param artifact_path: Relative source path to the desired artifact.
        :type artifact_path: str
        :return: Full path to the directory which contains the path to the desired
        artifact.
        """
        artifact_path = artifact_path

        # list all artifacts which have artifact_path as prefix
        artifacts = []
        for file in self._amlflow_run.aml_run._client.artifacts.get_file_paths(RUN_ORIGIN, self._container):
            if file[:len(artifact_path)] == artifact_path:
                artifacts.append(file)

        for artifact in artifacts:
            self._download_file(artifact, artifact)

        return os.path.abspath(".")

    def _download_file(self, remote_file_path, local_path):
        """
        Download the file at the specified relative remote path and save it at the specified local path.

        :param remote_file_path: Source path to the remote file, relative to the
        root directory of the artifact repository.
        :type remote_file_path: str
        :param local_path: The path to which to save the downloaded file.
        :type local_path: str
        """
        self._amlflow_run.aml_run._client.artifacts.download_artifact(
            RUN_ORIGIN,
            self._container,
            remote_file_path,
            local_path
        )

    @staticmethod
    def _build_dest_path(local_path, artifact_path):
        return artifact_path if artifact_path else os.path.basename(local_path)

    @staticmethod
    def _normalize_slashes(path):
        return "/".join(path.split("\\"))

    @staticmethod
    def _normalize_slash_end(path):
        return path if path[-1] == "/" else path + "/"
