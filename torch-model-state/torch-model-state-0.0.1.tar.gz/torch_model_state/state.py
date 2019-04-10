import json
import logging
import shutil
import typing
from pathlib import Path
from typing import List, Optional

import jsonschema
import torch
import torch.nn as nn
from torch.optim import Optimizer

from .configs import StateConfig


class State:
    with open(str(Path(__file__).parent / 'schema' / 'state_config.json')) as f:
        schema = json.load(f)

    def __init__(self, config: StateConfig):
        self._config = config

        self.step: int = -1
        self.score = 0.0
        self.best_score: float = 0.0

        self.model_state: Optional[dict] = None
        self.optimizer_states: Optional[List[dict]] = None

    def __repr__(self):
        return '\n'.join((
            f'{self.__class__.__name__} (',
            f'  step: {self.step}',
            f'  score: {self.score}',
            f'  best score: {self.best_score}',
            *[
                f'  {key}: {value}' for key, value in vars(self._config).items()
            ],
            f')'
        ))

    def keys(self) -> typing.List[str]:
        return [key for key, value in vars(self).items() if not key.startswith('_') and not callable(value)]

    def _to_dict(self) -> dict:
        return dict((key, getattr(self, key)) for key in self.keys())

    def _from_dict(self, checkpoint: dict):
        missing_keys = []
        for key in self.keys():
            if key in checkpoint:
                setattr(self, key, checkpoint[key])
            else:
                missing_keys.append(key)  # pragma: no cover
        if missing_keys:  # pragma: no cover
            logging.warning('caution: checkpoint missing keys {}'.format(list(missing_keys)))

    def update(self, step: int, score: float, model: nn.Module, optimizers: List[Optimizer]):
        self.step = step
        self.score = score
        self.best_score = max(self.best_score, score)
        self.model_state = model.state_dict()
        self.optimizer_states = [optimizer.state_dict() for optimizer in optimizers]

    def save(self, score: float):
        torch.save(self._to_dict(), self._config.checkpoint_path)

        if self.best_score == score:
            shutil.copyfile(self._config.checkpoint_path, self._config.best_checkpoint_path)

    def load(self, checkpoint_path: typing.Union[str, Path] = None, gpu: bool = True):
        checkpoint_path = checkpoint_path or self._config.checkpoint_path
        checkpoint = torch.load(str(checkpoint_path), map_location=lambda tensor, *_: tensor.cuda() if gpu else None)
        self._from_dict(checkpoint)

    def resume_model(self, model: nn.Module):
        model.load_state_dict(self.model_state, strict=False)

        model_keys = set(model.state_dict().keys())
        saved_keys = self.model_state.keys()
        missing_keys = model_keys - saved_keys
        if missing_keys:  # pragma: no cover
            logging.warning('caution: model state missing keys {}'.format(list(missing_keys)))

    def resume_optimizers(self, optimizers: List[Optimizer]):
        for optimizer, state_dict in zip(optimizers, self.optimizer_states):
            optimizer.load_state_dict(state_dict)

    def resume(self, model: nn.Module, optimizers: List[Optimizer], gpu: bool = True):
        config = self._config
        if config.resume:
            if config.from_best:
                checkpoint_path = config.best_checkpoint_path
            else:
                checkpoint_path = config.checkpoint_path

            logging.info(f'load state from {checkpoint_path}')
            self.load(checkpoint_path, gpu=gpu)
            self.resume_model(model)
            self.resume_optimizers(optimizers)

    @classmethod
    def factory(cls, config: dict):
        jsonschema.validate(config, cls.schema)
        config = StateConfig(config)
        if config.checkpoint_path is None:
            config.checkpoint_path = str(Path(config.serialization_root) / 'checkpoint.pt')
        if config.best_checkpoint_path is None:
            config.best_checkpoint_path = str(Path(config.serialization_root) / 'best_checkpoint.pt')
        assert config.checkpoint_path and config.best_checkpoint_path
        return cls(config=config)
