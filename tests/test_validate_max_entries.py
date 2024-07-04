import pytest
import click
from headline_grabber.validators.click.validate_site_name import validate_max_entries

def test_validate_number_single_value():
    result = validate_max_entries(None, None, '5')
    assert result == 5

def test_validate_number_comma_separated():
    result = validate_max_entries(None, None, '5, 10, 15')
    assert result == 5

def test_validate_number_space_separated():
    result = validate_max_entries(None, None, '5 10 15')
    assert result == 5

def test_validate_number_invalid_value():
    with pytest.raises(click.BadParameter):
        validate_max_entries(None, None, 'abc, 10, 15')

def test_validate_number_default_value():
    result = validate_max_entries(None, None, None)
    assert result == None