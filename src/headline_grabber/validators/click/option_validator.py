import click
import re

from sys import platform
from headline_grabber.configurations.sites import site_names


class OptionValidator:

    @staticmethod
    def validate_site_name(ctx, param, value):
        if value is not None:
            for site_abbr in value.split(","):
                if site_abbr not in site_names.keys():
                    formatted_pairs = [
                        f"{key} ({value})" for key, value in sorted(site_names.items())
                    ]
                    result = "\n\t".join(formatted_pairs)
                    raise click.BadParameter(
                        f"""'{site_abbr}' is not a valid site. Valid sites are:\n\t{result}"""
                    )
        return value
    

    @staticmethod
    def validate_target_dir(ctx, param, value):
        if value is None or value == "":
            return None
        win_regex = r'^(([a-zA-Z]\:)|(\\))(\\{1}|((\\{1})[^\\]([^/:*?<>"|]*))+)$'
        nonwin_regex = r'^(/?)((?:[a-zA-Z0-9]+/)*)([a-zA-Z0-9]+?)(\*?)(/?)$'
        if not re.match(win_regex if platform == 'win32' else nonwin_regex, value):
            raise click.BadParameter(f"'{value}' is not a valid directory")
        return value
    
    @staticmethod
    def validate_max_entries(ctx, param, value):
        if value is None:
            return value
        
        if isinstance(value, str):
            value = value.replace(",", " ").split()[0]

        try:
            value = int(value)
        except ValueError:
            raise click.BadParameter(f'{value} must be a number')
        
        return value
    
    @staticmethod
    def validate_filter_sentiment(ctx, param, value):
        if value is None or value =="":
            return None
        value = str(value)
        value = value.upper()
        if value != 'POS' and value != 'POSITIVE' and value != 'NEG' and value != 'NEGATIVE':
            raise click.BadParameter(f'{value} must be either negative/positive/neg/pos')
        value = 'POSITIVE' if 'POS' in value else 'NEGATIVE'

        return value
    