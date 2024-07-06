# test_filter_sites.py
import pytest
import click
from src.headline_grabber.models.pipeline_context import PipelineContext
from src.headline_grabber.models.user_preferences import UserPreferences
from src.headline_grabber.pipeline_steps.filter_sites import FilterSites
from src.headline_grabber.configurations.sites import sites
from src.headline_grabber.models.news_site import NewsSite

#comamnd to run this test file : pytest -s .\test_filter_sites.py

@pytest.fixture
def sample_sites():
    # Returns actual site configurations loaded from YAML files
    return sites


def test_include_option(sample_sites):
    # Print the number of YAML files loaded
    total_sites = len(sample_sites)
    print(f"Total number of YAML files: {total_sites}")
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

     # Check if only the included sites are present
    expected_abbreviations = {"nyt", "wsj"}
    print(f"Expected sites length: {len(expected_abbreviations)}")
    result_abbreviations = {site.abbreviation for site in result_context.site_configs}
    assert len(result_context.site_configs) == len(expected_abbreviations)
    assert result_abbreviations == expected_abbreviations
    print("***test_include_option passed***")

    '''
    # Check if only the included site is present
    assert len(result_context.site_configs) == 1
    assert result_context.site_configs[0].abbreviation == "nyt"
    assert result_context.site_configs[0].abbreviation == "nyt" 
    '''

def test_exclude_option(sample_sites):
    # Print the number of YAML files loaded
    total_sites = len(sample_sites)
    print(f"Total number of YAML files: {total_sites}")

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

    # Check if the excluded site is not present and the count is correct
    expected_length = total_sites - 1
    print(f"Expected length of YAML files: {expected_length}")
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

'''
def test_no_options(sample_sites):
    user_input = UserPreferences()
    context = PipelineContext(
        site_configs=sample_sites,
        user_input=user_input,
        headlines=[],
        grouped_headlines={},
        documents_for_display={}
    )
    filter_sites = FilterSites(context)
    result_context = filter_sites.run()
    assert len(result_context.site_configs) == len(sample_sites)
    assert result_context.site_configs == sample_sites
'''