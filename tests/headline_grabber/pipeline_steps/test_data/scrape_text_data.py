import yaml
from headline_grabber.models.news_site import *
from headline_grabber.configurations.sites import *


class ScrapeTextData:

    NYT_CONFIG = load_site_config("nyt.yaml")

    TOL_CONFIG = load_site_config("tol.yaml")

    REU_CONFIG = load_site_config("reu.yaml")

    NO_ENGING_CONFIG = NewsSite(
        abbreviation="nyt",
        name="The New York Times",
        url="https://www.nytimes.com",
        engine="",
        selectors=PageSelectors(
            headline=ElementSelector(tag="section", identifier="story-wrapper"),
            link=ElementSelector(tag="a", identifier="href"),
            description=ElementSelector(tag="p", identifier="indicate-hover"),
            title=ElementSelector(tag="h1", identifier="summary-class"),
        ),
    )

    ERROR_CONFIG = NewsSite(
        abbreviation="bgb",
        name="The Boston Globe",
        url="https://www.bostonglobe.com",
        engine="beautifulsoup",
        selectors=PageSelectors(
            headline=ElementSelector(tag="section", identifier="story-wrapper"),
            link=ElementSelector(tag="a", identifier="href"),
            description=ElementSelector(tag="p", identifier="indicate-hover"),
            title=ElementSelector(tag="h1", identifier="summary-class"),
        ),
    )

    def __init__(self):
        pass
