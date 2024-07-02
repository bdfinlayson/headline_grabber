from typing import List

from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.pipeline_steps.pipeline_step import PipelineStep


class Pipeline:
    def __init__(self, steps: List[PipelineStep]):
        self.steps = steps

    def add_step(self, step):
        self.steps.append(step)
        return self

    def run(self, context: PipelineContext) -> PipelineContext:
        for step in self.steps:
            context = step.run(context)
        return context
