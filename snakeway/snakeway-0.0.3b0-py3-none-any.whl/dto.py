from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class Stage(Enum):
    START = auto()
    IN = auto()
    END = auto()


@dataclass(frozen=True)
class CheckpointInfo:
    cid: int
    label: str
    ts: int
    stage: Stage
    checkpoint_label: Optional[str] = field(default=None)
