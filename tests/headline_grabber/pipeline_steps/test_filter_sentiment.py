import pytest
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.pipeline_steps.pipeline_step import PipelineStep
from headline_grabber.pipeline_steps.filter_sentiment import FilterSentiment
from src.headline_grabber.pipelines.pipeline import Pipeline
from src.headline_grabber.models.user_preferences import UserPreferences
from src.headline_grabber.models.headline import Classification
from src.headline_grabber.models.headline import Headline

test_pipline = Pipeline([FilterSentiment()])

def test_user_input_none():
    context = PipelineContext(
        site_configs=[],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=None,
            exclude=None,
            target_dir=None,
            limit=None,
            filter_sentiment=None,
        ),
    )
    context.headlines.append(Classification("sports", 0.1))
    context.headlines[0].sentiment = Classification('POSITIVE', 0.1)
    context = test_pipline.run(context)
    assert len(context.headlines) == 1

def test_user_input_pos_no_filter():
    context = PipelineContext(
        site_configs=[],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=None,
            exclude=None,
            target_dir=None,
            limit=None,
            filter_sentiment='POSITIVE',
        ),
    )
    context.headlines.append(Classification("sports", 0.1))
    context.headlines[0].sentiment = Classification('NEGATIVE', 0.1)
    context = test_pipline.run(context)
    assert len(context.headlines) == 1

def test_user_input_pos_filter():
    context = PipelineContext(
        site_configs=[],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=None,
            exclude=None,
            target_dir=None,
            limit=None,
            filter_sentiment='POSITIVE',
        ),
    )
    context.headlines.append(Classification("sports", 0.1))
    context.headlines[0].sentiment = Classification('POSITIVE', 0.1)
    context.headlines.append(Classification("sports", 0.1))
    context.headlines[1].sentiment = Classification('NEGATIVE', 0.1)
    context = test_pipline.run(context)
    assert len(context.headlines) == 1

def test_user_input_neg_no_filter():
    context = PipelineContext(
        site_configs=[],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=None,
            exclude=None,
            target_dir=None,
            limit=None,
            filter_sentiment='NEGATIVE',
        ),
    )
    context.headlines.append(Classification("sports", 0.1))
    context.headlines[0].sentiment = Classification('POSITIVE', 0.1)
    context = test_pipline.run(context)
    assert len(context.headlines) == 1
    
def test_user_input_neg_filter():
    context = PipelineContext(
        site_configs=[],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=None,
            exclude=None,
            target_dir=None,
            limit=None,
            filter_sentiment='NEGATIVE',
        ),
    )
    context.headlines.append(Classification("sports", 0.1))
    context.headlines[0].sentiment = Classification('POSITIVE', 0.1)
    context.headlines.append(Classification("sports", 0.1))
    context.headlines[1].sentiment = Classification('NEGATIVE', 0.1)
    context = test_pipline.run(context)
    assert len(context.headlines) == 1