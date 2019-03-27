from typing import List
from dataclasses import dataclass, field
from datetime import datetime


class WrongUsername(Exception):
    pass


@dataclass(frozen=True)
class User:
    """GitHub user"""
    login: str
    name: str
    url: str
    html_url: str
    avatar_url: str


@dataclass
class Comment:
    """Blog commont"""
    user: User
    body: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Post:
    """Blog post"""
    user: User
    title: str
    created_at: datetime
    updated_at: datetime
    description: str
    body: str
    comments: List[Comment] = field(default_factory=list)
