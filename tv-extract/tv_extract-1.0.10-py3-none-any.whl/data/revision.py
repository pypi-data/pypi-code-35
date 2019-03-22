from dataclasses import dataclass, field
from .file_info import FileInfo
from typing import Dict

@dataclass
class Revision:
    hash: str
    stamp: int
    timezone: int = 0
    author: str = ''
    email: str = ''
    domain: str = ''
    comments: str = ''
    branch_parent: str = ''
    master_parent: str = ''
    file_infos: Dict[str, FileInfo] = field(default_factory=lambda: {})
    delta: Dict[str, FileInfo] = field(default_factory=lambda: {})
    is_a_pr: bool = False
    original_commit: bool = False