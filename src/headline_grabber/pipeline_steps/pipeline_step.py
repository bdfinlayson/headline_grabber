from abc import ABC, abstractmethod

from src.headline_grabber.models.pipeline_context import PipelineContext


class PipelineStep(ABC):
    @abstractmethod
    def run(self, context: PipelineContext):
        raise NotImplementedError
