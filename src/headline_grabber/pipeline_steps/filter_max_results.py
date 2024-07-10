from src.headline_grabber.models.pipeline_context import PipelineContext
from src.headline_grabber.pipeline_steps.pipeline_step import PipelineStep
from src.headline_grabber.models.headline import Headline
from typing import List
from collections import defaultdict

class FilterMaxResults(PipelineStep):
    def run(self, context: PipelineContext):
        if context.user_input.limit is not None:
            
            subject_count = defaultdict(int)
            filtered_headline_list: List[Headline] = []
            for headline in context.headlines:    
                if subject_count[headline.subject.label] < context.user_input.limit:
                    filtered_headline_list.append(headline)
                    subject_count[headline.subject.label] += 1
            
            context.headlines = filtered_headline_list

        return context