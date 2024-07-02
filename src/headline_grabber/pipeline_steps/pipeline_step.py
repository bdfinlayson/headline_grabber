from abc import ABC, abstractmethod

from headline_grabber.models.pipeline_context import PipelineContext


class PipelineStep(ABC):
    @abstractmethod
    def run(self, context: PipelineContext):
        raise NotImplementedError
