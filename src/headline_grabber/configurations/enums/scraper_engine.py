from src.headline_grabber.configurations.enums.str_enum import StrEnum


class ScraperEngine(StrEnum):
    BEAUTIFULSOUP = ("beautifulsoup",)
    SELENIUM = "selenium"
