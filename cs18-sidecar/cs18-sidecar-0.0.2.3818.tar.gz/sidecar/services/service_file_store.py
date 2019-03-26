import os
import pathlib

from sidecar.cloud_logger.file_logger import ICloudLogger, LogPath
from sidecar.services.service_logger import ServiceLogger


@ServiceLogger.wrap
class ServiceFileStore:
    def __init__(self,
                 file_logger: ICloudLogger):
        self._file_logger = file_logger
        ServiceLogger.set_logger(file_logger)

    def save_execution_output(self, name: str, cmd: str, output: bytes):
        path = os.path.join(LogPath, name)
        if not os.path.exists(path):
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(path, cmd), "wb") as f:
            f.write(output)
