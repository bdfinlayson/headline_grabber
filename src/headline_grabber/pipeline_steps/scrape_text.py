from src.headline_grabber.configurations.enums.scraper_engine import ScraperEngine
from src.headline_grabber.models.headline import Headline
from src.headline_grabber.models.news_site import NewsSite, PageSelectors
from src.headline_grabber.models.pipeline_context import PipelineContext
from src.headline_grabber.pipeline_steps.pipeline_step import PipelineStep

from typing import List
import requests
from bs4 import BeautifulSoup, Tag
from selenium import webdriver


class ScrapeText(PipelineStep):
    def run(self, context: PipelineContext) -> PipelineContext:
        headlines: List[Headline] = []
        for site_config in context.site_configs:
            h = self._get_headlines(site_config)
            headlines = headlines + h
        context.headlines = headlines
        if not context.headlines:
            print("No headlines found. Please check the site configurations and try again.")
            exit()
        return context

    def _filter_results(self, x: Headline) -> bool:
        min_content_length = 150
        return len(x.link) > 0 and len(' '.join([x.title, x.description])) > min_content_length

    def _parse_headline(self, tag: Tag, page_selectors: PageSelectors) -> Headline:
        link_selector = page_selectors.link
        title_selector = page_selectors.title
        description_selector = page_selectors.description

        return Headline(
            link=tag.find(link_selector.tag)[link_selector.identifier] if tag.find(link_selector.tag) else '',
            title=tag.find(title_selector.tag, class_=title_selector.identifier).text if tag.find(
                title_selector.tag, class_=title_selector.identifier) else '',
            description=tag.find(description_selector.tag, class_=description_selector.identifier).text if tag.find(
                description_selector.tag, class_=description_selector.identifier) else ''
        )

    def _get_headlines_beautifulsoup(self, config: NewsSite, html: str = None):
        if html is None:
            html = requests.get(config.url).text
        soup = BeautifulSoup(html, 'html.parser')
        page_selectors = config.selectors
        headlines = list(filter(self._filter_results, [self._parse_headline(tag, page_selectors) for tag in
                                                 soup.find_all(page_selectors.headline.tag,
                                                               class_=page_selectors.headline.identifier)]))
        return headlines

    def _get_headlines_selenium(self, config: NewsSite):
        driver = webdriver.Firefox()
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
            print('Unsupported engine')