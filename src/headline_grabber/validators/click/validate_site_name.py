import click

from src.headline_grabber.configurations.sites import site_names


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
