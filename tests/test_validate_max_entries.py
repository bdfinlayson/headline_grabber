import pytest
import click
from headline_grabber.validators.click.option_validator import OptionValidator

def test_validate_number_single_value():
    result = OptionValidator.validate_max_entries(None, None, '5')
    assert result == 5

def test_validate_number_comma_separated():
    result = OptionValidator.validate_max_entries(None, None, '5, 10, 15')
    assert result == 5

def test_validate_number_space_separated():
    result = OptionValidator.validate_max_entries(None, None, '5 10 15')
    assert result == 5

def test_validate_number_invalid_value():
    with pytest.raises(click.BadParameter):
        OptionValidator.validate_max_entries(None, None, 'abc, 10, 15')

def test_validate_number_default_value():
    result = OptionValidator.validate_max_entries(None, None, None)
    assert result == None

def test_validate_number_int():
    result = OptionValidator.validate_max_entries(None, None, 5)
    assert result == 5