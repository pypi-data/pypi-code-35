from .repo import Repo
from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import datetime, timezone

@dataclass
class Extract:
    name: str
    repos: List[Repo]
    start_date:str = ''
    end_date:str = ''
    adjustments:List[str] = field(default_factory=lambda: [])
    tod_adjustments:List[Tuple[str, int]] = field(default_factory=lambda: [])

    def get_begin_end_timestamps(self):
        if self.start_date:
            begin = int(datetime.strptime(self.start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp())
        else:
            begin = 0
        if self.end_date:
            end = int(datetime.strptime(self.end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp())
        else:
            end = 99999999999
        return begin, end
