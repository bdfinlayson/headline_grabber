from dataclasses import dataclass
from typing import List, Dict

from headline_grabber.models.display_document import DisplayDocument
from headline_grabber.models.headline import Headline
from headline_grabber.models.news_site import NewsSite
from headline_grabber.models.user_preferences import UserPreferences


@dataclass
class PipelineContext:
    site_configs: List[NewsSite]
    user_input: UserPreferences
    headlines: List[Headline]
    grouped_headlines: Dict[str, List[Headline]]
    documents_for_display: Dict[str, List[DisplayDocument]]
