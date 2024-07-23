import pytest
import click
from headline_grabber.validators.click.option_validator import OptionValidator

def test_validate_filter_sentiment():
    # Test cases for valid input
    assert OptionValidator.validate_filter_sentiment(None, None, 'POS') == 'POSITIVE'
    assert OptionValidator.validate_filter_sentiment(None, None, 'PoS') == 'POSITIVE'
    assert OptionValidator.validate_filter_sentiment(None, None, 'pos') == 'POSITIVE'
    assert OptionValidator.validate_filter_sentiment(None, None, 'POSITIVE') == 'POSITIVE'
    assert OptionValidator.validate_filter_sentiment(None, None, 'positive') == 'POSITIVE'
    assert OptionValidator.validate_filter_sentiment(None, None, 'PoSiTiVe') == 'POSITIVE'
    assert OptionValidator.validate_filter_sentiment(None, None, 'NEG') == 'NEGATIVE'
    assert OptionValidator.validate_filter_sentiment(None, None, 'NeG') == 'NEGATIVE'
    assert OptionValidator.validate_filter_sentiment(None, None, 'neg') == 'NEGATIVE'
    assert OptionValidator.validate_filter_sentiment(None, None, 'NEGATIVE') == 'NEGATIVE'
    assert OptionValidator.validate_filter_sentiment(None, None, 'negative') == 'NEGATIVE'
    assert OptionValidator.validate_filter_sentiment(None, None, 'NeGaTiVe') == 'NEGATIVE'

    # Test cases for invalid input
    with pytest.raises(click.BadParameter):
        OptionValidator.validate_filter_sentiment(None, None, 'neutral')
    
    with pytest.raises(click.BadParameter):
        OptionValidator.validate_filter_sentiment(None, None, '123')

    with pytest.raises(click.BadParameter):
        OptionValidator.validate_filter_sentiment(None, None, 'positive123')

    with pytest.raises(click.BadParameter):
        OptionValidator.validate_filter_sentiment(None, None, 'positeve')

    with pytest.raises(click.BadParameter):
        OptionValidator.validate_filter_sentiment(None, None, 'negitive')

    # Test cases for None or empty input
    assert OptionValidator.validate_filter_sentiment(None, None, None) is None
    assert OptionValidator.validate_filter_sentiment(None, None, "") is None