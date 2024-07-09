import yaml
from headline_grabber.models.news_site import *
from headline_grabber.configurations.sites import *

class ScrapeTextWap:

    WAP_CONFIG = load_site_config("wap.yaml")

    NO_ENGING_CONFIG = NewsSite(
        abbreviation="wap",
        name="The Washington Post",
        url="https://www.washingtonpost.com",
        engine="",
        selectors=PageSelectors(
            headline=ElementSelector(tag="div", identifier="card-text"),
            link=ElementSelector(tag="a", identifier="href"),
            description=ElementSelector(tag="div", identifier="font-size-blurb"),
            title=ElementSelector(tag="div", identifier="headline")
        )
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
            title=ElementSelector(tag="h1", identifier="summary-class")
        )
    )

    def __init__(self):
        pass
