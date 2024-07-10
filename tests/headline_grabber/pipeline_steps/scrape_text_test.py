import pytest

from bs4 import BeautifulSoup
from headline_grabber.models.headline import Headline
from headline_grabber.models.news_site import *
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.models.user_preferences import UserPreferences
from headline_grabber.pipeline_steps.scrape_text import ScrapeText, ScrapeTextException
from tests.headline_grabber.pipeline_steps.test_data.scrape_text_data import ScrapeTextData

def test_get_headlines_nyt_beautifulsoup():
    scrape_text = ScrapeText()
    config = ScrapeTextData.NYT_CONFIG
    assert scrape_text._get_headlines(config) != []

def test_get_headlines_tol_beautifulsoup():
    scrape_text = ScrapeText()
    config = ScrapeTextData.TOL_CONFIG
    assert scrape_text._get_headlines(config) != []

def test_parse_headline_tol():
    scrape_text = ScrapeText()
    config = ScrapeTextData.TOL_CONFIG
    with open("tests/headline_grabber/pipeline_steps/test_data/tol.html", "r") as file:
        html = file.read()
    soup = BeautifulSoup(html, "html.parser")
    headline = soup.find_all(config.selectors.headline.tag, class_=config.selectors.headline.identifier)[0]
    actualResult = scrape_text._parse_headline(headline, config.selectors, config.url)
    assert actualResult.title.strip() == "Braverman claims leadership rival Jenrick is from left of Tory party"
    assert actualResult.description.strip() == 'Suella Braverman has accused Robert Jenrick of being a “centrist Rishi supporter” who is “from the left of the party”, after one of her key supporters switched to backing the former immigration minister. Jenrick and Braverman, the former home secretary, are among seven of the remaining 121 Tory MPs preparing to stand for the leadership...'
    assert actualResult.link.strip() == "https://www.thetimes.com/uk/politics/article/suella-braverman-tory-leadership-race-robert-jenrick-rivals-mnghlk9fn"

def test_run_TOL_Success():
    scrape_text = ScrapeText()
    config = ScrapeTextData.TOL_CONFIG
    pipeline_context = PipelineContext(
        site_configs=[config],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=['tol'],
            exclude=None,
        ),
    )
    actualResult = scrape_text.run(pipeline_context)
    assert len(actualResult.headlines) > 0

def test_get_headlines_no_engine():
    scrape_text = ScrapeText()
    config = ScrapeTextData.NO_ENGING_CONFIG
    with pytest.raises(ScrapeTextException) as exceptionInfo:
        scrape_text._get_headlines(config)
    assert "No defined or unsupported engine" in str(exceptionInfo)


def test_get_headlines_beautifulsoup_nyt():
    scrape_text = ScrapeText()
    config = ScrapeTextData.NYT_CONFIG
    actualResult = scrape_text._get_headlines_beautifulsoup(config)
    assert actualResult != []


def test_get_headlines_selenium_nyt():
    scrape_text = ScrapeText()
    config = ScrapeTextData.NYT_CONFIG
    actualResult = scrape_text._get_headlines_selenium(config)
    assert actualResult != []


def test_parse_headline_nyt():
    scrape_text = ScrapeText()
    config = ScrapeTextData.NYT_CONFIG
    with open("tests/headline_grabber/pipeline_steps/test_data/nyt.html", "r") as file:
        html = file.read()
    soup = BeautifulSoup(html, "html.parser")
    headline = soup.find_all(config.selectors.headline.tag, class_=config.selectors.headline.identifier)[0]
    actualResult = scrape_text._parse_headline(headline, config.selectors, config.url)
    assert actualResult.description.strip() == "President Biden's conversations are the first indication that he is seriously considering whether he can recover after a devastating debate performance."
    assert actualResult.title.strip() == 'Biden Tells Allies He Knows He Has Only Days to Salvage Candidacy'
    assert actualResult.link.strip() == 'https://www.nytimes.com/2024/07/03/us/politics/biden-withdraw-election-debate.html'


def test_filter_results_False():
    scrape_text = ScrapeText()
    link = "https://www.nytimes.com/2024/07/03/us/politics/biden-withdraw-election-debate.html"
    description = "hello"
    title = "hello"
    headline = Headline(link, title, description)
    assert scrape_text._filter_results(headline) is False

    empty_link = ""
    headline = Headline(empty_link, title, description)
    assert scrape_text._filter_results(headline) is False

    long_title = "Biden Tells Allies He Knows He Has Only Days to Salvage Candidacy"
    long_description = "President Biden's conversations are the first indication that he is seriously considering whether he can recover after a devastating debate performance."
    headline = Headline(empty_link, long_title, long_description)
    assert scrape_text._filter_results(headline) is False


def test_filter_results_True():
    scrape_text = ScrapeText()
    link = "https://www.nytimes.com/2024/07/03/us/politics/biden-withdraw-election-debate.html"
    description = "President Biden's conversations are the first indication that he is seriously considering whether he can recover after a devastating debate performance."
    title = "Biden Tells Allies He Knows He Has Only Days to Salvage Candidacy"
    headline = Headline(link, title, description)
    assert scrape_text._filter_results(headline) is True


def test_run_Exception():
    scrape_text = ScrapeText()
    config = ScrapeTextData.ERROR_CONFIG
    pipeline_context = PipelineContext(
        site_configs=[config],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=['bgb'],
            exclude=None,
        ),
    )
    with pytest.raises(ScrapeTextException) as exceptionInfo:
        scrape_text.run(pipeline_context)
    assert "No headlines found." in str(exceptionInfo)

def test_run_Success():
    scrape_text = ScrapeText()
    config = ScrapeTextData.NYT_CONFIG
    pipeline_context = PipelineContext(
        site_configs=[config],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=['nyt'],
            exclude=None,
        ),
    )
    actualResult = scrape_text.run(pipeline_context)
    assert len(actualResult.headlines) > 0