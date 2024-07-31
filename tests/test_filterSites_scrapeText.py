import pytest
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.models.user_preferences import UserPreferences
from headline_grabber.pipeline_steps.filter_sites import FilterSites
from headline_grabber.pipeline_steps.scrape_text import ScrapeText
from headline_grabber.configurations.sites import sites

@pytest.fixture
def sample_sites():
    return sites

def test_filter_and_scrape_integration(sample_sites):
    user_input = UserPreferences(include=["bgb"], exclude=None)
    context = PipelineContext(
        site_configs=sample_sites,
        user_input=user_input,
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
    )
    filter_sites_step = FilterSites()
    context = filter_sites_step.run(context)
    scrape_text_step = ScrapeText()
    context = scrape_text_step.run(context)
    assert len(context.headlines) > 0, "No headlines were scraped."
    included_sites = {site.abbreviation for site in context.site_configs}
    expected_included_sites = {"bgb"}
    assert included_sites == expected_included_sites, f"Expected sites: {expected_included_sites}, but got: {included_sites}"
    for headline in context.headlines:
        assert isinstance(headline.title, str) and len(headline.title) > 0
        assert isinstance(headline.description, str)
        assert isinstance(headline.link, str) and "http" in headline.link