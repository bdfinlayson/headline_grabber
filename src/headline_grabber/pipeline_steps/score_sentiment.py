from src.headline_grabber.models.pipeline_context import PipelineContext
from src.headline_grabber.pipeline_steps import sentiment_analysis_classifier
from src.headline_grabber.pipeline_steps.pipeline_step import PipelineStep


class ScoreSentiment(PipelineStep):
    def run(self, context: PipelineContext):
        texts = [
            " ".join([headline.title, headline.description])
            for headline in context.headlines
        ]
        sentiment_scores = sentiment_analysis_classifier(texts)
        context.headlines = [
            headline.set_sentiment_score(sentiment_score)
            for headline, sentiment_score in zip(context.headlines, sentiment_scores)
        ]
        return context
