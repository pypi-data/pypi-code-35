# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Context manager that wraps an AutoML run context."""
from typing import Any, cast, Optional, Callable
from abc import ABC, abstractmethod
from contextlib import contextmanager
import os
import pickle
import tempfile

from .onnx_convert import OnnxConverter


class AutoMLAbstractRunContext(ABC):
    """Wrapper class for an AutoML run context."""

    def __init__(self):
        """Initialize the run context wrapper."""
        self._run_id = None     # type: Optional[str]

    @abstractmethod
    def _get_run_internal(self):
        """Retrieve the run context. Must be overridden by subclasses."""
        raise NotImplementedError

    @property
    def run_id(self) -> str:
        """
        Get the run id associated with the run wrapped by this run context. The run id is assumed to be immutable.

        :return: the run id
        """
        if self._run_id is None:
            with self.get_run() as run:
                self._run_id = run.id
        return cast(str, self._run_id)

    @contextmanager
    def get_run(self):
        """
        Yield a run context.

        Wrapped by contextlib to convert it to a context manager. Nested invocations will return the same run context.
        """
        yield self._get_run_internal()

    def save_model_output(self, fitted_pipeline: Any, remote_path: str) -> None:
        """
        Save the given fitted model to the given path using this run context.

        :param fitted_pipeline: the fitted model to save
        :param remote_path: the path to save to
        """
        self._save_model(fitted_pipeline, remote_path, self._save_python_model)

    def save_onnx_model_output(self, onnx_model: object, remote_path: str) -> None:
        """
        Save the given onnx model to the given remote path using this run context.

        :param onnx_model: the onnx model to save
        :param remote_path: the path to save to
        """
        self._save_model(onnx_model, remote_path, self._save_onnx_model)

    def _save_model(self, model_object: Any, remote_path: str,
                    serialization_method: Callable[..., Optional[Any]]) -> None:
        model_output = None
        try:
            model_output = tempfile.NamedTemporaryFile(mode='wb+', delete=False)
            serialization_method(model_object, model_output)
            with(open(model_output.name, 'rb')):
                with self.get_run() as run_object:
                    run_object.upload_file(remote_path, model_output.name)
        finally:
            if model_output is not None:
                model_output.close()
                os.unlink(model_output.name)

    def _save_onnx_model(self, model_object: Any, model_output: Any) -> None:
        OnnxConverter.save_onnx_model(model_object, model_output.name)

    def _save_python_model(self, model_object: Any, model_output: Any) -> None:
        with(open(model_output.name, 'wb')):
            pickle.dump(model_object, model_output)
            model_output.flush()
