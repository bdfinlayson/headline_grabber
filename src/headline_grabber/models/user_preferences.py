from dataclasses import dataclass
from typing import List


@dataclass
class UserPreferences:
    def __init__(self, include: List[str] = None, exclude: List[str] = None, target_dir: str = None, limit : int = None, **kwargs):
        self.include = include
        self.exclude = exclude
        self.target_dir = target_dir
        self.limit = limit