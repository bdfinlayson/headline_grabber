from src.headline_grabber.models.pipeline_context import PipelineContext
from src.headline_grabber.pipeline_steps.pipeline_step import PipelineStep


class GroupBySimilarity(PipelineStep):
    def run(self, context: PipelineContext):
        groups = {}
        for headline in context.headlines:
            if headline.similarity_grouping.label not in groups:
                groups[headline.similarity_grouping.label] = [headline]
            else:
                groups[headline.similarity_grouping.label] = groups[
                    headline.similarity_grouping.label
                ] + [headline]
        context.grouped_headlines = groups
        return context
