from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.pipeline_steps import sentiment_analysis_classifier
from headline_grabber.pipeline_steps.pipeline_step import PipelineStep
from tqdm import tqdm

class ScoreSentiment(PipelineStep):
    def run(self, context: PipelineContext):
        texts = [
            " ".join([headline.title, headline.description])
            for headline in context.headlines
        ]
        sentiment_scores = sentiment_analysis_classifier(texts)
        context.headlines = [
            headline.set_sentiment_score(sentiment_score)
            for headline, sentiment_score in tqdm(zip(context.headlines, sentiment_scores), desc="Setting sentiment scores", unit="headline", total=len(context.headlines))
        ]
        return context
