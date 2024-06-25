from src.headline_grabber.pipeline_steps.classify_subject import ClassifySubject
from src.headline_grabber.pipeline_steps.display_report import DisplayReport
from src.headline_grabber.pipeline_steps.filter_sites import FilterSites
from src.headline_grabber.pipeline_steps.group_by_similarity import GroupBySimilarity
from src.headline_grabber.pipeline_steps.prepare_for_display import PrepareForDisplay
from src.headline_grabber.pipeline_steps.score_sentiment import ScoreSentiment
from src.headline_grabber.pipeline_steps.scrape_text import ScrapeText
from src.headline_grabber.pipeline_steps.text_similarity import TextSimilarity
from src.headline_grabber.pipelines.pipeline import Pipeline

news_pipeline = Pipeline([
    FilterSites(),
    ScrapeText(),
    ScoreSentiment(),
    ClassifySubject(),
    TextSimilarity(),
    GroupBySimilarity(),
    PrepareForDisplay(),
    DisplayReport()
])
