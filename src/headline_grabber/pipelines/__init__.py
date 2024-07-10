from headline_grabber.pipeline_steps.classify_subject import ClassifySubject
from headline_grabber.pipeline_steps.display_report import DisplayReport
from headline_grabber.pipeline_steps.filter_sites import FilterSites
from headline_grabber.pipeline_steps.group_by_similarity import GroupBySimilarity
from headline_grabber.pipeline_steps.prepare_for_display import PrepareForDisplay
from headline_grabber.pipeline_steps.score_sentiment import ScoreSentiment
from headline_grabber.pipeline_steps.scrape_text import ScrapeText
from headline_grabber.pipeline_steps.text_similarity import TextSimilarity
from headline_grabber.pipelines.pipeline import Pipeline

news_pipeline = Pipeline(
    [
        FilterSites(),
        ScrapeText(),
        ClassifySubject(),
        FilterMaxResults(),
        ScoreSentiment(),
        TextSimilarity(),
        GroupBySimilarity(),
        PrepareForDisplay(),
        DisplayReport(),
    ]
)
