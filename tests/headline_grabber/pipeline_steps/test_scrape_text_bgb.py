from bs4 import BeautifulSoup
import pytest
from headline_grabber.models.news_site import ElementSelector, NewsSite, PageSelectors
from headline_grabber.models.pipeline_context import PipelineContext
from headline_grabber.models.user_preferences import UserPreferences
from headline_grabber.pipeline_steps.scrape_text import ScrapeText


STUB_HTML = """
<div class="card | inline_block img_r padding_none margin_top margin_left margin_right margin_bottom width_full i_h_d-hw">
    <a class="card color_inherit" href="/2024/07/13/nation/trump-rally-shooting-assassination-attempt-investigation/" aria-label="Trump is injured but ‘fine’ after assassination attempt leaves rally-goer and gunman dead">
        <div>
            <h2 class="headline | bold border_box font_primary margin_bottom" style="font-size: 22px;">
                <div id="" class="image | relative margin_left_16 margin_bottom_10 width_full false false">
                    <figure class="font_primary margin_center false false" style="height: auto;" id="img-f0f7rlvRUVxS3AM">
                        <img id="img-f0f7rlvRUVxS3AM-image" alt="Republican presidential candidate former President Donald Trump is surround by U.S. Secret Service agents at a campaign rally, Saturday, July 13, 2024, in Butler, Pa. (AP Photo/Evan Vucci)" class="height_a width_full width_full--mobile width_full--tablet-only" data-src="https://bostonglobe-prod.cdn.arcpublishing.com/resizer/55Zbch4SsFQHtjgJJW1Qd_IMJRk=/480x319/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg" data-srcset="https://bostonglobe-prod.cdn.arcpublishing.com/resizer/q6mq0Kn__FKDWHdnzbAUJwO9dgw=/1440x959/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 1440w, https://bostonglobe-prod.cdn.arcpublishing.com/resizer/IsvfHzKJmUGKFaddfMrdkruXOAI=/1280x853/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 1280w, https://bostonglobe-prod.cdn.arcpublishing.com/resizer/7HTPXr8vKPKCDukmHfwqBrK66F8=/1024x682/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 1024w, https://bostonglobe-prod.cdn.arcpublishing.com/resizer/Ncm9IEp1b-_rRB9X24XOOZWwWMA=/820x546/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 820w, https://bostonglobe-prod.cdn.arcpublishing.com/resizer/FML5-bLhmX3nBcqwoFdoDAQFTbc=/600x399/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 600w, https://bostonglobe-prod.cdn.arcpublishing.com/resizer/27MoWwU1Ke41Smpif-O54DpSPX0=/420x279/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 420w, https://bostonglobe-prod.cdn.arcpublishing.com/resizer/eoisYKufJquSk4rNegoYfN_V3Jg=/240x159/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 240w" src="https://bostonglobe-prod.cdn.arcpublishing.com/resizer/55Zbch4SsFQHtjgJJW1Qd_IMJRk=/480x319/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg" srcset="https://bostonglobe-prod.cdn.arcpublishing.com/resizer/q6mq0Kn__FKDWHdnzbAUJwO9dgw=/1440x959/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 1440w, https://bostonglobe-prod.cdn.arcpublishing.com/resizer/IsvfHzKJmUGKFaddfMrdkruXOAI=/1280x853/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 1280w, https://bostonglobe-prod.cdn.arcpublishing.com/resizer/7HTPXr8vKPKCDukmHfwqBrK66F8=/1024x682/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 1024w, https://bostonglobe-prod.cdn.arcpublishing.com/resizer/Ncm9IEp1b-_rRB9X24XOOZWwWMA=/820x546/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 820w, https://bostonglobe-prod.cdn.arcpublishing.com/resizer/FML5-bLhmX3nBcqwoFdoDAQFTbc=/600x399/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 600w, https://bostonglobe-prod.cdn.arcpublishing.com/resizer/27MoWwU1Ke41Smpif-O54DpSPX0=/420x279/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 420w, https://bostonglobe-prod.cdn.arcpublishing.com/resizer/eoisYKufJquSk4rNegoYfN_V3Jg=/240x159/filters:focal(1927.5x10:1937.5x0)/cloudfront-us-east-1.images.arcpublishing.com/bostonglobe/PSKJTVN4Z3VQQROSEH4LWOHJ4A.jpg 240w" loading="lazy">
                        <figcaption class=" img_caption | margin_horizontal_0--mobile margin_horizontal_0--tablet text_align_right">
                            <span class="credit uppercase"></span>
                        </figcaption>
                    </figure>
                </div>
                <span id="headline-f0f7rlvRUVxS3AM">Trump is injured but ‘fine’ after assassination attempt leaves rally-goer and gunman dead.</span>
                <div class="deck | border_box inline_block  font_primary padding_bottom" style="font-size: 14px; line-height: 1.3;">
                    <span id="deck-f0f7rlvRUVxS3AM" class="display_block">Former president Trump is in “great spirits” and doing well after an assassination attempt on Saturday, aides said. The shooter and a spectator were killed.    </span>
                </div>
            </h2>
        </div>
    </a>
</div>
"""

@pytest.fixture
def scrape_text_instance():
    return ScrapeText()


def test_get_headlines_beautifulsoup_with_stub_html(scrape_text_instance):
    config = NewsSite(
        abbreviation="bgb",
        name="The Boston Globe",
        url="https://www.bostonglobe.com",
        engine="beautifulsoup",
        selectors=PageSelectors(
            headline=ElementSelector(tag="div", identifier="card"),
            link=ElementSelector(tag="a", identifier="href"),
            description=ElementSelector(tag="div", identifier="deck"),
            title=ElementSelector(tag="h2", identifier="headline"),
        ),
    )
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
    headlines = scrape_text_instance._get_headlines_beautifulsoup(config, html=STUB_HTML)
    assert len(headlines) > 0
    pipeline_context.headlines.extend(headlines)
    assert len(pipeline_context.headlines) > 0

def test_parse_headline(scrape_text_instance):
    dummy_tag = BeautifulSoup(STUB_HTML, "html.parser").find("div", class_="card")
    selectors = PageSelectors(
        headline=ElementSelector(tag="div", identifier="card"),
        link=ElementSelector(tag="a", identifier="href"),
        description=ElementSelector(tag="div", identifier="deck"),
        title=ElementSelector(tag="h2", identifier="headline"),
    )
    stub_url = 'https://www.bostonglobe.com'
    parsed_headline = scrape_text_instance._parse_headline(dummy_tag, selectors, stub_url)
    parsed_headline.title = parsed_headline.title.lstrip()
    parsed_headline.title = parsed_headline.title.rstrip()
    parsed_headline_title_cleaned = parsed_headline.title.splitlines()[0]
    parsed_headline_description_cleaned = ' '.join(parsed_headline.description.split())
    parsed_headline_link_cleaned = parsed_headline.link.replace(" ", "")
    print(parsed_headline_link_cleaned)
    assert parsed_headline_title_cleaned == "Trump is injured but ‘fine’ after assassination attempt leaves rally-goer and gunman dead."

    assert parsed_headline_description_cleaned == (
        'Former president Trump is in “great spirits” and doing well after an assassination attempt on Saturday, aides said. The shooter and a spectator were killed.'
    )
    assert parsed_headline_link_cleaned == 'https://www.bostonglobe.com/2024/07/13/nation/trump-rally-shooting-assassination-attempt-investigation/'
    
if __name__ == "__main__":
    pytest.main()