from bs4 import BeautifulSoup
import pytest
from headline_grabber.models.news_site import ElementSelector, NewsSite, PageSelectors
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.models.user_preferences import UserPreferences
from headline_grabber.pipeline_steps.scrape_text import ScrapeText

STUB_HTML = """
<div class="card-left card-text next-to-art no-bottom">
    <div class="headline relative gray-darkest pb-xs">
        <h2 class="wpds-c-iiQaMf wpds-c-iiQaMf-ikZTsyd-css">
            <a data-pb-local-content-field="web_headline" href="https://www.washingtonpost.com/business/2024/07/10/three-mile-island-nuclear-artificial-intelligence/">
                <span>Surging AI energy needs could bring Three Mile Island back online</span>
            </a>
        </h2>
    </div>    
    <div class="pb-xs font-size-blurb lh-fronts-tiny font-light gray-dark" style="font-size: 0.9375rem;">
        <a href="https://www.washingtonpost.com/business/2024/07/10/three-mile-island-nuclear-artificial-intelligence/">
            <span>The Pennsylvania plant, site of a partial meltdown in 1979, is part of a burst of fresh activity at mothballed plants as tech companies, manufacturers and energy regulators scramble to find enough zero emissions electricity.
            </span>
        </a>
    </div>
    <div class="byline gray-dark font-xxxxs pb-xs">By <a href="https://www.washingtonpost.com/people/evan-halper/">Evan Halper</a>
    </div>
</div>
"""


@pytest.fixture
def scrape_text_instance():
    return ScrapeText()


def test_get_headlines_beautifulsoup_with_stub_html(scrape_text_instance):
    config = NewsSite(
        abbreviation="wap",
        name="The Washington Post",
        url="https://www.washingtonpost.com",
        engine="beautifulsoup",
        selectors=PageSelectors(
            headline=ElementSelector(tag="div", identifier="card-text"),
            link=ElementSelector(tag="a", identifier="href"),
            description=ElementSelector(tag="div", identifier="font-size-blurb"),
            title=ElementSelector(tag="div", identifier="headline"),
        ),
    )
    pipeline_context = PipelineContext(
        site_configs=[config],
        headlines=[],
        grouped_headlines={},
        documents_for_display={},
        user_input=UserPreferences(
            include=["wap"],
            exclude=None,
        ),
    )
    headlines = scrape_text_instance._get_headlines_beautifulsoup(
        config, html=STUB_HTML
    )
    assert len(headlines) > 0
    pipeline_context.headlines.extend(headlines)
    assert len(pipeline_context.headlines) > 0


def test_parse_headline(scrape_text_instance):
    dummy_tag = BeautifulSoup(STUB_HTML, "html.parser").find("div", class_="card-text")
    selectors = PageSelectors(
        headline=ElementSelector(tag="div", identifier="card-text"),
        link=ElementSelector(tag="a", identifier="href"),
        description=ElementSelector(tag="div", identifier="font-size-blurb"),
        title=ElementSelector(tag="div", identifier="headline"),
    )
    stub_url = "https://www.washingtonpost.com/business/2024/07/10/three-mile-island-nuclear-artificial-intelligence/"
    parsed_headline = scrape_text_instance._parse_headline(
        dummy_tag, selectors, stub_url
    )
    parsed_headline_title_cleaned = " ".join(parsed_headline.title.split())
    parsed_headline_description_cleaned = " ".join(parsed_headline.description.split())
    parsed_headline_link_cleaned = parsed_headline.link.replace(" ", "")
    stub_url_cleaned = stub_url.replace(" ", "")

    assert (
        parsed_headline_title_cleaned
        == "Surging AI energy needs could bring Three Mile Island back online"
    )
    assert parsed_headline_description_cleaned == (
        "The Pennsylvania plant, site of a partial meltdown in 1979, is part of a burst of fresh activity at mothballed plants as tech companies, manufacturers and energy regulators scramble to find enough zero emissions electricity."
    )
    assert parsed_headline_link_cleaned == stub_url_cleaned


if __name__ == "__main__":
    pytest.main()
