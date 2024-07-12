from headline_grabber.configurations.enums.scraper_engine import ScraperEngine
from headline_grabber.models.headline import Headline
from headline_grabber.models.news_site import NewsSite, PageSelectors
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.pipeline_steps.pipeline_step import PipelineStep
from typing import List
import requests
from bs4 import BeautifulSoup, Tag
from selenium import webdriver

class ScrapeTextException(Exception):
    pass

class ScrapeText(PipelineStep):
    def run(self, context: PipelineContext) -> PipelineContext:
        headlines: List[Headline] = []
        for site_config in context.site_configs:
            h = self._get_headlines(site_config)
            headlines = headlines + h
        context.headlines = headlines
        if not context.headlines:
            self.throw_error("No headlines found. Please check the site configurations and try again.")
        return context

    def _filter_results(self, x: Headline) -> bool:
        min_content_length = 150
        return (
            len(x.link) > 0
            and len(" ".join([x.title, x.description])) > min_content_length
        )

    def _parse_headline(self, tag: Tag, page_selectors: PageSelectors, url: str) -> Headline:
        link_selector = page_selectors.link
        title_selector = page_selectors.title
        description_selector = page_selectors.description
        raw_link = tag.find(link_selector.tag)[link_selector.identifier] if tag.find(link_selector.tag) else ""
        return Headline(
            link=(
                raw_link if "http" in raw_link else url + raw_link
            ),
            title=(
                tag.find(title_selector.tag, class_=title_selector.identifier).text
                if tag.find(title_selector.tag, class_=title_selector.identifier)
                else ""
            ),
            description=(
                tag.find(
                    description_selector.tag, class_=description_selector.identifier
                ).text
                if tag.find(
                    description_selector.tag, class_=description_selector.identifier
                )
                else ""
            ),
        )

    def _get_headlines_beautifulsoup(self, config: NewsSite, html: str = None):
        if html is None:
            html = requests.get(config.url).text
        soup = BeautifulSoup(html, "html.parser")
        page_selectors = config.selectors
        headlines = list(
            filter(
                self._filter_results,
                [
                    self._parse_headline(tag, page_selectors, config.url)
                    for tag in soup.find_all(
                        page_selectors.headline.tag,
                        class_=page_selectors.headline.identifier,
                    )
                ],
            )
        )
        return headlines

    def _get_headlines_selenium(self, config: NewsSite):
        firefoxOptions = webdriver.FirefoxOptions()
        firefoxOptions.add_argument('--headless')
        firefoxOptions.add_argument('--disable-gpu')
        driver = webdriver.Firefox(options=firefoxOptions)
        driver.get(config.url)
        html = driver.page_source
        headlines = self._get_headlines_beautifulsoup(config, html)
        return headlines

    def _get_headlines(self, config: NewsSite):
        if config.engine == ScraperEngine.BEAUTIFULSOUP.value:
            return self._get_headlines_beautifulsoup(config)
        elif config.engine == ScraperEngine.SELENIUM.value:
            return self._get_headlines_selenium(config)
        else:
            self.throw_error("No defined or unsupported engine!")
       
    
    def throw_error(self, message: str):
        print(message)
        raise ScrapeTextException(message)