import pytest
import os
from bs4 import BeautifulSoup
from headline_grabber.models.headline import Headline
from headline_grabber.models.news_site import *
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.models.user_preferences import UserPreferences
from headline_grabber.pipeline_steps.scrape_text import ScrapeText, ScrapeTextException
from tests.headline_grabber.pipeline_steps.test_data.scrape_text_wap import ScrapeTextWap

def test_get_headlines_wap_beautifulsoup():
    scrape_text = ScrapeText()
    config = ScrapeTextWap.WAP_CONFIG
    assert scrape_text._get_headlines(config) != []


def test_get_headlines_no_engine():
    scrape_text = ScrapeText()
    config = ScrapeTextWap.NO_ENGING_CONFIG
    with pytest.raises(ScrapeTextException) as exceptionInfo:
        scrape_text._get_headlines(config)
    assert "No defined or unsupported engine" in str(exceptionInfo)


def test_get_headlines_beautifulsoup_wap():
    scrape_text = ScrapeText()
    config = ScrapeTextWap.WAP_CONFIG
    actualResult = scrape_text._get_headlines_beautifulsoup(config)
    assert actualResult != []


def test_get_headlines_selenium_wap():
    scrape_text = ScrapeText()
    config = ScrapeTextWap.WAP_CONFIG
    actualResult = scrape_text._get_headlines_selenium(config)
    assert actualResult != []


def test_parse_headline_wap():
    scrape_text = ScrapeText()
    config = ScrapeTextWap.WAP_CONFIG
    test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    file_path = os.path.join(test_data_dir, 'wap.html')
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()
    soup = BeautifulSoup(html, "html.parser")
    headline = soup.find_all(config.selectors.headline.tag, class_=config.selectors.headline.identifier)[0]

     

    print("***AAAA****")
     # Print the HTML of the selected headline element for debugging
    print(f"Selected headline element HTML: {headline}")
    
    # Debugging prints for selectors
    print(f"Title selector: {config.selectors.title.tag}, {config.selectors.title.identifier}")
    print(f"Description selector: {config.selectors.description.tag}, {config.selectors.description.identifier}")
    
    title_element = headline.find(config.selectors.title.tag, class_=config.selectors.title.identifier)
    description_element = headline.find(config.selectors.description.tag, class_=config.selectors.description.identifier)
    
     # Print the extracted title and description elements
    print(f"Extracted title element: {title_element}")
    print(f"Extracted description element: {description_element}")
  
    
    print("***BBBB****")
    actualResult = scrape_text._parse_headline(headline, config.selectors, config.url)
    print(f"Actual Result Description: '{actualResult.description.strip()}'")
    print(f"Expected Description: 'While critics may worry that he is cocooned from the worst of the news, living in a bit of a bubble, President Biden has chosen to focus on the positives.'")
    print("***CCCC****")

    assert actualResult.description.strip() == "While critics may worry that he is cocooned from the worst of the news, living in a bit of a bubble, President Biden has chosen to focus on the positives."
    assert actualResult.title.strip() == "Biden is seeing a different world than other Democrats"
    assert actualResult.link.strip() == 'https://www.washingtonpost.com/politics/2024/07/08/biden-different-world-bubble/'


def test_filter_results_False():
    scrape_text = ScrapeText()
    link = "https://www.washingtonpost.com/politics/2024/07/08/biden-different-world-bubble/"
    description = "hello"
    title = "hello"
    headline = Headline(link, title, description)
    assert scrape_text._filter_results(headline) is False
    print("***EEEE****")

    empty_link = ""
    headline = Headline(empty_link, title, description)
    
    assert scrape_text._filter_results(headline) is False
    print("***FFFF****")

    long_title = "Biden is seeing a different world than other Democrats"
    long_description = "While critics may worry that he is cocooned from the worst of the news, living in a bit of a bubble, President Biden has chosen to focus on the positives."
   
    headline = Headline(empty_link, long_title, long_description)
    
    assert scrape_text._filter_results(headline) is False
    print("***GGGG****")


def test_filter_results_True():
    print("***HHHH****")

    scrape_text = ScrapeText()
    link = "https://www.washingtonpost.com/politics/2024/07/08/biden-different-world-bubble/"
    description = "While critics may worry that he is cocooned from the worst of the news, living in a bit of a bubble, President Biden has chosen to focus on the positives."
    title = "Biden is seeing a different world than other Democrats"
    headline = Headline(link, title, description)
    
    print("***II****")

    assert scrape_text._filter_results(headline) is True
    print("***JJ****")


def test_run_Exception():
    scrape_text = ScrapeText()
    config = ScrapeTextWap.ERROR_CONFIG
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
    config = ScrapeTextWap.WAP_CONFIG
    pipeline_context = PipelineContext(
        site_configs=[config],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=['wap'],
            exclude=None,
        ),
    )
    actualResult = scrape_text.run(pipeline_context)
    assert len(actualResult.headlines) > 0