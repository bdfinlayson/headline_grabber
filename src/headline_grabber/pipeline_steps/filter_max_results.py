from src.headline_grabber.models.pipeline_context import PipelineContext
from src.headline_grabber.pipeline_steps.pipeline_step import PipelineStep
from src.headline_grabber.models.headline import Headline
from typing import List

class FilterMaxResults(PipelineStep):
    def run(self, context: PipelineContext):
        if context.user_input.entries is not None:
            print(context)
            subject_count = {}
            fl: List[Headline] = []
            for headline in context.headlines:
                
                if headline.subject.label not in subject_count:
                    subject_count[headline.subject.label] = 0
                    
                if subject_count[headline.subject.label] < context.user_input.entries:
                    fl.append(headline)
                    subject_count[headline.subject.label] += 1
            
            context.headlines = fl
            for headline in context.headlines:
                print(headline.subject.label)
        print(context)
        return context