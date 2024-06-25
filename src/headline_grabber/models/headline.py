from dataclasses import dataclass
from typing import List, Optional, Union, Dict
from typing_extensions import Self


@dataclass
class Classification:
    label: str
    score: float


@dataclass
class Headline:
    link: str
    title: str
    description: str
    subject: Optional[Classification] = None
    similarity_scores: Optional[List[float]] = None
    similarity_grouping: Optional[Classification] = None
    sentiment: Optional[Classification] = None

    def set_sentiment_score(self, sentiment: Dict[str, Union[str, float]]) -> Self:
        self.sentiment = Classification(**sentiment)
        return self

    def set_subject_classification(self, subject: Classification) -> Self:
        self.subject = subject
        return self

    def set_similarity_classification(self, similarity_group: int, similarity_scores: List[float]) -> Self:
        self.similarity_scores = similarity_scores
        self.similarity_grouping = Classification(label=str(similarity_group), score=max(filter(lambda x: x != 1.0, similarity_scores)))
        return self
