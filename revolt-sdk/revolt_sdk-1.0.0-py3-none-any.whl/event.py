from typing import Any, Optional


class _Event:

    def __init__(self, id: str,
                 type: str,
                 data: Optional[Any],
                 timestamp: int):
        self.id: str = id
        self.type: str = type
        self.data: Optional[Any] = data
        self.timestamp: int = timestamp
