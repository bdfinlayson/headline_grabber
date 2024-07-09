import pytest
import click
import copy
from src.headline_grabber.models.pipeline_context import PipelineContext
from src.headline_grabber.models.user_preferences import UserPreferences
from src.headline_grabber.pipeline_steps.filter_sites import FilterSites
from src.headline_grabber.configurations.sites import sites
from src.headline_grabber.models.news_site import NewsSite

#comamnd to run this test file : pytest -s .\test_filter_sites.py

@pytest.fixture
def sample_sites():
    return copy.copy(sites)


def test_include_option(sample_sites):
    total_sites = len(sample_sites)
    #user_input = UserPreferences(include=["nyt"])
    user_input = UserPreferences(include=["nyt", "wsj"])
    context = PipelineContext(
        site_configs=sample_sites,
        user_input=user_input,
        headlines=[],
        grouped_headlines={},
        documents_for_display={}
    )
    filter_sites = FilterSites()
    result_context = filter_sites.run(context)
    expected_abbreviations = {"nyt", "wsj"}
    result_abbreviations = {site.abbreviation for site in result_context.site_configs}
    assert len(result_context.site_configs) == len(expected_abbreviations)
    assert result_abbreviations == expected_abbreviations
    print("***test_include_option passed***")

def test_exclude_option(sample_sites):
    total_sites = len(sample_sites)
    user_input = UserPreferences(exclude=["nyt"])
    context = PipelineContext(
        site_configs=sample_sites,
        user_input=user_input,
        headlines=[],
        grouped_headlines={},
        documents_for_display={}
    )
    filter_sites = FilterSites()
    result_context = filter_sites.run(context)
    expected_length = total_sites - 1
    assert len(result_context.site_configs) == expected_length
    assert all(site.abbreviation != "nyt" for site in result_context.site_configs)
    print("***test_exclude_option passed***")


def test_include_and_exclude_option(sample_sites):
    user_input = UserPreferences(include=["nyt"], exclude=["bbc"])
    context = PipelineContext(
        site_configs=sample_sites,
        user_input=user_input,
        headlines=[],
        grouped_headlines={},
        documents_for_display={}
    )
    filter_sites = FilterSites()
    #result_context = filter_sites.run(context)
    with pytest.raises(click.BadParameter):
        filter_sites.run(context)
    print("***test_include_and_exclude_option passed***")

