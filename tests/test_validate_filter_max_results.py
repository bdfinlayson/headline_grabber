import pytest
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.pipeline_steps.pipeline_step import PipelineStep
from headline_grabber.pipeline_steps.filter_max_results import FilterMaxResults
from src.headline_grabber.pipelines.pipeline import Pipeline
from src.headline_grabber.models.user_preferences import UserPreferences
from src.headline_grabber.models.headline import Classification
from src.headline_grabber.models.headline import Headline

test_pipline = Pipeline([FilterMaxResults()])


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
        ),
    )
    context.headlines.append(Classification("sports", 0.1))
    context.headlines.append(Classification("sports", 0.1))
    context.headlines.append(Classification("sports", 0.1))
    context = test_pipline.run(context)
    assert len(context.headlines) == 3


def test_user_input_two_clips_results():
    context = PipelineContext(
        site_configs=[],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=None,
            exclude=None,
            target_dir=None,
            limit=2,
        ),
    )
    context.headlines.append(Headline("a", "b", "c", Classification("sports", 0.1)))
    context.headlines.append(Headline("a", "b", "c", Classification("sports", 0.1)))
    context.headlines.append(Headline("a", "b", "c", Classification("sports", 0.1)))
    context = test_pipline.run(context)

    assert len(context.headlines) == 2


def test_user_input_two_does_not_clip_results():
    context = PipelineContext(
        site_configs=[],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=None,
            exclude=None,
            target_dir=None,
            limit=3,
        ),
    )
    context.headlines.append(Headline("a", "b", "c", Classification("sports", 0.1)))
    context.headlines.append(Headline("a", "b", "c", Classification("sports", 0.1)))
    context.headlines.append(Headline("a", "b", "c", Classification("World", 0.1)))
    context = test_pipline.run(context)

    assert len(context.headlines) == 3


def test_user_input_two_clips_3_but_not_one():
    context = PipelineContext(
        site_configs=[],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=None,
            exclude=None,
            target_dir=None,
            limit=2,
        ),
    )
    context.headlines.append(Headline("a", "b", "c", Classification("sports", 0.1)))
    context.headlines.append(Headline("a", "b", "c", Classification("sports", 0.1)))
    context.headlines.append(Headline("a", "b", "c", Classification("sports", 0.1)))
    context.headlines.append(Headline("a", "b", "c", Classification("World", 0.1)))
    context = test_pipline.run(context)

    assert len(context.headlines) == 3
