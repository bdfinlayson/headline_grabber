from .configurations.sites import sites
import click


@click.command
@click.option(
    '--include',
    type=click.STRING,
    default=None,
    required=False,
    help='Comma-separated list of news sources to include in the search'
)
@click.option(
    '--exclude',
    type=click.STRING,
    default=None,
    help='Comma-separated list of news sources to exclude from the search'
)
def main(include: str, exclude: str):
    """ Simple program to collect headlines from various news sources and summarize them in a helpful way """
    if include is not None:
        news_sources = include.split(',')
        print(' '.join(news_sources))

    if exclude is not None:
        news_sources = exclude.split(',')
        print(' '.join(news_sources))

    for site in sites:
        print(site.name)


