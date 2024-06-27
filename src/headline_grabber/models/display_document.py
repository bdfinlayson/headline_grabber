from dataclasses import dataclass
from typing import List

from src.headline_grabber.models.headline import Classification


@dataclass
class DisplayDocument:
    links: List[str]
    summarized_title: str
    summarized_description: str
    average_sentiment: Classification
    subjects: List[str]
    most_common_subject: str
