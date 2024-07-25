from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.pipeline_steps.pipeline_step import PipelineStep
from headline_grabber.models.headline import Headline
from typing import List
from sys import exit

class FilterTopic(PipelineStep):
    def run(self, context: PipelineContext):
        if context.user_input.filter_topic is not None:
            
            filtered_headline_list: List[Headline] = []
            for headline in context.headlines:
                if headline.subject.label == context.user_input.filter_topic:
                    filtered_headline_list.append(headline)
            
            context.headlines = filtered_headline_list
        return context