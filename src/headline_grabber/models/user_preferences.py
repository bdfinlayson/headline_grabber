from dataclasses import dataclass
from typing import List


@dataclass
class UserPreferences:
    def __init__(self, include: List[str] = None, exclude: List[str] = None):
        self.include = include
        self.exclude = exclude
