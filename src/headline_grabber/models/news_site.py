from dataclasses import dataclass


@dataclass
class ElementSelector:
    tag: str
    identifier: str


@dataclass
class PageSelectors:
    headline: ElementSelector
    link: ElementSelector
    title: ElementSelector
    description: ElementSelector


@dataclass
class NewsSite:
    abbreviation: str
    name: str
    url: str
    selectors: PageSelectors
    engine: str = 'beautifulsoup'
