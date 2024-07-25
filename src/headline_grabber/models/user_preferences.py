from dataclasses import dataclass
from typing import List


@dataclass
class UserPreferences:
    def __init__(
        self,
        include: List[str] = None,
        exclude: List[str] = None,
        target_dir: str = None,
        limit: int = None,
        filter_sentiment: str = None,
        filter_topic: str = None, 
        **kwargs
    ):
        self.include = include
        self.exclude = exclude
        self.target_dir = target_dir
        self.limit = limit
        self.filter_sentiment = filter_sentiment
        self.filter_topic = filter_topic

