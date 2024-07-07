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
        win_regex = r'^(([a-zA-Z]\:)|(\\))(\\{1}|((\\{1})[^\\]([^/:*?<>"|]*))+)$'
        nonwin_regex = r'^(/?)((?:[a-zA-Z0-9]+/)*)([a-zA-Z0-9]+?)(\*?)(/?)$'
        if not re.match(win_regex if platform == 'win32' else nonwin_regex, value):
            raise click.BadParameter(f"'{value}' is not a valid directory")
        return value
    